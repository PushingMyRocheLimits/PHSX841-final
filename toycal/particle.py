import numpy as np

class Particle:
#Simple particle record for transport.
#Attributes: pid (str), E (MeV), pos (x,y,z) in cm, dir (unit vector), t (ns)

    def __init__(self, pid, E, pos=(0.0,0.0,0.0), direction=(0,0,1), t=0.0):
        self.pid = pid
        self.E = float(E)
        self.pos = np.array(pos, dtype=float)
        self.dir = np.array(direction, dtype=float) / (np.linalg.norm(direction) + 1e-12)
        self.t = float(t)


    def copy(self):
        return Particle(self.pid, self.E, self.pos.copy(), self.dir.copy(), self.t)

