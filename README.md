# Nutri_Level_SAW
# SPK Kelayakan Susu UHT Low Fat - Metode SAW (Auto-Grade)

Sistem Pendukung Keputusan (SPK) berbasis desktop ini dikembangkan menggunakan bahasa pemrograman **Python** dan pustaka **Tkinter (GUI)**. Sistem ini dirancang untuk mengotomatisasi proses evaluasi dan perangkingan kelayakan konsumsi produk susu UHT kategori *Low Fat* / *Skim Milk* lintas merk di Indonesia menggunakan metode **Simple Additive Weighting (SAW)**.

Model evaluasi pada sistem ini mengintegrasikan regulasi batasan zat gizi kritis (Gula, Garam, Lemak Jenuh) berdasarkan standar **Nutri-Level Kementerian Kesehatan RI**, akumulasi makronutrisi (Protein), serta variabel ekonomi (Harga Produk).

---

## 🚀 Fitur Utama Perangkat Lunak

* **Dynamic User-Driven Input:** Menggunakan komponen pengetikan bebas (`tk.Entry`) yang memungkinkan pengguna memasukkan hingga 15 varian sampel secara fleksibel dan skalabel tanpa batasan jumlah alternatif.
* **Hybrid Normalization Handler:** Mesin komputasi yang mampu memproses kriteria multivariat secara simultan, menerapkan fungsi *Cost* untuk meminimalkan zat gizi kritis & harga, serta fungsi *Benefit* untuk memaksimalkan kandungan Protein.
* **Intelligent Auto-Grading Dashboard:** Mentransformasikan hasil kalkulasi numerik desimal $V_i$ menjadi predikat kelayakan mutu produk secara otomatis (**GRADE A, B, C, dan D**).
* **In-Memory Data Queue View:** Integrasi komponen `tk.Listbox` sebagai penampung antrean data temporer sebelum proses kalkulasi final dieksekusi.
* **Safety Reset Controller:** Fitur tombol `Clear All` untuk membersihkan memori matriks keputusan secara instan tanpa harus memuat ulang program dari IDE.

---

## 📊 Pemodelan Kriteria & Bobot SAW

Sistem ini menggunakan 5 kriteria terikat dengan total bobot preferensi ($W$) bernilai 1.0 (100%):

| Kode | Nama Kriteria | Sifat Atribut | Bobot Preferensi ($W_j$) | Skala Konversi |
| :---: | :--- | :---: | :---: | :---: |
| **C1** | Kandungan Gula (g/100mL) | *Cost* (Semakin kecil semakin baik) | 0.25 (25%) | Skor 1 - 4 |
| **C2** | Natrium / Garam (mg/100mL) | *Cost* (Semakin kecil semakin baik) | 0.15 (15%) | Skor 1 - 4 |
| **C3** | Lemak Jenuh (g/100mL) | *Cost* (Semakin kecil semakin baik) | 0.25 (25%) | Skor 1 - 4 |
| **C4** | Kandungan Protein (g/100mL) | *Benefit* (Semakin besar semakin baik) | 0.20 (20%) | Skor 1 - 4 |
| **C5** | Harga Jual Toko (Rp) | *Cost* (Semakin murah semakin ekonomis) | 0.15 (15%) | Nilai Riil Nominal |

---

## 🛠️ Logika Transformasi Nilai (Scoring Engine)

Sebelum matriks dinormalisasi, data kontinu dari kemasan dikonversikan menjadi data ordinal (Skor 1-4) melalui aturan pengkondisian berikut:

### Kriteria Gula (C1) & Karakteristik Pemanis
* $\le 1.0\text{ g}$ & Tanpa Pemanis Tambahan $\rightarrow$ **Skor 1** (Grade A)
* $> 1.0 - 5.0\text{ g}$ & Pemanis Alami / Tanpa Pemanis $\rightarrow$ **Skor 2** (Grade B)
* $> 5.0 - 10.0\text{ g}$ $\rightarrow$ **Skor 3** (Grade C)
* $> 10.0\text{ g}$ $\rightarrow$ **Skor 4** (Grade D)

### Kriteria Garam / Natrium (C2)
* $\le 5.0\text{ mg}$ $\rightarrow$ **Skor 1**
* $> 5.0 - 120.0\text{ mg}$ $\rightarrow$ **Skor 2**
* $> 120.0 - 500.0\text{ mg}$ $\rightarrow$ **Skor 3**
* $> 500.0\text{ mg}$ $\rightarrow$ **Skor 4**

### Kriteria Lemak Jenuh (C3)
* $\le 0.7\text{ g}$ $\rightarrow$ **Skor 1**
* $> 0.7 - 1.2\text{ g}$ $\rightarrow$ **Skor 2**
* $> 1.2 - 2.8\text{ g}$ $\rightarrow$ **Skor 3**
* $> 2.8\text{ g}$ $\rightarrow$ **Skor 4**

### Kriteria Protein (C4)
* $\le 2.9\text{ g}$ $\rightarrow$ **Skor 1** (Rendah)
* $3.0 - 3.1\text{ g}$ $\rightarrow$ **Skor 2** (Standar)
* $3.2 - 3.4\text{ g}$ $\rightarrow$ **Skor 3** (Tinggi)
* $\ge 3.5\text{ g}$ $\rightarrow$ **Skor 4** (Sangat Tinggi)

---

## 💻 Persyaratan Sistem & Cara Menjalankan

### Prasyarat (Prerequisites)
Pastikan perangkat Anda telah terinstal **Python 3.x**. Aplikasi ini hanya menggunakan pustaka bawaan Python (*built-in standard library*), sehingga tidak memerlukan instalasi `pip` tambahan.

### Langkah Menjalankan Aplikasi
1. *Clone* repositori ini ke penyimpanan lokal Anda:
   ```bash
   git clone [https://github.com/username-anda/nama-repositori.git](https://github.com/username-anda/nama-repositori.git)
