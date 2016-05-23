import operator
import codecs
import os
from collections import namedtuple

Author = namedtuple('Author', 'author, channel, time_limit')
Video = namedtuple("Video", "video_id title source click_count time_string")
Video.__new__.__defaults__ = ('',)*len(Video._fields)
Author.__new__.__defaults__ = (None,)*len(Author._fields)

def fetch_author():
	author_file = open("author_input.txt")
	author_text = author_file.read()
	author_text = author_text.replace('\r', '')
        authors = author_text.split('\n')
	author_file.close()
	try:
		done_authors = open("author_output.txt", 'r')
		file_text = done_authors.read()
		file_text = file_text.replace('\r', '')
		authored = file_text.split('\n')
		done_authors.close()
	except:
		authored = []	
	for author in authors:
		if len(author) == 0 or author.startswith('#'):
			continue
		author_attr = author.split(',')
		author_item = author_attr[0]
		if author_item in authored:
			continue
		else:
			arr = author_attr
			if len(arr) ==  1:
				return Author(arr[0])
			else:
				def getfeature(feature):
					for item in arr:
						if item.strip().startswith(feature):
							return item.replace(feature, '')		
				channel = getfeature('channel:')
				time_limit = getfeature('time_limit:')
				if channel is not None:
					channel = channel.strip()
				if time_limit is not None:
					time_limit = time_limit.strip()
				print("author arr: %s" % arr)
				return Author(arr[0], channel, time_limit)

def record_author(author):
	file = open("author_output.txt", 'a')
	file.write(author.author + '\n\r')
	file.close()


def record_fail_download(url, output):
	file = open("fail_videos.txt", 'a')
	file.write(url + ',,' + output + '\n')
	print("failed for dest: " + output)
	file.close()

def record_success_download(url):
	#update success_videos.txt
	file = open('success_videos.txt', 'a')
	file.write(url + '\n');
	file.close()
	#update fail_videos.txt
	file = open("fail_videos.txt")
	urls = file.read().split('\n')
	file.close()
	if len(urls) == 0:
		return
	file = open("fail_videos.txt", 'w')
	for line in urls:
		if len(line) == 0:
			continue
		if not line.startswith(url):
			file.write(line + '\n')

def fetch_fail_video():
	try:
		file = open("fail_videos.txt")
	except:
		return
	urls = file.read().split('\n')
	if len(urls) == 0:
		reutrn
	else:
		url_dict = dict()
		for url in urls:
			if len(url) == 0:
				continue
			if url not in url_dict:
				url_dict[url] = 1
			else:
				url_dict[url] = url_dict[url] + 1
		new_dict = {k:v for k,v in url_dict.items() if v < 3 }
		if len(new_dict) == 0:
			return
		sorted_dict = sorted(new_dict.items(), key = operator.itemgetter(1))
		return sorted_dict[0][0]

def fetch_success_videos():
	if not os.path.isfile('success_videos.txt'):
		return
	file = open('success_videos.txt')
	urls = file.read().split('\n')
	file.close()
	return urls

def store_videos_to_file(videos, author):
	if len(videos) == 0:
		return
	file_out = codecs.open(author+"_videos.txt", 'w', 'utf-8')
	for video in videos:
		write_line = video.video_id  + "##" + video.title
		if video.source != None:
			write_line += '##' + video.source
		if video.click_count != None:
			write_line += '##' + video.click_count
		if video.time_string != None:
			write_line += '##' + video.time_string
		file_out.write(write_line + '\n')
	file_out.close()

def cached_videos_for_author(author):
	try:
		file_in = open(author + '_videos.txt', 'r')
		videos = []
		for line in file_in.readlines():
			line = line.replace('\n', '')
			arr = line.split('##')
			video = None
			if len(arr) == 2:
				video = Video(arr[0], arr[1])
			elif len(arr) == 3:
				video = Video(arr[0], arr[1], arr[2])
			elif len(arr) == 4:
				video = Video(arr[0], arr[1], arr[2], arr[3])
			elif len(arr) == 5:
				video = Video(arr[0], arr[1], arr[2], arr[3], arr[4])
			if video is not None:
				videos.append(video)
		return videos
	except Exception as e:
		print("error: %s" % e)
		return	

def test():
	item = fetch()
	print(item)
	record_author(item)
	item = fetch()
	print(item)
	record_author(item)

def test2():
	record_fail_download('aaaa', 'bbbb')
	record_fail_download('cccc', 'dddd')
	fail = fetch_fail_video()
	print(fail)
	record_success_download('cccc')
	print(fetch_fail_video())
#test2()
