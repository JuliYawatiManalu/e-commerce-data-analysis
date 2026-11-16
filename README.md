# E-Commerce Data Analysis Dashboard

## Deskripsi Proyek

Proyek ini merupakan analisis data e-commerce menggunakan dataset Brazilian E-Commerce Public Dataset by Olist. Proyek bertujuan untuk memahami performa penjualan, pola penggunaan metode pembayaran, serta karakteristik pelanggan berdasarkan data transaksi e-commerce.

Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan Streamlit agar informasi dapat dipahami dengan lebih mudah melalui visualisasi data.

## Tujuan Analisis

Proyek ini berfokus pada dua pertanyaan bisnis utama:

### Business Question 1
Kategori produk mana yang menyumbang pendapatan terbesar pada Januari-Agustus 2018, dan bagaimana pertumbuhannya dibandingkan Januari-Agustus 2017?

Analisis dilakukan dengan melihat pendapatan produk berdasarkan kategori, membandingkan pendapatan pada kedua periode, serta mengamati tren pendapatan setiap bulan.

### Business Question 2
Bagaimana komposisi dan tren penggunaan metode pembayaran pelanggan setiap bulan, serta bagaimana perbedaan rata-rata nilai pembayaran dan jumlah cicilan berdasarkan metode pembayaran selama Januari 2017 hingga Agustus 2018?

Analisis dilakukan untuk memahami distribusi metode pembayaran, perubahan penggunaannya setiap bulan, rata-rata nilai pembayaran, dan jumlah cicilan berdasarkan metode pembayaran.

## Analisis Lanjutan

Selain menjawab pertanyaan bisnis utama, proyek ini juga melakukan analisis lanjutan menggunakan beberapa teknik:

- **Binning:** Mengelompokkan pesanan berdasarkan rentang total nilai pembayaran.
- **Manual Grouping:** Mengelompokkan metode pembayaran dan jumlah cicilan untuk melihat pola transaksi berdasarkan kelompok nilai pesanan.
- **RFM Analysis:** Mengelompokkan pelanggan berdasarkan Recency, Frequency, dan Monetary untuk memahami aktivitas dan nilai transaksi pelanggan.

## Dataset

Dataset yang digunakan berasal dari Brazilian E-Commerce Public Dataset by Olist.

Enam file dataset yang digunakan dalam dashboard:

1. `orders_dataset.csv`
2. `order_items_dataset.csv`
3. `products_dataset.csv`
4. `product_category_name_translation.csv`
5. `order_payments_dataset.csv`
6. `customers_dataset.csv`

Dataset sumber disimpan dalam folder `data/` dan digunakan sebagai input notebook serta dashboard. Notebook tidak menimpa dataset sumber. Hasil proses cleaning disimpan secara terpisah di folder `cleaned_data/` yang dibuat otomatis ketika notebook dijalankan.

## Teknologi yang Digunakan

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit

## Struktur Folder

```text
E-Commerce Analysis/
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── products_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── order_payments_dataset.csv
│   └── customers_dataset.csv
│
├── README.md
├── requirements.txt
├── .gitignore
└── url.txt
```

## Cara Menjalankan Dashboard

Pastikan Python sudah terpasang pada perangkat.

1. Clone repository:

```bash
git clone <URL-REPOSITORY>
```

2. Masuk ke folder proyek:

```bash
cd "E-Commerce Analysis"
```

3. Buat dan aktifkan virtual environment (opsional):

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

4. Install library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

5. Jalankan dashboard:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka melalui browser menggunakan alamat lokal yang diberikan oleh Streamlit.

## Dashboard

Dashboard dikembangkan menggunakan Streamlit dan menyediakan visualisasi interaktif untuk membantu pengguna memahami hasil analisis data e-commerce.

**Link Dashboard:** (https://e-commerce-data-analysis-abvyueid9u7kaywa5z86jd.streamlit.app/)