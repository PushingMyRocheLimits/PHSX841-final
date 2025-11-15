import numpy as np
from .particle import Particle
from .material import Material
from .transport import ToyTransport
from .calorimeter import SamplingCalorimeter


def default_material():
    # Example: scintillating/plastic-like material
    return Material('ToyScint', density=1.03, X0=43.0, lambda_int=120.0)


def run_example(primary_pid='gamma', E0_MeV=1000.0):
    mat = default_material()
    prim = Particle(primary_pid, E0_MeV, pos=(0,0,0), direction=(0,0,1), t=0.0)
    engine = ToyTransport(mat)
    deposits = engine.propagate([prim], max_steps=20000)
    # simple sampling cal / change as desired
    cal = SamplingCalorimeter(sampling_fraction=0.25, noise_sigma=0.2, tau=30.0)
    shaped, times = cal.digitize(deposits, dt=1.0, tmax=1000.0)
    return deposits, shaped, times
