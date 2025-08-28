import sqlite3
import time
import numpy as np
from rtlsdr import RtlSdr

DB = "bandscope.db"
FREQ = 27016000   # 27.016 MHz – próbamérésre
SAMPLE_RATE = 240000
GAIN = 'auto'

# SQLite előkészítés
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS measurements (
                timestamp INTEGER,
                freq INTEGER,
                mean_power REAL,
                peak_power REAL
            )""")
conn.commit()

# RTL-SDR inicializálás
sdr = RtlSdr()
sdr.sample_rate = SAMPLE_RATE
sdr.gain = GAIN
sdr.direct_sampling = 3   # DS mód (1=I, 2=Q, 3=auto)

def measure(freq, n_samples=262144):
    sdr.center_freq = freq
    samples = sdr.read_samples(n_samples)

    # FFT és teljesítmény
    spectrum = np.fft.fftshift(np.fft.fft(samples))
    psd = 10 * np.log10(np.abs(spectrum)**2 / len(samples))

    # frekvenciafelbontás
    hz_per_bin = sdr.sample_rate / len(psd)

    # ablak: ±1.25 kHz → összesen 2.5 kHz széles
    bw = 2500
    center = len(psd) // 2
    bins = int(bw / hz_per_bin)
    window = psd[center - bins//2 : center + bins//2]

    return np.mean(window), np.max(window)

try:
    while True:
        ts = int(time.time())
        mean_val, peak_val = measure(FREQ)
        c.execute("INSERT INTO measurements VALUES (?,?,?,?)",
                  (ts, FREQ, mean_val, peak_val))
        conn.commit()
        diff = peak_val - mean_val
        print(f"{time.strftime('%H:%M:%S')}  {FREQ/1e6:.3f} MHz  "
              f"mean={mean_val:.1f} dB  peak={peak_val:.1f} dB  Δ={diff:.1f} dB")
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    sdr.close()
    conn.close()
