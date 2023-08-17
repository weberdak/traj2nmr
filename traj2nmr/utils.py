import numpy as np
import scipy.optimize as optimization

# GLOBALS

# Dictionary to convert between 
CONVERT = {
	'ALA': 'A', 'A': 'ALA', 'ARG': 'R', 'R': 'ARG', 'ASN': 'N', 'N': 'ASN', 'ASP': 'D', 'D': 'ASP',
	'CYS': 'C', 'C': 'CYS', 'GLN': 'Q', 'Q': 'GLN', 'GLU': 'E', 'E': 'GLU', 'GLY': 'G', 'G': 'GLY',
	'HIS': 'H', 'HSE': 'H', 'HID': 'H', 'HSD': 'H', 'HSP': 'H', 'H': 'HIS', 'ILE': 'I', 'I': 'ILE',
	'LEU': 'L', 'L': 'LEU', 'LYS': 'K', 'K': 'LYS', 'MET': 'M', 'M': 'MET', 'PHE': 'F', 'F': 'PHE',
	'PRO': 'P', 'P': 'PRO', 'SER': 'S', 'S': 'SER', 'THR': 'T', 'T': 'THR', 'SER': 'S', 'S': 'SER',
	'THR': 'T', 'T': 'THR', 'TRP': 'W', 'W': 'TRP', 'TYR': 'Y', 'Y': 'TYR', 'VAL': 'V', 'V': 'VAL',
	'ASX': 'B', 'B': 'ASX',
}

def convert_resname(resname):
	"""Convert between single and three-letter amino acid codes

	Parameters
	----------
	resname: str
		One or three-letter amino acid code

	Returns
	-------
	resname_out: str
		One-letter code if three-letter code input, or three-ltter code if one-letter code input
	"""
	return CONVERT[resname]


def evolving_stats(data):
	"""Fast proc to compute running mean and standard deviation

	Parameters
	----------
	data: list of floats
		List of data, usually a time series

	Returns
	-------
	result: list of tuples
		[(mean1, stdev1), (mean2, stdev2),...,(meann, stdevn)]
	"""
	means = [] # List to store evolving means
	cumsum = 0 # Evolving cumulative sum
	stdevs = [] # List to store evolving standard deviations
	cumsumsqrd = 0 # Evolving cumulative sum of squares
	n = 0 # Data count
	for d in data:
		n += 1
		cumsum += d
		cumsumsqrd += d**2
		means.append(cumsum/n)
		if n > 1:
			stdevs.append(np.sqrt(((n*cumsumsqrd)-cumsum**2)/(n*(n-1))))
		else:
			stdevs.append(np.nan)
	return zip(means,stdevs)


def linear(x, m, c):
	"""Linear function"""
	return m * x + c


def fit_linear(x_data, y_data):
	"""Return m and c"""
	fit = optimization.curve_fit(linear, x_data, y_data)
	return fit[0][0],fit[0][1]


