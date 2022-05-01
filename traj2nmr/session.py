from .shifts import chemical_shifts_traj
from .resonance import Resonance
from .ucsf import gen_ucsf


class Session:
	"""Primary class for executing Traj2NMR
	"""	

	def __init__(self, trajectory):
		"""Initialise Traj2NMR session

		:param trajectory: MDTraj trajectory
		:type trajectory: class:`mdtraj.Trajectory`
		"""
		self.trajectory = trajectory # MDTraj trajectory
		self.resonances = dict()


	def compute_shifts(self, backbone=True, sidechain=True, overwrite=True, 
		verbose=True, **kwargs):
		"""Compute chemical shifts per chain, atom and frame. Results stored
		as traj2nmr.Resonance classes in self.resonances dictionary keyed by 
		'chainID.resName.resID.name'.

		:param backbone: Save backbone shifts to instance, defaults to True
		:type backbone: bool, optional
		:param sidechain: Save sidechain shifts to instance, defaults to True
		:type sidechain: bool, optional
		:param overwrite: Overwrite existing shifts, defaults to True
		:type overwrite: bool, optional
		:param verbose: Print run status to terminal, defaults to True
		:type verbose: bool, optional
		:param method: Method to compute chemical shifts. Options 'shiftx2', 
			'spartaplus', 'ppm', defaults to 'shiftx2'
		:type method: str, optional
		:param stride: Compute shifts only for every nth frame, defaults to 1 
			(all frames in trajectory)
		:type stride: int, optional
		:param first: Frame to start, defaults to 0 (all frames)
		:type first: int, optional
		:param last: Last frame, defaults to last frame
		:type last: int, optional
		:param chainIDs: Limit computation to these chains, defaults to [0] 
			(first chain only)
		:type chainIDs: list of int, optional
		:param threads: Number of threads to run in parallel, defaults to 1.
			Note that threading does not work well at present
		:type threads: int, optional
		:param stdout: Print ShiftX2, SPARTA+, PPM messages to stdout, 
			defaults to False
		:type stdout: bool, optional
		:param rename_HN: Rename HN in SPARTA+ output to H, defaults to True
		:type rename_HN: bool, optional
		:param pH: pH used for shiftx2 method, defaults to 5.0
		:type pH: float, optional
		:param temperature: Temperature, in Kelvin, used by shiftx2 method, 
			defaults to 298.00
		:type temperature: float, optional
		"""		
		# Define Backbone atom names
		backbone_atoms = {'H', 'HN', 'N', 'C', 'CA', 'CB'}

		# Helpful feedback
		if verbose:
			print('Computing chemical shifts from trajectory...')
			if (not backbone) and (not sidechain):
				print('WARNING: Neither backbone or sidechain resonances are '
					  'set to be saved!')
			if not backbone:
				print('Backbone resonances will not be saved')
			if not sidechain:
				print('Sidechain resonances will not be saved')

		# Compute chemical shifts for entire trajectory or specified frames
		results = chemical_shifts_traj(self.trajectory, verbose=verbose, 
			**kwargs)

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
			print('\nChemical shifts were computed for {} resonances from {} '
				  'frames'.format(len(keys), num_frames))
			if saved > 0:
				print('{} resonances were saved'.format(saved))
			if overwritten > 0:
				print('{} existing resonances were overwritten'.format(
					overwritten))
			if backbone_not_saved > 0:
				print('{} backbone resonances were not saved'.format(
					backbone_not_saved))
			if sidechain_not_saved > 0:
				print('{} sidechain resonances were not saved'.format(
					sidechain_not_saved))
			if not_overwitten > 0:
				print('{} resonances existed and could not be '
				      'overwritten'.format(not_overwitten))


	def query_resonances(self, chainID=[], resName=[], resSeq=[], name=[], 
		verbose=True):
		"""Select resonances based on chainID, resName, resSeq and name values

		:param chainID: Select resonances belonging to these chain IDs, 
			defaults to [] (all chainIDs)
		:type chainID: list of int, optional
		:param resName: Select resonances having these residue names, 
			defaults to [] (all resNames)
		:type resName: list of str, optional
		:param resSeq: Select resonances having these residue IDs, 
			defaults to [] (all resSeqs)
		:type resSeq: list of int, optional
		:param name: Select resonances having these atom names, 
			defaults to [] (all atom names)
		:type name: list of str, optional
		:param verbose: Print self.resonances keys belonging to returned 
			resonances, defaults to True
		:type verbose: bool, optional
		:return: List of resonances matching query
		:rtype: list of class:`traj2nmr.Resonance`
		"""
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
				print('{}.{}.{}.{}'.format(
					r.chainID, r.resName, r.resSeq, r.name))

		return to_return


	def get_resonance_keys(self):
		"""Get an ordered list of self.resonance dictionary keys

		:return: List of dictionary keys ('chainID.resName.resID.name')
		:rtype: list of str
		"""
		tl = [(int(k.split('.')[0]), k.split('.')[1], int(k.split('.')[2]), 
			   k.split('.')[3]) for k in self.resonances.keys()]
		tl = sorted(tl, key=lambda x: (x[0], x[2], x[3]))
		return ['.'.join([str(k[0]), k[1], str(k[2]), k[3]]) for k in tl]


	def write_resonances_to_csv(self, filename):
		"""Write average all average chemical shifts to CSV file 
		(chainID,resName,resSeq,name,average_shift)

		:param filename: Output file name
		:type filename: str
		"""		
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
				f.write('{0},{1},{2},{3},{4:.3f}\n'.format(
					chainID,resName,resSeq,name,shift))
				n += 1


	def _gen_shift_data(self):
		"""Generate data tuples for write_ucsf function

		:return: list of tuples (resSeq, resName, name, shift)
		:rtype: list of tuples (int, str, str, float)
		"""		
		data = []
		for k in self.get_resonance_keys():
			#chainID = k.split('.')[0] Need gen_ucsf to support chainID
			resName = k.split('.')[1]
			resSeq = int(k.split('.')[2])
			name = k.split('.')[3]
			shift = round(self.resonances[k].average(), 3)
			data.append((resSeq, resName, name, shift))
		return data


	def write_ucsf(self, experiment_type, out_prefix, 
		sfreq=600.00, xlw=20.0, ylw=20.0):
		"""Generate spectra and peak list from current data in UCSF format

		:param experiment_type: Experiment type, choices: 'nhsqc'
		:type experiment_type: str
		:param out_prefix: Prefix of output .ucsf and .list files
		:type out_prefix: str
		:param sfreq: Spectrometer 1H frequency in MHz, defaults to 600.00
		:type sfreq: float, optional
		:param xlw: X-dimension peak linewidth in Hz, defaults to 20.0
		:type xlw: float, optional
		:param ylw: Y-dimension peak linewidth in Hz, defaults to 20.0
		:type ylw: float, optional
		:raises ValueError: If experiment_type is not supported
		"""
		# Gyromagnetic ratios (10^6 rad.s−1.T−1)
		gyros = {
			'1H': 267.52218744,
			'13C': 67.2828, 
			'15N': -27.116,
		}
		# Raise exception of experiment not listed
		valid_types = ['nhsqc']
		if experiment_type not in valid_types:
			raise ValueError('Experiment type \'{}\' not supported. Supported'
				' options include {}'.format(type, ', '.join(valid_types)))

		# Reformat data for gen_uscf function
		data = self._gen_shift_data()

		# Settings for simple 2D HSQC experiment
		if experiment_type == 'nhsqc':
			intra_corr = [('H','N'),('HD21','ND2'),('HD22','ND2'),
				('HE21','NE2'), ('HE22','NE2'),('HE1','NE1')]
			inter_corr = [0]
			nuc1_label = '1H'
			nuc2_label = '15N'
			nuc1_freq = sfreq*(gyros[nuc1_label]/gyros['1H'])
			nuc2_freq = sfreq*(gyros[nuc2_label]/gyros['1H'])
			nuc1_center = 8.30
			nuc2_center = 120.00
			nuc1_sw = 8.00
			nuc2_sw = 40.00
			nuc1_size = 1024
			nuc2_size = 1024

		# Output spectrum
		gen_ucsf(data, out_prefix, intra_corr, inter_corr, nuc1_label, nuc2_label, 
    		nuc1_freq, nuc2_freq, nuc1_center, nuc2_center, nuc1_sw, nuc2_sw, 
    		nuc1_size, nuc2_size, xlw, ylw)

