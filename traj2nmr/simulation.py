from .shifts import chemical_shifts_traj
from .resonance import Resonance


class Simulation():
	"""Highest-level class mapping all data in a single project

	Attributes
	----------
	trajectory: obj
		MDTraj trajectory
	resonances: dict
		Dictionary of resonance objects keyed by [chainID.resName.resID.name]
	notebook: bool
		Set to True if using a Jupyter of iPython notebook. Affects the way 
		verbose is printed to cells. Default: False
	
	Methods
	-------
	compute_shifts:
	"""


	def __init__(self, trajectory):
		"""
		"""
		self.notebook = False
		self.trajectory = trajectory # MDTraj trajectory
		self.resonances = dict() # .resonances[0.ALA.1.H] (dictionary of resonance objects indexed by )


	def compute_shifts(self, method='shiftx2', **kwargs):
		'''Compute chemical shifts for all resonances

		Parameters
		----------
		kwargs:
			Passed to shifts.chemical_shifts_traj
		'''
		results = chemical_shifts_traj(self.trajectory, method, notebook=self.notebook, **kwargs)
		imported = 0
		for key in results.keys():
			self.resonances[key] = Resonance(key, results[key], method)
			imported += 1
		print('\nSuccessfully computed chemical shifts for {} atoms'.format(imported))


	def query_resonances(self, chainID=[], resName=[], resSeq=[], name=[], verbose=True):
		to_return = []
		for key in self.resonances.keys():
			keep = True
			if chainID:
				if self.resonances[key].chainID not in chainID:
					keep = False
			if resName:
				if self.resonances[key].resName not in resName:
					keep = False
			if resSeq:
				if self.resonances[key].resSeq not in resSeq:
					keep = False
			if name:
				if self.resonances[key].name not in name:
					keep = False
			if keep == True:
				to_return.append(self.resonances[key])

		if verbose:
			print('Found {} resonances matching query:'.format(len(to_return)))
			for r in to_return:
				print('{}.{}.{}.{}'.format(r.chainID, r.resName, r.resSeq, r.name)) 

		return to_return


	def update(self):
		'''Update shifts and dipolar couplings if trajectory changed - only get frames added
		'''
		pass


	def getDipolarCouplings(self, index):
		'''Get all of the couplings this resonance is involved in (may have to alias the indices if homonuclear)
		'''

	def writeUCSF(self, name):
		pass


	def writeShifts(self):
		pass


	def writeDipolarCouplings(self):
		pass

