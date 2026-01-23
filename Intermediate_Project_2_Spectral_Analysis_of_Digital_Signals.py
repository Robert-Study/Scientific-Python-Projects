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
2) Filters can be expressed via a transfer function T(f), so that: Y(f) = X(f) · T(f)
   and the filtered time-domain signal is recovered via inverse FFT.

Workflow
---------------------------
A) Generate a swept-sine input and inspect it in time and frequency.
B) Pass the swept-sine through a chosen box filter and compare spectra.
C) Analyse a recorded signal spectrum, locate noise peaks, and apply a custom frequency-
   domain filter (R, L, C, order N) repeatedly to suppress noise and improve SNR.
   """

import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# Pseudocode / course interface (intentionally not runnable in showcase)
# =============================================================================

from module_engine.assignment import Boxes
studentID = ""  #showcase-only
# t1_box1, t1_box2, t1_box3, t1_box4, t2_box, t3_rec, check_SNR, play = Boxes.get_boxes(studentID)
# sampling_rate = Boxes.SAMP_RATE


# =============================================================================
# Signal generation and plotting utilities
# =============================================================================

def generate_swept_sine(
    duration_s: float,
    sampling_rate_hz: int,
    f_min_hz: float = 10.0,
    f_max_hz: float = 4000.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate a swept-sine (chirp-like) test signal where frequency increases linearly
    from f_min to f_max over the given duration.

    Returns:
        times:       time axis [s]
        frequencies: instantaneous frequency per sample [Hz]
        signal:      swept-sine samples
    """
    n = int(duration_s * sampling_rate_hz)
    times = np.linspace(0.0, duration_s, n, endpoint=False)
    frequencies = np.linspace(f_min_hz, f_max_hz, n)
    signal = np.sin(2.0 * np.pi * frequencies * times)
    return times, frequencies, signal


def plot_time_series(times: np.ndarray, signal: np.ndarray, title: str) -> None:
    plt.figure(figsize=(15, 3))
    plt.plot(times, signal)
    plt.title(title)
    plt.xlabel("t [s]")
    plt.ylabel("Amplitude")
    plt.xlim(times[0], times[-1])
    plt.ylim(-1.1, 1.1)
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


# =============================================================================
# Spectral analysis utilities
# =============================================================================

def magnitude_spectrum(signal: np.ndarray, sampling_rate_hz: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the one-sided magnitude spectrum of a real-valued time signal.

    Returns:
        freqs_pos: non-negative frequencies [Hz]
        mag_pos:   corresponding magnitudes
    """
    freqs = np.fft.fftfreq(len(signal), d=1.0 / sampling_rate_hz)
    fft_vals = np.fft.fft(signal)
    mag = np.abs(fft_vals)

    mask = freqs >= 0
    return freqs[mask], mag[mask]


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


# =============================================================================
# Box processing (course filters) — treated as pseudocode in showcase
# =============================================================================

def process_with_box(times: np.ndarray, signal_in: np.ndarray, box) -> np.ndarray:
    """
    Pseudocode wrapper for course-provided box processing.
    In the course environment this would call: box.process(times, signal_in)
    """
    # return box.process(times, signal_in)
    raise NotImplementedError("Showcase-only: box processing requires course module_engine.")


# =============================================================================
# Custom frequency-domain filter (RLC-style transfer function)
# =============================================================================

def apply_transfer_filter_once(
    times: np.ndarray,
    signal_in: np.ndarray,
    R: float,
    L: float,
    C: float,
    sampling_rate_hz: int,
) -> np.ndarray:
    """
    Apply a frequency-domain filter once using a transfer function.

    This uses:
        f0 = 1 / (2π sqrt(LC))
        g  = R / (2π L)

    Transfer function form (as used in the original coursework):
        T(f) = (f^2 - f0^2) / (f^2 - f0^2 - i g f)

    Returns a real-valued time-domain filtered signal.
    """
    f0 = 1.0 / (2.0 * np.pi * np.sqrt(L * C))
    g = R / (2.0 * np.pi * L)

    dt = times[1] - times[0]
    freqs = np.fft.fftfreq(len(times), d=dt)

    s_in_freq = np.fft.fft(signal_in)

    # Build transfer function across full FFT frequency axis.
    # (Avoid divide-by-zero at f=0 implicitly handled by numpy complex arithmetic.)
    T = (freqs**2 - f0**2) / (freqs**2 - f0**2 - 1j * g * freqs)

    s_out_freq = s_in_freq * T
    s_out = np.fft.ifft(s_out_freq)

    return np.real(s_out)


def apply_transfer_filter_n_times(
    times: np.ndarray,
    signal_in: np.ndarray,
    R: float,
    L: float,
    C: float,
    sampling_rate_hz: int,
    order_n: int,
) -> np.ndarray:
    """
    Apply the transfer filter repeatedly (order N).
    """
    if order_n < 1:
        raise ValueError("Filter order N must be a positive integer.")

    signal = signal_in
    for _ in range(order_n):
        signal = apply_transfer_filter_once(times, signal, R, L, C, sampling_rate_hz)
    return signal


# =============================================================================
# Example analysis flow (showcase structure)
# =============================================================================

def example_workflow_showcase() -> None:
    """
    Showcase-only structure of the original notebook workflow.
    Values and course calls are preserved conceptually, but course objects are not included.
    """

    # -------------------------------------------------------------------------
    # A) Swept-sine input generation
    # -------------------------------------------------------------------------
    # sampling_rate = Boxes.SAMP_RATE
    sampling_rate = ...  # placeholder in showcase
    duration = 1.0

    times, freqs_inst, ssine_in = generate_swept_sine(
        duration_s=duration,
        sampling_rate_hz=sampling_rate,
        f_min_hz=10.0,
        f_max_hz=4000.0,
    )

    plot_time_series(times, ssine_in, title="Input signal (swept sine) — time domain")
    plot_signal_vs_frequency(freqs_inst, ssine_in, title="Input signal (swept sine) — instantaneous frequency axis")

    # -------------------------------------------------------------------------
    # B) Spectrum of input
    # -------------------------------------------------------------------------
    freq_in, mag_in = magnitude_spectrum(ssine_in, sampling_rate_hz=sampling_rate)
    plot_spectrum(freq_in, mag_in, title="Input spectrum |X(f)|")

    # -------------------------------------------------------------------------
    # C) Spectrum after unknown box filter (pseudocode)
    # -------------------------------------------------------------------------
    # box = t1_box4
    # signal_box = box.process(times, ssine_in)
    # freq_out, mag_out = magnitude_spectrum(signal_box, sampling_rate_hz=sampling_rate)
    # plot_spectrum(freq_out, mag_out, title="Output spectrum after box |Y(f)|")
    #
    # Box identification logic (kept as comments for showcase)
    # RL_circuit       -> behaves like high-pass
    # RC_circuit       -> behaves like low-pass
    # RLC_bandpass     -> peak around resonance
    # RLC_bandstop     -> notch around resonance

    # -------------------------------------------------------------------------
    # D) Recorded signal noise analysis + filtering (pseudocode data)
    # -------------------------------------------------------------------------
    # t3_rec is the recorded signal from the course environment.
    t3_rec = ...  # placeholder in showcase

    # Inspect spectrum (log-log is useful for wide dynamic range)
    freqs_pos, mag_pos = magnitude_spectrum(t3_rec, sampling_rate_hz=sampling_rate)
    plot_spectrum(freqs_pos, mag_pos, title="Recorded signal spectrum", loglog=True)

    # Identify dominant noise peak
    noise_idx = int(np.argmax(mag_pos))
    noise_freq = freqs_pos[noise_idx]
    print(f"Dominant noise peak at ~{noise_freq:.1f} Hz")

    # Apply repeated filter with chosen R, L, C, N (from original notebook)
    duration_rec = len(t3_rec) / sampling_rate
    times_rec = np.linspace(0.0, duration_rec, len(t3_rec), endpoint=False)

    R = 300.0
    L = 0.0255
    C = 1.14e-6
    N = 3

    filtered = apply_transfer_filter_n_times(
        times=times_rec,
        signal_in=t3_rec,
        R=R,
        L=L,
        C=C,
        sampling_rate_hz=sampling_rate,
        order_n=N,
    )

    # Pseudocode: play(filtered) and compute SNR using course-provided function
    # play(filtered)
    # print(check_SNR(R, L, C, N))

    student_PIN = "5737"  # coursework response (kept for completeness, showcase-only)
    # Boxes.check()  # course-provided validation


# No execution guard intentionally required for showcase-only display.
# If you *do* want it runnable locally, add:
# if __name__ == "__main__":
#     example_workflow_showcase()
