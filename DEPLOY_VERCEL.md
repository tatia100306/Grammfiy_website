Panduan singkat: Deploy Django ke Vercel (untuk repo ini)

Ringkasan
- Saya sudah menambahkan `vercel.json` dan `api/wsgi.py` di repo.
- Langkah berikut membuat deploy di Vercel jadi mudah: push repo → import di Vercel → set Environment Variables → Deploy → jalankan migrate lokal.

1) Pastikan kode sudah di-push ke GitHub
```bash
git add .
git commit -m "ready for vercel"
git push origin main
```

> Untuk lokal development, letakkan file `.env` di root proyek yang sama dengan `manage.py`.
> Jika .env Anda saat ini berada di `langlearn_project/langlearn_project/.env`, settings sekarang juga akan memuatnya.

2) Siapkan database Postgres eksternal
- Pilih Supabase / Railway / ElephantSQL / RDS.
- Catat `DATABASE_URL` (format: `postgres://user:pass@host:port/dbname`).

3) Import repo di Vercel (Web UI)
- Buka https://vercel.com/new lalu pilih repo Anda.
- Application Preset: pilih `Django`.
- Root Directory: `./` (kalau `manage.py` ada di root)
- Install Command: `pip install -r requirements.txt`
- Build Command: `python -u manage.py collectstatic --noinput`
- Output Directory: kosong (N/A)

4) Tambahkan Environment Variables di Vercel (Project → Settings → Environment Variables)
- `DJANGO_SECRET_KEY` = (generate random)
- `DJANGO_DEBUG` = `False`
- `DJANGO_ALLOWED_HOSTS` = `<your-project>.vercel.app` (atau `*` sementara)
- `DATABASE_URL` = `postgres://...`
- `GROQ_API_KEY` = (jika diperlukan)
- `GEMINI_API_KEY` = (jika diperlukan)

Catatan: Anda bisa juga mengimpor file `.env` di UI jika sudah punya.

5) Jalankan migrasi (dari mesin lokal Anda)
- Pastikan `DATABASE_URL` dan env lain tersedia secara lokal (mis. simpan ke `.env`, atau export sebelum run)
```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # opsional
```

6) Deploy
- Di Vercel UI: klik Deploy setelah import & env diset.
- Atau CLI (jika sudah menginstall `vercel`): `vercel --prod`.

7) Troubleshooting cepat
- Jika error DB: periksa `DATABASE_URL` dan apakah DB menerima koneksi eksternal.
- Jika static tidak muncul: periksa `collectstatic` output di logs, dan pastikan `whitenoise` ada (sudah di requirements).
- Jika ada error terkait `GROQ_API_KEY`: pastikan env `GROQ_API_KEY` di-set (settings kini hanya me-raise error saat `DEBUG=False`).

Opsional: Auto-deploy + migrate via GitHub Actions
- Jika Anda ingin otomatisasi (deploy + migrate), tambahkan secret `VERCEL_TOKEN` ke GitHub dan buat workflow seperti di bawah.

Contoh `.github/workflows/vercel-deploy.yml` (opsional):
```
name: Deploy to Vercel
on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: python -m pip install -r requirements.txt
      - name: Run migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          python manage.py migrate --noinput
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```
- Secrets yang diperlukan: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`, `DATABASE_URL`.

Selesai — setelah Anda tekan Deploy di Vercel, beri tahu saya hasilnya atau kirim error log jika ada, saya bantu perbaiki.
