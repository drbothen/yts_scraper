import argparse

__author__ = 'Joshua Magady'

desc = "This program ties into YTS api and builds a database. \
It can also send magnetlinks to transmission for downloading"

def args_parse(args):
    try:
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help="Enables Verbose Output")
        parser.add_argument('-d', '--database',
                            default='YTS_DATA.db',
                            help="This option specifies a database (the Default is YTS_DATA.db)")
        parser.add_argument('-u', '--update',
                            action='store_true',
                            help="This option updates the database. if -d is not given uses the default value. if database does not exist one will be created")
        parser.add_argument('-rn', '--rawnames',
                            action='store_true',
                            help='Starts an instance of libtorrent and downloads metadata to parse filenames. Mast have created a database already for this to work (use at your own risk)')        
        parser.add_argument('-ru', '--recursiveupdate',
                            action='store_true',
                            help="Recursively updates the entire database")
        parser.add_argument('-ls', '--libraryscan',
                            help="This option scans your personal library and builds a table in your database P_Library with your collection (requires location of your library)")
        parser.add_argument('-lu', '--libraryupdate',
                            action='store_true',
                            help="Updates you YTS library. Use only after you use -u and requires a quality selection (-h or -l)")
        #parser.add_argument()
        parser.add_argument('-md', '--massdownload',
                            action='store_true',
                            help='Downloads ALL movies from YTS unless a quality is set and then it will only download movies with selected quality')
        parser.add_argument('-hq', '--highquality',
                            action='store_true',
                            help='favor 1080p movies over 720p')
        parser.add_argument('-lq', '--lowquality',
                            action='store_true',
                            help='favor 720p over 1080p')        
        pArgs = parser.parse_args(args)
        
        return pArgs
    
    except:
        
        return False
        


