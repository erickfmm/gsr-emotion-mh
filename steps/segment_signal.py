

#gsr, 6, 256
def get_middle_seconds(signal, seconds, frequency):
	half_seconds = seconds/2
	min = int(len(signal)/2-(frequency*half_seconds))
	max = int(len(signal)/2+(frequency*half_seconds))
	return signal[min:max]