import numpy as np
from model import simulate_synapse

def fitness_function(parametreler, hedef_konsantrasyon):
    """
    Algoritmanın başarısını ölçen uygunluk fonksiyonu. 
    Hedef konsantrasyon ile simülasyon sonucu arasındaki mutlak farkı (hatayı) hesaplar.
    """
    release, reuptake, deg = parametreler
    
    # Parametrelerin negatif olamayacağı biyolojik kısıtı (Constraint handling)
    if release < 0 or reuptake < 0 or deg < 0:
        return 9999.0 
        
    # Mevcut parametrelerle simülasyonu çalıştır
    max_c = simulate_synapse(release, reuptake, deg, plot=False)
    
    # Hata değeri (Fitness value - minimize edilmesi hedeflenir)
    return abs(hedef_konsantrasyon - max_c)

def basitlestirilmis_voa(hedef_konsantrasyon, populasyon_sayisi=30, iterasyon=100):
    """
    Basitleştirilmiş Girdap Optimizasyon Algoritması (VOA).
    Sürüler halindeki parçacıkların girdap benzeri hareketlerle en iyi çözüme yaklaşmasını sağlar.
    """
    # Başlangıç popülasyonunun rastgele oluşturulması (Sınırlı aralıklarda)
    populasyon = np.random.rand(populasyon_sayisi, 3)
    populasyon[:, 0] *= 20.0 # Salınım hızı üst sınırı
    populasyon[:, 1] *= 0.5  # Geri alım hızı üst sınırı
    populasyon[:, 2] *= 0.5  # Yıkım hızı üst sınırı
    
    en_iyi_cozum = None
    en_iyi_hata = float('inf')
    
    # Optimizasyon döngüsü
    for i in range(iterasyon):
        # Tüm bireylerin performansının değerlendirilmesi
        hatalar = [fitness_function(birey, hedef_konsantrasyon) for birey in populasyon]
        
        # En iyi bireyin seçilmesi (Girdap merkezi)
        mevcut_en_iyi_idx = np.argmin(hatalar)
        if hatalar[mevcut_en_iyi_idx] < en_iyi_hata:
            en_iyi_hata = hatalar[mevcut_en_iyi_idx]
            en_iyi_cozum = populasyon[mevcut_en_iyi_idx].copy()
            
        # Girdap yarıçapının iterasyonla azalması (Exploitation artırımı)
        r = 1.0 - (i / iterasyon)
        
        # Popülasyonun güncellenmesi
        for j in range(populasyon_sayisi):
            if j != mevcut_en_iyi_idx:
                # Rastgele sapma ve merkeze yönelim (Vortex motion)
                rastgele_sapma = np.random.randn(3) * r * 0.1 
                populasyon[j] = populasyon[j] + rastgele_sapma + (en_iyi_cozum - populasyon[j]) * np.random.rand() * r
                
    return en_iyi_cozum, en_iyi_hata