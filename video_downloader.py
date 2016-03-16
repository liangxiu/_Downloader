import youtube_dl
import persists

def download_video(url, output):
	def download_progress(d):
		if d['status'] == 'error':
			persists.record_fail_download(url, output)
		elif d['status'] == 'finished':
			persists.record_success_download(url)		
	ydl_opts = {
		'outtmpl': output+'_%(title)s_%(upload_date)s.%(ext)s',
		'progress_hooks': [download_progress]
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try:	
			ydl.download([url])
		except Exception as e:
			print("Download error: %s" % e)
			persists.record_fail_download(url, output)


def re_download_fails():
	while(True):
		fail = persists.fetch_fail_video()
		if fail == None:
			break
		fails = fail.split(',')
		download_video(fails[0], fails[1])	


