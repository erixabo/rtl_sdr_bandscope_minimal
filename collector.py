import sqlite3
import time
import numpy as np
from rtlsdr import RtlSdr

DB = "bandscope.db"
FREQ = 7_040_000   # 7.040 MHz – próbamérésre
SAMPLE_RATE = 240000
GAIN = 'auto'

# SQLite előkészítés
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS measurements (
                timestamp INTEGER,
                freq INTEGER,
                power REAL
            )""")
conn.commit()

# RTL-SDR inicializálás
sdr = RtlSdr()
sdr.sample_rate = SAMPLE_RATE
sdr.gain = GAIN

def measure(freq, n_samples=128*1024):
    sdr.center_freq = freq
    samples = sdr.read_samples(n_samples)
    return 10 * np.log10(np.mean(np.abs(samples)**2))

try:
    while True:
        ts = int(time.time())
        pwr = measure(FREQ)
        c.execute("INSERT INTO measurements VALUES (?,?,?)", (ts, FREQ, pwr))
        conn.commit()
        print(f"{time.strftime('%H:%M:%S')}  {FREQ/1e6:.3f} MHz  {pwr:.1f} dB")
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    sdr.close()
    conn.close()
