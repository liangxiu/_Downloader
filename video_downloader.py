from __future__ import unicode_literals
import youtube_dl
import persists
import os

def download_video(url, dest):
	def download_progress(d):
		if d['status'] == 'error':
			persists.record_fail_download(url, dest)
		elif d['status'] == 'finished':
			persists.record_success_download(url)		
	ydl_opts = {
		'outtmpl': dest,
		'progress_hooks': [download_progress]
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try:	
			ydl.download([url])
		except Exception as e:
			print("Download error: %s" % e)
			persists.record_fail_download(url, dest)

def has_download_item(title, file_dir):
	try:
		for item in os.listdir(file_dir):
			if item.find(title) >= 0:
				#newitem = item.replace('.part', '')	
				return item
	except:
		return None

def re_download_fails():
	while(True):
		fail = persists.fetch_fail_video()
		if fail == None:
			break
		fails = fail.split(',,')
		print(fail)
		download_video(fails[0], fails[1])	

if __name__ == '__main__':
	download_video('https://vimeo.com/159120552', './vimeo_test.mp4', None, True)
