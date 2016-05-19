from __future__ import unicode_literals
import bs4
import requests
import time
import json
import persists as p
from collections import namedtuple
import codecs
import os
import video_downloader as downer

root_url = "https://vimeo.com"

def parse_video_div(div):
	video_url = div.find("a").get("href")
	video_id = video_url.split("/")[-1]
    	title = div.find("p", 'title').find('a').text
	p_tag = div.find("p", 'meta')
	author = p_tag.find('a').text
	span_tag = p_tag.find("span", "icon")
	click_count = None
	if span_tag is not None:
		click_count = span_tag.text.strip()
    #duration = div.find("span", "video-time").contents[0].text
    #views = int(div.find("ul", "yt-lockup-meta-info").contents[0].text.rstrip(" views").replace(",", ""))
    #img = div.find("img")
    #thumbnail = "http:" + img.get("src", "") if img else ""
    #return Video(video_id, title, duration, views, thumbnail)
	return p.Video(video_id, title, author, click_count)

def parse_videos_page(page):
    video_divs = page.find_all("li", "clearfix")
    if len(video_divs) == 0:
	return
    return [parse_video_div(div) for div in video_divs]

def download_page(url):
    print("Downloading page url: %s" % url)
    try:
        return requests.get(url).text
    except Exception as e:
	print("Error!!! downloading url:%s with exception: %s" % (url, e))

def get_videos(channel):
    cached_videos = p.cached_videos_for_author(channel)
    if cached_videos != None:
	print("has cached videos")
	return cached_videos
    page_url_tp = root_url + '/channels/%s/videos/page:%d/sort:preset/format:detail'
    i = 1
    videos = []
    while True:
        page_url = page_url_tp % (channel, i)
	page_text = download_page(page_url)
	if page_text == None:
		print("sleep 5 seconds and continue the page")
		time.sleep(5)
		continue
        page = bs4.BeautifulSoup(page_text, "html.parser")
        sub_videos = parse_videos_page(page)
        if sub_videos == None:
            break
	videos.extend(sub_videos)
	i += 1
        time.sleep(1)
    p.store_videos_to_file(videos, channel)
    return videos

def video_url(video_id):
	return root_url + '/' +  video_id

def video_dest(author, video):
	full_path = dir_path(author) + '/' + '%(upload_date)s_' + video.title.decode('utf-8') + '_' + video.source.decode('utf-8')
	if video.click_count != None:
		full_path += '_' + video.click_count 
        return full_path + '.%(ext)s'

def dir_path(author):
        root = os.getcwd()
        dir_path = root + '/' + author.replace("vimeo:", '')
        if not os.path.isdir(dir_path):
                os.mkdirs(dir_path)
        return dir_path	

if __name__ == "__main__":
	videos = get_videos('buildporn')
	print(videos)
