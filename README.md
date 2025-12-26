# Sistem Donasi Flask

Aplikasi web sistem donasi berbasis Flask dengan autentikasi multi-role (Admin & Donor), manajemen campaign, dan pencatatan donasi.

## 🚀 Fitur

### Admin

- ✅ Dashboard dengan statistik (total campaign, donasi, donatur)
- ✅ CRUD Campaign (Create, Read, Update, Delete)
- ✅ Lihat semua donasi dari semua donatur

### Donor

- ✅ Registrasi akun baru
- ✅ Login/Logout
- ✅ Lihat daftar campaign aktif
- ✅ Melakukan donasi ke campaign
- ✅ Lihat riwayat donasi pribadi

## 🛠️ Teknologi

- **Backend**: Flask (Python)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Password Hashing**: Werkzeug

## 📦 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/sasamaylina/responsi-paw.git
cd responsi-paw
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
python run.py
```

Aplikasi akan berjalan di: `http://127.0.0.1:5000`

## 👤 Akun Default

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |

## 📁 Struktur Proyek

```
donasi/
├── app/
│   ├── __init__.py          # Inisialisasi Flask app
│   ├── models.py            # Model database (User, Campaign, Donation)
│   ├── forms.py             # Form validasi (Login, Register, Campaign, Donation)
│   ├── routes/
│   │   ├── auth.py          # Route autentikasi (login, register, logout)
│   │   ├── admin.py         # Route admin (dashboard, campaigns, donations)
│   │   └── donor.py         # Route donor (dashboard, donate, history)
│   ├── templates/
│   │   ├── base.html        # Template dasar
│   │   ├── auth/            # Template autentikasi
│   │   ├── admin/           # Template admin
│   │   └── donor/           # Template donor
│   └── static/
│       └── css/
│           └── style.css    # Stylesheet
├── config.py                # Konfigurasi aplikasi
├── run.py                   # Entry point aplikasi
├── requirements.txt         # Dependencies
└── README.md
```

## 📸 Screenshots

### Login Page

![Login](docs/login.png)

### Admin Dashboard

![Admin Dashboard](docs/admin-dashboard.png)

### Donor Dashboard

![Donor Dashboard](docs/donor-dashboard.png)

## 📝 API Endpoints

### Authentication

| Method | Endpoint   | Deskripsi           |
|--------|------------|---------------------|
| GET    | /login     | Halaman login       |
| POST   | /login     | Proses login        |
| GET    | /register  | Halaman registrasi  |
| POST   | /register  | Proses registrasi   |
| GET    | /logout    | Logout user         |

### Admin

| Method | Endpoint              | Deskripsi              |
|--------|-----------------------|------------------------|
| GET    | /admin/               | Dashboard admin        |
| GET    | /admin/campaigns      | Daftar campaign        |
| GET    | /admin/campaigns/create | Form buat campaign   |
| POST   | /admin/campaigns/create | Simpan campaign baru |
| GET    | /admin/campaigns/edit/:id | Form edit campaign |
| POST   | /admin/campaigns/edit/:id | Update campaign    |
| POST   | /admin/campaigns/delete/:id | Hapus campaign   |
| GET    | /admin/donations      | Semua donasi           |

### Donor

| Method | Endpoint           | Deskripsi              |
|--------|--------------------|------------------------|
| GET    | /donor/            | Dashboard donor        |
| GET    | /donor/donate/:id  | Form donasi            |
| POST   | /donor/donate/:id  | Proses donasi          |
| GET    | /donor/history     | Riwayat donasi         |

## 📄 Lisensi

MIT License

## 👨‍💻 Author

[sasamaylina](https://github.com/sasamaylina)
