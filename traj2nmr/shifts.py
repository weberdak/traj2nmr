from .utils import convert_resname
from collections import OrderedDict
import concurrent.futures
from IPython.display import display, clear_output
from mdtraj.utils import enter_temp_directory
from mdtraj.nmr.shift_wrappers import find_executable, _get_lines_to_skip
import pandas as pd
import subprocess
import time


def chemical_shifts_spartaplus(trj, frame, stdout=False, rename_HN=True):
	"""Wrapper to get chemical shifts for a single frame of the trajectory using SPARTA+. 

	Parameters
	----------
	trj: obj
		MDTraj trajectory
	frame: int
		Index of frame to compute shifts for. Indicies start at zero
	stdout: bool
		Print SPARTA+ verbose to stdout (recommended for troubleshooting)
	rename_HN: bool
		Rename HN in SPARTA+ output to H

	Returns
	-------
	result: dict
		Chemicals shifts indexed by [resName.resID.name]

	Notes
	-----
	SPARTA+ must be installed and in your executable path. This function
	has been modified by the shift_wrappers.py module of MDTraj and adjusted
	to return shifts for a single frame in a dictionary indexed consistantly
	with the rest of the program.
	"""
	binary = find_executable(['sparta+', 'SPARTA+', 'SPARTA+.linux'])

	if binary is None:
		raise OSError('Could not find SPARTA+ in PATH!')

	names = ['resSeq', 'resName', 'name', 'SS_SHIFT', 'SHIFT', 'RC_SHIFT', 'HM_SHIFT', 'EF_SHIFT', 'SIGMA']

	# Temporary files created and deleted once complete
	with enter_temp_directory():
		trj[frame].save('./trj{}.pdb'.format(frame))

		if stdout:
			subprocess.run([binary, '-in trj{}.pdb'.format(frame)] + ['-out', 'trj{}_pred.tab'.format(frame)])
		else: 
			subprocess.run([binary, '-in trj{}.pdb'.format(frame)] + ['-out', 'trj{}_pred.tab'.format(frame)], 
	              	  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

		lines_to_skip = _get_lines_to_skip('trj{}_pred.tab'.format(frame))
		d = pd.read_table('./trj{}_pred.tab'.format(frame), names=names, header=None, sep='\s+', skiprows=lines_to_skip)

	# Change HN to H
	if rename_HN:
		d.loc[(d.name == 'HN'),'name'] ='H'

	# Create a dictionary from dataframe
	result = { '{}.{}.{}'.format(convert_resname(rn), ri, n): s for rn, ri, n, s in zip(d['resName'], d['resSeq'], d['name'], d['SHIFT']) if rn != '?' }

	return result


def chemical_shifts_ppm(trj, frame, stdout=False):
	"""Wrapper to get chemical shifts for a single frame of the trajectory using PPM. 

	Parameters
	----------
	trj: obj
		MDTraj trajectory
	frame: int
		Index of frame to compute shifts for. Indicies start at zero
	stdout: bool
		Print PPM verbose to stdout (recommended for troubleshooting)

	Returns
	-------
	result: dict
		Chemicals shifts indexed by [resName.resID.name]

	Notes
	-----
	SPARTA+ must be installed and in your executable path. This function
	has been modified by the shift_wrappers.py module of MDTraj and adjusted
	to return shifts for a single frame in a dictionary indexed consistantly
	with the rest of the program.
	"""
	binary = find_executable(['ppm_linux'])

	first_resSeq = trj.top.residue(0).resSeq

	if binary is None:
		raise OSError('Could not find PPM in PATH!')

	with enter_temp_directory():

		trj[frame].save('./trj{}.pdb'.format(frame))

		if stdout:
			subprocess.run([binary, '-pdb', 'trj{}.pdb'.format(frame), '-para', 'old'])
		else:
			subprocess.run([binary, '-pdb', 'trj{}.pdb'.format(frame), '-para', 'old'], 
				stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

		# Read PPM outputs of backbone (MDTraj copy/adaption)
		d = pd.read_table('./bb_details.dat', index_col=False, header=None, sep='\s+')
		d = d.rename(columns={0: 'resSeq', 1: 'resName', 2: 'name', 3: '?', 4: 'SHIFT'})
		d['resSeq'] += first_resSeq - 1  # Fix bug in PPM that reindexes to 1
		#d = d.set_index(['resSeq', 'name'])
		result_bb = { '{}.{}.{}'.format(rn, ri, n): s for rn, ri, n, s in zip(d['resName'], d['resSeq'], d['name'], d['SHIFT']) if rn != '?' }

		# Read PPM outputs of methyl side chains
		d = pd.read_table('./proton_details.dat', index_col=False, header=None, sep='\s+')
		d = d.rename(columns={0: 'resSeq', 1: 'resName', 2: 'name', 3: '?', 4: 'SHIFT'})
		d['resSeq'] += first_resSeq - 1  # Fix bug in PPM that reindexes to 1
		#d = d.set_index(['resSeq', 'name'])
		result_sc = { '{}.{}.{}'.format(rn, ri, n): s for rn, ri, n, s in zip(d['resName'], d['resSeq'], d['name'], d['SHIFT']) if rn != '?' }

		# Merge to datasets and return results
		return {**result_bb, **result_sc}


def chemical_shifts_shiftx2(trj, frame, pH=5.0, temperature=298.00, stdout=False):
	"""
	"""


	binary = find_executable(['shiftx2.py'])

	if binary is None:
		raise OSError('Could not find shiftx2.py in PATH!')

	with enter_temp_directory():
		trj[frame].save('./trj{}.pdb'.format(frame))

		# Run with --noshifty (-n) since having difficulties with blast
		if stdout:
			subprocess.run(['python2.7', binary, '-i', 'trj{}.pdb'.format(frame),
									'-p', '{:.1f}'.format(pH),
									'-t', '{:.2f}'.format(temperature),
						   ])
		else:
			subprocess.run(['python2.7', binary, '-i', 'trj{}.pdb'.format(frame),
									'-p', '{:.1f}'.format(pH),
									'-t', '{:.2f}'.format(temperature),
						   ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

		d = pd.read_csv('./trj{}.pdb.cs'.format(frame))
		d.rename(columns={"NUM": "resSeq", "RES": "resName", "ATOMNAME": "name"}, inplace=True)
		
	return { '{}.{}.{}'.format(convert_resname(rn), ri, n): s for rn, ri, n, s in zip(d['resName'], d['resSeq'], d['name'], d['SHIFT']) }


def chemical_shifts_traj(traj, method='shiftx2', first=0, last=[], stride=1,
						  threads=1, notebook=False, verbose=True, **kwargs):
	'''Higher level function of chemical_shifts_<method> over multiple 
	frames. Multiprocessing optionally enabled but not working great.

	Parameters
	----------
	trj: obj
		MDTraj trajectory
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
		Print progress to terminal. Default: True
	
	Other Parameters
	----------------
	rename_HN: bool
		Used by chemical_shifts_spartaplus()
	pH: float
		Used by chemical_shifts_shiftx2()
	temperature: float
		Used by chemical_shifts_shiftx2()

	Returns
	-------
	shifts: dict()
		[chainID.resName.resID.name][frame]: float
		Chemical shifts indexed by chainID.resName.resid.atomname then frame
	'''
	# Check if method is valid
	valid_methods = ['spartaplus', 'ppm', 'shiftx2']
	if method not in valid_methods:
		raise ValueError('\'{}\' is not a valid method. Valid options include {}'.format(method, ', '.join(valid_methods))) 

	# Assign frames and correct inputs if needed
	if not last:
		last = traj.n_frames-1
	if last > traj.n_frames-1:
		last = traj.n_frames-1

	# Get chainIDs
	table, bonds = traj.topology.to_dataframe()
	chains = set(table['chainID'])
	chains = sorted(list(chains))

	# Set frames
	frames = [x for x in range(first, last+1, stride)]

	# Trim trajectory to protein atoms. Remove protons if shiftx2
	if method == 'shiftx2':
		selection = traj.top.select("protein and not (symbol == 'H')")
		traj_stripped = traj.atom_slice(selection)
	else:
		selection = traj.top.select("protein")
		traj_stripped = traj.atom_slice(selection)

	# Iterate through frame and get shifts
	shifts = dict()

	# SERIAL VERSION
	time_start = time.time()
	if threads == 1:
		for chain in chains:
			for frame in frames:
				# Get chemical shifts using desired program
				if method == 'spartaplus':
					results = chemical_shifts_spartaplus(traj_stripped, frame, **kwargs)
				if method == 'ppm':
					results = chemical_shifts_ppm(traj_stripped, frame, **kwargs)
				if method == 'shiftx2':
					results = chemical_shifts_shiftx2(traj_stripped, frame, **kwargs)

				# Write results to new dictionary
				for key in results.keys():
					new_key = str(chain)+'.'+key
					if new_key not in shifts:
						shifts[new_key] = dict()
					shifts[new_key][frame] = results[key]

				# Get current progress from number frames from last atom saved
				progress = round((100*len(shifts[new_key].keys())/len(frames)), 2)
				rate = round((len(shifts[new_key].keys()) / ((time.time() - time_start)/60)), 2)
				_verbose(method, chain, first, last, stride, rate, progress, notebook)

	# PARALLEL VERSION
	if threads > 1:
		# Do "threads" number jobs in parallel. This method is not very efficient if jobs takes different lengths of
		# time (i.e., bottleneck in collection stage). But the continous progress updates are useful for long jobs.
		f_chunks = _chunks(frames, threads)

		for chain in chains:
		# Process one chunk at a time
			for chunk in f_chunks:
				with concurrent.futures.ProcessPoolExecutor(max_workers=threads) as executor:
					# Submit async tasks to processors
					futures = dict()
					for frame in chunk:
						if method == 'spartaplus':
							futures[frame] = executor.submit(chemical_shifts_spartaplus, traj_stripped, frame, **kwargs)
						if method == 'ppm':
							futures[frame] = executor.submit(chemical_shifts_ppm, traj_stripped, frame, **kwargs)
						if method == 'shiftx2':
							futures[frame] = executor.submit(chemical_shifts_shiftx2, traj_stripped, frame, **kwargs)

				# Collect results and 
				for frame in chunk:
					results = futures[frame].result()
					for key in results.keys():
						new_key = str(chain)+'.'+key
						if new_key not in shifts:
							shifts[new_key] = dict()
						shifts[new_key][frame] = results[key]

				# Print Progress
				progress = round((100*len(shifts[new_key].keys())/len(frames)), 2)
				rate = round((len(shifts[new_key].keys()) / ((time.time() - time_start)/60)), 2)
				_verbose(method, chain, first, last, stride, rate, progress, notebook)

	return shifts


def _verbose(method, chain, first, last, stride, rate, progress, notebook):
	"""Simple function to print current progress to stdout"""
	prog = OrderedDict()
	prog['Method'] = method
	prog['Chain'] = str(chain)
	prog['First'] = str(first)
	prog['Last'] = str(last)
	prog['Stride'] = str(stride)
	prog['Rate'] = str(rate)+'f/min'
	prog['Progress'] = str(progress)+'%'
	line = ', '.join([key+': '+prog[key] for key in prog.keys()])
	if notebook:
		clear_output(wait=True)
		display(line)
	else:
		print(line, end='\r')


def _chunks(l, n):
    """Yield successive n-sized chunks from l. From stackoverflow 312443"""
    for i in range(0, len(l), n):
        yield l[i:i + n]


