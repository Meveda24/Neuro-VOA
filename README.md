# Neuro-VOA: Sinaptik İletim Dinamiklerinin Sezgisel Algoritmalar ile Optimizasyonu

Bu proje, sinaptik boşluktaki nörotransmitter derişimlerini zamana bağlı diferansiyel denklemler aracılığıyla modelleyen ve hedeflenen terapötik konsantrasyon değerine (referans aralığına) ulaşmak için gerekli olan presinaptik ve postsinaptik parametreleri otonom olarak optimize eden bir biyomedikal simülasyon sistemidir.

Çalışma, farmakolojik karar destek sistemlerinde (örn. dozaj ayarlaması ve etki mekanizması tahmini) kullanılabilecek, düşük işlemci yüküne sahip (Edge-computing uyumlu) bir prototip niteliği taşımaktadır.

## 🧬 Matematiksel Model ve Biyolojik Temeller

Sistemdeki sinaptik derişim seviyesi ($C$), üç temel farmakokinetik / farmakodinamik parametre üzerinden tanımlanmıştır:

*   **$R(t)$ (Salınım Oranı):** Nörotransmitterin presinaptik terminalden sinaptik aralığa salınım hızı.
*   **$k_u$ (Geri Alım Sabiti):** Nörotransmitterin taşıyıcı proteinler aracılığıyla hücre içine geri alınım (reuptake) hızı.
*   **$k_d$ (Yıkım Sabiti):** Ortamdaki enzimler (örn. MAO, COMT) tarafından gerçekleştirilen degradasyon hızı.

Konsantrasyonun zamana bağlı değişimi, SciPy kütüphanesi entegrasyonu ile aşağıdaki diferansiyel denklem (ODE) çözülerek modellenmiştir:

$$\frac{dC}{dt} = R(t) - (k_u + k_d) \cdot C(t)$$

## 🌀 Optimizasyon Yaklaşımı: VOA (Vortex Optimization Algorithm)

Parametrelerin hedef derişim noktasına milimetrik olarak yakınsaması amacıyla literatürdeki doğadan esinlenen metotlardan biri olan Girdap Optimizasyon Algoritması (Vortex Optimization Algorithm) kullanılmıştır.

Arama uzayında oluşturulan popülasyon (çözüm adayları), girdap merkezindeki optimal (en düşük fitness hata değerine sahip) çözüme sarmal bir çekim kuvvetiyle yaklaşır. Bu yapı, yerel minimum (local minima) problemlerine takılmadan en ideal biyolojik ayarların hızlıca tespit edilmesini sağlar.

## ⚠️ Biyolojik Kısıtlar ve Arama Uzayı (Search Space) Sınırları

Optimizasyon algoritmasının arama uzayı, biyolojik ve fizyolojik kısıtlar göz önüne alınarak kasıtlı olarak sınırlandırılmıştır.

Kullanıcı arayüzü üzerinden hedef konsantrasyon değeri, presinaptik vezikül kapasitesinin ve reseptör doygunluk seviyelerinin dışına çıkacak şekilde (örneğin 2000 birim gibi aşırı bir değer) girildiğinde sistem doğal olarak yüksek bir hata (fitness) skoru üretecektir. Bu durum mimari bir kısıtlılık veya kodlama hatası değildir; hedeflenen değerin nörotoksik veya fizyolojik olarak imkansız olduğunu gösteren, karar destek sisteminin gerçeğe uygunluğunu sağlayan bir tasarım kuralıdır.

## 🚀 Kurulum ve Sistem Gereksinimleri

Proje, Flask mikro web iskeleti ile servis edilmektedir ve standart donanımlı sistemlerde çalıştırılabilir.

### Bağımlılıkların Yüklenmesi:
```bash
pip install flask numpy scipy matplotlib
```

### Uygulamanın Başlatılması:
```bash
python app.py
```

Uygulama çalıştırıldıktan sonra web tarayıcısı üzerinden [http://127.0.0.1:5000](http://127.0.0.1:5000) adresine giderek arayüze erişebilir, farklı hedef konsantrasyon değerleri için algoritmanın parametre optimizasyonunu ve grafiksel çıktılarını anlık olarak inceleyebilirsiniz.

## 📂 Mimari Yapı

*   `model.py` : Dinamik ODE çözümlerinin ve biyolojik sınırların tanımlandığı çekirdek modül.
*   `optimize.py` : VOA tabanlı hedef fonksiyon (fitness) ve sarmal optimizasyon mimarisi.
*   `app.py` : Flask sunucu yapılandırması ve Base64 üzerinden Matplotlib entegrasyonu.
*   `templates/index.html` : Kullanıcı etkileşimini sağlayan Bootstrap tabanlı UI.
