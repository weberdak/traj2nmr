# Traj2NMR

User-friendly NMR spectral predictions from molecular dynamics simulation trajectories


## Overview

Traj2NMR is a Python module developed to streamline the computation of NMR observables from molecular dynamics (MD) trajectories. This module is essentially a user-friendly wrapper for popular NMR and molecular dynamics analysis packages, including ShiftX2, PPM, SPARTA+, Nmrglue and MDTraj. Traj2NMR is designed to be usable by practitioners in either MD simulation or NMR spectroscopy with some prior exposure to Python.


## Features

Feature that are currently active include:

* Prediction of ensemble-averaged chemical shifts from PDB files and molecular dynamics trajectories
* Easy inspection of chemical shifts over the ensemble
* Direct output of 2D USCF spectral and peak list files (N-HSQC, NCA, NCO currently) for direct comparison to experimental data

Feature that will be introduced in the near future include:

* Convergence metrics for chemical shifts
* Computation of ensemble-averaged dipolar couplings
* Generation of spectra based on through-space contacts


## Instructions

Detailed installation and usage instructions are maintained on the [documention page](https://weberdak.github.io/traj2nmr/).
