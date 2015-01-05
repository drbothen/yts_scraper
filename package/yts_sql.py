
import sqlite3 as db
import os
import sys

def yts_database_init(databasename='YTS_DATA.db'):
	"""Creates Initial Database to Store Data in from raw_torrents function. Usfull for creating a copy of YTS in conjuction with yts_database_populate_init
	
	ARGS:
	  databasename: (str, optional): Sets the name of the database to create
	"""
	try:
		conn = db.connect(databasename)
		c = conn.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS YTS_DATA
		(
		MovieID INT,
		MovieTitle TEXT,
		MovieTitleClean TEXT,
		AgeRating TEXT,
		Genre TEXT,
		Quality TEXT,
		MovieYear INT,
		SizeByte INT,
		Size TEXT,
		ImdbCode TEXT,
		ImdbLink TEXT,
		TorrentHash TEXT,
		TorrentMagnetUrl TEXT,
		State TEXT,
		RAWFileNames TEXT,
		RAWMovieName TEXT,
		SUBS TEXT
		);''')
	
		#Create 1080p Movie View
		c.execute("CREATE VIEW IF NOT EXISTS YTS_1080p AS \
		SELECT * \
		FROM YTS_DATA \
		WHERE Quality = '1080p'")
		#Create 720p Movie View
		c.execute("CREATE VIEW IF NOT EXISTS YTS_720p AS \
		SELECT * \
		FROM YTS_DATA \
		WHERE Quality = '720p'")
		#Create 3D Movie View
		c.execute("CREATE VIEW IF NOT EXISTS YTS_3D AS \
		SELECT * \
		FROM YTS_DATA \
		WHERE Quality = '3D'")
		#Create the 1080p Movie List that is not in 720p
		c.execute("CREATE VIEW IF NOT EXISTS YTS_1080p_NOT_IN_720p AS \
		SELECT * \
		FROM YTS_1080p \
		WHERE MovieTitleClean NOT IN \
		(SELECT MovieTitleClean FROM YTS_720p)")
		#Create 720p Movie List that is no in 1080p
		c.execute("CREATE VIEW IF NOT EXISTS YTS_720p_NOT_IN_1080p AS \
		SELECT * \
		FROM YTS_720p \
		WHERE MovieTitleClean NOT IN \
		(SELECT MovieTitleClean FROM YTS_1080p)")
		
		conn.commit()
		conn.close()
		
		return True
	except:
		return False
	

def yts_database_present(databasename='YTS_DATA.db'):
	
	try:
		if os.path.isfile(databasename):
			conn = db.connect(databasename)
			c = conn.cursor()
			c.execute("SELECT name \
			FROM sqlite_master \
			WHERE type='table'\
			AND name='YTS_DATA'")
			rows = c.fetchall()
			
			if len(rows) == 1:
				conn.close()
				return True
			else:
				conn.close()
				return False
		else:
			return False
	except:
		return False
	
def yts_isdatabase(databasename='YTS_DATA.db'):
	
	try:
		conn = db.connect(databasename)
		c = conn.cursor()
		c.execute("SELECT MovieID \
		FROM 'YTS_DATA'")
		rows = c.fetchall()
	
		if len(rows) > 0:
			conn.close()
			return True
		else:
			conn.close()
			return False
	except:
		
		return False
				
		
	
	
	

def yts_database_write(dic, databasename='YTS_DATA.db'):
	
	try:
		conn = db.connect(databasename)
		c = conn.cursor()
		
		c.execute('INSERT INTO YTS_DATA (MovieID,MovieTitle,MovieTitleClean,AgeRating,Genre,Quality,MovieYear,SizeByte,Size,ImdbCode,ImdbLink,TorrentHash,TorrentMagnetUrl,State)\
		VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (dic['MovieID'],dic['MovieTitle'],dic['MovieTitleClean'],dic['AgeRating'],dic['Genre'],dic['Quality'],dic['MovieYear'],dic['SizeByte'],dic['Size'],dic['ImdbCode'],dic['ImdbLink'],dic['TorrentHash'],dic['TorrentMagnetUrl'],dic['State']))
		
		conn.commit()
		conn.close()
		
		return True
	except:
		return False
	
	
def yts_isindatabase(mID, databasename='YTS_DATA.db'):
	
	try:
		conn = db.connect(databasename)
		c = conn.cursor()
		c.execute("SELECT YTS_DATA.MovieID FROM 'YTS_DATA' WHERE MovieID = ? ", (mID,))
		rows = c.fetchall()
		if len(rows) >= 1:
			
			conn.close()
			return True
		else:
			
			conn.close()
			return False
	except:
		
		return False


def yts_magnet_query(databasename='YTS_DATA.db'):
	
	try:
		conn = db.connect(databasename)
		c = conn.cursor()
		c.execute("SELECT TorrentMagnetUrl FROM 'YTS_DATA' WHERE RAWFileNames is null or RAWFileNames = ''")
		rows = c.fetchall()
		
		if len(rows) < 1:
			
			conn.close()
			return False
		else:
			conn.close()
			return rows
	except:
		
		return False
def yts_gen_sql_change(table, col1, col2, dataf, datac, databasename='YTS_DATA.db'):
	
	try:
		conn = db.connect(databasename)
		c = conn.cursor()
		
		sql = """
		UPDATE {tablen} 
		SET {colm1} = '{datachange}' 
		WHERE {colm2} = '{datafind}'""".format(tablen=table.replace("'","''"), colm1=col1.replace("'","''"), colm2=col2.replace("'","''"), datachange=datac.replace("'","''"), datafind=dataf.replace("'","''"))
		#print sql
		#c.execute("UPDATE %s SET %s = %s WHERE %s = %s"%(table, col1, col2, datac, dataf))
		c.execute(sql)
		conn.commit()
		conn.close()		
		#sys.exit()
		return True
	except:
		return False