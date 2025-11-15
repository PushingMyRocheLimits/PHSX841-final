import numpy as np
from scipy.signal import fftconvolve


class SamplingCalorimeter:
    """Toy sampling calorimeter response.
    - sampling_fraction: fraction of deposited energy that appears in readout
    - noise_sigma (MeV): electronics noise (gaussian for simplicity)
    - shaping: single-pole exponential shaping with time constant tau (ns)
    """
    def __init__(self, sampling_fraction=0.3, noise_sigma=0.5, tau=50.0):
        self.sampling_fraction = sampling_fraction
        self.noise_sigma = noise_sigma
        self.tau = tau


    def digitize(self, deposits, dt=1.0, tmax=500.0):
        # deposits: list of (x,y,z,E,t)
        # Returns digitized waveform (time bins) and time array.
        nbins = int(tmax / dt) + 1
        wave = np.zeros(nbins)
        for x,y,z,E,t in deposits:
            it = int(t // dt)
            if it < 0 or it >= nbins:
                continue
            wave[it] += E * self.sampling_fraction
        # shaping kernel: causal exponential
        t_kernel = np.arange(0, 10 * self.tau, dt)
        kernel = (1.0 / self.tau) * np.exp(-t_kernel / self.tau)
        shaped = fftconvolve(wave, kernel)[:nbins] * dt
        # add gaussian noise
        shaped += np.random.normal(0, self.noise_sigma, size=shaped.shape)
        return shaped, np.linspace(0, dt*(nbins-1), nbins)


    def total_energy(self, shaped_waveform):
        # simple integrator: sum of samples (units MeV*samples)
        return shaped_waveform.sum()
