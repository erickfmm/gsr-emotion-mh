from sklearn import svm
from sklearn.model_selection import cross_val_score


def svm_rbf(inputs, outputs):
	clf = svm.SVC(kernel='rbf', C=1)
	scores = cross_val_score(clf, inputs, outputs, cv=10)
	model = clf.fit(inputs, outputs)
	return model, scores