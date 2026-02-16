
# Dynamic Quiz API dengan Google Gemini

Backend aplikasi Kuis yang canggih, dibangun dengan **Django Ninja**, **PostgreSQL**, dan **Google Gemini AI**.
Backend ini dapat membuat kuis secara dinamis berdasarkan topik apa pun, menilainya secara otomatis, dan menyediakan fitur review (kunci jawaban).

## Fitur Utama

*   **Generasi AI**: Menggunakan Google Gemini 1.5/2.0 Flash untuk membuat soal pilihan ganda dari *topik apa saja*.
*   **Kuis Fleksibel**: Mendukung topik kustom (contoh: "Python", "Sejarah Indonesia") dan jumlah soal yang bisa diatur.
*   **API Aman**: Dibangun dengan Django Ninja untuk performa tinggi (async) dan dokumentasi Swagger UI otomatis.
*   **Integrasi Admin**: Bisa generate kuis langsung dari halaman Django Admin.
*   **Review Kuis**: Endpoint khusus untuk melihat kunci jawaban setelah pengerjaan.
*   **Database**: Penyimpanan data yang robust menggunakan PostgreSQL (via Neon atau lokal).

## Stack Teknologi

*   **Bahasa**: Python 3.12+
*   **Framework**: Django 5.x + Django Ninja
*   **AI Model**: Google Gemini 1.5 Flash (via `google-generativeai`)
*   **Database**: PostgreSQL
*   **Autentikasi**: JWT (JSON Web Tokens) via `ninja-jwt`

## Prasyarat

*   Python 3.10 atau lebih baru
*   Google Gemini API Key ([Dapatkan di sini](https://aistudio.google.com/))
*   PostgreSQL Database URL (contoh: dari Neon.tech)

## Instalasi

1.  **Clone Repository**
    ```bash
    git clone https://github.com/username-anda/quiz-backend.git
    cd quiz-backend
    ```

2.  **Buat Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Di Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi (.env)**
    Buat file `.env` di direktori root:
    ```env
    DEBUG=True
    SECRET_KEY=kunci-rahasia-anda
    DATABASE_URL=postgres://user:pass@host/dbname
    GOOGLE_API_KEY=api-key-gemini-anda
    ```

5.  **Jalankan Migrasi Database**
    ```bash
    python manage.py migrate
    ```

6.  **Buat User Admin (Superuser)**
    ```bash
    python manage.py createsuperuser
    ```

## Menjalankan Aplikasi

Jalankan development server:
```bash
python manage.py runserver 2000
```
Buka Dokumentasi API (Swagger UI) di: **[http://127.0.0.1:2000/api/docs](http://127.0.0.1:2000/api/docs)**

## Ringkasan Endpoint API

| Method | Endpoint | Deskripsi |
| :--- | :--- | :--- |
| **POST** | `/api/quiz/generate/` | Membuat kuis baru (Payload: `topic`, `num_questions`) |
| **POST** | `/api/quiz/{id}/submit/` | Mengirim jawaban dan mendapatkan nilai |
| **GET** | `/api/quiz/{id}/answers/` | Melihat detail kuis **beserta kunci jawaban** (Mode Review) |
| **GET** | `/api/quiz/history/` | Melihat riwayat sesi kuis yang pernah dibuat |
| **POST** | `/api/auth/signup` | Registrasi user baru |
| **POST** | `/api/token/pair` | Login dan mendapatkan Token JWT |

## Fitur Panel Admin

1.  Akses: [http://127.0.0.1:2000/admin/](http://127.0.0.1:2000/admin/)
2.  **Tambah Sesi Kuis (Add Quiz Session)**:
    *   Isi **Topic** (misal: "Javascript Async")
    *   Isi **Target Question Count** (misal: 10)
    *   Klik Save.
3.  **Generate Soal (Generate Questions)**:
    *   Pilih sesi dari daftar (centang kotak di kiri).
    *   Pilih Action: **Generate Questions from Gemini**.
    *   Klik **Go**.

## Lisensi

Proyek ini bersifat open-source dan tersedia di bawah Lisensi MIT.
