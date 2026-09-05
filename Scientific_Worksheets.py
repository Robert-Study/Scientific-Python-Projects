"""Scientific Worksheets 1–6 (Merged Showcase)

This single file consolidates Worksheets 6 → 1 (most advanced first)
Data files are NOT included provided
"""

import math
import random
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = Path("data.txt")  # placeholder path for original notebooks

# Worksheet 6
def worksheet_6() -> None:
    rng = np.random.default_rng()

    trails = 1000000
    six_pairs = 0

    def dice_roll():                        #function that returns the result of a dice roll (random 1->6)
        return rng.integers(1,7)

    for i in range(trails):
        x1 = dice_roll()                    #using function generates 2 dice roll results and if both 6, add 1 count
        x2 = dice_roll()
        if x1 == 6 and x2 == 6:
            six_pairs += 1


    print("Observed Probability", six_pairs / trails)     #experimental probability = sucessful trials / total trials

    comparison = ((six_pairs/trails)-(1/36)) / (six_pairs/trails)
    #fractional comparison is the difference in probability / probability, where expected probability is 1/36

    print("Percentage difference =", abs(comparison*100) )

    # part a


    rng = np.random.default_rng()

    trails = 1000000
    results = []                    #two new variables, instead of six_pairs in question 1
    probabilities = []

    def dice_roll():
        return rng.integers(1,7)


    for i in range(trails):
        x1 = dice_roll()
        x2 = dice_roll()
        x3 = dice_roll()
        x4 = dice_roll()                                                             #up until now pretty much same as Q1
        dice_rolls = [x1,x2,x3,x4]
        dice_rolls.remove(min(dice_rolls))                                           #using array to remove lowest and find sum
        results.append(sum(dice_rolls))

    for i in range(3,19):
        count = results.count(i)              #counts how many of each number is 'totals'
        probability = count / trails          #converts to probability
        probabilities.append(probability)     #adds probability of the result being said number, into the array of probabilities

    print("Probability of getting the result 3 through 18 is:")
    print(probabilities)

    sum(probabilities) #checking purposes

    # part b


    rng = np.random.default_rng()
    trails = 1000000
    results = []                         #here we are using the density function so we can use results directly for the plot
    def dice_roll():
        return rng.integers(1,7)
    for i in range(trails):
        x1 = dice_roll()
        x2 = dice_roll()
        x3 = dice_roll()
        x4 = dice_roll()
        dice_rolls = [x1,x2,x3,x4]
        dice_rolls.remove(min(dice_rolls))    #mostly copied from part a until now, except we removed the probabilty parts
        results.append(sum(dice_rolls))            #as we can just use the density function instead with the results array

    plt.hist(results , bins=range(0,21), density=True)
    plt.title("Probability Distribution for dice game")
    plt.xlabel("Outcome")
    plt.ylabel("Probability")
    plt.xticks(range(0, 21))
    plt.grid(True)
    plt.show()

    #part a


    rng = np.random.default_rng()

    n = 10000
    N = 1+n               #to account for initial position (0)
    x = np.zeros(N)                      #I decided to use a numpy array to help with plotting
    for i in range(1, N):                #instead of appending to x I am replacing the 0's with it's new position
        step = rng.choice([-1,1])
        x[i] = x[i-1] + step
    print("position per step:", x) #array is too long to display when n=10000

    #part b


    rng = np.random.default_rng()
    n = 10000
    N = 1+n
    x = np.zeros(N)
    for i in range(1, N):
        step = rng.choice([-1,1])
        x[i] = x[i-1] + step            #copy pasted from part a


    plt.plot(range(N), x)
    plt.title('x-position against steps')
    plt.xlabel('Steps')
    plt.ylabel('x-pos')
    plt.grid(True)
    plt.show()

    #part c


    rng = np.random.default_rng()
    n = 10000
    N = 1+n
    x = np.zeros(N)
    mean_x = np.zeros(N)    #new variable
    for i in range(1, N):
        step = rng.choice([-1,1])
        x[i] = x[i-1] + step
        mean_x[i] = (mean_x[i - 1] * i + x[i]) / (i + 1)

    plt.plot(range(N), mean_x)
    plt.title('Mean x-pos against steps')
    plt.xlabel('Steps')
    plt.ylabel('x-pos')
    plt.grid(True)
    plt.show()


# Worksheet 5
def worksheet_5() -> None:
    mu1 = -np.pi                      #parameters
    mu2 = np.pi
    sigma = np.sqrt(2)

    x = np.linspace(-10, 10, 300)     #generates 300 x values, is a compromised amount between smoothness and loading time

    #calculates the PDF / probability density function for both values of mu
    pdf1 = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu1) / sigma) ** 2)
    pdf2 = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu2) / sigma) ** 2)

    plt.plot(x, pdf1)                      #the plot
    plt.plot(x, pdf2)
    plt.title('Normal Distributions')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.show()

    data = np.genfromtxt('data/yaletrigplx.dat') # store file as array or arrays

    apparent_magnitude = data[:, 1] #column 2 stored to array
    observed_BV_colour = data[:, 2]  #column 3 stored to array
    observed_parallax = data[:, 3]  #column 4 stored to array

    distance_parsecs = 1 / observed_parallax                                                            #array of distances
    absolute_magnitude = apparent_magnitude - 5 * (np.log10(distance_parsecs) - 1)                 #array of absolute magnitudes
    temperature = 4600 * (1/(0.92*observed_BV_colour + 1.7)+1/(0.92*observed_BV_colour + 0.62))        #array of temperatures
               #(i couldn't get the PyAstronomy package to work here so i used Ballesteros' formulae instead)


    plt.scatter(temperature, absolute_magnitude, s=0.1)         #plots diagram s=0.1 makes points small
    plt.title('Hertzsprung-Russell Diagram')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Absolute Magnitude')
    plt.gca().invert_yaxis()                                     #flips the axis so hottest at top, bluest at left
    plt.gca().invert_xaxis()
    plt.show()

    pos = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])
    q = 1  #(assuming that all charges are +1)

    r_i = np.array([0.25, 0.5]) #position of charge q_i

    force_x = 0.0
    force_y = 0.0

    for r_j in pos:
        r_ij = r_i - r_j                                                          #distance in charge in x and y
        r_ij_squared = np.sum(r_ij ** 2)                                          #distance squared
        force_x += (q**2 / (4 * np.pi * 8.854e-12)) * (r_ij[0] / r_ij_squared)
        force_y += (q**2 / (4 * np.pi * 8.854e-12)) * (r_ij[1] / r_ij_squared)


    print(f"Force on q_i at {r_i} is ({int(force_x)}i + {int(force_y)}j) N.")


    # part b

    x = np.linspace(-3, 3, 15)    # 15 points spanning between x of -3 and 3
    y = np.linspace(-3, 3, 15)    # same for points in y

    force_x = np.zeros((15, 15))  # initalizing a matrix for each point and it's x force value
    force_y = np.zeros((15, 15))  # same for force in y

    for i in range(15):
        for j in range(15):
            r_i = np.array([x[i], y[j]])    #all of this is similar to part a just using a matrix for 15x15 points rather than 1
            for r_j in pos:
                r_ij = r_i - r_j
                r_ij_squared = np.sum(r_ij ** 2)
                force_x[j, i] += (q ** 2 / (4 * np.pi * 8.854e-12)) * (r_ij[0] / r_ij_squared)
                force_y[j, i] += (q ** 2 / (4 * np.pi * 8.854e-12)) * (r_ij[1] / r_ij_squared)

    plt.quiver(x, y, force_x, force_y)         #quiver plot
    plt.title('Vector Field of Force due to square of point charges')
    plt.grid(True)                             #grid lines help to show that charges are at points (+-1, +-1)
    plt.show()


    #part c
    pos = np.array([[-1, -1], [1, 1]])

    x = np.linspace(-3, 3, 15)  #all the below code is the same as in part b
    y = np.linspace(-3, 3, 15)

    force_x = np.zeros((15, 15))
    force_y = np.zeros((15, 15))

    for i in range(15):
        for j in range(15):
            r_i = np.array([x[i], y[j]])
            for r_j in pos:
                r_ij = r_i - r_j
                r_ij_squared = np.sum(r_ij ** 2)
                force_x[j, i] += (q ** 2 / (4 * np.pi * 8.854e-12)) * (r_ij[0] / r_ij_squared)
                force_y[j, i] += (q ** 2 / (4 * np.pi * 8.854e-12)) * (r_ij[1] / r_ij_squared)

    plt.quiver(x, y, force_x, force_y)
    plt.title('Vector Field of Force due to Symmetric Charges')
    plt.grid(True)
    plt.show()


# Worksheet 4
def worksheet_4() -> None:
    def bisection_method(f, x1, x2, max_iterations, atol):                #function to find the roots of a function (part a)
        i = 0                                #iteration number
        while i < max_iterations:
            c = (x1 + x2) / 2

            if abs(f(c)) < atol:  # if within tolerance, return c as the root
                return c

            elif f(c) > 0 and f(x1) > 0:   # if a,c both positive
                x1 = c
            elif f(c) < 0 and f(x1) < 0:   # if a,c both negative
                x1 = c

            else:                          # if a,c different signs
                x2 = c

            i += 1

        return "No root found in", max_iterations, "iterations"

    def function(x):                                                         #the objective function (part b)

        return (x + 0.6) * (x - 1.73) * (x - np.pi)

    root1 = bisection_method(function, -2, 0, 1000, 1E-10)  # search window between -2 and 0
    root2 = bisection_method(function, 1, 2, 1000, 1E-10)   # search window between 1 and 2

    print("Root 1:", root1, "(to the nearest 1E-10)")
    print("Root 2: ", root2, "(to the nearest 1E-10)")

    X = [10, 1, 19, -7, 14, -3]

    min_val = min(X)
    max_val = max(X)

    X_normalized = []

    for x in X:
        range_ = max_val - min_val             #range_ is used as range is already a function in python
        difference = x - min_val
        X_normalized.append(difference/range_)

    print(X_normalized)

    X = [10, 1, 19, -7, 14, -3]

    min_val = float('+inf')   #sets minimum initially to a arbitrarily large number
    max_val = float('-inf')   #sets maximum initially to a arbitrarily small number

    for x in X:
        if x < min_val:       # replaces minimum with x if x is smaller
            min_val = x
        if x > max_val:       # replaces maximum with x if x is larger
            max_val = x


    X_normalized = []              #same as part a

    for x in X:
        range_ = max_val - min_val
        difference = x - min_val
        X_normalized.append(difference/range_)
    print(X_normalized)

    L = 100     #compromise (not too small to still give a good value, but not to large as to take too long)
    Madelung = 0
    for i in range(-L, L+1):
        for j in range(-L, L+1):
            for k in range(-L, L+1):       #loops through all 50 in i,j,k (50x50x50 iterations total)
                if i == j == k == 0:
                        continue          #sodium at 0,0,0 has 0 distance, so this atom is skipped to stop dividing by 0 error
                elif (i + j + k) % 2 == 0:
                    charge = 1.602e-19               #Na atoms (positive)
                else:
                    charge = -1.602e-19              #Cl atoms (negative)

                a = np.sqrt(i**2 + j**2 + k**2)
                V = charge / (4 * np.pi * 8.854e-12 * a)
                Madelung += V

    print(f"The Madelung constant for sodium chloride with L = {L} is approximately: {Madelung}")


# Worksheet 3
def worksheet_3() -> None:
    X = np.loadtxt("dice_rolls.txt", dtype=int)


    total_heads = 0                                                              #looping through all heads in file
    for toss in X[:, 0]:
        total_heads = total_heads + toss

    p_heads = total_heads / 10000                                                #calculating (prob/num) of (heads/tails)
    p_tails = 1-p_heads
    total_tails = 10000 * p_tails
    print("the probability of filling a head is:", p_heads, " /  for tails:", p_tails)

    red = np.zeros(6)                                                 #setting up arrays for the results from red/blue dice
    blue = np.zeros(6)

    i=0
    while i < 10000:
        if X[i, 0] == 0:                                                   #Tails
            red[(X[i, 1] - 1)] = red[(X[i, 1] - 1)] + 1                #adds result to red array

        elif X[i, 0] == 1:                                                 # Heads
            blue[(X[i, 1] - 1)] = blue[(X[i, 1] - 1)] + 1              #adds result to blue array
        i = i+1

    print("")
    print("value rolled:      1          2          3          4          5          6")
    print("red dice:    " , red/total_tails)
    print("blue dice:   ", blue/total_heads)

    A = int(input("enter A:  "))                                             #part (a) and part (b)
    Z = int(input("enter Z:  "))
    a_5 = [0,12,-12]

    if A%2 == 1:
        a_5 = a_5[0]         #A is odd
    elif A%2 == 0:
        if Z%2 == 0:
            a_5 = a_5[1]     #both even
        elif Z%2 == 1:
            a_5 = a_5[2]     #A even, Z odd


    B = 15.8*A - 18.3*(A**(2/3)) - 0.714*(Z**2)/(A**(1/3)) - 23.2*(A-2*Z)**2/A + a_5/(A**0.5)
    print("a).  B  =", B)
    print("b). B/A =", B/A)

    Z = int(input("enter Z value:   "))                                              #part (c)
    A = Z-1
    a_5 = [0,12,-12]
    B = []
    while A < 3*Z:
        A = A + 1
        if A%2 == 1:
            val_a_5 = a_5[0]         #A is odd
        elif A%2 == 0:
            if Z%2 == 0:
                val_a_5 = a_5[1]     #both even
            elif Z%2 == 1:
                val_a_5 = a_5[2]     #A even, Z odd
        B.append((15.8*A - 18.3*(A**(2/3)) - 0.714*(Z**2)/(A**(1/3)) - 23.2*(A-2*Z)**2/A + val_a_5/(A**0.5))/A)

    print("c). for Z =", Z , "the maximum binding energy per nucleon is at A =", Z+B.index(max(B)), "and is =", max(B), "MeV")

    Z = 0                                                 #part (d)
    a_5 = [0,12,-12]
    B_max = [0,0,0]
    while Z < 100:
        A = Z
        Z = Z + 1
        B = []
        while A < 3*Z:
            A = A + 1
            if A%2 == 1:
                val_a_5 = a_5[0]         #A is odd
            elif A%2 == 0:
                if Z%2 == 0:
                    val_a_5 = a_5[1]     #both even
                elif Z%2 == 1:
                    val_a_5 = a_5[2]     #A even, Z odd
            B.append((15.8*A - 18.3*(A**(2/3)) - 0.714*(Z**2)/(A**(1/3)) - 23.2*(A-2*Z)**2/A + val_a_5/(A**0.5))/A)
        A_max = Z+B.index(max(B))
        if max(B) > B_max[0]:
            B_max[0] = max(B)
            B_max[1] = Z
            B_max[2] = A_max
        print("for Z =", Z , "the maximum binding energy per nucleon is at A =", A_max, "and is =", max(B), "MeV")
    print("Maximum binding energy per nucleon is,",B_max[0], "MeV when Z =", B_max[1], "/ A =", B_max[2])



# Worksheet 2
def worksheet_2() -> None:
    print("n     fn")
    n = 0
    fn = 0
    fns1 = 1

    while n<20:
        n=n+1
        fns2 = fns1
        fns1 = fn
        fn = fns1 + fns2
        print(n, "   ",fn)

                                #question b
    n = 0
    fn = 0
    fns1 = 1
    total = 0
    while n<40:
        n=n+1
        fns2 = fns1
        fns1 = fn
        fn = fns1 + fns2
    print("golden ratio estimate =", fn/fns1)
    print("golden ratio real val =", (1+5**0.5)/2)
    print("difference is negilible")

    n = -1                                    #part a
    e_x = 0
    while n<10:
        n=n+1
        e_x = e_x + x**n/math.factorial(n)
    print("a).", e_x)


    e_real = math.exp(0.5)                    #part b
    print("b).", e_real)


    print("c).", abs((e_x-e_real)/e_real))    #part c


    x = 0.5                                   #part d
    n = 0
    e_x = 0
    while abs((e_x-e_real)/e_real)>0.01:
        e_x = e_x + x**n/math.factorial(n)
        n=n+1
    print("d). N =", n)

    T = input("Was the particle detected in the tracking chamber? (y/n):     ")
    E = input("Was the particle detected in the E/M calorimeter? (y/n):      ")
    H = input("Was the particle detected in the hadronic calorimeter? (y/n): ")
    M = input("Was the particle detected in the muon detector? (y/n):        ")
    if T == "y":
        if M == "y":
            x = "a muon"
        elif H == "y":
            x = "a proton/pion"
        elif E == "y":
            x = "an electron"
        else:
            x = "an unknown particle"
    elif T == "n":
        if E == "y":
            x = "a photon"
        elif H == "y":
            x = "a neutron/lambda"
        elif M == "n":
            x = "a neutrino"
        else:
            x = "an unknown particle"
    print("the particle is:" , x)



# =============================================================================
# Worksheet 1
# =============================================================================

def worksheet_1() -> None:
    result1 = 2 * np.pi
    result2 = np.pi / 2
    result3 = np.pi ** 2
    result4 = np.sqrt(np.pi)
    result5 = (1j)**2
    result6 = np.sqrt(-1+0j)
    result7 = np.log(2)
    result8 = np.log10(100)
    result9 = (np.sin(np.pi/4) + np.cos(np.pi/4))**2
    result10 = np.exp(1j * np.pi) + 1

    print("Result 1: ", result1)
    print("Result 2: ", result2)
    print("Result 3: ", result3)
    print("Result 4: ", result4)
    print("Result 5: ", result5)
    print("Result 6: ", result6)
    print("Result 7: ", result7)
    print("Result 8: ", result8)
    print("Result 9: ", result9)
    print("Result 10: ", result10)

    m = 1  # mass in kg
    v = 1e8  # velocity in m/s
    c = 3e8  # speed of light in m/s

    E = m * c**2 / np.sqrt(1 - (v**2 / c**2))

    print("Total energy:", E)

    a = 5
    b = 29
    c = 2

    delta = b**2 - 4*a*c

    root1 = (-b + np.sqrt(delta)) / (2*a)
    root2 = (-b - np.sqrt(delta)) / (2*a)

    print("Root 1:", root1)
    print("Root 2:", root2)

    result1 = a * root1**2 + b * root1 + c
    result2 = a * root2**2 + b * root2 + c

    print("subbing root 1 back in:", result1, " ~ 0")
    print("subbing root 2 back in:", result2, " ~ 0")
