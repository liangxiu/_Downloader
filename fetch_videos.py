import bs4
import requests
import time
import json
import persists as p
from collections import namedtuple
import codecs
import os

root_url = "https://www.youtube.com"

def parse_video_div(div):
	video_id = div.get("data-context-item-id", "")
    	title = div.find("a", "yt-uix-tile-link").text
	first_li_tag = div.find("ul", 'yt-lockup-meta-info').find('li')
	click_count = first_li_tag.text.replace('views', '').strip()
	time_string = first_li_tag.find_next_sibling('li').text.strip()
    #duration = div.find("span", "video-time").contents[0].text
    #views = int(div.find("ul", "yt-lockup-meta-info").contents[0].text.rstrip(" views").replace(",", ""))
    #img = div.find("img")
    #thumbnail = "http:" + img.get("src", "") if img else ""
    #return Video(video_id, title, duration, views, thumbnail)
	return p.Video(video_id, title, '', click_count, time_string)

def parse_videos_page(page):
    video_divs = page.find_all("div", "yt-lockup-video")
    return [parse_video_div(div) for div in video_divs]

def find_load_more_url(page):
    for button in page.find_all("button"):
        url = button.get("data-uix-load-more-href")
        if url:
            return root_url + url

def download_page(url):
    try:
        return requests.get(url).text
    except Exception as e:
	print("Error!!! downloading url:%s with exception: %s" % (url, e))

def get_videos(username):
    cached_videos = p.cached_videos_for_author(username.author)
    if cached_videos != None:
	print("has cached videos")
	return cached_videos
    if username.channel != None:
	page_url = "{0}/channel/{1}/videos".format(root_url, username.channel.strip())	
    else: 
	page_url = "{0}/user/{1}/videos".format(root_url, username.author)
    page = bs4.BeautifulSoup(download_page(page_url), "html.parser")
    videos = parse_videos_page(page)
    page_url = find_load_more_url(page)
    while page_url:
	print("getting more page")
	page_response = download_page(page_url)
	if page_response == None:
		print("Download fail, sleep then continue")
		time.sleep(4)
		continue
        json_data = json.loads(page_response)
        page = bs4.BeautifulSoup(json_data.get("content_html", ""), "html.parser")
        videos.extend(parse_videos_page(page))
        page_url = find_load_more_url(bs4.BeautifulSoup(json_data.get("load_more_widget_html", ""), 'html.parser'))
	time.sleep(1)
    p.store_videos_to_file(videos, username.author)
    return videos

def video_url(video_id):
        return root_url + '/watch?v=' + video_id

def video_dest(author, video):
	full_path = dir_path(author) + '/%(upload_date)s_' + video.title.replace('/','') + '.%(ext)s'
	return full_path

def dir_path(author):
        root = os.getcwd()
        dir_path = root + '/' + author
        if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
        return dir_path	

if __name__ == "__main__":
	videos = get_videos(p.Author('FunForLouis', None))
	print(videos)
