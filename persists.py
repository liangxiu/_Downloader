import operator
from collections import namedtuple

Author = namedtuple('Author', 'author, channel')

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
		if len(author) == 0:
			continue
		author_attr = author.split(',')
		author_item = author_attr[0]
		if author_item in authored:
			continue
		else:
			if len(author_attr) > 1:
				return Author(author_attr[0], author_attr[1])
			return Author(author_attr[0], None)


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
