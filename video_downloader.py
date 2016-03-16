import youtube_dl

def download_video(url, output):
	ydl_opts = {
		'outtmpl': output+'_%(title)s_%(upload_date)s.%(ext)s'
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try:	
			ydl.download([url])
		except Exception as e:
			print("Download error: %s" % e)
