import steps.helper as helper
import steps.denoise as denoise
import steps.classification as classification
import steps.extract_features as extractFeatures
import steps.get_data as getData
import steps.segment_signal as segmentSignal
import steps.optimization as optimization


if __name__ == '__main__':
	print("to read files")
	datas = getData.read_files('./gsr_mahnob_data')
	print("files readed")
	print("to extract features")
	inputs = []
	outputs = []
	i = 1
	for data in datas:
		print("Processing input: %d Percentage: %0.1f%%" % (i, i*100/len(datas)))
		cA = denoise.denoise_wavelet(data['data'])
		extracted_signal = segmentSignal.get_middle_seconds(cA, 6, 256)
		features = extractFeatures.get_feature_vector(extracted_signal)
		inputs.append(features)
		outputs.append(data['tag'])
		i += 1
	print("to learn")
	#optimization.all_combinations_of_features(inputs, outputs, classification.svm_rbf)
	model, scores = classification.svm_rbf(inputs, outputs)
	print("Accuracy: %0.3f. Standard Deviation: %0.3f" % (scores.mean(), scores.std()))