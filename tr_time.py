time_level = ['hour', 'day', 'week', 'month', 'year']

def time_meet(video_time, time_require):
	arr = video_time.split(' ')
	ref_arr = time_require.split(' ')
	if len(arr) != 3:
		print("Error!!! time string not legal for %s and ref: %s" % (video_time, time_require))
		print("the time must be like '1 hour ago'")
		return False
	arr[1] = arr[1].replace('s', '')
	if arr[1] not in time_level:
		return False

	level = time_level.index(arr[1])
	level_ref = time_level.index(ref_arr[1])
	if level > level_ref:
		return False
	elif level == level_ref:
		return arr[0] < ref_arr[0]
	else:
		return True
		
