import matplotlib.pyplot as plt
import numpy as np
from . import utils

class Resonance():
	"""Class to store data and implement calculations.

	Attributes
	----------
	chainID: int
		Chain ID of residue assigned by MDTraj resonance belongs to
	resName: str
		Three-letter residue code resonance belongs to
	resSeq: int
		Residue number resonance belongs to
	name: str
		Atom name

	Methods
	-------
	plot(xlim=[], ylim=[], figsize=(8.0,6.0), textsize=12):
		TO INCLUDE DETAILS
	"""

	def __init__(self, key, shifts, method):
		"""Create new resonance object from chemical shifts output

		Parameters
		----------
		key: str
			Dictionary key of chemical shift results. Format: [chainID.resName.resID.name]
		data: dict()
			shifts[frame]: float
			Chemical shift indexed by frame number (int) for residue.
		"""

		# Get resonance information from keys passed from shifts.chemical_shifts_traj()
		info = key.split('.')
		self.chainID = int(info[0])
		self.resName = info[1]
		self.resSeq = int(info[2])
		self.name = info[3]
		self.shifts = shifts
		self.method = method
		

	def average(self):
		# Order frames and get shifts
		sorted_frames = sorted(self.shifts.keys())
		shifts = [self.shifts[frame] for frame in sorted_frames]
		return np.mean(shifts)


	def converge():
		pass


	def plot(self, xlim=[], ylim=[], figsize=(8.0,4.0), textsize=16):
		"""Plot and show chemical shifts of residue as a function of frame number

		Parameters
		----------
		"""
		# Order frames and get shifts
		sorted_frames = sorted(self.shifts.keys())
		shifts = [self.shifts[frame] for frame in sorted_frames]
		stats = utils.evolving_stats(shifts)
		means = [mean for mean, stdev in stats]
		#means_plus_stdev = [mean + stdev for mean, stdev in stats]
		#means_minus_stdev = [mean - stdev for mean, stdev in stats]

		# Plot line plot
		fig, ax = plt.subplots(figsize=figsize)
		plt.xticks(fontsize=textsize)
		plt.yticks(fontsize=textsize)
		ax.set_xlabel('Frame', size=textsize)
		ax.set_ylabel('Chemical shift (ppm)', size=textsize)
		if xlim:
			ax.set_xlim(*xlim)
		if ylim:
			ax.set_ylim(*ylim)
		ax.scatter(sorted_frames, shifts, c='black')
		ax.plot(sorted_frames,means, c='black')
		#ax.plot(sorted_frames,means_plus_stdev, c='red')
		#ax.plot(sorted_frames,means_minus_stdev, c='red')
		plt.show()