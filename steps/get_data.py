import os
from os.path import join, splitext, basename
import pickle
import re
import steps.helper as helper




all_features = {}
def read_files(folder_with_sessions):
	extracted_data = []
	for root, dirs, files in os.walk(folder_with_sessions):
		for file in files:
			if os.path.splitext(file)[1] == '.dat':
				basename = os.path.basename(file)
				emo = re.search(r"(\d)+_*", basename)
				if emo:
					emo = emo.group(0)[:-1]
					if helper.is_integer(emo):
						if not (int(emo, 10) in [0, 1, 3, 4, 12]):
							continue
						if not (int(emo, 10) in all_features):
							all_features[int(emo, 10)] = []
						gsr = pickle.load(open(join(root, file), 'rb'))
						extracted_data.append({'tag': int(emo, 10), 'data': gsr})
	return extracted_data