import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def synapse_dynamics(C, t, release_rate, reuptake_rate, degradation_rate):
    """
    Sinaptik aralıktaki nörotransmitter konsantrasyon değişimini tanımlayan diferansiyel denklem.
    Model: dC/dt = Salınım(t) - (Geri Alım + Enzimatik Yıkım) * C
    """
    # 10-20 ms aralığında nörotransmitter salınımı gerçekleştiği varsayılır (Pulse modelleme)
    if 10 <= t <= 20:
        R = release_rate
    else:
        R = 0.0
        
    # Konsantrasyon değişimi (Derişim hızı)
    dCdt = R - (reuptake_rate + degradation_rate) * C
    return dCdt

def simulate_synapse(release_rate, reuptake_rate, degradation_rate, plot=False):
    """
    Verilen biyolojik parametrelerle sinaptik iletimi simüle eder ve tepe konsantrasyon değerini döndürür.
    """
    t = np.linspace(0, 100, 1000) # 100 ms'lik zaman penceresi
    C0 = 0.0 # Başlangıç konsantrasyonu
    
    # Diferansiyel denklemin sayısal çözümü (ODE Integration)
    C = odeint(synapse_dynamics, C0, t, args=(release_rate, reuptake_rate, degradation_rate))
    
    if plot:
        plt.figure(figsize=(8, 4))
        plt.plot(t, C, label='Nörotransmitter Konsantrasyonu', color='b')
        plt.axhline(y=40, color='r', linestyle='--', label='Sağlıklı Hedef Eşik Değeri')
        plt.title('Sinaptik İletim Dinamiği Simülasyonu')
        plt.xlabel('Zaman (ms)')
        plt.ylabel('Konsantrasyon (C)')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    return C.max() # Optimizasyon için kullanılan maksimum konsantrasyon (peak value)

if __name__ == "__main__":
    # Örnek parametrelerle test çalışması
    print("Simülasyon test ediliyor...")
    max_c = simulate_synapse(10.0, 0.1, 0.05, plot=True)
    print(f"Ulaşılan Maksimum Konsantrasyon: {max_c:.2f}")