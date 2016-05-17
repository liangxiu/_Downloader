from __future__ import unicode_literals
import youtube_dl
import persists
import os

def download_video(url, output, title, full_path=False):
	new_out = output
	if not full_path:	
		new_out = new_out + '/%(upload_date)s_' + title + '.%(ext)s'	
	def download_progress(d):
		if d['status'] == 'error':
			persists.record_fail_download(url, new_out)
		elif d['status'] == 'finished':
			persists.record_success_download(url)		
	ydl_opts = {
		'outtmpl': new_out,
		'progress_hooks': [download_progress]
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try:	
			ydl.download([url])
		except Exception as e:
			print("Download error: %s" % e)
			persists.record_fail_download(url, new_out)

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
		download_video(fails[0], fails[1], True)	


