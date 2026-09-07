# Scientific Python Projects

Assessed computational-physics work from my degree at the University of Birmingham, covering **quantum mechanics, Fourier analysis, signal processing and feedback control**.

## Quantum systems — 95%

[Source code](Project_1_Quantum_Systems.py)

I modelled the bound states of an electron in a finite square well, reformulating the Schrödinger equation into dimensionless even- and odd-parity equations. Numerical root finding gives the allowed energy eigenvalues and their dependence on the well parameters.

The energy diagram below shows the six bound states for a 1 nm well with a 10 eV barrier.

## Spectral analysis — 80%

[Source code](Project_2_Spectral_Analysis.py)

I used swept-sine signals and Fourier analysis to identify the behaviour of unknown electronic filters, locate unwanted spectral components and reconstruct filtered signals through a custom transfer function.

![Finite-well energy levels and a signal-processing illustration with broadband noise and multiple interfering frequencies](assets/scientific-python.png)

*Computational illustrations: finite-well energy levels, and a three-component signal with broadband noise and three interfering tones. The filtering panel combines notch and low-pass filtering; the noise trace is generated for this figure.*

## Self-landing rockets — 90%, cohort highest

[Source code](Project_3_Self_Landing_Rockets.py)

I investigated a two-dimensional rocket simulator, using numerical experiments to identify its dynamics before constructing positioning and landing controllers. The work covered thruster offsets, mass and thrust estimates, acceleration-to-thrust mapping, proportional feedback and damped PD-style control using position and velocity.

## Programming worksheets — 98% average, cohort highest

[Source code](Scientific_Worksheets.py)

Six worksheets covering scientific Python and numerical methods: complex arithmetic, sequences and series, conditional probability, nuclear binding energies, bisection, lattice sums, stellar data, electrostatic fields and Monte Carlo simulation.

The consolidated source separates calculations from plots and uses named functions for reusable methods. Dice sampling and random walks use vectorised array operations; physical quantities and input units are documented alongside the calculations.

**Methods:** Python, NumPy, SciPy, Matplotlib, numerical root finding, Fourier analysis, transfer functions, feedback control and scientific visualisation.

The marks refer to the assessed coursework. This repository collects the work as a portfolio, with later improvements to clarity and numerical implementation.
