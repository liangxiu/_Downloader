from __future__ import unicode_literals
import os
import fetch_video_info as parse 
import sys
import video_downloader as downer
import persists as p
import time
import fetch_videos as fetcher_youtube
import fetch_videos_vimeo as fetcher_vimeo
import tr_time
import signal
from multiprocessing.dummy import Pool as ThreadPool, Lock, Value

pid = os.getpid()

def handler(signum, frame):
    	print('stop the job')
	os.kill(pid, 1)

# Set the signal handler and a 5-second alarm
#signal.signal(signal.SIGINT, handler)

while (True): 
	print("check fail videos")
	downer.re_download_fails()
	print("fail videos redownload done")
	
	author = p.fetch_author()
	if author == None:
		time.sleep(10)
		continue

	print("getting video lists for " + author.author)
	fetcher = fetcher_youtube
	if author.author.startswith('vimeo:'):
		fetcher = fetcher_vimeo
		videos = fetcher.get_videos(author.author.replace('vimeo:', ''))
	else:
		videos = fetcher.get_videos(author)
	#play_lists = parse.get_play_list(author)
	print("got video lists for %s with len: %d" % (author, len(videos)))
	total = len(videos)
	lock = Lock()
	count = Value('i', 0)
	success_videos = p.fetch_success_videos()
	if success_videos is None:
		success_videos = []
	#i = 1
	#start_time = time.time()
	#for video in videos:
	def download_video(video):
		#cost = (time.time() - start_time)/60
		#i = i + 1
		with lock:
			count.value += 1
			print("fetching the %dth/%d video: %s" % (count.value, total, video.video_id))
		#check download video item
		dir_path = fetcher.dir_path(author.author)
		before_item = downer.has_download_item(video.title, dir_path)
		print("has before item: %s" % before_item)
		if before_item is not None and not before_item.endswith('.part'):
	        	return
		#check time limit from settings
		if author.time_limit is not None:
			print("check time condition: %s" % video.time_string)
			if not tr_time.time_meet(video.time_string, author.time_limit):
				print('No download, time not meet for ' + video.time_string)
				return	
		video_url = fetcher.video_url(video.video_id)
		#check download urls
		if video_url in success_videos:
			return
		full_path = fetcher.video_dest(author.author, video)
                downer.download_video(video_url, full_path)	
	
	pool = ThreadPool(3)
	pool.map_async(download_video, videos).get(999999999)
	pool.close()
	pool.join()
	p.record_author(author)
