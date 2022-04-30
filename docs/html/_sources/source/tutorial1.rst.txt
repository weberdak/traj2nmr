.. _tutorial1:

Tutorial 1: Loading trajectories
================================

Create MDTraj trajectory object
-------------------------------

Traj2NMR uses MDTraj for reading and analysing protein structure files and MD trajectories. Supported formats are (kind of) listed in the `MDTraj documentation <https://mdtraj.org/1.9.4/load_functions.html#format-specific-loading-functions>`_. In this example, we will use the NMR structure of GB1 (2lgi.pdb) and the same structure simulated for 100 ns (2lgi.psf, 2lgi_100ns.dcd). These files are included in the `examples folder <https://github.com/weberdak/traj2nmr/tree/main/examples>`_ of the GitHub repository and will need to be copied into the current working directory. Now create an MDTraj trajectory object for each system:

.. code-block:: python

    import mdtraj as md

    gb1_traj_static = md.load('2lgi.pdb')
    gb1_traj_simulated = md.load('2lgi_100ns.dcd', top='2lgi.psf')

You may see a warning regarding cell vectors for the PB file - ignore this. These objects will now be used to initialise Traj2NMR sessions.


Initialise Traj2NMR session
---------------------------

Traj2NMR uses a Session object as a container for storing trajectories and calculated NMR observables. Numerous analysis and output methods are also built into this object class, making the computation of NMR observables and data output (i.e., CSV files and spectral files) relatively straightforward. Using Session objects also allows Traj2NMR to simultaneously analyse multiple systems at once, as demonstrated below. Traj2NMR Session objects must be initialised from an MDTraj trajectory object. Using those created above:

.. code-block:: python

    import traj2nmr

    gb1_session_static = traj2nmr.Session(gb1_traj_static)
    gb1_session_simulated = traj2nmr.Session(gb1_traj_simulated)

Now we can move on to the interesting stuff.