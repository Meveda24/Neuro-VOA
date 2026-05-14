from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import io
import base64
from optimize import basitlestirilmis_voa
from model import synapse_dynamics

app = Flask(__name__)

def plot_comparison_to_base64(params_a, params_b, hedef):
    """
    İki farklı ajanın performansını aynı grafik üzerinde karşılaştırır.
    """
    t = np.linspace(0, 100, 1000)
    
    # Ajan A Simülasyonu
    C_a = odeint(synapse_dynamics, 0.0, t, args=tuple(params_a))
    
    # Ajan B Simülasyonu
    C_b = odeint(synapse_dynamics, 0.0, t, args=tuple(params_b))
    
    plt.figure(figsize=(12, 6))
    plt.plot(t, C_a, label='Ajan A Profili', color='#0d6efd', linewidth=2.5)
    plt.plot(t, C_b, label='Ajan B Profili', color='#198754', linewidth=2.5, linestyle='--')
    
    plt.axhline(y=hedef, color='#dc3545', linestyle=':', label=f'Referans Hedef ({hedef})', alpha=0.7)
    
    plt.title('Ajan Parametrelerinin Referans İndekse Yakınsama Grafiği (In-Silico ODE Çözümü)', fontsize=14)
    plt.xlabel('Zaman (ms)')
    plt.ylabel('Konsantrasyon (C)')
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=150)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hedef_deger = float(request.form['hedef'])
        preset = request.form.get('preset', 'genel')
        
        # Ajan A Maskesi
        mask_a = [
            'salinim' in request.form.getlist('mask_a'),
            'reuptake' in request.form.getlist('mask_a'),
            'yikim' in request.form.getlist('mask_a')
        ]
        
        # Ajan B Maskesi
        mask_b = [
            'salinim' in request.form.getlist('mask_b'),
            'reuptake' in request.form.getlist('mask_b'),
            'yikim' in request.form.getlist('mask_b')
        ]
        
        # Eğer maske boşsa varsayılan olarak hepsini seç
        if not any(mask_a): mask_a = [True, True, True]
        if not any(mask_b): mask_b = [True, True, True]
        
        # İki ajan için ayrı optimizasyon çalıştır
        params_a, hata_a = basitlestirilmis_voa(hedef_deger, preset_key=preset, active_mask=mask_a)
        params_b, hata_b = basitlestirilmis_voa(hedef_deger, preset_key=preset, active_mask=mask_b)
        
        plot_url = plot_comparison_to_base64(params_a, params_b, hedef_deger)
        
        sonuclar = {
            'hedef': hedef_deger,
            'preset': preset,
            'ajan_a': {
                'salinim': round(params_a[0], 4),
                'reuptake': round(params_a[1], 4),
                'yikim': round(params_a[2], 4),
                'hata': round(hata_a, 6)
            },
            'ajan_b': {
                'salinim': round(params_b[0], 4),
                'reuptake': round(params_b[1], 4),
                'yikim': round(params_b[2], 4),
                'hata': round(hata_b, 6)
            },
            'grafik': plot_url
        }
        return render_template('index.html', sonuclar=sonuclar)
        
    return render_template('index.html', sonuclar=None)

if __name__ == '__main__':
    app.run(debug=True)
