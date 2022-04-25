from numpy import save
from .shifts import chemical_shifts_traj
from .resonance import Resonance


class Analysis:
	"""A Traj2NMR instance intialized from an MDTraj trajectory. Encapsulates
	all functions and organises all data for spectral simulation.

	Attributes
	----------
	trajectory: MDTraj trajectory object
		I.e., by running mdtraj.load(<coordinates file>, top=<topology file>)
	resonances: dict
		Dictionary of Resonance objects keyed by [chainID.resName.resID.name]
	notebook: bool
		Set to True if using a Jupyter of iPython notebook. Affects the way 
		verbose is printed to cells. Default: False
	"""

	def __init__(self, trajectory):
		"""Initialize new instance from MDTraj trajectory.

		Parameters
		----------
		trajectory: MDTraj trajectory object
			I.e., by running mdtraj.load(<coordinates file>, top=<topology file>)
		"""
		self.trajectory = trajectory # MDTraj trajectory
		self.resonances = dict() # .resonances[0.ALA.1.H] (dictionary of resonance objects indexed by )


	def compute_shifts(self, backbone=True, sidechain=True, overwrite=True, 
		verbose=True, **kwargs):
		'''Compute chemical shifts by chain and for all frames. Creates a 
		Resonance object for every residue in self.trajectory resolved by 
		chain. All resonances computed are stored in self.resonances.

		Parameters
		----------
		backbone: bool
			Save all backbone chemical shifts to self.resonances. Default: True
		sidechain: bool
			Save all sidechain chemical shifts to self.resonances. Default: True
		overwrite: bool
			Overwrite existing resonances. Default: True

		Other Parameters
		----------------
		method: str
			Program to compute shifts. Choices: 'shiftx2' (default), 
			'spartaplus' and 'ppm'.
		stride: int
			Skip every nth frame. Default: 1 (no skipping)
		first: int
			Index of first frame. Default: 0 (first frame)
		last: int
			Index of last frame. Default: traj.n_frames-1 (last frame)
		threads: int
			Number of threads to run in parallel. Default: 1
		notebook: bool
			Set if using a Jupyter or iPython notebook. Clear cell output when 
			progress is updated. Default: False
		verbose: bool
			Print messages to terminal. Default: True
		'''
		# Define Backbone atom names
		backbone_atoms = {'H', 'HN', 'N', 'C', 'CA', 'CB'}

		# Helpful feedback
		if verbose:
			print('Computing chemical shifts from trajectory...')
			if (not backbone) and (not sidechain):
				print('WARNING: Neither backbone or sidechain resonances are set to be saved!')
			if not backbone:
				print('Backbone resonances will not be saved')
			if not sidechain:
				print('Sidechain resonances will not be saved')

		# Compute chemical shifts for entire trajectory or specified frames
		results = chemical_shifts_traj(self.trajectory, verbose=verbose, **kwargs)

		# Create and save resonances
		saved = 0
		overwritten = 0
		sidechain_not_saved = 0
		backbone_not_saved = 0
		not_overwitten = 0

		# Get key and determine number of frames computed
		keys = list(results.keys())
		num_frames = len(results[keys[0]].keys())

		# Save resonances to self.resonances (if not filtered out)
		for key in keys:
			name = key.split('.')[3]

			# Is this a backbone or sidechain atom?
			if name in backbone_atoms:
				isbackbone = True
				issidechain = False
			else:
				isbackbone = False
				issidechain = True

			# Check if resonance already exists in resonances
			if key in self.resonances:
				resonance_exists = True
			else:
				resonance_exists = False

			# Save resonance?
			save_resonance = True
			if (not backbone) and (isbackbone):
				save_resonance = False
				backbone_not_saved += 1

			if (not sidechain) and (issidechain):
				save_resonance = False
				sidechain_not_saved += 1

			if (not overwrite) and (resonance_exists):
				save_resonance = False
				not_overwitten += 1

			# If all good, create and save resonance to resonances
			if save_resonance:
				
				# Get MTRaj atom index of resonance
				# This needs to be done. save index to Resonance Object
				# Needed for easily linking to dipolar couplings.

				self.resonances[key] = Resonance(key, results[key])
				saved += 1
				if resonance_exists:
					overwritten += 1

		# Final results
		if verbose:
			print('\nChemical shifts were computed for {} resonances from {} frames'.format(len(keys), num_frames))
			if saved > 0:
				print('{} resonances were saved'.format(saved))
			if overwritten > 0:
				print('{} existing resonances were overwritten'.format(overwritten))
			if backbone_not_saved > 0:
				print('{} backbone resonances were not saved'.format(backbone_not_saved))
			if sidechain_not_saved > 0:
				print('{} sidechain resonances were not saved'.format(sidechain_not_saved))
			if not_overwitten > 0:
				print('{} resonances existed and could not be overwritten'.format(not_overwitten))


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


	def get_resonance_keys(self):
		'''Return a an ordered list of resonance keys.

		Returns
		-------
		keys: list
			Resonance keys ordered by chainID
		'''
		temp_list = [(int(k.split('.')[0]), k.split('.')[1], int(k.split('.')[2]), k.split('.')[3]) for k in self.resonances.keys()]
		temp_list = sorted(temp_list, key=lambda x: (x[0], x[2], x[3]))
		return ['.'.join([str(k[0]), k[1], str(k[2]), k[3]]) for k in temp_list]


	def write_resonances_to_csv(self, filename, verbose=True):
		'''Write all average chemical shifts to CSV file
		
		Parameters
		----------
		filename: str
			File name/path to output resonances
		'''
		with open(filename, 'w') as f:
			n = 0

			# Write header
			f.write('chainID,resName,resSeq,name,shift\n')
			for k in self.get_resonance_keys():
				chainID = k.split('.')[0]
				resName = k.split('.')[1]
				resSeq = k.split('.')[2]
				name = k.split('.')[3]
				shift = self.resonances[k].average()
				f.write('{0},{1},{2},{3},{4:.3f}\n'.format(chainID,resName,resSeq,name,shift))
				n += 1

		if verbose:
			print('Average shifts of {} resonances written to \'{}\''.format(n, filename))


	def get_dipolar_couplings(self, index):
		'''Get all of the couplings this resonance is involved in (may have to alias the indices if homonuclear)
		'''
		return
