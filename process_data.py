import os
from os.path import join, splitext, basename
import pickle
import pywt
import re
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score


all_features = {}
inputs = []
outputs = []

def is_integer(s, base=10):
	try:
		val = int(s, base)
		return True
	except ValueError:
		return False

def denoise_wavelet(gsr):
	min = int(len(gsr)/2-(256*3))
	max = int(len(gsr)/2+(256*3))
	cA, cD = pywt.dwt(gsr[min:max], 'db5')
	return cA

def denoise_butterworth(gsr):
	"""To implement. band pass between"""
	return [1]

def get_feature_vector(signal):
	features = []
	features.append(np.median(signal))
	features.append(np.mean(signal))
	features.append(np.std(signal))
	features.append(np.min(signal))
	features.append(np.max(signal))

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
	"""
	Frequency
	Median, mean, standard deviation, maximum, minimum, maximum and minimum (¿6?)
	"""
	return features

i = []
i.append(0)

def process_data(emo, gsr):
	cA = denoise_wavelet(gsr)
	features = get_feature_vector(cA)
	all_features[emo].append(features)
	inputs.append(features)
	outputs.append(emo)
	i[0] += 1
	print(i[0])
	#print("valores de cA (6 segundos del medio) para emocion: "+str(emo)+" es: ", features)


def read_files(folder_with_sessions):
	for root, dirs, files in os.walk(folder_with_sessions):
		for file in files:
			if os.path.splitext(file)[1] == '.dat':
				basename = os.path.basename(file)
				emo = re.search(r"(\d)+_*", basename)
				if emo:
					emo = emo.group(0)[:-1]
					if is_integer(emo):
						if not (int(emo, 10) in [0, 1, 3, 4, 12]):
							continue
						if not (int(emo, 10) in all_features):
							all_features[int(emo, 10)] = []
						gsr = pickle.load(open(join(root, file), 'rb'))
						process_data(int(emo, 10), gsr)


if __name__ == '__main__':
	read_files('./gsr_mahnob_data')
	with open("features.txt", 'w') as features_file:
		features_file.write(str(all_features))
	print("learning")
	clf = svm.SVC(kernel='rbf', C=1)
	scores = cross_val_score(clf, inputs, outputs, cv=10)
	print("Accuracy: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std() * 2))