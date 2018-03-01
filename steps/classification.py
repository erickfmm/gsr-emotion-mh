from sklearn import svm
from sklearn.model_selection import cross_val_score


def learn_svm(inputs, outputs, kernel, C):
	clf = svm.SVC(kernel=kernel, C=C)
	scores = cross_val_score(clf, inputs, outputs, cv=10)
	model = clf.fit(inputs, outputs)
	return model, scores

def learn_svm_linear(inputs, outputs, C):
	clf = svm.LinearSVC(C=C)
	scores = cross_val_score(clf, inputs, outputs, cv=10)
	model = clf.fit(inputs, outputs)
	return model, scores