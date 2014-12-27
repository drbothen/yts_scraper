import transmissionrpc
#from smb.SMBConnection import SMBConnection
import os as o
import package as yts
import sqlite3 as db


conn = db.connect(':memory:')

#for moveie in o.listdir("Y:\")




#tc = transmissionrpc.Client('192.168.1.14', port=9091)
#for torrent in tc.get_torrents():
#    print torrent

t = yts.Rawyts()

dic = t.raw_torrents()

print dic

#print dic['MovieCount']