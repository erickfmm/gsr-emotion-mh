import os
from os.path import join
import xml.etree.ElementTree as ET
import pyedflib
import numpy as np
import pickle

def is_integer(s, base=10):
	try:
		val = int(s, base)
		return True
	except ValueError:
		return False

def process_file(felt_emo, filename, session_id, folder_to_save):
	with pyedflib.EdfReader(filename) as f:
		#num_samples = f.getNSamples()[40]
		gsr = f.readSignal(40)
		pickle_file_path = join(folder_to_save, str(felt_emo)+"_"+str(session_id)+"_gsr.dat")
		print("filename: ", pickle_file_path)
		with open(pickle_file_path, 'w') as pickle_file:
			pickle.dump(gsr, pickle_file)

def process_session(root_dir, filename, files, folder_to_save):
	tree = ET.parse(join(root_dir, filename))
	root = tree.getroot()
	session_id = str(root.get('sessionId'));
	felt_emo = str(root.get('feltEmo'))
	if is_integer(session_id) and is_integer(felt_emo):
		felt_emo = int(felt_emo, 10)
		for file in files:
			if file.lower().endswith('.bdf'):
				print(felt_emo, join(root_dir, file))
				process_file(felt_emo ,join(root_dir, file), session_id, folder_to_save)


def  process_all_sessions(folder_with_sessions, folder_to_save):
	for root, dirs, files in os.walk(folder_with_sessions):
		if 'session.xml' in files:
			process_session(root, 'session.xml', files, folder_to_save)


if __name__ == '__main__':
	process_all_sessions('./Sessions', './selected_train_data/')