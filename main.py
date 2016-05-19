from __future__ import unicode_literals
import os
import fetch_video_info as parse 
import sys
import video_downloader as downer
import persists as p
import time
import fetch_videos as fetcher_youtube
import fetch_videos_vimeo as fetcher_vimeo

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
	
	i = 1
	start_time = time.time()
	for video in videos:
		cost = (time.time() - start_time)/60
		print("fetching the %dth/%d video: %s time cost:%d minutes " % (i, len(videos), video.video_id, cost))
		i = i + 1
		dir_path = fetcher.dir_path(author.author)
		before_item = downer.has_download_item(video.title, dir_path)
		print("has before item: %s" % before_item)
		if before_item is not None and not before_item.endswith('.part'):
			continue
		video_url = fetcher.video_url(video.video_id)
		full_path = fetcher.video_dest(author.author, video.title)
                downer.download_video(video_url, full_path)	
	fetcher.record_author(author)
