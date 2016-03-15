#!/usr/bin/python
import requests
import bs4
import re

root_url = 'https://www.youtube.com/'
user_url = root_url + 'user/'
user_list_suffix = '/playlists'
list_url = root_url + 'playlist?list='

def get_play_list(author):
	try:
		response = requests.get(user_url + author + user_list_suffix)
	except Exception as e:
		print("Error!!! %s" % e)
		return []
	soup = bs4.BeautifulSoup(response.text, 'html.parser')
	return [a.attrs.get('href') for a in soup.select('div.yt-lockup-content a[href^="/playlist?"]')]

def get_watch_list(list_suffix):
	try:
		response = requests.get(root_url + list_suffix.replace("/",""))
	except Exception as e:
		print("Error!!! %s" % e)
		return []
	soup = bs4.BeautifulSoup(response.text, 'html.parser')
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
	try:
		response = requests.get(url)
	except Exception as e:
		print("Error!!! %s" % e)
		return
	html = response.text
	count_s = re.findall(r'<meta itemprop="interactionCount" content="(\d+)">', html)
	count = int(count_s[0])
	title_s = re.findall(r'"title":"(.*?)"', html)
	title = title_s[0]
	dist_s = re.findall(r'<strong class="watch-time-text">(.*)</strong>', html)
	dist_date = dist_s[0]
	return [title, dist_date, count]

#print(get_view_count_for_watch('watch?v=19kPdeqJxYU'))
#print(get_play_lists('itsJudysLife'))
