import nmrglue as ng
import numpy as np


def residue_letter(resname):
    '''Convert 3-letter amino acid code to 1-letter code.
    '''
    conversion = {
        "ALA": "A",
        "ARG": "R",
        "ASN": "N",
        "ASP": "D",
        "CYS": "C",
        "GLN": "Q",
        "GLU": "E",
        "GLY": "G",
        "HIS": "H",
        "HSE": "H",
        "HID": "H",
        "HSD": "H",
        "HSP": "H",
        "ILE": "I",
        "LEU": "L",
        "LYS": "K",
        "MET": "M",
        "PHE": "F",
        "PRO": "P",
        "SER": "S",
        "THR": "T",
        "TRP": "W",
        "TYR": "Y",
        "VAL": "V",
        "ASX": "B",
        "GLX": "Z"
    }
    try:
        return conversion[resname]
    except KeyError:
        print('WARNING! Unknown residue name \'{}\'. Single letter code \'U\' will be used.'.format(resname))
        return "U"


def gen_ucsf(data, out_prefix, intra_corr, inter_corr, nuc1_label, nuc2_label, 
    nuc1_freq, nuc2_freq, nuc1_center, nuc2_center, nuc1_sw, nuc2_sw, 
    nuc1_size, nuc2_size, nuc1_lw, nuc2_lw):
    '''Master function for generating Sparky UCSF spectra

    Parameters
    ----------
    data: list of tuples
        [(resSeq, resName, name, shift) for every resonance]
    out_prefix: str
        Output prefix of .ucsf and .list files
    intra_corr: list of tuples
        Intra-residue corrections. I.e., [('H', 'N'), ('HD21','ND2'), ...]
    inter_corr: list of int
        Indices for sequential correlations. I.e., [-1, 0, 1] for i-1, 
        intra-residue and i+1 corrleations
    nuc1_label: str
        Label for nucleus 1 (direct dimension). I.e., '1H'
    nuc2_label: str
        Label for nucleus 2 (indirect dimension). I.e., '15N'
    nuc1_freq: float
        Frequency of nucleus 1 in MHz. I.e., 600.00
    nuc2_freq: float
        Frequency of nucleus 2 in MHz. I.e., 60.7639142
    nuc1_center: float
        Center position of nucleus 1 in PPM. I.e., 8.30
    nuc2_center: float
        Center position of nucleus 2 in PPM. I.e., 120.00
    nuc1_sw: float
        Spectral width of nucleus 1 in PPM. I.e., 8.00
    nuc2_sw: float
        Spectral width of nucleus 1 in PPM. I.e., 40.00
    nuc1_size: int
        Number of points in nucleus 1 dimension. I.e., 1024
    nuc2_size: int
        Number of points in nucleus 2 dimension. I.e., 1024
    nuc1_lw: float
        Peak linewidths in dimension of nucleus 1 in Hz. I.e., 20.0
    nuc2_lw: float
        Peak linewidths in dimension of nucleus 2 in Hz. I.e., 20.0
    '''
    # Arrange data into dictionaries.
    data_shifts = {}
    data_rnames = {}
    data_atypes = {}
    for r_id, r_name, a_name, shift in data:
        try:
            data_shifts[r_id][a_name] = shift
        except KeyError:
            data_shifts[r_id] = {}
            data_shifts[r_id][a_name] = shift
        try:
            data_atypes[r_id][a_name] = a_name[0][:1]
        except KeyError:
            data_atypes[r_id] = {}
            data_atypes[r_id][a_name] = a_name[0][:1]
        data_rnames[r_id] = r_name           
    print('Read chemical shifts for {} residues.'.format(len(data_shifts.keys())))

    # Interate through each residue and find correlations. Output to Sparky peak list file.
    fo = open(out_prefix+'.list', 'w')
    fo.write('      Assignment         w1         w2  \n\n')
    num_intra = 0
    for r_id in data_shifts.keys():
        for s in inter_corr:
            for c in intra_corr:
                try:
                    shift1 = str(data_shifts[r_id][c[0]])
                    shift1 = shift1.rjust(11,' ')
                    shift2 = str(data_shifts[r_id+s][c[1]])
                    shift2 = shift2.rjust(11,' ')
                    if s == 0:
                        assignment = residue_letter(data_rnames[r_id])+str(r_id)+c[1]+'-'+c[0]
                    else:
                        assignment = residue_letter(data_rnames[r_id+s])+str(r_id+s)+c[1]+'-'+data_rnames[r_id]+str(r_id)+c[0]
                    assignment = assignment.rjust(17)
                    fo.write('{}{}{}\n'.format(assignment,shift2,shift1))
                    num_intra += 1
                except KeyError:
                    pass
    fo.close()
    print('List of {} peaks output to {}.list.'.format(num_intra,out_prefix))
    # Iterate through inter-residue connections
    # Mirror for homonuclear spectra

    # Simulate Sparky spectrum file from peak list
    # Make NMRGlue universal dictionary
    nuc1_center_hz = nuc1_freq*nuc1_center
    nuc2_center_hz = nuc2_freq*nuc2_center
    nuc1_sw_hz = nuc1_freq*nuc1_sw
    nuc2_sw_hz = nuc2_freq*nuc2_sw
    
    udic = {
        'ndim': 2,
        0: {'car': nuc2_center_hz,
            'complex': False,
            'encoding': 'states',
            'freq': True,
            'label': nuc2_label,
            'obs': nuc2_freq,
            'size': nuc2_size,
            'sw': nuc2_sw_hz,
            'time': False},
        1: {'car': nuc1_center_hz,
            'complex': False,
            'encoding': 'direct',
            'freq': True,
            'label': nuc1_label,
            'obs': nuc1_freq,
            'size': nuc1_size,
            'sw': nuc1_sw_hz,
            'time': False}
    }
    dic = ng.sparky.create_dic(udic)
    data = np.empty((nuc1_size, nuc2_size), dtype='float32')

    # read in the peak list
    peak_list = np.recfromtxt(out_prefix+'.list', names=True, dtype=None, encoding=None)
    npeaks = len(peak_list)

    # convert the peak list from PPM to points
    uc_nuc2 = ng.sparky.make_uc(dic, None, 0)
    uc_nuc1 = ng.sparky.make_uc(dic, None, 1)

    lw_nuc1 = (nuc1_lw/nuc1_sw_hz)*nuc1_size    # Nuc1 dimension linewidth in points
    lw_nuc2 = (nuc2_lw/nuc2_sw_hz)*nuc2_size    # Nuc2 dimension linewidth in points

    params = []
    for name, ppm_nuc2, ppm_nuc1 in peak_list:
        pts_nuc1 = uc_nuc1.f(ppm_nuc1, 'ppm')
        pts_nuc2 = uc_nuc2.f(ppm_nuc2, 'ppm')
        params.append([(pts_nuc2, lw_nuc2), (pts_nuc1, lw_nuc1)])

    # simulate the spectrum
    shape = (nuc2_size, nuc1_size)      # size should match the dictionary size
    lineshapes = ('g', 'g')  # gaussian in both dimensions
    amps = [100.0] * npeaks
    data = ng.linesh.sim_NDregion(shape, lineshapes, params, amps)

    # save the spectrum
    ng.sparky.write(out_prefix+'.ucsf', dic, data.astype('float32'), overwrite=True)

