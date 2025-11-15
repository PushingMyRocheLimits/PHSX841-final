import numpy as np
from .particle import Particle

# ----- Electromagnetic toy models -----
def sample_brems_photon_fraction():
    # Return fraction x of electron energy taken by a bremsstrahlung photon.
    # We use a simple power-law bias towards low-x but allow wide range.
    # PDF ~ 1/x (infrared divergence) regularized with exponent
    a = 0.6
    return np.random.rand() ** (1.0 / (1.0 + a))

def sample_pair_fraction():
#Fraction of photon energy to electron in pair production - use near symmetric split.
    return 0.5 + 0.2 * (np.random.rand() - 0.5)


# ----- Hadronic toy models -----
def hadronic_multiplicity(E):
    #Estimate number of secondaries from a hadronic interaction (toy)
    #multiplicity grows slowly with log E (E in MeV).
    return max(1, int(1 + np.log10(max(E,1)) / 1.0 + np.random.poisson(1)))

def hadronic_fragmentation(E, n):
    # Split hadron energy E into n secondaries with a simple Dirichlet.
    # Returns list of energies (MeV).
    if n == 1:
        return [E * 0.6] # single secondary gets chunk
    a = np.ones(n)
    parts = np.random.dirichlet(a)
    return list(parts * E)
