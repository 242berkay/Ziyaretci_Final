from flask import Flask, redirect, url_for, render_template, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gelistirme_anahtari'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'giris'  # Genel login sayfası

# Kullanıcı modeli (admin ve ziyaretçi)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    rezervasyonlar = db.relationship('Visitor', backref='kullanici', lazy=True)

# Ziyaretçi modeli (adminin kaydettiği ziyaretçiler ve kullanıcıların rezervasyonları)
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    ziyaret_saati = db.Column(db.String(5), nullable=False)  # Saat:dakika string
    ziyaret_suresi = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def ana_sayfa():
    return render_template('index.html')

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_paneli'))
        else:
            return redirect(url_for('kayitli_kullanici'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            flash('Lütfen tüm alanları doldurun.', 'warning')
            return redirect(url_for('ana_sayfa'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Geçerli bir e-posta giriniz.', 'warning')
            return redirect(url_for('ana_sayfa'))

        if User.query.filter_by(email=email).first():
            flash('Bu e-posta zaten kayıtlı.', 'danger')
            return redirect(url_for('ana_sayfa'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        yeni_kullanici = User(name=name, email=email, password=hashed_password, is_admin=False)
        db.session.add(yeni_kullanici)
        db.session.commit()
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('giris'))

    return redirect(url_for('ana_sayfa'))

@app.route('/giris', methods=['GET', 'POST'])
def giris():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_paneli'))
        else:
            return redirect(url_for('kayitli_kullanici'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and not user.is_admin and check_password_hash(user.password, password):
            login_user(user)
            flash('Giriş başarılı.', 'success')
            return redirect(url_for('kayitli_kullanici'))
        else:
            flash('Geçersiz e-posta veya şifre.', 'danger')
            return redirect(url_for('ana_sayfa'))

    return redirect(url_for('ana_sayfa'))

@app.route('/admin/giris', methods=['GET', 'POST'])
def admin_giris():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_paneli'))
        else:
            logout_user()
            return redirect(url_for('admin_giris'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, is_admin=True).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Admin girişi başarılı.', 'success')
            return redirect(url_for('admin_paneli'))
        else:
            flash('Geçersiz admin e-posta veya şifre.', 'danger')
            return redirect(url_for('admin_giris'))

    return render_template('admin_giris.html')

@app.route('/admin/panel')
@login_required
def admin_paneli():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('ana_sayfa'))
    return render_template('admin_paneli.html', name=current_user.name)

@app.route('/kayitli_kullanici')
@login_required
def kayitli_kullanici():
    if current_user.is_admin:
        return redirect(url_for('admin_paneli'))
    rezervasyonlar = current_user.rezervasyonlar
    return render_template('kayitli_kullanici.html', name=current_user.name, email=current_user.email, rezervasyonlar=rezervasyonlar)

@app.route('/cikis')
@login_required
def cikis():
    logout_user()
    flash('Başarıyla çıkış yapıldı.', 'success')
    return redirect(url_for('ana_sayfa'))

# Yeni ziyaretçi kaydı formu (admin için)
@app.route('/kayit_formu', methods=['GET', 'POST'])
@login_required
def kayit_formu():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('ana_sayfa'))

    if request.method == 'POST':
        ad = request.form.get('ad')
        soyad = request.form.get('soyad')
        ziyaret_saati = request.form.get('ziyaret_saati')
        ziyaret_suresi = request.form.get('ziyaret_suresi')

        if not ad or not soyad or not ziyaret_saati:
            flash('Lütfen zorunlu alanları doldurun.', 'warning')
            return redirect(url_for('kayit_formu'))

        try:
            ziyaret_suresi = int(ziyaret_suresi) if ziyaret_suresi else None
        except ValueError:
            flash('Ziyaret süresi sayı olmalı.', 'warning')
            return redirect(url_for('kayit_formu'))

        yeni_ziyaretci = Visitor(
            ad=ad,
            soyad=soyad,
            ziyaret_saati=ziyaret_saati,
            ziyaret_suresi=ziyaret_suresi
        )
        db.session.add(yeni_ziyaretci)
        db.session.commit()

        flash('Yeni ziyaretçi başarıyla kaydedildi.', 'success')
        return redirect(url_for('admin_paneli'))

    return render_template('kayit_formu.html')

@app.route('/listele')
@login_required
def listele():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('ana_sayfa'))

    ziyaretciler = Visitor.query.all()
    return render_template('listele.html', ziyaretciler=ziyaretciler)

@app.route('/guncelle/<int:ziyaretci_id>', methods=['GET', 'POST'])
@login_required
def guncelle_formu(ziyaretci_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('ana_sayfa'))

    ziyaretci = Visitor.query.get_or_404(ziyaretci_id)

    if request.method == 'POST':
        ad = request.form.get('ad')
        soyad = request.form.get('soyad')
        ziyaret_saati = request.form.get('ziyaret_saati')
        ziyaret_suresi = request.form.get('ziyaret_suresi')

        if not ad or not soyad or not ziyaret_saati:
            flash('Lütfen zorunlu alanları doldurun.', 'warning')
            return render_template('guncelleformu.html', ziyaretci=ziyaretci)

        try:
            ziyaret_suresi = int(ziyaret_suresi) if ziyaret_suresi else None
        except ValueError:
            flash('Ziyaret süresi sayı olmalı.', 'warning')
            return render_template('guncelleformu.html', ziyaretci=ziyaretci)

        ziyaretci.ad = ad
        ziyaretci.soyad = soyad
        ziyaretci.ziyaret_saati = ziyaret_saati
        ziyaretci.ziyaret_suresi = ziyaret_suresi
        db.session.commit()
        flash('Ziyaretçi bilgileri başarıyla güncellendi.', 'success')
        return redirect(url_for('listele'))

    return render_template('guncelleformu.html', ziyaretci=ziyaretci)

@app.route('/sil/<int:ziyaretci_id>')
@login_required
def sil(ziyaretci_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('ana_sayfa'))

    ziyaretci = Visitor.query.get_or_404(ziyaretci_id)
    db.session.delete(ziyaretci)
    db.session.commit()
    flash('Ziyaretçi başarıyla silindi.', 'success')
    return redirect(url_for('listele'))

@app.route('/filtrele', methods=['GET', 'POST'])
@login_required
def filtrele():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('ana_sayfa'))

    ziyaretciler = Visitor.query.all()  # Sayfa ilk açıldığında tüm ziyaretçileri getir
    filtre = ""

    if request.method == 'POST':
        filtre = request.form.get('filtre', '')
        ziyaretciler = Visitor.query.filter(db.or_(Visitor.ad.contains(filtre), Visitor.soyad.contains(filtre))).all()

    return render_template('filtrele.html', ziyaretciler=ziyaretciler, filtre=filtre)

@app.route('/kayitli_ziyaretciler')
@login_required
def kayitli_ziyaretciler():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('ana_sayfa'))
    ziyaretciler = User.query.filter_by(is_admin=False).all()
    return render_template('kayitli_ziyaretciler.html', ziyaretciler=ziyaretciler)

# --- Buraya rezervasyon kayıt endpoint'i eklendi ---
@app.route('/rezervasyon', methods=['GET'])
def rezervasyon_formu():
    return render_template('rezervasyon_formu.html')

@app.route('/rezervasyon_kaydet', methods=['POST'])
def rezervasyon_kaydet():
    ad = request.form.get('ad')
    soyad = request.form.get('soyad')
    ziyaret_saati = request.form.get('ziyaret_saati')
    ziyaret_suresi = request.form.get('ziyaret_suresi')

    if not ad or not soyad or not ziyaret_saati:
        flash('Lütfen zorunlu alanları doldurun.', 'warning')
        return redirect(url_for('ana_sayfa'))

    try:
        ziyaret_suresi = int(ziyaret_suresi) if ziyaret_suresi else None
    except ValueError:
        flash('Ziyaret süresi sayı olmalı.', 'warning')
        return redirect(url_for('ana_sayfa'))

    yeni_ziyaretci = Visitor(
        ad=ad,
        soyad=soyad,
        ziyaret_saati=ziyaret_saati,
        ziyaret_suresi=ziyaret_suresi,
        user_id=current_user.id if current_user.is_authenticated else None
    )
    db.session.add(yeni_ziyaretci)
    db.session.commit()

    flash('Rezervasyon başarıyla kaydedildi.', 'success')
    return redirect(url_for('ana_sayfa'))

@app.route('/api/kullanici_durumu')
def kullanici_durumu():
    return jsonify({'giris_yapildi': current_user.is_authenticated and not current_user.is_admin})

@app.route('/api/flash_messages')
def get_flash_messages():
    messages = []
    if '_flashes' in session:
        for category, message in session['_flashes']:
            messages.append({'category': category, 'message': message})
    return jsonify({'messages': messages})

@app.route('/api/clear_flash_messages')
def clear_flash_messages():
    if '_flashes' in session:
        session['_flashes'].clear()
    return jsonify({'status': 'success'})

@app.route('/kayitli_kullanici/<int:kullanici_id>')
@login_required
def kayitli_kullanici_detay(kullanici_id):
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('ana_sayfa'))
    kullanici = User.query.get_or_404(kullanici_id)
    return render_template('kayitli_kullanici_detay.html', kullanici=kullanici)

if __name__ == '__main__':
  
    app.run(debug=True)