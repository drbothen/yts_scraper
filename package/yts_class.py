import requests

class Rawyts:
	def __init__(self):
		pass

	def raw_upcoming(self):
		"""This function pulls the upcomming movies list from yst
		Args:
		  None
		Returns:
		  Dictionary of values
		Raises:
		  No error checking is performed
		"""
		url = 'https://yts.re/api/upcoming.json'
		res = requests.get(url)
		dic = res.json()
		return dic

	def raw_torrents(self,limit=20,page=1,quality='ALL',rating=0,genre='ALL',sort='date',order='desc'):
		"""This function will retrieve all movies that match the given parameters
		
		Args:
		  limit (int, optional): sets the limit on how many matches to return per page. int value between 1 - 50, defualt is 20
		  page (int, optional): used to set the page number to see the next set of movies. eg: limit=15 and set=2 will show you movies 16-39
		  quality (str, optional): ability to selct a quality type to filter by. valid options 720p, 1080p, 3D, ALL. All is the defualt
		  rating (int, optional): set minimum movie rating for display. int between 0-9
		  genre (str, optional): display movies from chosen type genre. defualt is ALL. See www.imdb.com/genre/ for a full list.
		  sort (str, optional): sorts results by the choosen method. Acceptable methods are: date, seeds, peers, size, alphabet, rating, downloaded, year
		  order (str, optional): Orders the results with either asending or descending, acceptable methods are: desc, asc
		Returns:
		  returns a dictionary as first #and pagecount as secound#. first entry is the total list of movies 'MovieCount', the second is the list of movies with dictionaries per movie 'MovieList'.
		  #Page count is determined by dividing moviecount by limit and adding 1 if the value is float#
		Raises:
		  currently no error checking is performed
		  
		"""
		
		url = 'https://yts.re/api/list.json'
		payload = {'limit':limit,'set':page,'quality':quality,'rating':rating,'genre':genre,'sort':sort,'order':order}
		res = requests.get(url,params=payload)
		dic = res.json()
		#pagecount = dic['MovieCount']/limit
		#if isinstance(pagecount, float):
		#	pagecount += 1
		
		return dic

	def raw_latest(self):
		url = 'https://yts.re/api/list.json'
		res = requests.get(url)
		dic = res.json()
		return dic

	def raw_search(self,movie):
		url = 'https://yts.re/api/list.json'
		res = requests.get(url,params={'keywords':movie})
		dic = res.json()
		return dic

	def raw_requests_confirmed(self):
		url = 'https://yts.re/api/requests.json'
		res = requests.get(url,params={'page':'confirmed'})
		dic = res.json()
		return dic
	
	def raw_requests_page_count(self, limit):
		url = 'https://yts.re/api/list.json'
		payload = {'limit':limit}
		res = requests.get(url,params=payload)
		dic = res.json()
		pagecount = dic['MovieCount']/limit
		if isinstance(pagecount, float):
			pagecount += 1
		
		return pagecount		
	
	
	
