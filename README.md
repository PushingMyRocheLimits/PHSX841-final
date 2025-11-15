# PHSX 841 Final Project

## Digital Twin of an Electromagnetic and Hadronic Calorimeter

## Or... Little Tikes: My First Calorimeter
<img width="1500" height="1500" alt="image" src="https://github.com/user-attachments/assets/9a21485d-6d7b-4567-a9c0-d000bd1bd83c" />

---
### Running the code:
1) The code is written in Python, so be sure you have an up to date installion of it
2) Be sure to have the following python packages installed:
	+ `matplotlib`, `scipy`, `numpy`, `PyQt6`
	+ e.g.  `>> pip install scipy	`
	
3) Clone the repo: `git clone https://github.com/PushingMyRocheLimits/PHSX841-final.git`
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
- Implement Molière multiple scattering & lateral profile (Highland formula) to get realistic transverse shower RMS.
- Implement calibration and energy resolution study: run many primaries and compute reconstructed energy distributions and fit resolution vs E.
- Add multi-threading or vectorized stepping to speed large-statistics runs (so it don't murder yer 'puter)
