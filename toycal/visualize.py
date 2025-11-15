import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_deposits(deposits, show=True):
    xs = [d[0] for d in deposits]
    ys = [d[1] for d in deposits]
    zs = [d[2] for d in deposits]
    Es = [d[3] for d in deposits]
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(xs, ys, zs, s=np.clip(np.array(Es) * 2, 1, 200), alpha=0.6)
    ax.set_xlabel('x (cm)')
    ax.set_ylabel('y (cm)')
    ax.set_zlabel('z (cm)')
    if show:
        plt.show()
    return fig

def plot_longitudinal(deposits, bins=50, show=True):
    zs = [d[2] for d in deposits]
    Es = [d[3] for d in deposits]
    zmin, zmax = min(zs), max(zs)
    hist, edges = np.histogram(zs, bins=bins, weights=Es)
    centers = 0.5 * (edges[:-1] + edges[1:])
    import matplotlib.pyplot as plt
    plt.step(centers, hist, where='mid')
    plt.xlabel('z (cm)')
    plt.ylabel('Deposited Energy (MeV)')
    if show:
        plt.show()
    return centers, hist

