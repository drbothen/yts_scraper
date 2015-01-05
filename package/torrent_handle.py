import shutil
import tempfile
import sys
import libtorrent as lt
from time import sleep
import string


def magnet2torrent(magnet):


    tempdir = tempfile.mkdtemp()
    ses = lt.session()
    params = {
        'save_path': tempdir,
        'duplicate_is_error': True,
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True
    }
    handle = lt.add_magnet_uri(ses, magnet, params)

    #print("Downloading Metadata (this may take a while)")
    count = 0
    while (not handle.has_metadata()):
        try:
            sleep(1)
            s = handle.status()
            if s.active_time > 600:
                count += 1
                #print "Restarting Download Stalled"
                ses.pause()
                ses.remove_torrent(handle)
                ses.resume()
                handle = lt.add_magnet_uri(ses, magnet, params)
            if count > 2:
                break
        except KeyboardInterrupt:
            #print("Aborting...")
            ses.pause()
            #print("Cleanup dir " + tempdir)
            shutil.rmtree(tempdir)
            sys.exit(0)
    ses.pause()

    
    #print("Done")
    if handle.has_metadata():
        torinfo = handle.get_torrent_info()
        filelist = []
        for f in torinfo.files():
            filtereds = filter(lambda x: x in string.printable,str(f.path))
        #print f.path
        #print filtereds.encode(encoding="unicode_escape")
            fsplit = filtereds.split('\\')
    #sys.exit()
        #print fsplit
            filelist.append(fsplit[-1])
    #torfile = lt.create_torrent(torinfo)
    #torcontent = lt.bencode(torfile.generate())
    #print torcontent
    
    ses.remove_torrent(handle)
    check = False
    while check == False:
        try:
            
            shutil.rmtree(tempdir)
            check = True
            
        except:
        
            check = False
    
    return filelist

    
    
    
#magnet2torrent("magnet:?xt=urn:btih:a3fe0ab5ec6aeb66ec955202998933e9c239ae1b&dn=Harry+Potter+and+the+Half-Blood+Prince&tr=http://exodus.desync.com:6969/announce&tr=udp://tracker.openbittorrent.com:80/announce&tr=udp://open.demonii.com:1337/announce&tr=udp://exodus.desync.com:6969/announce&tr=udp://tracker.yify-torrents.com/announce") 