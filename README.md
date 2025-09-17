# Ankara House Prices Prediction 🏠

Bu proje, Ankara’daki kiralık evlerin fiyatlarını tahmin etmek için bir Machine Learning pipeline içerir. Kullanıcı Streamlit arayüzü üzerinden evin özelliklerini girerek tahmini fiyat alabilir.

## Özellikler

Kullanıcıdan alınan girdiler:

İlçe (County)

Metrekare (m²)

Oda sayısı (Room)

Salon sayısı (Saloon)

Tahmin modeli: GradientBoostingRegressor (hiperparametre tuning ile)


## Kurulum

```bash
# Ortam oluşturma
python3 -m venv scraping_env
source scraping_env/bin/activate  # Windows için: scraping_env\Scripts\activate

# Gereksinimleri yükleme
pip install -r requirements.txt


```
## Çalıştırma

```bash

streamlit run app.py

```
Sol panelden evin özelliklerini girin.

Tahmini fiyat ekranda görüntülenecektir.

## Limitasyonlar ⚠️

Dataset yeterli değil; bazı kritik özellikler (bina yaşı, metroya yakınlık vb.) yok.

Veri dağılımı dengesiz; bu nedenle tahminler referans amaçlıdır ve ticari olarak kullanılmaya uygun değildir!
