import pywt


def denoise_wavelet(signal):
	cA, cD = pywt.dwt(signal, 'db5')
	return cA

def denoise_butterworth(signal):
	"""To implement. band pass between"""
	return [1]