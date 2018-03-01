import pywt
from scipy.signal import butter, lfilter

def denoise_wavelet(signal):
	cA, cD = pywt.dwt(signal, 'db5')
	return cA

def denoise_butterworth(signal):
	"""To implement. band pass between"""
	b, a = butter(4, 0.3, btype='low')
	y = lfilter(b, a, signal)
	return y