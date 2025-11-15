"""
Example script (outside the package) to run and visualize a shower.
>> python run_example.py

"""
if __name__ == '__main__':
    from toycal.run_sim import run_example
    from toycal.visualize import plot_3d_deposits, plot_longitudinal
    deps, shaped, times = run_example('gamma', 2000.0)
    print('n deposits =', len(deps))
    plot_3d_deposits(deps)
    plot_longitudinal(deps)
    # simple display of shaped waveform
    import matplotlib.pyplot as plt
    plt.plot(times, shaped)
    plt.xlabel('time (ns)')
    plt.ylabel('ADC (arb)')
    plt.show()
