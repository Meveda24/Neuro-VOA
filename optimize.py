import numpy as np
from model import simulate_synapse

# Fizyolojik Ön Ayarlar (Literature-based presets)
PRESETS = {
    "genel": {
        "bounds": [(0, 50.0), (0, 1.0), (0, 1.0)],
        "baseline": [10.0, 0.1, 0.05]
    },
    "noradrenalin_sican": {
        "bounds": [(5.0, 30.0), (0.01, 0.3), (0.01, 0.2)],
        "baseline": [15.0, 0.05, 0.05]
    },
    "serotonin_sican": {
        "bounds": [(2.0, 15.0), (0.01, 0.2), (0.005, 0.1)],
        "baseline": [8.0, 0.03, 0.02]
    }
}

def fitness_function(parametreler, hedef_konsantrasyon, active_mask, baseline):
    """
    Uygunluk fonksiyonu. Sadece aktif parametreleri optimize eder, 
    diğerlerini baseline değerinde sabit tutar.
    """
    # Gerçek parametre setini oluştur (active_mask'e göre)
    final_params = []
    for i in range(3):
        if active_mask[i]:
            final_params.append(parametreler[i])
        else:
            final_params.append(baseline[i])
            
    release, reuptake, deg = final_params
    
    # Negatif değer kontrolü (Algoritma dışına çıkarsa)
    if any(p < 0 for p in final_params):
        return 9999.0 
        
    max_c = simulate_synapse(release, reuptake, deg, plot=False)
    return abs(hedef_konsantrasyon - max_c)

def basitlestirilmis_voa(hedef_konsantrasyon, preset_key="genel", active_mask=[True, True, True], populasyon_sayisi=30, iterasyon=50):
    """
    Kısıtlanmış ve Özelleştirilmiş VOA Algoritması.
    active_mask: [Salınım, Geri Alım, Yıkım] -> Hangi parametrelerin optimize edileceği.
    """
    preset = PRESETS.get(preset_key, PRESETS["genel"])
    bounds = preset["bounds"]
    baseline = preset["baseline"]
    
    # Başlangıç popülasyonu (Sadece aktif parametreler için rastgele değerler)
    populasyon = np.zeros((populasyon_sayisi, 3))
    for i in range(3):
        if active_mask[i]:
            low, high = bounds[i]
            populasyon[:, i] = np.random.uniform(low, high, populasyon_sayisi)
        else:
            populasyon[:, i] = baseline[i]
            
    en_iyi_cozum = None
    en_iyi_hata = float('inf')
    
    for i in range(iterasyon):
        hatalar = [fitness_function(birey, hedef_konsantrasyon, active_mask, baseline) for birey in populasyon]
        
        mevcut_en_iyi_idx = np.argmin(hatalar)
        if hatalar[mevcut_en_iyi_idx] < en_iyi_hata:
            en_iyi_hata = hatalar[mevcut_en_iyi_idx]
            en_iyi_cozum = populasyon[mevcut_en_iyi_idx].copy()
            
        r = 1.0 - (i / iterasyon)
        
        for j in range(populasyon_sayisi):
            if j != mevcut_en_iyi_idx:
                # Girdap hareketi: Sadece aktif parametreler üzerinde değişim yap
                for k in range(3):
                    if active_mask[k]:
                        rastgele_sapma = np.random.randn() * r * (bounds[k][1] - bounds[k][0]) * 0.05
                        yeni_deger = populasyon[j, k] + rastgele_sapma + (en_iyi_cozum[k] - populasyon[j, k]) * np.random.rand() * r
                        # Sınır kontrolü (Clamping)
                        populasyon[j, k] = np.clip(yeni_deger, bounds[k][0], bounds[k][1])
                
    # Final çözümü baseline ile birleştirerek döndür
    final_sonuc = []
    for k in range(3):
        if active_mask[k]:
            final_sonuc.append(en_iyi_cozum[k])
        else:
            final_sonuc.append(baseline[k])
            
    return final_sonuc, en_iyi_hata