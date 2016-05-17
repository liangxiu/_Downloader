from __future__ import unicode_literals
import os
import fetch_video_info as parse 
import sys
import video_downloader as downer
import persists as fetcher
import time
import fetch_videos as fetcher2

while (True): 
	print("check fails")
	downer.re_download_fails()
	print("fails redownload done")
	
	author = fetcher.fetch_author()
	if author == None:
		time.sleep(10)
		continue

	root_url = parse.root_url
	dir_path = '%s/%s' % (os.getcwd(), author.author)
	try:
		os.makedirs(dir_path)
	except OSError as e:
		print("dir already exists")

	print("getting video lists for " + author.author)
	videos = fetcher2.get_videos(author)
	#play_lists = parse.get_play_list(author)
	print("got video lists for %s with len: %d" % (author, len(videos)))
	
	i = 1
	start_time = time.time()
	for video in videos:
		cost = (time.time() - start_time)/60
		print("fetching the %dth/%d video: %s time cost:%d minutes " % (i, len(videos), video.video_id, cost))
		i = i + 1
		video_url = root_url + '/watch?v=' + video.video_id
		before_item = downer.has_download_item(video.title, dir_path)
                full_path = False
                if before_item is None:
                	output = dir_path
                else:
			print("has before download item: %s" % before_item)
			if before_item.endswith('.mp4'):
				continue
                	output = dir_path + "/" +  before_item.replace('.part', '')
                        full_path = True
                downer.download_video(video_url, output, video.title, full_path)	
	fetcher.record_author(author)
