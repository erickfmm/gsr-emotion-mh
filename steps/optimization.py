import itertools
import steps.helper as helper


def all_combinations_of_features(inputs, outputs, classification_algorithm):
	i_model = 0
	max_i = 15
	best_acc = 0
	with open('output.txt', 'w') as output_file:
		output_file.write("Number of features, Features, Mean Accuracy, Std Accuracy\n")
		for number_of_features in range(len(inputs[0])):
			if number_of_features < 1:
				continue
			combinations = itertools.combinations(range(len(inputs[0])), number_of_features)
			for combination in list(combinations):
				new_inputs = []
				for model_input in inputs:
					new_input = []
					for i in combination:
						new_input.append(model_input[i])
					new_inputs.append(new_input)
				#if i_model >= max_i:
				#	return
				model, scores = classification_algorithm(new_inputs, outputs)
				#print("number_of_features: ", number_of_features, "combination: ", combination)
				
				output_file.write(str(number_of_features)+","+helper.list_to_str(combination, '+')+","+str(scores.mean())+","+str(scores.std())+"\n")
				if best_acc < scores.mean():
					best_acc = scores.mean()
				if i_model % 100 == 0:
					print("it: %d, Accuracy: %0.3f" % (i_model, best_acc))
					output_file.flush()
				i_model += 1