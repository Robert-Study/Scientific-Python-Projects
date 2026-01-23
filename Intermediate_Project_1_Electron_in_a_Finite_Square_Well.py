"""
Intermediate Project 1: Electron in a Finite Square Well (95%)

Aim
---------------------------
Find the bound-state energy eigenvalues (E < V0) for an electron in the finite
square potential well:

    V(x) = { V0,  |x| >= a/2
           { 0,   |x| <  a/2

Theory
---------------------------
Define a dimensionless parameter x (not the coordinate x) related to the energy E by:

    x = (a / ħ) * sqrt(m E / 2)

where:
- a is the well width (SI units),
- ħ is reduced Planck’s constant,
- m is electron mass.

Let:

    λ0 = (m a^2 V0) / (2 ħ^2)

Then the bound-state eigenvalues reduce to solving the transcendental equations:

Even states:
    tan(x) = sqrt(λ0 - x^2) / x

Odd states:
   -cot(x) = sqrt(λ0 - x^2) / x

Numerical approach
------------------
1) Build λ0 from the well parameters (a, V0).
2) Visualise tan(x), -cot(x), and f(x)=sqrt(λ0-x^2)/x to identify root brackets.
3) Use bisection to solve:
   even_equation(x) = tan(x) - f(x) = 0
   odd_equation(x)  = -cot(x) - f(x) = 0
4) Convert each solution x -> energy E (Joules, then eV).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from scipy import optimize

a, V0 = student.get_parameters() #Required to be running module engine

# Potential well plot (V(x))

def plot_potential(a: float, V0: float) -> None:
    x_coord = np.linspace(-a, a, 1000)
    V = np.piecewise(
        x_coord,
        [np.abs(x_coord) >= a / 2, np.abs(x_coord) < a / 2],
        [V0, 0.0],)

    plt.figure(figsize=(8, 4))
    plt.title("Finite Square Well Potential")
    plt.xlabel(r"$x$ (m)")
    plt.ylabel(r"$V(x)$ (eV)")
    plt.ylim(0, 4 / 3 * np.max(V))
    plt.plot(x_coord, V)
    plt.show()

# Dimensionless setup
e = constants.e          # elementary charge [C]
hbar = constants.hbar    # reduced Planck constant [J s]
m_e = constants.m_e      # electron mass [kg]

# Convert V0 from eV to Joules inside λ0:
lambda_0 = (m_e * a**2 * (V0 * e)) / (2 * hbar**2)

def f_rhs(x: np.ndarray | float) -> np.ndarray | float:
    """f(x) = sqrt(λ0 - x^2)/x (domain: 0 < x < sqrt(λ0))."""
    return np.sqrt(lambda_0 - x**2) / x


# Visualise transcendental functions (to bracket roots)
def plot_transcendental(lambda_0: float) -> None:
    x = np.linspace(0.1, np.sqrt(lambda_0), 1000, endpoint=False)

    tan_x = np.tan(x)
    neg_cot_x = -1.0 / np.tan(x)
    f_x = f_rhs(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, tan_x, label="tan(x)")
    plt.plot(x, neg_cot_x, label="-cot(x)")
    plt.plot(x, f_x, label=r"$\sqrt{\lambda_0-x^2}/x$")
    plt.title("Root-finding guide: tan(x), -cot(x), and f(x)")
    plt.xlabel("x")
    plt.ylabel("Value")
    plt.xlim(0.1, np.sqrt(lambda_0))
    plt.ylim(-15, 15)
    plt.legend()
    plt.show()


# Root equations (even/odd)
def even_equation(x: float) -> float:
    return np.tan(x) - f_rhs(x)

def odd_equation(x: float) -> float:
    # -cot(x) - f(x) = 0  ->  -(cos/sin) - f = 0  -> -1/tan - f = 0
    return (-1.0 / np.tan(x)) - f_rhs(x)


# Solve for roots (replace brackets with those identified from your plot)
def solve_eigenvalues() -> list[float]:
    # Returns a sorted list of dimensionless roots x.
    # Brackets should be chosen by inspection of plot_transcendental().
    roots: list[float] = []

    # Example brackets
    roots.append(optimize.bisect(even_equation, 1.0, 1.5))
    roots.append(optimize.bisect(odd_equation, 2.0, 3.0))
    roots.append(optimize.bisect(even_equation, 3.5, 4.5))

    roots.sort()
    return roots


def x_to_energy_eV(x: float, a: float) -> float:
    # Convert dimensionless root x -> energy in eV.
    # From x = (a/ħ)*sqrt(mE/2)  =>  E = 2(ħx/a)^2 / m
    E_J = 2.0 * (hbar * x / a)**2 / m_e
    return E_J / e

# Main execution (showcase flow)
def main() -> None:
    plot_potential(a, V0)
    plot_transcendental(lambda_0)

    roots = solve_eigenvalues()
    print("Dimensionless roots x:", [f"{r:.6f}" for r in roots])

    energies = [x_to_energy_eV(r, a) for r in roots]
    for i, E_eV in enumerate(energies, start=1):
        print(f"Eigenvalue {i}: E = {E_eV:.3f} eV")
    student.check()

main()
