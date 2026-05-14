from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg') # Sunucu tarafında grafik çizimi için Agg backend kullanımı
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import io
import base64
from optimize import basitlestirilmis_voa
from model import synapse_dynamics

app = Flask(__name__)

def plot_to_base64(release, reuptake, deg, hedef):
    """
    Optimal parametreleri kullanarak nihai simülasyon grafiğini oluşturur 
    ve HTML'de görüntülenebilmesi için Base64 formatına dönüştürür.
    """
    t = np.linspace(0, 100, 1000)
    C = odeint(synapse_dynamics, 0.0, t, args=(release, reuptake, deg))
    
    plt.figure(figsize=(10, 5))
    plt.plot(t, C, label='Optimize Edilmiş Nörotransmitter Salınımı', color='#0d6efd', linewidth=2)
    plt.axhline(y=hedef, color='#dc3545', linestyle='--', label=f'Hedef Konsantrasyon ({hedef})')
    plt.title('VOA ile Sinaptik İletim Optimizasyonu', fontsize=14)
    plt.xlabel('Zaman (ms)')
    plt.ylabel('Konsantrasyon (C)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Grafiği bellek üzerinde (RAM) PNG olarak sakla
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    
    # Binary veriyi Base64 string'e dönüştür
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Ana sayfa rotası: Kullanıcıdan hedef değeri alır, optimizasyonu başlatır 
    ve sonuçları şablon üzerinden döndürür.
    """
    if request.method == 'POST':
        # Kullanıcının girdiği hedef değeri al
        hedef_deger = float(request.form['hedef'])
        
        # VOA Algoritmasını çalıştırarak en iyi parametreleri bul
        optimal_parametreler, hata = basitlestirilmis_voa(hedef_konsantrasyon=hedef_deger)
        
        # Bulunan sonuçlarla görselleştirmeyi hazırla
        plot_url = plot_to_base64(*optimal_parametreler, hedef_deger)
        
        sonuclar = {
            'hedef': hedef_deger,
            'salinim': round(optimal_parametreler[0], 4),
            'geri_alim': round(optimal_parametreler[1], 4),
            'yikim': round(optimal_parametreler[2], 4),
            'hata': round(hata, 6),
            'grafik': plot_url
        }
        return render_template('index.html', sonuclar=sonuclar)
        
    return render_template('index.html', sonuclar=None)

if __name__ == '__main__':
    # Flask uygulamasını hata ayıklama moduyla başlat
    app.run(debug=True)
