#!/usr/bin/python
import requests
import bs4
import re
import time

root_url = 'https://www.youtube.com/'
user_url = root_url + 'user/'
user_list_suffix = '/playlists'
list_url = root_url + 'playlist?list='

def get_play_list(author):
	soup = bs4.BeautifulSoup(get_remote_response(user_url + author + user_list_suffix), 'html.parser')
	return [a.attrs.get('href') for a in soup.select('div.yt-lockup-content a[href^="/playlist?"]')]

def get_watch_list(list_suffix):
	soup = bs4.BeautifulSoup(get_remote_response(root_url + list_suffix.replace("/","")), 'html.parser')
	hrefs = soup.select('a[href^="/watch?"]')
	print("count: %d" % len(hrefs))
	watchs = set()
	for a in hrefs:
		watch = a.attrs.get('href').split('&')[0]
		watch = watch.replace('/','')
		watchs.add(watch)
	return watchs

def get_video_for_watch(watch_suffix):
	url = root_url + watch_suffix
	html = get_remote_response(url)
	count_s = re.findall(r'<meta itemprop="interactionCount" content="(\d+)">', html)
	count = int(count_s[0])
	title_s = re.findall(r'"title":"(.*?)"', html)
	title = title_s[0]
	dist_s = re.findall(r'<strong class="watch-time-text">(.*)</strong>', html)
	dist_date = dist_s[0]
	return [title, dist_date, count]

def get_remote_response(url): 
	while(True):
		try:
                	response = requests.get(url)
			break
        	except Exception as e:
                	print("Error!!! for url: %s with reason:\n%s" % (url, e))
           		time.sleep(60)     
	return response.text
#print(get_view_count_for_watch('watch?v=19kPdeqJxYU'))
#print(get_play_lists('itsJudysLife'))
