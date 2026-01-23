"""
Intermediate Project 3: Landing the Rocket (90%)

Showcase-only source converted from a Jupyter notebook.
Any student ID fields have been intentionally left blank.

NOTE: This code references the course-provided `module_engine` package in places.
The repository does not include `module_engine` (academic integrity / plagiarism prevention).
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from module_engine.assignment import Rocket


# Do not alter any of the code within this cell other than the value of studentID


# Setting global plotting settings
plt.rcParams['font.size'] = 20
plt.rcParams['axes.formatter.useoffset'] = False

# Enter your student ID here
studentID = ""  # intentionally left blank for showcase

# Your Rocket object to be used throughout this assignment
# Please do NOT change the line below! Your studentID must be inserted ABOVE
my_rocket = Rocket(studentID)

N = 0           # Step counter
Nmax = 300      # Number of tracking steps of 1/60 s duration
thrust = 2000.0 # A random test thrust

my_rocket.reset('space')
# Apply right thrust for a while
while N<Nmax:
    N+=1
    pos = my_rocket.advance(0.0,thrust)
# Now apply left thrust
N=0
while N<2*Nmax:
    N+=1
    pos = my_rocket.advance(thrust,0.0)
# Apply right thrust again
N=0
while N<Nmax:
    N+=1
    pos = my_rocket.advance(0.0,thrust)

track = my_rocket.get_flight_data()

t=track[:,0]
x=track[:,1]
y=track[:,2]
# Plot the x-position as a function of time
fig = plt.figure(figsize=(15,5))
ax = plt.plot(t, x, 'b-')
plt.title('Rocket coordinate: x(t)')
plt.xlabel('Time [s]')
plt.ylabel('x position [m]')
plt.grid()
plt.show()

# Compute the speed and acceleration of our rocket
v = np.diff(x)/np.diff(t)
a = np.diff(v)/np.diff(t)[1:]

fig = plt.figure(figsize=(15,5))
# Plot velocity and acceleration as a function of time
plt.plot(t[1:],v, 'b-', label='Velocity')
plt.plot(t[2:],a, 'r-', label='Acceleration')
plt.title('Rocket horizontal velocity and acceleration')
plt.xlabel('Time [s]')
plt.ylabel('a.u.')
plt.grid()
plt.legend()
plt.show()

# Experiment 1 - Observing motion with only one thruster on (right) at constant thrust output
# Right: min thrust 619.68 -> accel; Left: min below 774.38 -> accel

my_rocket.reset('space')
Nmax = 1000
N = 0
thrust_left = 0
thrust_right = 619.68  # min right thrust for accel


while N < Nmax:
    N += 1
    pos = my_rocket.advance(thrust_left, thrust_right)

track = my_rocket.get_flight_data()  # (t,x,y)

x = track[:, 1]
y = track[:, 2]
t = track[:, 0]


plt.figure(figsize=(20, 5))
plt.plot(t, x)
plt.xlabel('Time')
plt.ylabel('x-pos')
plt.show()

v = np.diff(x) / np.diff(t)
a = np.diff(v) / np.diff(t)[1:]

print("max displacement:", max(abs(x)))
# i tried 'print(max(abs(x)))' for F(max), but it was imprecise
# max abs(x) is 649.432m at max thrust (F(max))
# Left max at 8980N, right max at 8826N, F(max) = 8206N

# Experiment 2 - Equal thrust applied to both thrusters to get accerlation and mass

my_rocket.reset('space')
F0_left = 774.38  # Offset for left thruster
F0_right = 619.68  # Offset for right thruster
N = 0
Nmax = 500
thrust_left = thrust_right = 7000 #setting to any value above offsets but below F(max) gives same acceleration

#-------

while N < Nmax:
    N += 1
    pos = my_rocket.advance(thrust_left, thrust_right)  # Both thrusters active
track = my_rocket.get_flight_data()  # Data in form (t, x, y)

t = track[:, 0]
x = track[:, 1]
y = track[:, 2]

plt.figure(figsize=(20, 5))
plt.plot(t, x)
plt.xlabel('Time')
plt.ylabel('x-pos')
plt.grid()
plt.show()

v = np.diff(x) / np.diff(t)
a = np.diff(v) / np.diff(t)[1:]

plt.figure(figsize=(20, 5))
plt.plot(t[1:], v)
plt.grid()
plt.xlabel('Time')
plt.ylabel('Velocity')
plt.show()

plt.figure(figsize=(20, 5))
plt.plot(t[2:], a)
plt.grid()
plt.xlabel('Time')
plt.ylabel('Acceleration')
plt.show()

acceleration = np.mean(a)
resultant_force = (thrust_left - F0_left) - (thrust_right - F0_right)  #with left as positive
mass = resultant_force / acceleration

print("mass:",mass," / acceleration:", acceleration," / resultant force:", resultant_force)

# Experiment 3 - Acceleration vs thrust to get Fmax for both thrusters
thrusts= np.arange(300, 10000, 10)  # Test thrust values through range   # 300,10000 by 10 incremental

accelerations_left = []
for thrust in thrusts:
    my_rocket.reset('space')
    N = 0
    Nmax = 10
    while N < Nmax:
        N += 1
        my_rocket.advance(thrust, 0)
    track = my_rocket.get_flight_data()
    t = track[:, 0]
    x = track[:, 1]
    v = np.diff(x) / np.diff(t)
    a = np.diff(v) / np.diff(t)[1:]
    accelerations_left.append(np.mean(a))

accelerations_right = []
for thrust in thrusts:
    my_rocket.reset('space')
    N = 0
    Nmax = 10
    while N < Nmax:
        N += 1
        my_rocket.advance(0, thrust)
    track = my_rocket.get_flight_data()
    t = track[:, 0]
    x = track[:, 1]
    v = np.diff(x) / np.diff(t)
    a = np.diff(v) / np.diff(t)[1:]
    accelerations_right.append(np.mean(a))

plt.figure(figsize=(20, 5))
plt.plot(thrusts, accelerations_left)
plt.ylabel('Acceleration m/s2')
plt.axvline(x=774.38, linestyle='--')
plt.axvline(x=8980, linestyle='--')
plt.grid()
plt.show()
print("The portion where thrust is being applied is 8980 - 774:", 8980-774)

plt.figure(figsize=(20, 5))
plt.plot(thrusts, accelerations_right)
plt.ylabel('Acceleration m/s2')
plt.grid()
plt.axvline(x=619.68)
plt.axvline(x=8826)
plt.show()
print("The maximum effective thrust is 8826 - 620:", 8826-620)
print("Hence Fmax = 8206")
print("Fmax/m =", 8206/1784, "  /  max acceleration for left thruster only:", max(accelerations_left), "  /  right:", min(accelerations_right))

# Enter the results from your experiments into the variables below
# You may type the numerical values with the requested accuracy
# or you can assign these variables to another variable computed above
# Do not change the names of the variables, and do not reuse these variables later

o_left = 774.38
o_right = 619.68
m = 1784.0377
tmax = 8206

#thrust -> acceleration
def acc2thrust_left(acceleration):
    F0_left = 774.38  # Offset for left thruster
    Fmax = 8206         # Maximum achievable thrust
    m = 1784.0377     # Mass of the rocket

    # List to store the thrust values for each acceleration
    thrust = []
    for a in acceleration:
        if a == 0:
            thrust.append(F0_left)
        elif a <= (Fmax) / m:
            thrust.append(m * a + F0_left)
        else:
            thrust.append(None) #acceleration shouldn't be able to exceed 4.59, returns None to help with bugfixing

    return np.array(thrust) #returns thrust inputed to the thruster not the effective output thrust

def acc2thrust_right(acceleration):                  #copy and pasted just changed the numbers
    F0_right = 619.68  # Offset for right thruster
    Fmax = 8206        # Maximum achievable thrust
    m = 1784.0377        # Mass of the rocket

    # List to store the thrust values for each acceleration
    thrust = []
    for a in acceleration:
        if a == 0:
            thrust.append(F0_right)
        elif a <= (Fmax) / m:
            thrust.append(m * a + F0_right)
        else:
            thrust.append(None)

    return np.array(thrust)

#testing the above functions
accelerations = np.linspace(0, 5, 10000)

thrusts_left = acc2thrust_left(accelerations)
thrusts_right = acc2thrust_right(accelerations)

#####

thrusts = range(0, 10000, 10)

accelerations_left = []
for thrust in thrusts:
    my_rocket.reset('space')
    N = 0
    Nmax = 10
    while N < Nmax:
        N += 1
        my_rocket.advance(thrust, 0)
    track = my_rocket.get_flight_data()


    t = track[:, 0]
    x = track[:, 1]
    v = np.diff(x) / np.diff(t)
    a = np.diff(v) / np.diff(t)[1:]
    accelerations_left.append(np.mean(a))

accelerations_right = []
for thrust in thrusts:
    my_rocket.reset('space')
    N = 0
    Nmax = 10
    while N < Nmax:
        N += 1
        my_rocket.advance(0, thrust)
    track = my_rocket.get_flight_data()


    t = track[:, 0]
    x = track[:, 1]
    v = np.diff(x) / np.diff(t)
    a = np.diff(v) / np.diff(t)[1:]
    accelerations_right.append(np.mean(a))
accelerations_right = [abs(x) for x in accelerations_right]


#####


plt.figure(figsize=(20, 5))
plt.plot(thrusts_left, accelerations)
plt.scatter(thrusts_left, accelerations)
plt.ylabel("Acceleration")
plt.axvline(x=774.38, linestyle='--')
plt.axvline(x=8980, linestyle='--')
plt.xlim(0, 10000)
plt.ylim(-0.5, 5)
plt.grid()
plt.show()

plt.figure(figsize=(20, 5))
plt.plot(thrusts_right, accelerations)
plt.scatter(thrusts_right, accelerations)
plt.ylabel("Acceleration")
plt.xlim(0, 10000)
plt.ylim(-0.5, 5)
plt.axvline(x=619.68)
plt.axvline(x=8826)
plt.show()


######


plt.figure(figsize=(20, 5))
plt.plot(thrusts, accelerations_left)
plt.scatter(thrusts, accelerations_left)
plt.axvline(x=774.38, linestyle='--')
plt.axvline(x=8980, linestyle='--')
plt.ylabel('Acceleration')
plt.xlim(0, 10000)
plt.ylim(-0.5, 5)
plt.grid()
plt.show()

plt.figure(figsize=(20, 5))
plt.plot(thrusts, accelerations_right)
plt.scatter(thrusts, accelerations_right)
plt.ylabel('Acceleration')
plt.xlim(0, 10000)
plt.ylim(-0.5, 5)
plt.axvline(x=619.68)
plt.axvline(x=8826)
plt.show()

# Your code for 'there and stop' / Accelerate to 100 m, then decelerate to stop
my_rocket.reset('space')
F0_right = 619.68
F0_left = 774.38
m = 1784.0377
Fmax = 8206
total_time = 30
dt = 1 / 60  #applies for this long so setting it to increment
left_thrust = acc2thrust_left([1])[0]    #thrust in left booster to produce 1m/s^2 of acceleration
right_thrust = acc2thrust_right([1])[0]    #thrust in right booster to produce 1m/s^2 of decceleration


deceleration_thrust = -acc2thrust_right([1])

x = 0 #initial constraints
v = 0
t = 0

positions = []
times = []
velocities = []

for i in range(10 * 60): #10s of acceleration
    t += dt
    A_l = (left_thrust - F0_left) / m  #alternatively you can just use 1 here instead of using thrust input
    v += A_l * dt
    x += v * dt
    times.append(t)
    velocities.append(v)
    positions.append(x)
    my_rocket.advance(left_thrust, 0)

for i in range(10 * 60): #10s of decceleration
    t += dt
    a_right = -(right_thrust - F0_right) / m  #negative as right booster acts in opposite direction
    v += a_right * dt
    x += v * dt
    times.append(t)
    positions.append(x)
    velocities.append(v)
    my_rocket.advance(0,right_thrust)


for i in range(10 * 60): #10s stationairy
    t += dt
    acceleration = 0
    v += acceleration * dt
    x += v * dt
    positions.append(x)
    velocities.append(v)
    times.append(t)
    my_rocket.advance(0,0)

positions = np.array(positions)
velocities = np.array(velocities)
times = np.array(times)

final_velocity = velocities[-1]
final_position = positions[-1]


print(f"Position: {final_position:.15f} m")
print(f"Velocity: {final_velocity:.15f} m/s")

# The following records the track data to be marked.
# Make sure you call reset() before, but not during or after your flight!
student_track1 = my_rocket.get_flight_data()

# Cell for plotting the track to check results
plt.figure(figsize=(20, 5))
plt.plot(times, positions, label='Position m')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Rocket Position vs Time')
plt.grid()
plt.axhline(100, color='r', label='Target Position (100m)')
plt.show()

plt.figure(figsize=(20, 5))
plt.title('Rocket Velocity vs Time')
plt.plot(times, velocities, label='Velocity m/s')
plt.xlabel('Time s')
plt.ylabel('Velocity m/s')
plt.grid()
plt.show()

# Student code for position-based feedback,
# do *not* change the name or arguments of the function.
def position_feedback(pos, target):
    gain = 0.02               #to scale (don't go too much higher or else thrust > Fmax)
    target_acceleration = gain * (target - pos)
    L = R = 0

    if target_acceleration > 0:
        L = acc2thrust_left([target_acceleration])[0] #acceleration converted to thrust

    elif target_acceleration < 0:
        R = acc2thrust_right([-target_acceleration])[0] #returns a positive thrust due to -

    return L, R  #this is raw thrust not effective output

# Student code for creating flight path with an oscillation around target
my_rocket.reset("space")

pos = 0
target = 100
max_i = 3600
i = 0
t_step = 1/60
velocity = 0
acceleration = 0

positions = []
time = []


while i < max_i:
    time.append(i * t_step)
    positions.append(pos)
    left_thrust, right_thrust = position_feedback(pos, target)

    my_rocket.advance(left_thrust, right_thrust)
    if left_thrust > 0:
        effective_force = +(left_thrust - 774.38) #accounting for offsets
    elif right_thrust > 0:
        effective_force = -(right_thrust - 619.68) #negative as right acts leftwards

    acceleration = effective_force / 1784.0377   #F=ma
    velocity += acceleration * t_step
    pos += velocity * t_step  # Update position assuming constant velocity in the small time step
    i += 1

# The following records the track data to be marked, Make sure
# that you do not call `reset()` during or after your flight!
student_track2 = my_rocket.get_flight_data()

plt.figure(figsize=(20, 5))
plt.plot(time, positions)
plt.xlabel('Time (s)')
plt.ylabel('Position in m')
plt.title('Position vs Time')
plt.axhline(100, color='r')
plt.show()

def damped_feedback(pos, v, target):   #note i added in the constraint where if acceleration tries to exceed maximum then
    v_gain = 0.08                   #it limits the output to the max thrust
    pos_gain = 0.15

    target_acceleration = pos_gain * (target - pos) - v_gain * v
    L = R = 0

    if target_acceleration > 4.599316: #max a
        L = 8206 + 774  #Fmax + offset
    elif target_acceleration > 0:
        L = acc2thrust_left([target_acceleration])[0]
    elif target_acceleration < -4.599316:
        R = 8206 + 619 #Fmax + offset
    elif target_acceleration < 0:
        R = acc2thrust_right([-target_acceleration])[0] #returns positive value as that is needed for .advance()

    return L,R    #doesn't account for offsets

# Student code to create flight track with damped oscillation

my_rocket.reset("space")
pos = 0
velocity = 0
acceleration = 0
target = 100
max_i = 10000
i = 0
t_step = 1 / 60
positions = []
time = []

while i < max_i:
    positions.append(pos)
    time.append(i * t_step)
    left_thrust, right_thrust = damped_feedback(pos, velocity, target)
    my_rocket.advance(left_thrust, right_thrust)

    if left_thrust > 0:
        effective_force = +(left_thrust - 774.38) #account for offsets here
    elif right_thrust > 0:
        effective_force = -(right_thrust - 619.68) #offsets and set to negative as right thruster

    acceleration = effective_force / 1784.0377
    velocity += acceleration * t_step
    pos += velocity * t_step  #(small t_steps so can assume velocity is constant)
    i += 1

# The following records the track data to be marked, Make sure
# that you do not call `reset()` during or after your flight!
student_track3 = my_rocket.get_flight_data()

plt.figure(figsize=(20, 5))
plt.plot(time, positions)
plt.axhline(100, color='r')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Position vs Time')
plt.grid()
plt.show()

print("final position is:", pos, "  /  final velocity is:", velocity)

def acc2thrust_left(acceleration):                   #all functions copy and pasted from earlier for sake of convenience
    F0_left = 774.38  # Offset for left thruster
    Fmax = 8206         # Maximum achievable thrust
    m = 1784.0377      # Mass of the rocket

    # List to store the thrust values for each acceleration
    thrust = []
    for a in acceleration:
        if a == 0:
            thrust.append(F0_left)
        elif a <= (Fmax) / m:
            thrust.append(m * a + F0_left)
        else:
            thrust.append(None) #acceleration shouldn't be able to exceed 4.59, returns None to help with bugfixing

    return np.array(thrust) #returns thrust inputed to the thruster not the effective output thrust

def acc2thrust_right(acceleration):
    F0_right = 619.68  # Offset for right thruster
    Fmax = 8206        # Maximum achievable thrust
    m = 1784.0377        # Mass of the rocket

    # List to store the thrust values for each acceleration
    thrust = []
    for a in acceleration:
        if a == 0:
            thrust.append(F0_right)
        elif a <= (Fmax) / m:
            thrust.append(m * a + F0_right)
        else:
            thrust.append(None)

    return np.array(thrust)

def damped_feedback(pos, v, target):
    pos_gain = 0.15
    v_gain = 0.40
    target_acceleration = pos_gain * (target - pos) - v_gain * v
    L = R = 0

    if target_acceleration > 4.599316: #max a
        L = 8206 + 774          #max Thrust for L
    elif target_acceleration > 0:
        L = acc2thrust_left([target_acceleration])[0]
    elif target_acceleration < -4.599316:
        R = 8206 + 619
    elif target_acceleration < 0:
        R = acc2thrust_right([-target_acceleration])[0]

    return L,R

my_rocket.reset_flight_counter()
Nflights = 40
tracks = []
N = 0
dt = 1 / 60

while N < Nflights:
    my_rocket.reset('drop')
    x, y = 100, 2000
    v_x, v_y, t = 0, 0, 0
    prev_x, prev_y = x, y
    initial_target_x = my_rocket.get_platform_pos()[0]

    while y > 0 and t <= 25:  # Exit if y <= 0 or t exceeds 25 seconds
        target_x = my_rocket.get_platform_pos()[0]
        left_thrust, right_thrust = damped_feedback(x, v_x, target_x)
        data = my_rocket.advance(left_thrust, right_thrust)
        v_x = (x - prev_x) / dt
        v_y = (y - prev_y) / dt
        prev_x, prev_y = x, y
        x, y = data[0], data[1]
        t += dt  # Increment time

    tracks.append(my_rocket.get_flight_data())
    N += 1

data = tracks[-1]
times = data[:, 0]
x_pos = data[:, 1]
y_pos = data[:, 2]
final_target_x = my_rocket.get_platform_pos()[0]


#some graphs to help visualise the rocket coming into landing (first shows x-y, second shows t-x both useful)

plt.figure(figsize=(20, 5))
plt.plot(x_pos, y_pos, label='Flight Path', color='b')
plt.axvline(x=initial_target_x, color='r', linestyle='--', label="Initial Target")
plt.axvline(x=final_target_x, color='g', linestyle='--', label="Final Target")
plt.axhline(y=0, color='k', linestyle='-')
plt.title("Rocket Flight Path")
plt.xlabel("Horizontal Position (m)")
plt.ylabel("Vertical Position (m)")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(20, 5))
plt.plot(times, x_pos, label="Rocket Position", color='r')
plt.axhline(y=initial_target_x, color='y', linestyle='--', label="Initial Target")
plt.axhline(y=final_target_x, color='g', linestyle='--', label="Final Target")
plt.title("Rocket Position vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Horizontal Position (m)")
plt.legend()
plt.grid(True)
plt.show()

# Check how many flights succeeded:
print(my_rocket.successful_landing_counter)
