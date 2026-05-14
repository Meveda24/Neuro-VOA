import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def alpha_synapse_release(t, R_max, t0=10.0, tau_rise=1.0, tau_decay=10.0):
    """
    Alpha Fonksiyonu (Double Exponential) kullanarak gerçekçi nörotransmitter salınımı modeller.
    Bu model, ani bir yükseliş ve ardından yavaş bir sönümlenme (spike) sağlar.
    """
    if t < t0:
        return 0.0
    
    # Normalizasyon faktörü (Peak değerinin R_max olmasını sağlar)
    t_peak = (tau_rise * tau_decay) / (tau_decay - tau_rise) * np.log(tau_decay / tau_rise)
    norm = np.exp(-t_peak / tau_decay) - np.exp(-t_peak / tau_rise)
    
    # Alpha fonksiyonu hesabı
    rel_t = t - t0
    R = (R_max / norm) * (np.exp(-rel_t / tau_decay) - np.exp(-rel_t / tau_rise))
    return R

def synapse_dynamics(C, t, release_rate, reuptake_rate, degradation_rate):
    """
    Sinaptik aralıktaki nörotransmitter konsantrasyon değişimini tanımlayan diferansiyel denklem.
    Model: dC/dt = Alpha_Release(t) - (Geri Alım + Enzimatik Yıkım) * C
    """
    # Gerçekçi Alpha salınım modeli
    R = alpha_synapse_release(t, release_rate)
        
    # Konsantrasyon değişimi
    dCdt = R - (reuptake_rate + degradation_rate) * C
    return dCdt

def simulate_synapse(release_rate, reuptake_rate, degradation_rate, plot=False):
    """
    Verilen biyolojik parametrelerle sinaptik iletimi simüle eder.
    """
    t = np.linspace(0, 100, 1000)
    C0 = 0.0
    
    C = odeint(synapse_dynamics, C0, t, args=(release_rate, reuptake_rate, degradation_rate))
    
    if plot:
        plt.figure(figsize=(8, 4))
        plt.plot(t, C, label='Nörotransmitter Konsantrasyonu', color='#0d6efd', linewidth=2)
        plt.title('Alpha Sinaps Modeli ile Dinamik Simülasyon')
        plt.xlabel('Zaman (ms)')
        plt.ylabel('Konsantrasyon (C)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
        
    return C.max()

if __name__ == "__main__":
    print("Alpha Sinaps Simülasyonu test ediliyor...")
    max_c = simulate_synapse(20.0, 0.1, 0.05, plot=True)
    print(f"Ulaşılan Maksimum Konsantrasyon: {max_c:.2f}")