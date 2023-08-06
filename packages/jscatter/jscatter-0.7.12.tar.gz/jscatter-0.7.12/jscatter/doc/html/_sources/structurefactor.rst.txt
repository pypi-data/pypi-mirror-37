structurefactor (sf)
====================

.. automodule:: jscatter.structurefactor
    :noindex:
   
Structure Factors
-----------------
.. autosummary::
   RMSA
   PercusYevick
   PercusYevick1D
   PercusYevick2D
   stickyHardSphere
   adhesiveHardSphere
   criticalSystem
   latticeStructureFactor
   orientedLatticeStructureFactor
   radialorientedLSF

Hydrodynamics
-------------
.. autosummary::
   hydrodynamicFunct
   
Pair Correlation
----------------
.. autosummary::
   sq2gr

Lattice
-------
**Lattices with specific structure** :

3D

.. autosummary::
    bravaisLattice
    scLattice
    bccLattice
    fccLattice

    hcpLattice
    diamondLattice
    rhombicLattice
    pseudoRandomLattice


2D

.. autosummary::
    sqLattice
    hexLattice

1D

.. autosummary::
    lamLattice

**lattice methods** :

.. autosummary::
    lattice.X
    lattice.Y
    lattice.Z
    lattice.XYZ
    lattice.b
    lattice.array
    lattice.points
    lattice.set_b
    lattice.type
    lattice.move
    lattice.centerOfMass
    lattice.numberOfAtoms
    lattice.show
    lattice.filter
    lattice.planeSide
    lattice.inSphere
    lattice.inParallelepiped
    rhombicLattice.unitCellAtomPositions
    rhombicLattice.getReciprocalLattice
    rhombicLattice.getRadialReciprocalLattice
    rhombicLattice.rotate2hkl

.. include:: ../../lattice.py
    :start-after: ---
    :end-before:  END

--------

.. automodule:: jscatter.structurefactor
    :members:
    :undoc-members:
    :show-inheritance:
   
.. autoclass:: lattice
    :members:

.. autoclass:: rhombicLattice
    :members:

.. autoclass:: bravaisLattice
.. autoclass:: scLattice
.. autoclass:: bccLattice
.. autoclass:: fccLattice
.. autoclass:: hexLattice
.. autoclass:: hcpLattice
.. autoclass:: diamondLattice
.. autoclass:: pseudoRandomLattice
.. autoclass:: sqLattice
.. autoclass:: lamLattice
