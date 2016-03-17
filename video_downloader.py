from __future__ import unicode_literals
import youtube_dl
import persists
import os

def download_video(url, output, full_path=False):
	def download_progress(d):
		if d['status'] == 'error':
			persists.record_fail_download(url, output)
		elif d['status'] == 'finished':
			persists.record_success_download(url)		
	if not full_path:
		output = output+'_%(upload_date)s.%(ext)s'	
	ydl_opts = {
		'outtmpl': output,
		'progress_hooks': [download_progress]
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try:	
			ydl.download([url])
		except Exception as e:
			print("Download error: %s" % e)
			persists.record_fail_download(url, output)

def has_download_item(title, file_dir):
	for item in os.listdir(file_dir):
		if item.find(title) >= 0:
			newitem = item.replace('.part', '')	
			return newitem

def re_download_fails():
	while(True):
		fail = persists.fetch_fail_video()
		if fail == None:
			break
		fails = fail.split(',')
		download_video(fails[0], fails[1])	


