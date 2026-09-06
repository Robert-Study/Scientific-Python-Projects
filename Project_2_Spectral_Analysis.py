"""
Intermediate Project 2: Spectral Analysis of Digital Signals (80%)

Aim
---------------------------
Use Fourier analysis (FFT) to investigate the frequency content of digital audio signals
and identify the behaviour of unknown “box” filters (e.g., RC/RL/RLC). Apply a frequency-
domain transfer function to reduce noise and improve signal-to-noise ratio (SNR).

Theory
---------------------------
1) A sampled time-domain signal x(t) can be transformed into the frequency domain X(f)
   using the Fast Fourier Transform (FFT).
2) Filters can be expressed via a transfer function T(f), so that:
        Y(f) = X(f) · T(f)
   and the filtered time-domain signal is recovered via inverse FFT.

Execution
---------------------------
A) Generate a swept-sine input and inspect it in time and frequency.
B) Pass the swept-sine through a chosen box filter and compare spectra.
C) Analyse a recorded signal spectrum, locate noise peaks, and apply a custom frequency-
   domain filter (R, L, C, order N) repeatedly to suppress noise and improve SNR.
"""

import numpy as np
import matplotlib.pyplot as plt


# Signal generation

def generate_swept_sine(
    duration_s: float,
    sampling_rate_hz: int,
    f_min_hz: float = 10.0,
    f_max_hz: float = 4000.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate a swept-sine test signal where frequency increases linearly
    from f_min to f_max over the given duration.
    """
    if not all(np.isfinite(v) for v in [duration_s, sampling_rate_hz, f_min_hz, f_max_hz]):
        raise ValueError('Signal parameters must be finite.')
    if duration_s <= 0 or sampling_rate_hz <= 0 or not 0 <= f_min_hz < f_max_hz < sampling_rate_hz / 2:
        raise ValueError('Use a positive duration/rate and 0 <= f_min < f_max < Nyquist.')
    n = int(duration_s * sampling_rate_hz)
    if n < 2:
        raise ValueError('At least two samples are required.')
    times = np.linspace(0.0, duration_s, n, endpoint=False)
    sweep_rate = (f_max_hz - f_min_hz) / duration_s
    frequencies = f_min_hz + sweep_rate * times
    phase = 2.0 * np.pi * (f_min_hz * times + 0.5 * sweep_rate * times**2)
    signal = np.sin(phase)
    return times, frequencies, signal

# Plotting utilities

def plot_time_series(times: np.ndarray, signal: np.ndarray, title: str) -> None:
    plt.figure(figsize=(15, 3))
    plt.plot(times, signal)
    plt.title(title)
    plt.xlabel("t [s]")
    plt.ylabel("Amplitude")
    plt.xlim(times[0], times[-1])
    plt.grid(True)
    plt.show()


def plot_signal_vs_frequency(frequencies: np.ndarray, signal: np.ndarray, title: str) -> None:
    plt.figure(figsize=(15, 3))
    plt.plot(frequencies, signal)
    plt.title(title)
    plt.xlabel("f [Hz]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

# Spectral analysis utilities

def magnitude_spectrum(signal: np.ndarray, sampling_rate_hz: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the one-sided magnitude spectrum of a real-valued time signal.
    Returns (freqs>=0, |FFT|).
    """
    signal = np.asarray(signal, float)
    if signal.ndim != 1 or len(signal) < 2 or sampling_rate_hz <= 0:
        raise ValueError('Provide a real 1D signal and positive sampling rate.')
    return np.fft.rfftfreq(len(signal), d=1.0 / sampling_rate_hz), np.abs(np.fft.rfft(signal))


def plot_spectrum(freqs: np.ndarray, mag: np.ndarray, title: str, loglog: bool = False) -> None:
    plt.figure(figsize=(10, 5))
    if loglog:
        plt.loglog(freqs, mag)
    else:
        plt.plot(freqs, mag)
    plt.title(title)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()


# Box processing
def process_with_box(times: np.ndarray, signal_in: np.ndarray, box) -> np.ndarray:
    """Process a signal using a course-provided box filter."""
    return box.process(times, signal_in)


# Custom frequency-domain filter (transfer function)
def apply_transfer_filter_once(
    times: np.ndarray,
    signal_in: np.ndarray,
    R: float,
    L: float,
    C: float,
) -> np.ndarray:
    """
    Apply a frequency-domain filter once using a transfer function.

    Definitions:
        f0 = 1 / (2π sqrt(LC))
        g  = R / (2π L)

    Transfer function (as used in the original coursework):
        T(f) = (f^2 - f0^2) / (f^2 - f0^2 - i g f)

    Returns a real-valued time-domain filtered signal.
    """
    times, signal_in = np.asarray(times, float), np.asarray(signal_in, float)
    if times.ndim != 1 or times.shape != signal_in.shape or len(times) < 2:
        raise ValueError('Time and signal arrays must be matching 1D arrays with at least two samples.')
    if not np.all(np.isfinite(times)) or not np.all(np.isfinite(signal_in)):
        raise ValueError('Time and signal arrays must be finite.')
    dt_all = np.diff(times)
    if dt_all[0] <= 0 or not np.allclose(dt_all, dt_all[0], rtol=1e-7, atol=1e-12):
        raise ValueError('FFT filtering requires uniformly spaced, increasing times.')
    if any(not np.isfinite(v) or v <= 0 for v in [R, L, C]):
        raise ValueError('R, L and C must be finite and positive.')
    f0 = 1.0 / (2.0 * np.pi * np.sqrt(L * C))
    g = R / (2.0 * np.pi * L)

    dt = times[1] - times[0]
    freqs = np.fft.fftfreq(len(times), d=dt)

    s_in_freq = np.fft.fft(signal_in)
    T = (freqs**2 - f0**2) / (freqs**2 - f0**2 - 1j * g * freqs)

    s_out = np.fft.ifft(s_in_freq * T)
    return np.real(s_out)


def apply_transfer_filter_n_times(
    times: np.ndarray,
    signal_in: np.ndarray,
    R: float,
    L: float,
    C: float,
    order_n: int,
) -> np.ndarray:
    """Apply the transfer filter repeatedly (order N)."""
    if not isinstance(order_n, (int, np.integer)) or order_n < 1:
        raise ValueError("Filter order N must be a positive integer.")

    signal = signal_in
    for _ in range(order_n):
        signal = apply_transfer_filter_once(times, signal, R, L, C)
    return signal


# Execution
def main() -> None:
    try:
        from module_engine.assignment import Boxes, Assignment2
    except ImportError:
        raise SystemExit('The original recorded-signal exercise requires the university module_engine. Run python demo.py for a standalone synthetic example.')
    t1_box1, t1_box2, t1_box3, t1_box4, t2_box, t3_rec, check_SNR, play = Boxes.get_boxes(Assignment2())
    sampling_rate = Boxes.SAMP_RATE
    print("Audio sampling rate:", sampling_rate, "Hz")

    # A) Swept-sine input generation
    duration = 1.0
    f_min = 10.0
    f_max = 4000.0

    times, freqs_inst, ssine_in = generate_swept_sine(duration, sampling_rate, f_min, f_max)

    plot_time_series(times, ssine_in, "Input signal (swept sine) — time domain")
    plot_signal_vs_frequency(freqs_inst, ssine_in, "Input signal (swept sine) — instantaneous frequency axis")

    # B) Spectrum of input
    freq_in, mag_in = magnitude_spectrum(ssine_in, sampling_rate)
    plot_spectrum(freq_in, mag_in, "Input spectrum |X(f)|")

    # C) Spectrum after unknown box filter
    box = t1_box4  # change to compare other boxes
    y = process_with_box(times, ssine_in, box)

    freq_out, mag_out = magnitude_spectrum(y, sampling_rate)
    plot_spectrum(freq_out, mag_out, "Output spectrum after box |Y(f)|")

    # D) Recorded signal analysis
    play(t3_rec)

    freqs_pos, mag_pos = magnitude_spectrum(t3_rec, sampling_rate)
    plot_spectrum(freqs_pos, mag_pos, "Recorded signal spectrum", loglog=True)

    noise_idx = int(np.argmax(mag_pos))
    noise_freq = freqs_pos[noise_idx]
    print(f"Dominant noise peak frequency: {noise_freq:.1f} Hz")

    duration_rec = len(t3_rec) / sampling_rate
    times_rec = np.linspace(0.0, duration_rec, len(t3_rec), endpoint=False)

    # Filter parameters (from notebook)
    R = 300.0
    L = 0.0255
    C = 1.14e-6
    N = 3

    filtered_signal = apply_transfer_filter_n_times(times_rec, t3_rec, R, L, C, N)

    play(filtered_signal)
    print("SNR:", check_SNR(R, L, C, N))

    Boxes.check()


if __name__ == "__main__":
    main()
