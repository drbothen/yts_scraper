#from __future__ import division
import transmissionrpc
#from smb.SMBConnection import SMBConnection
#import os as o
import package as yts
import sys
from clint.textui import progress, colored




def main():
    # checks to insure args are present if not prompts user to use -h or --help and exits
    if len(sys.argv) == 1:
        print "use -h or --help for usage"
        sys.exit()
        
    # Sends Args to the args_builder module
    rArgs = yts.args_parse(sys.argv[1:])

    
    #Checks if -h or -help was used. if so it exists the application
    if rArgs == False:
        #print rArgs
        sys.exit()

        
    # if -u or --update was use this block of code will run    
    if rArgs.update == True:
        ytsObj = yts.Rawyts()
        rPagecount = ytsObj.raw_requests_page_count(50)        
        #checks to see if the database stored in rArgs.database is actually a database. if not, database will be created and populated
        if yts.yts_database_present(rArgs.database) == False:
            
            if rArgs.verbose == True:
                #build module for verbose
                print "{Database} does not exist. Creating...".format(Database=rArgs.database)
                print "Creating intial table and views..." 
                
            errorCheck = yts.yts_database_init(rArgs.database)
            if errorCheck == True:
                
                if rArgs.verbose == True:
                    #build module for verbose
                    pass
                


                for i in progress.bar(range(1, rPagecount + 1)):
                    rDic = ytsObj.raw_torrents(limit=50, page=i, order='asc')
                    for dics in rDic['MovieList']:
                        #rFiles = yts.magnet2torrent(dics['TorrentMagnetUrl'])
                        #print rFiles
                        writecheck = yts.yts_database_write(dics, rArgs.database)
                        if writecheck == False:
                            print colored.red("Failed to write to database")
                            sys.exit()
                        
        elif yts.yts_isdatabase(rArgs.database) == True:
            count = 0
            for i in progress.bar(range(1, rPagecount + 1)):
                rDic = ytsObj.raw_torrents(limit=50, page=i, order='asc')
                for dics in rDic['MovieList']:
                    inDatabase = yts.yts_isindatabase(dics['MovieID'], rArgs.database)
                    if inDatabase == True:
                        continue
                    else:
                        count += 1
                        yts.yts_database_write(dics, rArgs.database)            
            
            print ""
            print colored.green("{nMovies} where added to the database".format(nMovies=count))
        
        else:
            
            print colored.red("{database} is not a yts_scraper formated database".format(database=rArgs.database))
            sys.exit()
        
        
    #download magnetlink metadata to parse filenames (This needs to stay as last option or atleast below update)
    if rArgs.rawnames == True:
            if yts.yts_database_present(rArgs.database) == False:
                print colored.red('No database detected. Please run yts_scrape -u to create a database or check to see if your database exists')
                sys.exit()
            if yts.yts_isdatabase(rArgs.database) == False:
                print colored.red('This is not a yts_scrape formated database')
                sys.exit()
            rMAGs = yts.yts_magnet_query(rArgs.database)
        
            for MAGs in progress.bar(rMAGs):
                rFiles = yts.magnet2torrent(MAGs[0])
                for files in rFiles:
                    fslist = files.split(".")
                    if fslist[-1] == "mkv" or fslist[-1] == "mp4":
                        checkmod = yts.yts_gen_sql_change('YTS_DATA','RAWMovieName', 'TorrentMagnetUrl', MAGs[0], files, rArgs.database)
                        if checkmod == False:
                            print colored.red("Write Error Movie Name")
                            sys.exit()
                    if fslist[-1] == "srt":
                        checkmod = yts.yts_gen_sql_change('YTS_DATA','SUBS', 'TorrentMagnetUrl', MAGs[0], files, rArgs.database)
                        if checkmod == False:
                            print colored.red("Write Error SUBS")
                            sys.exit()                            
                    else:
                        checkmod = yts.yts_gen_sql_change('YTS_DATA','SUBS', 'TorrentMagnetUrl', MAGs[0], 'NA', rArgs.database)
                        if checkmod == False:
                            print colored.red("Write Error")
                            sys.exit()
                            
                listconvert = ','.join(rFiles)
                checkmod = yts.yts_gen_sql_change('YTS_DATA','RAWFileNames', 'TorrentMagnetUrl', MAGs[0], listconvert, rArgs.database)
                if checkmod == False:
                    print colored.red("Write Error RAW Names")
                    sys.exit()
        
    sys.exit()






if __name__ == '__main__':
    
    main()