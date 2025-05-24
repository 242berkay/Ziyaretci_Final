# Gümüşhane İkizevler Kent Müzesi Ziyaretçi Yönetim Sistemi

Bu proje, Gümüşhane İkizevler Kent Müzesi için tasarlanmış bir web arayüzüdür.  
Ziyaretçilerin temel müze bilgilerine ulaşabileceği ve ziyaretlerini planlayabileceği bir sistemdir.

---

## 🎨 Tasarım Özellikleri

- Modern ve responsive tasarım
- **Bootstrap 5** framework kullanımı
- **Bootstrap Icons** entegrasyonu
- Kullanıcı dostu arayüz

---

## 📄 Sayfalar

### Ziyaretçi Arayüzü
- **Ana Sayfa**: Müze karşılama alanı ve konum haritası (`index.html`)
- **Kayıt Formu**: Kullanıcı kaydı için form tasarımı (`kayit_formu.html`)
- **Giriş Formu**: Kullanıcı girişi için form tasarımı
- **Rezervasyon Formu**: Ad, Soyad, Ziyaret Saati, Ziyaret Süresi alanlarını içerir
- **Navbar Dinamikliği**:
  - Giriş yapmışsa: “Çıkış Yap” görünür
  - Giriş yapılmamışsa: “Giriş Yap” ve “Kayıt Ol” görünür
- **Rezervasyon Kontrolü**: Giriş yapılmamışsa, "Rezervasyon Yap" butonu giriş modalını açar
- **Pop-up Bildirimleri**: Başarılı veya hatalı işlemlerde kullanıcıya bildirim
- **Kayıtlı Kullanıcı Sayfaları**:
  - `kayitli_kullanici.html`
  - `kayitli_kullanici_detay.html`

### Yönetici Sayfaları
- **Admin Giriş Sayfası** (`admin_giris.html`)
- **Admin Paneli** (`admin_paneli.html`)
- **Ziyaretçi Listeleme**:
  - `kayitli_ziyaretciler.html`
  - `listele.html`
- **Güncelleme Formu** (`guncelleformu.html`)
- **Filtreleme Sayfası** (`filtrele.html`)

---

## 💻 Kullanılan Teknolojiler

- HTML5  
- CSS3  
- Bootstrap 5  
- Bootstrap Icons  
- Jinja2 Template Engine  
- Python Flask (Backend)  
- SQLite (Veritabanı)  
- Leaflet.js (Harita)

---

## 📁 Proje Yapısı

```text
FIRSTWEEK/
├── pycache/
├── instance/
├── static/
│ ├── css/ # Özel CSS ve Bootstrap CSS
│ └── img/ # Resimler (logo, arka plan vb.)
├── templates/
│ ├── admin_giris.html
│ ├── admin_paneli.html
│ ├── filtrele.html
│ ├── guncelleformu.html
│ ├── index.html
│ ├── kayit_formu.html
│ ├── kayitli_kullanici_detay.html
│ ├── kayitli_kullanici.html
│ ├── kayitli_ziyaretciler.html
│ └── listele.html
├── app.py # Ana Flask uygulama dosyası
├── db2json.py # Veritabanını JSON'a dönüştürme betiği
├── readme.txt # Bu README dosyası
├── requirements.txt # Python bağımlılıkları
├── users.json # Kullanıcı verisi
├── visitors.json # Ziyaretçi verisi
```

---

## 🎨 Tasarım Detayları

### 🎨 Renkler
- **Primary**: Mavi `#0d6efd`
- **Success**: Yeşil `#198754`
- **Info**: Açık Mavi `#0dcaf0`
- **Warning**: Sarı `#ffc107`

### 💡 Genel Tasarım Özellikleri
- Responsive tasarım (Mobil uyumlu)
- Grid sistemi ile esnek yerleşim
- Kart yapıları ile içerik sunumu
- Gölgeli modallar ve bilgi kutuları
- Hover efektleri (buton ve bağlantılar)
- Bootstrap Icons ile ikon kullanımı

---

## 📌 Not
Bu proje eğitim ve sunum amacıyla geliştirilmiştir.
