"""
Intermediate Project 3: Landing the Rocket (90%)

Aim
---------------------------
Characterise a 2D rocket dynamics simulator and design thrust-control strategies to:
1) Identify thruster offsets, maximum effective thrust, and rocket mass.
2) Produce controlled horizontal motion profiles (e.g., accelerate → stop at a target).
3) Implement feedback controllers to stabilise motion about a moving target position.
4) Apply a controller to repeated “drop” scenarios and evaluate landing success.

Model assumptions
---------------------------
- The simulator advances the rocket state in discrete time steps (dt = 1/60 s).
- Left and right thrusters produce horizontal forces with:
  - an activation offset (below which no net acceleration occurs),
  - a maximum effective thrust
  - approximately linear mapping between effective force and acceleration: F = m a.

Workflow
---------------------------
A) Warm-up: apply test thrust sequences and inspect flight data.
B) Experiments: estimate offsets, mass, and maximum effective thrust.
C) Construct thrust-mapping utilities: acceleration -> commanded thrust.
D) Control tasks:
   1) Open-loop “there and stop” to a fixed target (100 m).
   2) Position feedback (undamped) and then damped feedback (with velocity term).
   3) Multi-flight drop test: track success rate against a moving platform.
"""
import numpy as np
import matplotlib.pyplot as plt
my_rocket = None  # The course simulator is loaded only for the original demo.

# Global plotting settings
plt.rcParams["font.size"] = 10
plt.rcParams["axes.formatter.useoffset"] = False

# Utility helpers
def finite_difference_velocity(t: np.ndarray, x: np.ndarray) -> np.ndarray:
    return np.diff(x) / np.diff(t)

def finite_difference_acceleration(t: np.ndarray, x: np.ndarray) -> np.ndarray:
    v = finite_difference_velocity(t, x)
    return np.diff(v) / np.diff(t)[1:]


# A) Warm-up: simple thrust sequence and basic diagnostics
def warmup_demo() -> None:
    Nmax = 300
    thrust = 2000.0

    my_rocket.reset("space")

    # Right thrust
    for _ in range(Nmax):
        my_rocket.advance(0.0, thrust)

    # Left thrust
    for _ in range(2 * Nmax):
        my_rocket.advance(thrust, 0.0)

    # Right thrust again
    for _ in range(Nmax):
        my_rocket.advance(0.0, thrust)

    track = my_rocket.get_flight_data()
    t = track[:, 0]
    x = track[:, 1]

    plt.figure(figsize=(15, 5))
    plt.plot(t, x)
    plt.title("Rocket coordinate: x(t)")
    plt.xlabel("Time [s]")
    plt.ylabel("x position [m]")
    plt.grid(True)
    plt.show()

    v = finite_difference_velocity(t, x)
    a = finite_difference_acceleration(t, x)

    plt.figure(figsize=(15, 5))
    plt.plot(t[1:], v, label="Velocity")
    plt.plot(t[2:], a, label="Acceleration")
    plt.title("Rocket horizontal velocity and acceleration")
    plt.xlabel("Time [s]")
    plt.ylabel("a.u.")
    plt.grid(True)
    plt.legend()
    plt.show()

# B) Experiments: offsets, mass, and maximum effective thrust
def experiment_offset_right_only() -> float:
    """Observe motion with only the right thruster on at constant thrust."""
    my_rocket.reset("space")
    Nmax = 1000
    thrust_left = 0.0
    thrust_right = 619.68  # measured minimum right thrust for acceleration

    for _ in range(Nmax):
        my_rocket.advance(thrust_left, thrust_right)

    track = my_rocket.get_flight_data()
    t = track[:, 0]
    x = track[:, 1]

    plt.figure(figsize=(20, 5))
    plt.plot(t, x)
    plt.xlabel("Time [s]")
    plt.ylabel("x position [m]")
    plt.grid(True)
    plt.show()

    print("max displacement:", float(np.max(np.abs(x))))
    return thrust_right


def experiment_mass_from_equal_thrust() -> float:
    """
    Apply equal thrust to both thrusters above offsets and infer mass from resulting acceleration.
    (Uses the same logic as your notebook; kept as-is.)
    """
    my_rocket.reset("space")

    F0_left = 774.38
    F0_right = 619.68

    thrust_left = 7000.0
    thrust_right = 7000.0

    Nmax = 500
    for _ in range(Nmax):
        my_rocket.advance(thrust_left, thrust_right)

    track = my_rocket.get_flight_data()
    t = track[:, 0]
    x = track[:, 1]

    v = finite_difference_velocity(t, x)
    a = finite_difference_acceleration(t, x)

    plt.figure(figsize=(20, 5))
    plt.plot(t, x)
    plt.xlabel("Time [s]")
    plt.ylabel("x position [m]")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(20, 5))
    plt.plot(t[1:], v)
    plt.grid(True)
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity")
    plt.show()

    plt.figure(figsize=(20, 5))
    plt.plot(t[2:], a)
    plt.grid(True)
    plt.xlabel("Time [s]")
    plt.ylabel("Acceleration")
    plt.show()

    acceleration = float(np.mean(a))
    resultant_force = (thrust_left - F0_left) - (thrust_right - F0_right)  # left positive
    mass = resultant_force / acceleration

    print("mass:", mass, "/ acceleration:", acceleration, "/ resultant force:", resultant_force)
    return mass


def experiment_acceleration_vs_thrust() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Scan thrust range to estimate saturation (Fmax) behaviour."""
    thrusts = np.arange(300.0, 10000.0, 10.0)

    acc_left = []
    for thrust in thrusts:
        my_rocket.reset("space")
        for _ in range(10):
            my_rocket.advance(thrust, 0.0)
        track = my_rocket.get_flight_data()
        t = track[:, 0]
        x = track[:, 1]
        a = finite_difference_acceleration(t, x)
        acc_left.append(float(np.mean(a)))

    acc_right = []
    for thrust in thrusts:
        my_rocket.reset("space")
        for _ in range(10):
            my_rocket.advance(0.0, thrust)
        track = my_rocket.get_flight_data()
        t = track[:, 0]
        x = track[:, 1]
        a = finite_difference_acceleration(t, x)
        acc_right.append(float(np.mean(a)))

    plt.figure(figsize=(20, 5))
    plt.plot(thrusts, acc_left)
    plt.ylabel("Acceleration [m/s^2]")
    plt.axvline(x=774.38, linestyle="--")
    plt.axvline(x=8980.0, linestyle="--")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(20, 5))
    plt.plot(thrusts, acc_right)
    plt.ylabel("Acceleration [m/s^2]")
    plt.axvline(x=619.68, linestyle="--")
    plt.axvline(x=8826.0, linestyle="--")
    plt.grid(True)
    plt.show()

    return thrusts, np.array(acc_left), np.array(acc_right)

# C) Identified parameters (from experiments)

o_left = 774.38
o_right = 619.68
m = 1784.0377
tmax = 8206


# D) Thrust mapping: acceleration -> commanded thrust

def acc2thrust_left(acceleration: np.ndarray | list[float]) -> np.ndarray:
    """
    Convert desired acceleration(s) to commanded LEFT thruster thrust.
    Returns commanded thrust (including offset).
    """
    acceleration = np.asarray(acceleration, dtype=float)
    out = np.empty_like(acceleration)

    a_max = tmax / m
    out[acceleration == 0] = o_left
    mask = (acceleration > 0) & (acceleration <= a_max)
    out[mask] = m * acceleration[mask] + o_left
    out[acceleration > a_max] = np.nan  # out-of-range indicator
    out[acceleration < 0] = np.nan
    return out


def acc2thrust_right(acceleration: np.ndarray | list[float]) -> np.ndarray:
    """
    Convert desired acceleration(s) to commanded RIGHT thruster thrust.
    Returns commanded thrust (including offset).
    """
    acceleration = np.asarray(acceleration, dtype=float)
    out = np.empty_like(acceleration)

    a_max = tmax / m
    out[acceleration == 0] = o_right
    mask = (acceleration > 0) & (acceleration <= a_max)
    out[mask] = m * acceleration[mask] + o_right
    out[acceleration > a_max] = np.nan
    out[acceleration < 0] = np.nan
    return out

# Extension task 1) Open-loop “there and stop”: accelerate → decelerate → hold

def there_and_stop(target_x: float = 100.0) -> None:
    my_rocket.reset("space")

    dt = 1.0 / 60.0
    a_cmd = 1.0  # m/s^2

    left_thrust = acc2thrust_left([a_cmd])[0]
    right_thrust = acc2thrust_right([a_cmd])[0]

    x = 0.0
    v = 0.0
    t = 0.0

    positions, velocities, times = [], [], []

    # 10 s accelerate
    for _ in range(int(10 / dt)):
        t += dt
        a_eff = (left_thrust - o_left) / m
        v += a_eff * dt
        x += v * dt
        times.append(t); velocities.append(v); positions.append(x)
        my_rocket.advance(left_thrust, 0.0)

    # 10 s decelerate
    for _ in range(int(10 / dt)):
        t += dt
        a_eff = -(right_thrust - o_right) / m
        v += a_eff * dt
        x += v * dt
        times.append(t); velocities.append(v); positions.append(x)
        my_rocket.advance(0.0, right_thrust)

    # 10 s hold
    for _ in range(int(10 / dt)):
        t += dt
        x += v * dt
        times.append(t); velocities.append(v); positions.append(x)
        my_rocket.advance(0.0, 0.0)

    positions = np.array(positions)
    velocities = np.array(velocities)
    times = np.array(times)

    print(f"Position: {positions[-1]:.15f} m")
    print(f"Velocity: {velocities[-1]:.15f} m/s")

    global student_track1
    student_track1 = my_rocket.get_flight_data()

    plt.figure(figsize=(20, 5))
    plt.plot(times, positions, label="Position [m]")
    plt.axhline(target_x, color="r", label=f"Target ({target_x} m)")
    plt.xlabel("Time [s]")
    plt.ylabel("Position [m]")
    plt.title("There-and-stop: position vs time")
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(20, 5))
    plt.plot(times, velocities, label="Velocity [m/s]")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.title("There-and-stop: velocity vs time")
    plt.grid(True)
    plt.legend()
    plt.show()


# Extension 2) Feedback controllers
def position_feedback(pos: float, target: float) -> tuple[float, float]:
    """Simple proportional controller: acceleration ∝ (target - position)."""
    gain = 0.02
    target_acc = gain * (target - pos)

    L = 0.0
    R = 0.0
    if target_acc > 0:
        L = acc2thrust_left([target_acc])[0]
    elif target_acc < 0:
        R = acc2thrust_right([-target_acc])[0]
    return L, R


def damped_feedback(pos: float, v: float, target: float) -> tuple[float, float]:
    """PD-style controller: acceleration from position error and velocity damping."""
    pos_gain = 0.15
    v_gain = 0.40

    target_acc = pos_gain * (target - pos) - v_gain * v

    a_max = tmax / m
    L = 0.0
    R = 0.0

    if target_acc > a_max:
        L = tmax + o_left
    elif target_acc > 0:
        L = acc2thrust_left([target_acc])[0]
    elif target_acc < -a_max:
        R = tmax + o_right
    elif target_acc < 0:
        R = acc2thrust_right([-target_acc])[0]

    return L, R


def run_position_feedback_demo(target: float = 100.0, steps: int = 3600) -> None:
    my_rocket.reset("space")

    dt = 1.0 / 60.0
    pos = 0.0
    v = 0.0

    positions, times = [], []

    for i in range(steps):
        times.append(i * dt)
        positions.append(pos)

        L, R = position_feedback(pos, target)
        my_rocket.advance(L, R)

        # approximate state update (kept consistent with your original approach)
        if L > 0:
            F = +(L - o_left)
        elif R > 0:
            F = -(R - o_right)
        else:
            F = 0.0

        a = F / m
        v += a * dt
        pos += v * dt

    global student_track2
    student_track2 = my_rocket.get_flight_data()

    plt.figure(figsize=(20, 5))
    plt.plot(times, positions)
    plt.axhline(target, color="r")
    plt.xlabel("Time [s]")
    plt.ylabel("Position [m]")
    plt.title("Position feedback (P-control)")
    plt.grid(True)
    plt.show()


def run_damped_feedback_demo(target: float = 100.0, steps: int = 10000) -> None:
    my_rocket.reset("space")

    dt = 1.0 / 60.0
    pos = 0.0
    v = 0.0

    positions, times = [], []

    for i in range(steps):
        times.append(i * dt)
        positions.append(pos)

        L, R = damped_feedback(pos, v, target)
        my_rocket.advance(L, R)

        if L > 0:
            F = +(L - o_left)
        elif R > 0:
            F = -(R - o_right)
        else:
            F = 0.0

        a = F / m
        v += a * dt
        pos += v * dt

    global student_track3
    student_track3 = my_rocket.get_flight_data()

    plt.figure(figsize=(20, 5))
    plt.plot(times, positions)
    plt.axhline(target, color="r")
    plt.xlabel("Time [s]")
    plt.ylabel("Position [m]")
    plt.title("Damped feedback (PD-style)")
    plt.grid(True)
    plt.show()

    print("final position is:", pos, "/ final velocity is:", v)

# Extension 3) Drop test: repeated flights and success counter

def drop_test(Nflights: int = 40) -> None:
    my_rocket.reset_flight_counter()

    dt = 1.0 / 60.0
    tracks = []

    for _ in range(Nflights):
        my_rocket.reset("drop")

        x, y = 100.0, 2000.0
        v_x, v_y = 0.0, 0.0
        prev_x, prev_y = x, y
        t = 0.0

        initial_target_x = my_rocket.get_platform_pos()[0]

        while y > 0 and t <= 25.0:
            target_x = my_rocket.get_platform_pos()[0]
            L, R = damped_feedback(x, v_x, target_x)

            data = my_rocket.advance(L, R)
            x_new, y_new = data[0], data[1]

            v_x = (x_new - prev_x) / dt
            v_y = (y_new - prev_y) / dt

            prev_x, prev_y = x_new, y_new
            x, y = x_new, y_new
            t += dt

        tracks.append(my_rocket.get_flight_data())

    data = tracks[-1]
    times = data[:, 0]
    x_pos = data[:, 1]
    y_pos = data[:, 2]
    final_target_x = my_rocket.get_platform_pos()[0]

    plt.figure(figsize=(20, 5))
    plt.plot(x_pos, y_pos, label="Flight Path")
    plt.axvline(x=initial_target_x, color="r", linestyle="--", label="Initial Target")
    plt.axvline(x=final_target_x, color="g", linestyle="--", label="Final Target")
    plt.axhline(y=0, color="k")
    plt.title("Rocket Flight Path (final flight)")
    plt.xlabel("Horizontal Position [m]")
    plt.ylabel("Vertical Position [m]")
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(20, 5))
    plt.plot(times, x_pos, label="Rocket Position")
    plt.axhline(y=initial_target_x, color="y", linestyle="--", label="Initial Target")
    plt.axhline(y=final_target_x, color="g", linestyle="--", label="Final Target")
    plt.title("Rocket Horizontal Position vs Time (final flight)")
    plt.xlabel("Time [s]")
    plt.ylabel("Horizontal Position [m]")
    plt.grid(True)
    plt.legend()
    plt.show()

    print("Successful landings:", my_rocket.successful_landing_counter)

def control_trace(rocket, *, target=100.0, duration_s=60.0, damped=True):
    """Record feedback from simulator measurements, rather than predicted motion.

    Columns are time (s), horizontal position (m), estimated velocity (m/s),
    and left/right thrust commands (N). The first row is the initial state.
    """
    if not np.isfinite([target, duration_s]).all() or duration_s <= 0:
        raise ValueError("Use a finite target and positive duration.")
    rocket.reset("space")
    dt = float(rocket.TIMESTEP)
    pos = float(rocket.get_init_pos()[0])
    velocity = 0.0
    rows = [[0.0, pos, velocity, 0.0, 0.0]]
    for i in range(round(duration_s / dt)):
        left, right = (damped_feedback(pos, velocity, target) if damped
                       else position_feedback(pos, target))
        if not np.isfinite([left, right]).all():
            raise ValueError("Requested thrust lies outside the identified range.")
        new_pos = float(rocket.advance(left, right)[0])
        velocity = (new_pos - pos) / dt
        pos = new_pos
        rows.append([(i + 1) * dt, pos, velocity, left, right])
        if not rocket.is_in_bounds():
            break
    return np.asarray(rows)


# Main (module_engine required)
def main(parameter_set: int = 0) -> None:
    global my_rocket
    try:
        from module_engine.assignment import Rocket
    except ImportError:
        raise SystemExit('The rocket exercise uses the university-supplied module_engine package.')
    my_rocket = Rocket(parameter_set)
    warmup_demo()
    experiment_offset_right_only()
    experiment_mass_from_equal_thrust()
    experiment_acceleration_vs_thrust()
    there_and_stop(target_x=100.0)
    run_position_feedback_demo(target=100.0, steps=3600)
    run_damped_feedback_demo(target=100.0, steps=10000)
    drop_test(Nflights=40)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="University rocket-control exercise")
    parser.add_argument("--parameter-set", type=int, default=0, help="Course parameter set; 0 uses default settings")
    main(parser.parse_args().parameter_set)
