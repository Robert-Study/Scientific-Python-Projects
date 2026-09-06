import unittest

import numpy as np
from scipy.signal import chirp
from scipy.linalg import eigh_tridiagonal
from scipy.constants import hbar, m_e, e

from Project_1_Quantum_Systems import solve_eigenvalues, x_to_energy_eV, a, V0
from Project_2_Spectral_Analysis import generate_swept_sine, apply_transfer_filter_once, magnitude_spectrum


class NumericalPhysicsTests(unittest.TestCase):
    def test_well_energies_agree_with_independent_finite_difference_solution(self):
        # Discretise the Schrodinger Hamiltonian, independent of the root equations.
        x = np.linspace(-2*a, 2*a, 2401)[1:-1]
        dx = x[1] - x[0]
        kinetic = hbar**2 / (2*m_e*dx**2*e)
        diagonal = 2*kinetic + np.where(np.abs(x) < a/2, 0, V0)
        numeric = eigh_tridiagonal(diagonal, np.full(len(x)-1, -kinetic),
                                   select='v', select_range=(0, V0), eigvals_only=True)
        analytic = [x_to_energy_eV(r, a) for r in solve_eigenvalues()]
        self.assertEqual(len(analytic), 6)
        np.testing.assert_allclose(analytic, numeric, rtol=.005, atol=.003)

    def test_shallow_well_has_a_bound_state(self):
        roots = solve_eigenvalues(.01)
        self.assertEqual(len(roots), 1)
        self.assertTrue(0 < roots[0] < .1)

    def test_linear_sweep_matches_scipy_phase_integral(self):
        t, frequency, signal = generate_swept_sine(1, 2048, 10, 400)
        expected = chirp(t, f0=10, f1=400, t1=1, method='linear', phi=-90)
        np.testing.assert_allclose(signal, expected, atol=1e-12)
        self.assertLess(frequency[-1], 400)

    def test_sweep_rejects_aliasing(self):
        with self.assertRaises(ValueError):
            generate_swept_sine(1, 100, 10, 80)

    def test_notch_removes_resonant_tone(self):
        fs = 2048
        t = np.arange(fs) / fs
        L = .0255
        C = 1 / ((2*np.pi*320)**2 * L)
        filtered = apply_transfer_filter_once(t, np.sin(2*np.pi*320*t), 10, L, C)
        self.assertLess(np.max(np.abs(filtered)), 1e-11)

    def test_fft_includes_nyquist_bin(self):
        freq, magnitude = magnitude_spectrum((-1.0)**np.arange(16), 16)
        self.assertEqual(freq[-1], 8)
        self.assertAlmostEqual(magnitude[-1], 16)

    def test_fft_filter_rejects_nonuniform_sampling(self):
        with self.assertRaisesRegex(ValueError, 'uniformly'):
            apply_transfer_filter_once([0, 1, 3], [1, 2, 3], 1, 1, 1)


if __name__ == '__main__':
    unittest.main()
