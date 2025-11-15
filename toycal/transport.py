import numpy as np
from .particle import Particle
from .physics import sample_brems_photon_fraction, sample_pair_fraction, hadronic_multiplicity, hadronic_fragmentation

class TransportRecorder:
    # Records deposits as list of (x,y,z,E,t) tuples
    def __init__(self):
        self.deposits = []

    def deposit(self, pos, E, t):
        if E <= 0:
            return
        self.deposits.append((float(pos[0]), float(pos[1]), float(pos[2]), float(E), float(t)))

class ToyTransport:
    """Toy, modular transport engine for electrons, photons and hadrons.
    Responsibilities:
    - propagate primary and secondaries
    - apply stochastic step lengths
    - generate secondaries for bremsstrahlung, pair production, hadronic interactions
    - record local energy deposition (ionization-like continuous loss)

    This is intentionally simple and tunable for studies rather than physics accuracy.
    """
    def __init__(self, material, rng=None):
        self.mat = material
        self.rng = rng or np.random
        self.recorder = TransportRecorder()
        # cutoffs (MeV)
        self.E_cut_gamma = 0.1
        self.E_cut_electron = 0.1
        self.E_cut_hadron = 1.0

    def _sample_step(self, mean_free_path):
        # Exponential sampling for interaction lengths / radiation lengths
        return self.rng.exponential(mean_free_path)


    def _continuous_loss(self, pid, E, step):
        # Simple continuous dE/dx: electrons lose more, hadrons less; proportional to density
        rho = self.mat.density
        if pid == 'e-':
            dedx = 2.0 * rho # MeV/cm (toy)
        elif pid == 'gamma':
            dedx = 0.02 * rho
        else:
            dedx = 1.2 * rho
        dE = dedx * step
        dE = min(dE, E * 0.9)
        return dE

    def propagate(self, primaries, max_steps=10000):
        # Simple stack-based propagation
        stack = [p.copy() for p in primaries]
        steps = 0
        while stack and steps < max_steps:
            p = stack.pop()
            steps += 1
            if p.pid == 'gamma':
                if p.E < self.E_cut_gamma:
                # deposit remaining energy locally
                    self.recorder.deposit(p.pos, p.E, p.t)
                    continue
                # sample pair-production along radiation length scale
                mean_X = self.mat.X0
                step = self._sample_step(mean_X)
                # continuous loss negligible for gamma; but deposit small fraction
                # advance position along direction
                p.pos = p.pos + p.dir * step
                # decide if pair-production occurs within this step: use prob = 1 - exp(-step/X0)
                if self.rng.rand() < (1 - np.exp(-step / mean_X)):
                    # pair production: split energy into e+ e-
                    frac = sample_pair_fraction()
                    Ee = p.E * frac
                    Ep = p.E * (1 - frac)
                    e1 = Particle('e-', Ee, pos=p.pos.copy(), direction=p.dir.copy(), t=p.t)
                    e2 = Particle('e+', Ep, pos=p.pos.copy(), direction=p.dir.copy(), t=p.t)
                    stack.append(e1)
                    stack.append(e2)
                else:
                    # If no interaction, deposit tiny amount (Compton-like)
                    deposit = p.E * 0.01
                    self.recorder.deposit(p.pos, deposit, p.t)
                    p.E -= deposit
                    if p.E > self.E_cut_gamma:
                        stack.append(p)
                    else:
                        self.recorder.deposit(p.pos, p.E, p.t)
                continue
            elif p.pid in ('e-', 'e+'):
                if p.E < self.E_cut_electron:
                    self.recorder.deposit(p.pos, p.E, p.t)
                    continue
                # sample a step as fraction of radiation length
                mean_X = 0.2 * self.mat.X0
                step = self._sample_step(mean_X)
                # continuous ionization loss
                dE_cont = self._continuous_loss(p.pid, p.E, step)
                p.E -= dE_cont
                self.recorder.deposit(p.pos, dE_cont, p.t)
                # advance
                p.pos = p.pos + p.dir * step
                # stochastic bremsstrahlung emission with probability ~ step/X0
                if self.rng.rand() < (1 - np.exp(-step / self.mat.X0)):
                    frac = sample_brems_photon_fraction()
                    E_gamma = p.E * frac
                    p.E -= E_gamma
                    g = Particle('gamma', E_gamma, pos=p.pos.copy(), direction=p.dir.copy(), t=p.t)
                    stack.append(g)
                # multiple Coulomb scattering: random small deflection
                theta = np.random.normal(0, 0.02) # small deflection rad; toy
                # rotate direction about random axis (simple approximation)
                axis = np.random.normal(size=3)
                axis -= axis.dot(p.dir) * p.dir
                if np.linalg.norm(axis) > 1e-12:
                    axis = axis / np.linalg.norm(axis)
                    # Rodrigues' rotation
                    dir0 = p.dir
                    p.dir = (dir0 * np.cos(theta) +
                    np.cross(axis, dir0) * np.sin(theta) +
                    axis * (axis.dot(dir0)) * (1 - np.cos(theta)))
                if p.E > self.E_cut_electron:
                    stack.append(p)
                else:
                    self.recorder.deposit(p.pos, p.E, p.t)
                continue
            else:
                # treat everything else as hadron (pion, proton...) -> use hadronic interaction length
                if p.E < self.E_cut_hadron:
                    self.recorder.deposit(p.pos, p.E, p.t)
                    continue
                mean_int = self.mat.lambda_int
                step = self._sample_step(mean_int)
                # continuous ionization
                dE_cont = self._continuous_loss(p.pid, p.E, step)
                p.E -= dE_cont
                self.recorder.deposit(p.pos, dE_cont, p.t)
                p.pos = p.pos + p.dir * step
                # decide if hadronic inelastic occurs
                if self.rng.rand() < (1 - np.exp(-step / mean_int)):
                    n = hadronic_multiplicity(p.E)
                    parts = hadronic_fragmentation(p.E, n)
                    for i, Ei in enumerate(parts):
                        # choose secondary type (charged/neutral pions or nucleons)
                        typ = self.rng.choice(['pi+', 'pi-', 'pi0', 'n'], p=[0.4,0.4,0.1,0.1])
                        sec = Particle(typ, Ei, pos=p.pos.copy(), direction=self._random_dir(p.dir), t=p.t)
                        stack.append(sec)
                    # absorb the remnant
                else:
                    # no interaction -> continue
                    if p.E > self.E_cut_hadron:
                        stack.append(p)
                    else:
                        self.recorder.deposit(p.pos, p.E, p.t)
                continue
        return self.recorder.deposits

    def _random_dir(self, forward):
        # small spread around forward
        ang = np.random.normal(0, 0.2)
        axis = np.random.normal(size=3)
        axis -= axis.dot(forward) * forward
        if np.linalg.norm(axis) < 1e-12:
            return forward.copy()
        axis = axis / np.linalg.norm(axis)
        dir0 = forward
        theta = ang
        newdir = (dir0 * np.cos(theta) +
            np.cross(axis, dir0) * np.sin(theta) +
            axis * (axis.dot(dir0)) * (1 - np.cos(theta)))
        return newdir / (np.linalg.norm(newdir) + 1e-12)
