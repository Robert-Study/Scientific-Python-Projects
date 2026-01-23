"""
Intermediate Project 1: Electron in a Finite Square Well (95%)

Showcase-only source converted from a Jupyter notebook.
Any student ID fields have been intentionally left blank.

NOTE: This code references the course-provided `module_engine` package in places.
The repository does not include `module_engine` (academic integrity / plagiarism prevention).
"""

from __future__ import annotations

from module_engine.assignment import Assignment1
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
import scipy.optimize as optimize


# Enter your student ID here:
studentID = ""  # intentionally left blank for showcase

# Do not alter any of the code within this cell other than the value of studentID above

student = Assignment1(studentID)
a, V0 = student.get_parameters()

x = np.linspace(-a, a, num=1000)
# Each point of x is mapped to V0 if abs(x) >= a / 2 and 0 otherwise
potential_array = np.piecewise(x, [abs(x) >= a / 2, abs(x) < a / 2],[V0, 0])
plt.title('The Finite Square Well Potential')
plt.xlabel(r'$x / m$')
plt.ylabel(r'$V(x) / eV$')
# np.amin and np.amax return the maximum and minimum values of an array respectively
plt.axis([np.amin(x), np.amax(x), 0, 4/3*np.amax(potential_array)])
plt.plot(x, potential_array)
plt.show()

# Import the necessary constants from scipy.constants module

e = constants.e # Elementary Charge
hbar = constants.hbar # Reduced Planck's constant
m = constants.m_e # Electron mass

# Do not alter this constant below (note the conversion of eV to Joules)
lambda_0 = (m*(a**2)*V0*e)/(2*constants.hbar**2)


# Write your rhs function here

def rhs(x):
    y = np.sqrt(lambda_0 - x**2) / x
    return y

x = np.array([np.sqrt(lambda_0/2),np.sqrt(lambda_0/5)])
print(rhs(x))

# Creating the figure to be marked
student_figure = plt.figure(figsize=(10,6))
# You can now just add to and change this object by using plt.xxx function as usual.
# Do **not** use the 'figure' command again in this task.
# The marking script will only mark the object called 'student_figure'.
# Do **not** add extra lines or traces to the plot

# Add your code to plot onto student_figure here


x = np.linspace(0.1, np.sqrt(lambda_0), 1000, endpoint=False)

neg_cot_x = -1 / np.tan(x)   # functions
f_x = rhs(x)
tan_x = np.tan(x)

plt.plot(x, tan_x, label='tan(x)', color='red')
plt.plot(x, neg_cot_x, label='-cot(x)', color='blue')
plt.plot(x, f_x, label='f(x)', color='green')

plt.title("Graphs for: tan(x)   -cot(x)   f(x)")
plt.xlabel(r'$x$')
plt.ylabel(r'Val')
plt.legend()
plt.ylim(-15, 15)
plt.xlim(0.1, np.sqrt(lambda_0))

# Show the plot
plt.show()

# Write the two required functions here

def even_equation(x):
    return np.tan(x) - np.sqrt(lambda_0 - x**2) / x

def odd_equation(x):
    return 1/np.tan(x) + np.sqrt(lambda_0 - x**2) / x

# Append your solutions to this list, which should be sorted in ascending order
solution_list = []

even_1 = optimize.bisect(even_equation, 1, 1.5)           #even solution between 1 and 1.5
odd_1 = optimize.bisect(odd_equation, 2, 3)                 #odd solution between 2 and 3
even_2 = optimize.bisect(even_equation, 3.5, 4.5)           #even solution between 3.5 and 4.5

solution_list.append(even_1)
solution_list.append(odd_1)
solution_list.append(even_2)
solution_list.sort()
print(solution_list)

def find_energy(solution_list):
    energies = []
    for x in solution_list:
        J_energy = (x**2 * hbar**2 * np.pi**2) / (2 * m * a**2)
        eV_energy = J_energy / e
        energies.append(f"{eV_energy:.3f}")
    return energies

energy_solutions = find_energy(solution_list)

for i, energy in enumerate(energy_solutions):
    print('Energy eigenvalue {} is E = {} eV'.format(i, energy))

student.check()
