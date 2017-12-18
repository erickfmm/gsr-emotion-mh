import numpy as np



def get_feature_vector(signal):
	features = []
	features.append(np.median(signal))
	features.append(np.mean(signal))
	features.append(np.std(signal))
	features.append(np.min(signal))
	features.append(np.max(signal))
	features.append(np.max(signal)-np.min(signal))

	ratios = []
	first_differences = []
	last_sample = 0
	first = True
	for sample in signal:
		if first:
			last_sample = sample
			first = False
			continue
		first_differences.append(np.absolute(sample - last_sample))
		ratios.append(np.absolute(sample / last_sample))
		last_sample = sample

	features.append(np.min(first_differences))
	features.append(np.max(first_differences))

	features.append(np.min(ratios))
	features.append(np.max(ratios))

	#########################################################
	#second step
	features.append(np.median(first_differences))
	features.append(np.mean(first_differences))
	features.append(np.std(first_differences))
	features.append(np.max(first_differences)-np.min(first_differences))
	#features.append(np.min(first_differences))
	#features.append(np.max(first_differences))

	second_step_ratios = []
	second_differences = []
	last_sample = 0
	first = True
	for sample in first_differences:
		if first:
			last_sample = sample
			first = False
			continue
		second_step_ratios.append(np.absolute(sample / last_sample))
		second_differences.append(np.absolute(sample - last_sample))
		last_sample = sample

	features.append(np.min(second_differences))
	features.append(np.max(second_differences))

	features.append(np.min(second_step_ratios))
	features.append(np.max(second_step_ratios))
	#############################################################################3
	#third step
	features.append(np.median(second_differences))
	features.append(np.mean(second_differences))
	features.append(np.std(second_differences))
	features.append(np.max(second_differences)-np.min(second_differences))
	#features.append(np.min(second_differences))
	#features.append(np.max(second_differences))

	third_step_ratios = []
	third_differences = []
	last_sample = 0
	first = True
	for sample in second_differences:
		if first:
			last_sample = sample
			first = False
			continue
		third_differences.append(np.absolute(sample - last_sample))
		third_step_ratios.append(np.absolute(sample / last_sample))
		last_sample = sample

	features.append(np.min(third_differences))
	features.append(np.max(third_differences))

	features.append(np.min(third_step_ratios))
	features.append(np.max(third_step_ratios))
	features.append(np.max(third_differences)-np.min(third_differences))
	"""
	Median, mean, standard deviation, minimum, maximum, minimum, maximum ratio, and maximum and minimum difference
	first order difference and two order difference and 6
	Median, mean, standard deviation, minimum, maximum, minimum, maximum ratio, and maximum and minimum difference
	"""
	#################
	fft = np.fft.fft(signal)
	features.append(np.absolute(np.median(fft)))
	features.append(np.absolute(np.mean(fft)))
	features.append(np.absolute(np.std(fft)))
	features.append(np.absolute(np.max(fft)))
	features.append(np.absolute(np.min(fft)))
	features.append(np.absolute(np.min(fft)+np.max(fft))) #ni idea, dice "maximum and minimum" y no sé que es y es una sola cosa o no da la cantidad ._.
	features.append(np.absolute(np.max(fft)-np.min(fft)))
	"""
	Frequency
	Median, mean, standard deviation, maximum, minimum, maximum and minimum (¿6?)
	"""
	return features