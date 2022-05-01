.. _tutorial2:

Tutorial 2: Chemical shifts
===========================


Default settings
----------------

Chemical shifts can computed once a Session has been initialised. For now we will just work with the GB1 trajectory loaded in Tutorial 1. By default, ShiftX2 will be used to predict chemical shifts for all frames in the trajectory, i.e.:

.. code-block:: python

    gb1_traj_simulated.compute_shifts()

Traj2NMR will also handle multiple chains if present by using the chainIDs option. For example, if two chains are present, you specify chainIDs=[0,1] in the argument and a set of chemical shifts will be recorded for each chain, which can be averaged later if desired (i.e., for a symmetric homodimer). If using ShiftX2, you also have the option of changing temperature and pH (temperature=298.00, pH=5.0 by default). 


Hybridising methods
-------------------

ShiftX2 is advantageous in that it computes both backbone and sidechains shifts, however, it is by far the slowest method. On my system, ShiftX2 computes shifts at rate of 34 frames per minute while SPARTA+ (method='spartaplus') runs at ~100 frames per minute (backbone only) and PPM (method='ppm') is the fastest at ~1600 frames per minute (backbone and methyl sidechains only). An important feature of Traj2NMR is that it can hybridise methods to balance performance with statistical accuracy. For example, let's say we want to compute backbone atoms for all frames quickly with PPM, and fill the remaining sidechain atoms with ShiftX2, but for only 1/10th of the frames. This can be done by:

.. code-block:: python

    gb1_traj_simulated.compute_shifts(method='ppm')
    gb1_traj_simulated.compute_shifts(method='shiftx2', stride=10, backbone=False, overwrite=False)

In the second calculation, stride=10 prompts the Traj2NMR to only shifts every 10th frame, backbone=False prevents computed backbone shifts from being saved to the session (and overwriting those computed by PPM) and overwrite=False is needed if PPM-calculated methyl sidechain shifts need to be preserved. Note that in this example, specifying backbone=False and method='shiftx2' is somewhat redundant, but included here to help explain what is happening.


Accessing chemical shift data
-----------------------------

Chemical shifts are saved into the Session as Resonance objects (one per atom), which contain the chemical shifts for every frame computed by the compute_shifts() function. More to come...