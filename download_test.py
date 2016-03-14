import os
import fetch_video_info as parse 
import sys

#os.system("https_proxy=http://localhost:8123 youtube-dl -citk https://www.youtube.com/playlist?list=PL210C2267A8922854")

author = sys.argv[1] 
root_url = parse.root_url
#play_list = "PLArWY9K8FKZt0-UFYXs8hswGs0Lww59Cj"
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
		print("got videoInfo: %s" % videoInfo)
		print("downloading video for watch: " + watch)
		os.system("https_proxy=http://localhost:8123 youtube-dl -citk " + video_url)
