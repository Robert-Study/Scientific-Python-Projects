"""Scientific programming worksheets from computational physics coursework.

Each worksheet groups a few related exercises. Numerical helpers are separate
from plotting and console output; importing this file does not run an exercise.
Optional course data: dice_rolls.txt and the Yale stellar-parallax catalogue.
"""
from pathlib import Path
import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import c, epsilon_0


def fibonacci(count: int) -> list[int]:
    """Return F1 through Fcount, using F1 = F2 = 1."""
    if not isinstance(count, int) or count < 0:
        raise ValueError('count must be a nonnegative integer.')
    values = []
    previous, current = 0, 1
    for _ in range(count):
        values.append(current)
        previous, current = current, previous + current
    return values


def exponential_series(x: float, terms: int) -> float:
    """Evaluate the first terms of the Taylor series about zero."""
    if terms < 1 or not isinstance(terms, int):
        raise ValueError('terms must be a positive integer.')
    term = total = 1.0
    for order in range(1, terms):
        term *= x / order
        total += term
    return total


def classify_particle(tracker: bool, electromagnetic: bool,
                      hadronic: bool, muon: bool) -> str:
    """Apply the simplified detector rules used in the worksheet."""
    if tracker:
        if muon:
            return 'muon'
        if hadronic:
            return 'proton/pion'
        return 'electron' if electromagnetic else 'unknown'
    if electromagnetic:
        return 'photon'
    if hadronic:
        return 'neutron/lambda'
    return 'unknown' if muon else 'neutrino'


def binding_energy(mass_number, atomic_number: int):
    """Semi-empirical binding energy in MeV, with worksheet coefficients."""
    A = np.asarray(mass_number, dtype=float)
    Z = atomic_number
    if not isinstance(Z, (int, np.integer)) or Z < 1:
        raise ValueError('atomic_number must be a positive integer.')
    if np.any(~np.isfinite(A) | (A < Z) | (A != np.floor(A))):
        raise ValueError('Mass numbers must be finite integers at least as large as Z.')
    pairing = np.where(A % 2 == 1, 0.0, 12.0 if Z % 2 == 0 else -12.0)
    return (15.8*A - 18.3*A**(2/3) - .714*Z**2/A**(1/3)
            - 23.2*(A-2*Z)**2/A + pairing/np.sqrt(A))


def most_bound_isotope(atomic_number: int) -> tuple[int, float]:
    """Search integer A from Z to 3Z inclusive for maximum B/A."""
    binding_energy(atomic_number, atomic_number)  # Validate before allocating.
    masses = np.arange(atomic_number, 3*atomic_number + 1)
    per_nucleon = binding_energy(masses, atomic_number) / masses
    best = int(np.argmax(per_nucleon))
    return int(masses[best]), float(per_nucleon[best])


def dice_statistics(path: str | Path) -> dict:
    """Read rows of coin outcome (0/1) and die face (1..6)."""
    data = np.loadtxt(path, ndmin=2)
    if (data.shape[1] != 2 or len(data) == 0
            or not np.all(np.isin(data[:, 0], [0, 1]))
            or not np.all(np.isin(data[:, 1], np.arange(1, 7)))):
        raise ValueError('Expected two columns: coin 0/1 and die face 1..6.')
    coin, die = data.astype(int).T
    probabilities = {}
    for outcome, colour in [(0, 'red'), (1, 'blue')]:
        faces = die[coin == outcome]
        probabilities[colour] = (np.bincount(faces, minlength=7)[1:7] / len(faces)
                                 if len(faces) else np.full(6, np.nan))
    return {'trials': len(data), 'heads_probability': float(coin.mean()),
            'conditional_die_probabilities': probabilities}


def bisection(function, low: float, high: float, *, tolerance=1e-10,
              max_iterations=1000) -> float:
    """Bracketed root finding with an absolute tolerance on x."""
    if low >= high or tolerance <= 0 or max_iterations < 1:
        raise ValueError('Require low < high, positive tolerance and iteration limit.')
    f_low, f_high = function(low), function(high)
    if not np.all(np.isfinite([low, high, tolerance, f_low, f_high])):
        raise ValueError('Bounds, tolerance and endpoint values must be finite.')
    if f_low == 0:
        return float(low)
    if f_high == 0:
        return float(high)
    if np.signbit(f_low) == np.signbit(f_high):
        raise ValueError('The interval must bracket a sign change.')
    for _ in range(max_iterations):
        midpoint = low + (high-low)/2
        value = function(midpoint)
        if not np.isfinite(value):
            raise ValueError('Nonfinite function value inside the bracket.')
        if value == 0 or (high-low)/2 <= tolerance:
            return float(midpoint)
        if np.signbit(value) == np.signbit(f_low):
            low, f_low = midpoint, value
        else:
            high = midpoint
    raise RuntimeError('Bisection did not converge within the iteration limit.')


def minmax_normalise(values) -> np.ndarray:
    """Map a finite nonempty array to [0, 1]; constants map to zero."""
    values = np.asarray(values, dtype=float)
    if values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError('Provide nonempty finite data.')
    span = np.ptp(values)
    return np.zeros_like(values) if span == 0 else (values-values.min())/span


def madelung_cube(cutoff: int = 100) -> float:
    """Dimensionless NaCl lattice sum over [-cutoff, cutoff]^3.

    The positive convention is M = sum((-1)^(i+j+k+1)/r), omitting the origin.
    A finite cubic truncation approaches the infinite-lattice value slowly;
    this is not an Ewald summation. No charge or SI Coulomb factor belongs in M.
    """
    if not isinstance(cutoff, int) or cutoff < 1:
        raise ValueError('cutoff must be a positive integer.')
    coordinates = np.arange(-cutoff, cutoff + 1)
    j, k = np.meshgrid(coordinates, coordinates, indexing='ij')
    total = 0.0
    for i in coordinates:
        radius = np.sqrt(i*i + j*j + k*k)
        signs = np.where((i+j+k) % 2 == 0, -1.0, 1.0)
        total += np.divide(signs, radius, out=np.zeros_like(radius), where=radius > 0).sum()
    return float(total)


def electric_field(points, source_positions, source_charges) -> np.ndarray:
    """Field in N/C for point charges in a plane; distances are in metres.

    Sum k*q*r_vector/|r|^3. Locations coinciding with a source return NaN
    because the point-charge field is singular there.
    """
    points = np.asarray(points, dtype=float)
    sources = np.asarray(source_positions, dtype=float)
    charges = np.asarray(source_charges, dtype=float)
    if (points.ndim < 1 or points.shape[-1] != 2 or sources.ndim != 2
            or sources.shape[1] != 2 or charges.shape != (len(sources),)
            or not all(np.all(np.isfinite(x)) for x in [points, sources, charges])):
        raise ValueError('Use finite planar points, source positions and one charge per source.')
    displacement = points[..., None, :] - sources
    radius = np.linalg.norm(displacement, axis=-1)
    with np.errstate(divide='ignore', invalid='ignore'):
        contributions = charges[..., None]*displacement/radius[..., None]**3
    field = contributions.sum(axis=-2)/(4*np.pi*epsilon_0)
    return np.where(np.any(radius == 0, axis=-1)[..., None], np.nan, field)


def stellar_properties(catalogue, *, parallax_unit: str = 'arcsec') -> dict:
    """Extract magnitude, B−V and parallax from catalogue columns 1, 2 and 3.

    Specify the input parallax unit explicitly when using another catalogue.
    Nonpositive parallaxes and invalid colour temperatures are excluded.
    """
    data = np.asarray(catalogue, dtype=float)
    if data.ndim != 2 or data.shape[1] < 4:
        raise ValueError('The catalogue needs at least four columns.')
    if parallax_unit not in ('arcsec', 'mas'):
        raise ValueError('parallax_unit must be arcsec or mas.')
    magnitude, colour, parallax = data[:, 1:4].T
    parallax = parallax/(1000 if parallax_unit == 'mas' else 1)
    with np.errstate(divide='ignore', invalid='ignore'):
        distance = 1/parallax
        absolute = magnitude-5*(np.log10(distance)-1)
        temperature = 4600*(1/(.92*colour+1.7)+1/(.92*colour+.62))
    valid = (parallax > 0) & (temperature > 0) & np.isfinite(absolute) & np.isfinite(temperature)
    return {'temperature_K': temperature[valid], 'absolute_magnitude': absolute[valid],
            'valid_rows': valid}


def worksheet_1() -> dict:
    """Complex arithmetic, relativistic energy and quadratic roots."""
    expressions = [2*np.pi, np.pi/2, np.pi**2, np.sqrt(np.pi), 1j**2,
                   np.sqrt(-1+0j), np.log(2), np.log10(100),
                   (np.sin(np.pi/4)+np.cos(np.pi/4))**2, np.exp(1j*np.pi)+1]
    mass_kg, speed_m_s = 1.0, 1e8
    roots = np.roots([5, 29, 2])
    return {'expressions': expressions,
            'total_energy_J': mass_kg*c**2/np.sqrt(1-(speed_m_s/c)**2),
            'quadratic_roots': roots, 'quadratic_residuals': 5*roots**2+29*roots+2}


def worksheet_2() -> dict:
    """Sequences, Taylor approximation and a simple detector classifier."""
    sequence = fibonacci(40)
    x, reference = .5, math.exp(.5)
    terms = 1
    while abs(exponential_series(x, terms)/reference-1) > .01:
        terms += 1
    approximation = exponential_series(x, 11)
    return {'first_20_fibonacci': sequence[:20], 'golden_ratio_estimate': sequence[-1]/sequence[-2],
            'exp_approximation': approximation, 'exp_reference': reference,
            'relative_error': abs(approximation/reference-1), 'terms_for_one_percent': terms,
            'electron_example': classify_particle(True, True, False, False)}


def worksheet_3(dice_path: str | Path | None = None) -> dict:
    """Conditional dice probabilities and nuclear binding-energy searches."""
    isotopes = [(Z, *most_bound_isotope(Z)) for Z in range(1, 101)]
    return {'dice': dice_statistics(dice_path) if dice_path is not None else None,
            'iron_56_binding_MeV': float(binding_energy(56, 26)),
            'isotopes_Z_A_MeV_per_nucleon': isotopes,
            'most_bound_in_search': max(isotopes, key=lambda row: row[2])}


def worksheet_4(cutoff: int = 100) -> dict:
    """Bisection, normalisation and a finite lattice sum."""
    def polynomial(x):
        return (x+.6)*(x-1.73)*(x-np.pi)
    return {'roots': [bisection(polynomial, -2, 0), bisection(polynomial, 1, 2)],
            'normalised': minmax_normalise([10, 1, 19, -7, 14, -3]),
            'madelung_cutoff': cutoff, 'madelung_constant': madelung_cube(cutoff)}


def worksheet_5(catalogue_path: str | Path | None = None, *, parallax_unit='arcsec',
                plot: bool = True) -> dict:
    """Gaussian distributions, stellar properties and electrostatic fields."""
    x = np.linspace(-10, 10, 300)
    sigma = np.sqrt(2)
    densities = [np.exp(-.5*((x-mean)/sigma)**2)/(sigma*np.sqrt(2*np.pi))
                 for mean in [-np.pi, np.pi]]
    sources = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])
    field = electric_field([.25, .5], sources, np.ones(4))
    stars = (stellar_properties(np.loadtxt(catalogue_path, ndmin=2), parallax_unit=parallax_unit)
             if catalogue_path is not None else None)
    if plot:
        fig, ax = plt.subplots()
        for mean, density in zip([-np.pi, np.pi], densities):
            ax.plot(x, density, label=f'mean = {mean:.3f}')
        ax.set(xlabel='x', ylabel='Probability density', title='Normal distributions')
        ax.legend()
        grid = np.linspace(-3, 3, 15)
        xx, yy = np.meshgrid(grid, grid)
        points = np.stack([xx, yy], axis=-1)
        for positions in [sources, np.array([[-1, -1], [1, 1]])]:
            values = electric_field(points, positions, np.ones(len(positions)))
            fig, ax = plt.subplots()
            ax.quiver(xx, yy, values[..., 0], values[..., 1])
            ax.scatter(*positions.T, color='tab:red')
            ax.set(xlabel='x (m)', ylabel='y (m)', title='Point-charge electric field', aspect='equal')
        if stars is not None:
            fig, ax = plt.subplots()
            ax.scatter(stars['temperature_K'], stars['absolute_magnitude'], s=1)
            ax.set(xlabel='Temperature (K)', ylabel='Absolute magnitude', title='Hertzsprung–Russell diagram')
            ax.invert_xaxis()
            ax.invert_yaxis()
        plt.show()
    return {'field_at_sample_N_per_C': field, 'stellar_properties': stars}


def worksheet_6(*, trials: int = 1_000_000, steps: int = 10_000,
                seed: int | None = None, plot: bool = True) -> dict:
    """Vectorised dice experiments and one-dimensional random walks."""
    if not isinstance(trials, int) or trials < 1 or not isinstance(steps, int) or steps < 0:
        raise ValueError('trials must be positive and steps nonnegative integers.')
    rng = np.random.default_rng(seed)
    pairs = rng.integers(1, 7, size=(trials, 2), dtype=np.int8)
    observed = float(np.mean(np.all(pairs == 6, axis=1)))
    rolls = rng.integers(1, 7, size=(trials, 4), dtype=np.int8)
    totals = rolls.sum(axis=1)-rolls.min(axis=1)
    probabilities = np.bincount(totals, minlength=19)[3:19]/trials
    walk = np.r_[0, np.cumsum(rng.choice([-1, 1], size=steps))]
    running_mean = np.cumsum(walk)/np.arange(1, len(walk)+1)
    if plot:
        fig, axes = plt.subplots(1, 3, figsize=(13, 4), layout='constrained')
        axes[0].bar(np.arange(3, 19), probabilities)
        axes[0].set(xlabel='Best three of four dice', ylabel='Probability')
        axes[1].plot(walk)
        axes[1].set(xlabel='Step', ylabel='Position')
        axes[2].plot(running_mean)
        axes[2].set(xlabel='Step', ylabel='Running mean position')
        plt.show()
    return {'double_six_probability': observed, 'exact_double_six_probability': 1/36,
            'relative_error_percent': 100*abs(observed/(1/36)-1),
            'best_three_probabilities': probabilities, 'walk': walk, 'running_mean': running_mean}
