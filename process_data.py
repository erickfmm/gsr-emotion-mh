import os
from os.path import join, splitext, basename
import pickle
import pywt
import re
import numpy as np

def is_integer(s, base=10):
	try:
		val = int(s, base)
		return True
	except ValueError:
		return False


def process_data(emo, gsr):
	min = int(len(gsr)/2-(256*3))
	max = int(len(gsr)/2+(256*3))
	cA, cD = pywt.dwt(gsr[min:max], 'db5')
	print("promedio de cA (6 segundos del medio) para emocion: "+str(emo)+" es: ", np.mean(cA))


def read_files(folder_with_sessions):
	for root, dirs, files in os.walk(folder_with_sessions):
		for file in files:
			if os.path.splitext(file)[1] == '.dat':
				basename = os.path.basename(file)
				emo = re.search(r"(\d)+_*", basename)
				if emo:
					emo = emo.group(0)[:-1]
					if is_integer(emo):
						gsr = pickle.load(open(join(root, file), 'r'))
						process_data(int(emo, 10), gsr)


if __name__ == '__main__':
	read_files('./gsr_mahnob_data')