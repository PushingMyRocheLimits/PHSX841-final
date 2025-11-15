# PHSX 841 Final Project

## Digital Twin of an Electromagnetic and Hadronic Calorimeter

## Or... Little Tikes: My First Calorimeter
---
### Running the code:
1) The code is written in Python, so be sure you have an up to date installion of it
2) Be sure to have the following python packages installed:
	+ `matplotlib`, `scipy`, `numpy`, `PyQt6`
	+ e.g.  `>> pip install scipy	`
	
3) Download the files from the GitHub repo and put the package files into a folder on your `PYTHONPATH` (or run it from project folder)
4) Move into the folder containing the project (`cd ~/PHSX841-final/`)
5) Open a terminal and run the example script:
	+ `>> python run_example.py`
---
### Tweakable Items in the code:
- `transport.py`: cutoffs for `E_cut_gamma`, `E_cut_hadron`, `E_cut_electron`
- `material.py`: properties `density`, `X0`,`lambda_int`
- `physics.py`: 
	- EM model: continuous dE/dx + stochastic brems/pair with simple sampled fractions
	- Hadronic model: simple multiplicity & Dirichlet fragmentation
- Transverse spread: small-angle scattering approx in `ToyTransport._random_dir()` (inside `transport.py`)
- Calorimeter: sampling fraction, noise sigma, shaping tau in `SamplingCalorimeter`
---
### Stuff to be added
- TBA