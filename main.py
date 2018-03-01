import steps.helper as helper
import steps.denoise as denoise
import steps.classification as classification
import steps.extract_features as extractFeatures
import steps.get_data as getData
import steps.segment_signal as segmentSignal
import steps.optimization as optimization
import pickle
import numpy as np
import asyncio


async def mifun_train(i_c, inputs, outputs):
		print(i_c)
		model, scores = classification.learn_svm(inputs, outputs, 'rbf', 2**i_c)
		print("Accuracy: %0.3f. Standard Deviation: %0.3f" % (scores.mean(), scores.std()))

async def mifun_train_linear(i_c, inputs, outputs):
		print(i_c)
		model, scores = classification.learn_svm_linear(inputs, outputs, 2**i_c)
		print("Accuracy: %0.3f. Standard Deviation: %0.3f" % (scores.mean(), scores.std()))



if __name__ == '__main__':
	print("to read files")
	datas = getData.read_files('./gsr_mahnob_data')
	print("files readed")
	print("to extract features")
	inputs = []
	outputs = []
	i = 1
	for data in datas:
		print("Processing input: %d Percentage: %0.1f%% of secs: %0.2f" % (i, i*100/len(datas), len(data['data'])/256))
		cA = denoise.denoise_butterworth(data['data'])
		#cA = denoise.denoise_wavelet(cA)
		extracted_signal = segmentSignal.get_middle_seconds(cA, 30, 256)
		features = extractFeatures.get_feature_vector(extracted_signal)
		sub_features = [features[2], 
			features[4], 
			features[6], 
			features[7], 
			features[8], 
			features[9], 
			features[10], 
			features[14], 
			features[15], 
			features[16], 
			features[17], 
			features[18], 
			features[22], 
			features[23], 
			features[27] ]
		inputs.append(sub_features)
		outputs.append(data['tag'])
		#outputs.append(int(np.random.uniform(5)))
		i += 1
	print("to learn")
	#optimization.all_combinations_of_features(inputs, outputs, classification.svm_rbf)

	loop = asyncio.get_event_loop()

	
	try:
		for i_c in range(-10, 10):
			loop.run_until_complete(mifun_train(i_c, inputs, outputs))
	finally:
		loop.close()

	
	# Save to file in the current working directory
	#pkl_filename = "pickle_model.pkl"  
	#with open(pkl_filename, 'wb') as file:  
	#    pickle.dump(model, file)