"""Create separate figures from the coursework methods and supplied recordings."""
from pathlib import Path
from itertools import product
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from projects.Project_1_Quantum_Systems import solve_eigenvalues, x_to_energy_eV, a, V0
from projects.Project_2_Spectral_Analysis import apply_transfer_filter_n_times
from projects import Scientific_Worksheets as w
ROOT=Path(__file__).resolve().parents[1]
BLUE,ORANGE='#19647e','#ae725b'


def finish(fig, axes, filename):
    for ax in np.asarray(axes,dtype=object).ravel():
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.15)
    fig.savefig(ROOT/filename,dpi=160)
    plt.close(fig)


def quantum():
    energies=[x_to_energy_eV(x,a) for x in solve_eigenvalues()]
    fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
    ax.hlines(energies,-.4,.4,color=BLUE,linewidth=2)
    for i,E in enumerate(energies,1):ax.text(.45,E,f'{i}: {E:.3f} eV',va='center')
    ax.axhline(V0,color=ORANGE,linestyle='--',label='Barrier height')
    ax.set(xlim=(-.6,1.15),ylim=(0,11),xticks=[],ylabel='Energy (eV)',title='Finite square well: 1 nm width, 10 eV barrier')
    ax.legend(frameon=False,loc='center right')
    finish(fig,[ax],'quantum-energy-levels.png')
    return energies


def spectral():
    with np.load(ROOT/'data/course_audio.npz',allow_pickle=False) as d:
        clean,noise=d['clean'].astype(float),d['noise'].astype(float)
        fs=int(d['sampling_rate_hz'])
    noisy=clean+noise
    t=np.arange(len(clean))/fs
    f=np.fft.rfftfreq(len(t),1/fs)
    # Locate the interference from the corrupted input alone.
    mask=(f>=200)&(f<=1000)
    centre=float(f[mask][np.argmax(np.abs(np.fft.rfft(noisy))[mask])])
    R,L,N=8.0,.0255,3
    C=1/((2*np.pi*centre)**2*L)
    filtered=apply_transfer_filter_n_times(t,noisy,R,L,C,N)
    def snr(y):return float(10*np.log10(np.sum(clean**2)/np.sum((y-clean)**2)))
    before,after=snr(noisy),snr(filtered)
    fig,axes=plt.subplots(3,1,figsize=(11,8),layout='constrained')
    # Plot every sample: striding would alias the narrowband interference.
    step=1
    axes[0].plot(t[::step],noisy[::step]/np.max(np.abs(noisy)),color=ORANGE,linewidth=.5)
    axes[0].set(xlabel='Time (s)',ylabel='Normalised amplitude',title='University spoken-digit recording with the course noise model')
    axes[1].plot(t[::step],clean[::step],color='#999999',linewidth=1,label='Clean recording')
    axes[1].plot(t[::step],filtered[::step],color=BLUE,linewidth=.7,label='Filtered output')
    axes[1].set(xlabel='Time (s)',ylabel='Amplitude',title=f'Recovered speech | reference SNR {before:.1f} to {after:.1f} dB')
    axes[1].legend(frameon=False,loc='upper right')
    window=np.hanning(len(t))
    for y,label,colour in [(noisy,'Input',ORANGE),(clean,'Clean recording','#999999'),(filtered,'Filtered',BLUE)]:
        amplitude=2*np.abs(np.fft.rfft(y*window))/window.sum()
        axes[2].plot(f,20*np.log10(np.maximum(amplitude,1e-8)),color=colour,linewidth=.65,label=label)
    axes[2].set(xlim=(50,5000),xscale='log',ylim=(-100,90),xlabel='Frequency (Hz)',ylabel='Amplitude (dB re 1)',title=f'RLC band-stop filter: three passes, centre {centre:.1f} Hz')
    axes[2].legend(frameon=False,loc='upper right')
    finish(fig,axes,'spectral-analysis.png')
    return {'centre_hz':centre,'R_ohm':R,'L_H':L,'C_F':C,'passes':N,'reference_snr_before_db':before,'reference_snr_after_db':after,'snr_definition':'10 log10(sum(clean**2)/sum((output-clean)**2)), including distortion'}


def worksheets():
    trial=w.worksheet_6(trials=200000,seed=42,plot=False)
    rolls=np.array(list(product(range(1,7),repeat=4)))
    exact=np.bincount(rolls.sum(axis=1)-rolls.min(axis=1),minlength=19)[3:19]/len(rolls)
    cutoffs=[5,10,20,40,80]
    sums=[w.madelung_cube(L) for L in cutoffs]
    isotopes=[(Z,*w.most_bound_isotope(Z)) for Z in range(1,101)]
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    x=np.arange(3,19)
    axes[0,0].bar(x-.18,exact,width=.36,color=BLUE,label='Exact enumeration')
    axes[0,0].bar(x+.18,trial['best_three_probabilities'],width=.36,color=ORANGE,label='200,000 trials')
    axes[0,0].set(xlabel='Best three of four dice',ylabel='Probability',title='Monte Carlo and exact probabilities')
    axes[0,0].legend(frameon=False,fontsize=9)
    axes[0,1].plot([r[0] for r in isotopes],[r[2] for r in isotopes],color=BLUE)
    axes[0,1].set(xlabel='Atomic number Z',ylabel='Binding energy per nucleon (MeV)',title='Most-bound isotope for each Z')
    axes[1,0].plot(cutoffs,sums,'o-',color=BLUE)
    axes[1,0].set(xlabel='Cubic lattice cutoff',ylabel='Dimensionless lattice sum',title='NaCl Madelung sum: finite cubes')
    grid=np.linspace(-2,2,17)
    xx,yy=np.meshgrid(grid,grid)
    positions=np.array([[-1,-1],[-1,1],[1,-1],[1,1]])
    field=w.electric_field(np.stack([xx,yy],axis=-1),positions,np.ones(4))
    norm=np.linalg.norm(field,axis=-1)[...,None]
    unit=np.divide(field,norm,out=np.zeros_like(field),where=norm>0)
    axes[1,1].quiver(xx,yy,unit[...,0],unit[...,1],color=BLUE,pivot='mid',scale=22)
    axes[1,1].scatter(*positions.T,color=ORANGE,s=60,zorder=3)
    axes[1,1].set(xlabel='x (m)',ylabel='y (m)',title='Electric-field direction: four equal charges',aspect='equal')
    finish(fig,axes,'scientific-worksheets.png')
    return {'dice_trials':200000,'dice_seed':42,'dice_max_probability_error':float(np.max(np.abs(exact-trial['best_three_probabilities']))),'madelung_cutoffs':cutoffs,'madelung_sums':sums,'most_bound_Z_A_MeV_per_nucleon':max(isotopes,key=lambda r:r[2])}


def main():
    result={'quantum_energies_eV':quantum(),'spectral':spectral(),'worksheets':worksheets()}
    (ROOT/'data/figure_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
