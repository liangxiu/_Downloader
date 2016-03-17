import os
import fetch_video_info as parse 
import sys
import video_downloader as downer
import persists as fetcher
import time

while (True): 
	author = fetcher.fetch_author()
	if author == None:
		time.sleep(60)
		continue

	root_url = parse.root_url
	dir_path = '%s/%s' % (os.getcwd(), author)
	try:
		os.makedirs(dir_path)
	except OSError as e:
		print("dir already exists")

	print("getting playlists for " + author)
	play_lists = parse.get_play_list(author)
	print("got playlist for %s with len: %d" % (author, len(play_lists)))
	
	for item in play_lists:
		print("getting watch list for play list: " + item)
		watchs = parse.get_watch_list(item)
		print("got watch lists for %s with len: %d" % (item, len(watchs)))
		for watch in watchs:
			video_url = root_url + watch
			print("getting video info for watch " + watch)
			videoInfo = parse.get_video_for_watch(watch)
			if videoInfo is None:
				continue
			print("got videoInfo: %s" % videoInfo)
			print("downloading video for watch: " + watch)
			title = videoInfo[0]
			before_item = downer.has_download_item(title, dir_path)
			full_path = False
			if before_item is None:
				output = '%s/%d_%s' % (dir_path, videoInfo[2], videoInfo[0])
			else:
				output = dir_path + "/" +  before_item
				full_path = True
			downer.download_video(video_url, output, full_path)
	
	downer.re_download_fails()	
	fetcher.record_author(author)
