Gümüşhane İkizevler Kent Müzesi Ziyaretçi Yönetim Sistemi
Bu proje, Gümüşhane İkizevler Kent Müzesi için tasarlanmış bir web arayüzüdür. Ziyaretçilerin temel müze bilgilerine ulaşabileceği ve ziyaretlerini planlayabileceği bir sistemdir.

Tasarım Özellikleri
Modern ve responsive tasarım
Bootstrap 5 framework kullanımı
Bootstrap Icons entegrasyonu
Kullanıcı dostu arayüz
Sayfalar
Ana Sayfa
Müze karşılama alanı (index.html)
Müzenin konumu gösteren harita (index.html içinde yer alıyor)
Ziyaretçi İşlemleri
Kayıt Formu: Kullanıcı kaydı için form tasarımı (kayit_formu.html).
Giriş Formu: Kullanıcı girişi için form tasarımı 
Rezervasyon Formu: Ziyaret için Ad, Soyad, Ziyaret Saati, Ziyaret Süresi alanları içeren form 
Geri dön ve kaydet butonları (modallar içinde)
Navbar Dinamikliği: Kullanıcı giriş yapmışsa "Giriş Yap" ve "Kayıt Ol" butonları gizlenir, "Çıkış Yap" butonu görünür. Giriş yapılmamışsa tam tersi.
Rezervasyon Kontrolü: "Rezervasyon Yap" butonuna basıldığında, kullanıcı giriş yapmamışsa giriş modalı açılır.
Pop-up Bildirimleri: Başarılı işlem veya hata durumlarında kullanıcıya pop-up mesajları gösterilir.
Kayıtlı Kullanıcı Bilgisi: Giriş yapan kullanıcının bilgilerini gösteren sayfa (kayitli_kullanici.html, kayitli_kullanici_detay.html).
Yönetici Sayfaları 
Admin Giriş Sayfası: Yönetici girişi için bir sayfa (admin_giris.html).
Admin Paneli: Yönetici paneli ana sayfası (admin_paneli.html).
Ziyaretçi Listeleme: Kayıtlı ziyaretçileri listelemek için sayfalar (kayitli_ziyaretciler.html, listele.html).
Güncelleme Formu: Ziyaretçi bilgilerini güncellemek için bir form (guncelleformu.html).
Filtreleme Sayfası: Ziyaretçileri filtrelemek için bir sayfa (filtrele.html).
Kullanılan Teknolojiler
HTML5
CSS3
Bootstrap 5
Bootstrap Icons
Jinja2 Template Engine
Python Flask (Backend)
SQLite (Veritabanı)
Leaflet (Harita)
Proje Yapısı
FIRSTWEEK/
├── __pycache__/
├── instance/
├── static/
│   ├── css/              # Özel CSS ve Bootstrap CSS
│   └── img/              # Resimler (logo, arka plan vb.)
├── templates/
│   ├── admin_giris.html      # Admin giriş sayfası
│   ├── admin_paneli.html     # Admin paneli 
│   ├── filtrele.html         # Ziyaretçi filtreleme sayfası
│   ├── guncelleformu.html    # Ziyaretçi güncelleme formu 
│   ├── index.html            # Ana sayfa 
│   ├── kayit_formu.html      # Kullanıcı kayıt formu
│   ├── kayitli_kullanici_detay.html # Kayıtlı kullanıcının detay bilgileri
│   ├── kayitli_kullanici.html# Kayıtlı kullanıcının genel bilgileri
│   ├── kayitli_ziyaretciler.html # Kayıtlı ziyaretçileri listeleme 
│   └── listele.html          # Kayıtlı ziyaretçileri listeleme 
├── app.py                # Ana Flask uygulama dosyası
├── db2json.py            # Veritabanını JSON'a dönüştürme betiği 
├── readme.txt            # Bu README dosyası 
├── requirements.txt      # Python bağımlılıkları
├── users.json            # Kullanıcı verisi
├── visitors.json         # Ziyaretçi verisi 
Tasarım Özellikleri 
Renkler
Primary: Mavi (#0d6efd)
Success: Yeşil (#198754)
Info: Açık Mavi (#0dcaf0)
Warning: Sarı (#ffc107)
TASARIM
Responsive Tasarım
Grid sistemi ile esnek yerleşim
Kartlar
Gölgeli tasarım (modallar ve bazı bilgi alanları)
Hover efektleri (butonlar, linkler)
İkon entegrasyonu (Bootstrap Icons)
