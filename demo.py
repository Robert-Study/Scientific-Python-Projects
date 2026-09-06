"""Reproduce standalone quantum and synthetic signal-processing examples."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from Project_1_Quantum_Systems import solve_eigenvalues, x_to_energy_eV, a, V0
from Project_2_Spectral_Analysis import apply_transfer_filter_once, magnitude_spectrum


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('outputs/demo'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    energies = [x_to_energy_eV(x, a) for x in solve_eigenvalues()]
    fs = 2048
    t = np.arange(fs) / fs
    clean = np.sin(2*np.pi*80*t)
    noisy = clean + 0.6*np.sin(2*np.pi*320*t)
    inductance = .0255
    capacitance = 1 / ((2*np.pi*320)**2 * inductance)
    filtered = apply_transfer_filter_once(t, noisy, 10, inductance, capacitance)
    def snr(signal):
        return float(10*np.log10(np.sum(clean**2) / np.sum((signal-clean)**2)))
    freq, before = magnitude_spectrum(noisy, fs)
    _, after = magnitude_spectrum(filtered, fs)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout='constrained')
    axes[0].hlines(energies, -.35, .35, color='#176d8c')
    for i, energy in enumerate(energies, 1):
        axes[0].text(.38, energy, f'{i}: {energy:.3f} eV', va='center', fontsize=9)
    axes[0].axhline(V0, color='#aa513b', linestyle='--', label='Barrier height')
    axes[0].set(xlim=(-.6, 1.2), ylim=(0, 11), xticks=[], ylabel='Energy (eV)', title='Finite square well | 1 nm, 10 eV')
    axes[0].legend(frameon=False)
    axes[1].plot(freq, before, label='Synthetic input', color='#a5543d', alpha=.7)
    axes[1].plot(freq, after, label='Notch-filtered', color='#176d8c')
    axes[1].set(xlim=(0, 450), xlabel='Frequency (Hz)', ylabel='FFT magnitude', title='80 Hz signal + 320 Hz interference')
    axes[1].legend(frameon=False)
    for ax in axes:
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=.15)
    fig.savefig(args.output / 'scientific-python.png', dpi=160)
    plt.close(fig)
    np.savetxt(args.output / 'synthetic-signal.csv', np.column_stack([t, clean, noisy, filtered]),
               delimiter=',', header='time_s,clean,with_interference,filtered', comments='')
    summary = {'example_parameters': {'well_width_nm': 1, 'barrier_eV': V0},
               'bound_state_energies_eV': energies, 'signal_data': 'synthetic deterministic tones',
               'snr_before_db': snr(noisy), 'snr_after_db': snr(filtered),
               'note': 'Post-assessment portfolio example, not the university recorded audio or rocket simulator.'}
    (args.output / 'results.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
