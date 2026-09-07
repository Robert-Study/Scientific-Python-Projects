"""Draw the two computational-physics figures used in the README."""
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, sosfiltfilt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Project_1_Quantum_Systems import solve_eigenvalues, x_to_energy_eV, a, V0
from Project_2_Spectral_Analysis import apply_transfer_filter_once


def make_figure():
    energies = [x_to_energy_eV(x, a) for x in solve_eigenvalues()]
    fs = 2048
    time = np.arange(4*fs)/fs
    rng = np.random.default_rng(42)
    clean = (np.sin(2*np.pi*45*time) + .65*np.sin(2*np.pi*80*time+.4)
             + .35*np.sin(2*np.pi*140*time+1.2))
    interference = sum(amplitude*np.sin(2*np.pi*frequency*time+phase)
                       for frequency, amplitude, phase in [(260,.9,.3),(410,.65,1.1),(620,.5,2.4)])
    noisy = clean + interference + rng.normal(0, .7, len(time))
    filtered = noisy.copy()
    inductance = .0255
    for frequency in [260,410,620]:
        capacitance = 1/((2*np.pi*frequency)**2*inductance)
        filtered = apply_transfer_filter_once(time, filtered, 8, inductance, capacitance)
    # Broadband rejection complements the notches. The passband retains all
    # three signal components; filter coefficients do not use the clean trace.
    filtered = sosfiltfilt(butter(6, 190, fs=fs, output='sos'), filtered)
    interior = slice(fs//2, -fs//2)
    def snr(signal):
        return 10*np.log10(np.sum(clean[interior]**2)/np.sum((signal[interior]-clean[interior])**2))
    before_snr, after_snr = snr(noisy), snr(filtered)
    fig = plt.figure(figsize=(13,7),layout='constrained')
    grid = fig.add_gridspec(2,2,width_ratios=[.85,1.6])
    well, trace, spectrum = fig.add_subplot(grid[:,0]),fig.add_subplot(grid[0,1]),fig.add_subplot(grid[1,1])
    well.hlines(energies,-.35,.35,color='#19647e',linewidth=2)
    for number, energy in enumerate(energies,1):
        well.text(.39,energy,f'{number}: {energy:.3f} eV',va='center',fontsize=9)
    well.axhline(V0,color='#aa513b',linestyle='--',label='Barrier height')
    well.set(xlim=(-.55,1.15),ylim=(0,11),xticks=[],ylabel='Energy (eV)',title='Finite square well\n1 nm width · 10 eV barrier')
    well.legend(frameon=False,loc='upper left')
    visible=(time>=1)&(time<=1.18)
    trace.plot(time[visible]-1,noisy[visible],color='#b38778',alpha=.65,linewidth=.7,label='With noise')
    trace.plot(time[visible]-1,clean[visible],color='#555555',linestyle='--',linewidth=1,label='Clean reference')
    trace.plot(time[visible]-1,filtered[visible],color='#19647e',linewidth=1.3,label='Filtered')
    trace.set(xlabel='Time (s)',ylabel='Amplitude',title='Three signal components, broadband noise and three interferers')
    trace.legend(frameon=False,ncol=3,fontsize=9)
    freq=np.fft.rfftfreq(len(time),1/fs)
    window=np.hanning(len(time))
    for values,label,colour in [(noisy,'With noise','#b38778'),(filtered,'Filtered','#19647e')]:
        amplitude=2*np.abs(np.fft.rfft(window*values))/window.sum()
        spectrum.plot(freq,20*np.log10(np.maximum(amplitude,1e-6)),color=colour,linewidth=.65,label=label,alpha=.85)
    spectrum.set(xlim=(0,800),ylim=(-75,5),xlabel='Frequency (Hz)',ylabel='Amplitude (dB re 1)',
                 title=f'Notch and low-pass filtering | SNR {before_snr:.1f} → {after_snr:.1f} dB')
    for ax in [well,trace,spectrum]:
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.15)
    destination=ROOT/'assets/scientific-python.png'
    fig.savefig(destination,dpi=160)
    plt.close(fig)
    return {'snr_before_db':float(before_snr),'snr_after_db':float(after_snr),'figure':str(destination)}


if __name__ == '__main__':
    print(make_figure())
