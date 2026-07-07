# Canva Learning Dashboard

Dashboard interaktif berbasis Streamlit untuk menganalisis:
1. **Survei penerimaan pengguna Canva** (78 responden, 20 indikator, dikelompokkan ke 4 dimensi: Kemudahan Penggunaan, Manfaat, Kepercayaan, Loyalitas)
2. **Ulasan Google Play Canva** (147 ulasan: rating, sentimen, tren, kata kunci)
3. **Embed laporan Looker Studio** milik project ini

## Menjalankan secara lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

Buka `http://localhost:8501` di browser.

## Membuat dashboard ini PUBLIK (gratis, tanpa server sendiri)

Cara paling mudah adalah **Streamlit Community Cloud**:

1. Buat repository baru di GitHub (bisa public/private), lalu upload seluruh isi folder ini
   (`app.py`, `requirements.txt`, folder `data/`).
2. Buka https://share.streamlit.io → login dengan akun GitHub.
3. Klik **"New app"**, pilih repository dan branch tadi, file utama `app.py`.
4. Klik **Deploy**. Dalam 1–2 menit dashboard akan online dengan URL publik
   seperti `https://nama-app.streamlit.app` yang bisa dibagikan ke siapa saja
   (termasuk dosen) tanpa perlu login.

Alternatif lain: Hugging Face Spaces (pilih SDK "Streamlit") atau Render.com — caranya mirip, tinggal upload file yang sama.

## Agar tab "Laporan Looker Studio" tampil

Laporan Looker Studio hanya bisa di-embed (iframe) jika opsi embed diaktifkan:
1. Buka laporan di Looker Studio → menu **File** → **Embed report**.
2. Centang **"Enable embedding"**.
3. Pastikan akses report di-set **"Anyone with the link can view"**.

Jika langkah ini belum dilakukan, tab tersebut akan tampil kosong/diblokir browser (bukan error dari aplikasi Streamlit-nya).

## Struktur data

- `data/survey.csv` — hasil bersih dari `Salinan_dari_Survey_Canva.xlsx`
- `data/reviews.csv` — hasil bersih dari `Riview_Goggle_Play_Canva.xlsx`

## Catatan

- Pengelompokan 20 pertanyaan survei ke 4 indikator (`INDICATOR_GROUPS` di `app.py`) adalah interpretasi berdasarkan pola nama kolom kuesioner, bukan dari dokumen kodifikasi resmi. Silakan sesuaikan di `app.py` jika ada kodifikasi indikator yang berbeda dari dosen/pembimbing.
- 4 responden dengan usia "0" pada data asli diperlakukan sebagai data kosong (tidak diisi).
