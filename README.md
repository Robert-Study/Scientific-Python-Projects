# Scientific Python Projects

A collection of assessed computational-physics projects developed in Python, covering **quantum mechanics, Fourier analysis, signal processing and feedback control**.

The projects demonstrate numerical modelling, scientific programming and quantitative problem-solving across several different physical systems.

---

## Projects

### ⚛️ [Quantum Systems](Project_1_Quantum_Systems.py) — **95%**

Numerical solution of the bound states of an electron in a finite square potential well.

The project reformulates the Schrödinger problem into transcendental equations for even and odd eigenstates, visualises the solution structure and applies numerical bisection to recover the allowed energy eigenvalues.

**Methods:**
- Finite square-well modelling
- Dimensionless reformulation
- Numerical root finding
- Bisection algorithms
- Energy-eigenvalue calculation
- Scientific visualisation

---

### 🚀 [Self-Landing Rockets](Project_3_Self_Landing_Rockets.py) — **90%** *(cohort highest)*

Simulation and control project based around a two-dimensional rocket dynamics model.

The workflow characterises the unknown simulator from numerical experiments before constructing control strategies for target positioning and repeated landing scenarios.

**Methods:**
- Numerical differentiation of trajectory data
- Experimental identification of thruster offsets, mass and effective thrust limits
- Acceleration-to-thrust mapping
- Open-loop trajectory control
- Proportional feedback control
- Damped **PD-style feedback** using position and velocity
- Repeated landing/drop-test evaluation

---

### 📡 [Spectral Analysis](Project_2_Spectral_Analysis.py) — **80%**

Fourier-based analysis of digital signals and unknown electronic filters.

The project uses swept-sine signals and frequency-domain analysis to identify filter behaviour, locate spectral noise and apply a custom transfer function to suppress unwanted frequencies.

**Methods:**
- Fast Fourier Transforms (FFT)
- Time- and frequency-domain signal analysis
- Transfer functions
- Frequency-domain filtering
- Inverse FFT reconstruction
- Noise-frequency identification
- Signal-to-noise improvement

---

### 🐍 [Programming Worksheets](Scientific_Worksheets.py) — **98% average** *(cohort highest)*

A series of assessed scientific-programming exercises covering core Python, numerical methods and computational problem-solving.

---

## Technical Stack

`Python` · `NumPy` · `SciPy` · `Matplotlib`

**Methods:** numerical modelling · root finding · Fourier analysis · signal processing · simulation · feedback control · numerical differentiation · data visualisation

---

## Repository Structure

```text
Scientific-Python-Projects/
├── Project_1_Quantum_Systems.py
├── Project_2_Spectral_Analysis.py
├── Project_3_Self_Landing_Rockets.py
├── Scientific_Worksheets.py
├── requirements.txt
└── README.md
```

> These projects originated as assessed university computational-physics work. The repository is presented as a portfolio of the numerical methods and scientific-programming techniques developed through those assignments.
