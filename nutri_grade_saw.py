import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# =========================================================================
# ENGINE SPK - METODE SAW MURNI (4 COST, 1 BENEFIT) WITH AUTO-GRADE
# =========================================================================

# Matriks Bobot Preferensi (W)
BOBOT = [0.25, 0.15, 0.25, 0.20, 0.15]

def konversi_gula(gula, pemanis):
    if gula <= 1.0 and pemanis == "Tanpa Pemanis Tambahan": return 1
    elif gula <= 5.0 and pemanis in ["Tanpa Pemanis Tambahan", "Pemanis Alami"]: return 2
    elif gula <= 10.0: return 3
    else: return 4

def konversi_garam(garam):
    if garam <= 5.0: return 1
    elif garam <= 120.0: return 2
    elif garam <= 500.0: return 3
    else: return 4

def konversi_lemak(lemak):
    if lemak <= 0.7: return 1
    elif lemak <= 1.2: return 2
    elif lemak <= 2.8: return 3
    else: return 4

# FUNGSI BARU: Konversi Protein (Benefit: Semakin besar kandungan, skor semakin tinggi)
def konversi_protein(protein):
    if protein <= 2.9: return 1
    elif protein <= 3.1: return 2
    elif protein <= 3.4: return 3
    else: return 4

list_alternatif = []

def tambah_alternatif():
    try:
        nama = entry_varian.get().strip()
        if nama == "" or nama.startswith("Contoh:"):
            messagebox.showwarning("Input Kosong", "Harap masukkan nama merk/varian susu!")
            return
            
        gula = float(entry_gula.get())
        garam = float(entry_garam.get())
        lemak = float(entry_lemak.get())
        protein = float(entry_protein.get())
        harga = float(entry_harga.get())
        pemanis = combo_pemanis.get()
        
        # Proses Standardisasi Seluruh Kriteria ke Skala Ordinal 1-4
        skor_c1 = konversi_gula(gula, pemanis)
        skor_c2 = konversi_garam(garam)
        skor_c3 = konversi_lemak(lemak)
        skor_c4 = konversi_protein(protein) # Terkonversi ke skala 1-4 (Benefit)
        skor_c5 = harga                     # Nilai riil untuk kriteria Cost Harga
        
        list_alternatif.append({
            "nama": nama,
            "skor_matriks": [skor_c1, skor_c2, skor_c3, skor_c4, skor_c5],
            "riil": f"Gula: {gula}g | Garam: {garam}mg | Lemak: {lemak}g | Prot: {protein}g | Rp{int(harga)}"
        })
        
        update_table_view()
        clear_inputs()
        messagebox.showinfo("Sukses", f"Alternatif '{nama}' berhasil masuk matriks keputusan!")
    except ValueError:
        messagebox.showerror("Format Salah", "Harap masukkan angka numerik desimal yang valid!")

def hitung_saw():
    if len(list_alternatif) < 2:
        messagebox.showwarning("Data Kurang", "Tambahkan minimal 2 alternatif untuk membandingkan!")
        return
    
    n_alternatif = len(list_alternatif)
    
    # LANGKAH 1: Ambil nilai ekstrem limit kriteria (C4=MAX, Lainnya=MIN)
    limit_kriteria = []
    for j in range(5):
        nilai_kolom = [list_alternatif[i]["skor_matriks"][j] for i in range(n_alternatif)]
        if j == 3:
            limit_kriteria.append(max(nilai_kolom)) # MAX untuk Protein Benefit
        else:
            limit_kriteria.append(min(nilai_kolom)) # MIN untuk kriteria Cost
        
    # LANGKAH 2 & 3: Normalisasi dan Perhitungan V
    hasil_perangkingan = []
    for i in range(n_alternatif):
        v_total = 0
        for j in range(5):
            if j == 3:
                r_ij = list_alternatif[i]["skor_matriks"][j] / limit_kriteria[j] # Benefit
            else:
                r_ij = limit_kriteria[j] / list_alternatif[i]["skor_matriks"][j] # Cost
            v_total += BOBOT[j] * r_ij
            
        hasil_perangkingan.append({
            "nama": list_alternatif[i]["nama"],
            "v_score": round(v_total, 4),
            "riil": list_alternatif[i]["riil"]
        })
        
    # LANGKAH 4: Perangkingan
    hasil_perangkingan.sort(key=lambda x: x["v_score"], reverse=True)
    
    # Cetak ke Dashboard Output dengan Informasi Tingkat Kelayakan Grade
    txt_output.delete("1.0", tk.END)
    txt_output.insert(tk.END, f"======= HASIL REKOMENDASI PERANGKINGAN SAW =======\n")
    txt_output.insert(tk.END, f"Kriteria Terintegrasi: GGL Kemenkes, Protein & Harga\n")
    txt_output.insert(tk.END, f"--------------------------------------------------\n\n")
    
    for rank, item in enumerate(hasil_perangkingan, 1):
        medal = "👑 [REKOMENDASI 1]" if rank == 1 else f"[{rank}]"
        
        # Logika Penentuan Grade Kemenkes Subjektif Berdasarkan Skor Akumulasi V
        if item['v_score'] >= 0.88:
            grade_level = "GRADE A (Sangat Aman & Tinggi Protein)"
        elif item['v_score'] >= 0.75:
            grade_level = "GRADE B (Aman / Konsumsi Harian Standar)"
        elif item['v_score'] >= 0.60:
            grade_level = "GRADE C (Cukup Aman / Batasi Konsumsi Berlebih)"
        else:
            grade_level = "GRADE D (Kurang Direkomendasikan)"
            
        txt_output.insert(tk.END, f"{medal} {item['nama']}\n")
        txt_output.insert(tk.END, f"   ▶ Skor Preferensi (V) : {item['v_score']}\n")
        txt_output.insert(tk.END, f"   ▶ Standar Kelayakan   : {grade_level}\n")
        txt_output.insert(tk.END, f"   ▶ Informasi Nilai Gizi: {item['riil']}\n\n")

def reset_sistem():
    list_alternatif.clear()
    update_table_view()
    txt_output.delete("1.0", tk.END)
    txt_output.insert(tk.END, "Matriks keputusan dikosongkan.")

def update_table_view():
    listbox_alt.delete(0, tk.END)
    for idx, alt in enumerate(list_alternatif, 1):
        listbox_alt.insert(tk.END, f"{idx}. {alt['nama']} | {alt['riil']}")

def clear_inputs():
    entry_varian.delete(0, tk.END)
    entry_gula.delete(0, tk.END)
    entry_garam.delete(0, tk.END)
    entry_lemak.delete(0, tk.END)
    entry_protein.delete(0, tk.END)
    entry_harga.delete(0, tk.END)

# =========================================================================
# LAYOUT ANTARMUKA (GUI PANEL)
# =========================================================================
root = tk.Tk()
root.title("SPK Kelayakan Susu UHT Low Fat - Auto Grade SAW")
root.geometry("960x600")
root.resizable(False, False)

frame_input = tk.LabelFrame(root, text=" Form Entri Kandungan Gizi & Harga ", font=("Arial", 9, "bold"), padx=10, pady=5)
frame_input.place(x=20, y=15, width=440, height=380)

fields = [
    ("Nama Merk & Varian Susu:", "entry_varian"),
    ("Kandungan Gula (g/100mL):", "entry_gula"),
    ("Natrium/Garam (mg/100mL):", "entry_garam"),
    ("Lemak Jenuh (g/100mL):", "entry_lemak"),
    ("Kandungan Protein (g/100mL):", "entry_protein"),
    ("Harga Jual Toko (Rp):", "entry_harga")
]

for idx, (label_text, var_name) in enumerate(fields):
    tk.Label(frame_input, text=label_text).grid(row=idx, column=0, sticky="w", pady=5)
    entry = tk.Entry(frame_input, width=24, font=("Arial", 9))
    entry.grid(row=idx, column=1, pady=5)
    globals()[var_name] = entry

tk.Label(frame_input, text="Karakteristik Pemanis:").grid(row=6, column=0, sticky="w", pady=5)
combo_pemanis = ttk.Combobox(frame_input, values=["Tanpa Pemanis Tambahan", "Pemanis Alami", "Pemanis Buatan"], width=22, state="readonly")
combo_pemanis.set("Tanpa Pemanis Tambahan")
combo_pemanis.grid(row=6, column=1, pady=5)

btn_tambah = tk.Button(frame_input, text="➕ SIMPAN DATA KE MATRIKS KEPUTUSAN", command=tambah_alternatif, bg="#2E7D32", fg="white", font=("Arial", 9, "bold"))
btn_tambah.grid(row=7, column=0, columnspan=2, pady=12, sticky="we")

frame_list = tk.LabelFrame(root, text=" Antrean Alternatif Sementara Berhasil Masuk ", font=("Arial", 9, "bold"), padx=10, pady=5)
frame_list.place(x=20, y=405, width=440, height=170)

listbox_alt = tk.Listbox(frame_list, font=("Arial", 8), bg="#FFFDE7")
listbox_alt.pack(fill="both", expand=True)

frame_output = tk.LabelFrame(root, text=" Output Perangkingan Akhir & Penentuan Grade Level ", font=("Arial", 9, "bold"), padx=10, pady=10)
frame_output.place(x=480, y=15, width=450, height=460)

txt_output = tk.Text(frame_output, font=("Consolas", 9), bg="#F8F9FA", wrap=tk.WORD)
txt_output.insert(tk.END, "Masukkan ke-15 data sampel susu UHT Low Fat Anda di panel sebelah kiri, lalu jalankan metode SAW.")
txt_output.pack(fill="both", expand=True)

btn_hitung = tk.Button(root, text="🚀 JALANKAN METODE SAW & CEK GRADE", command=hitung_saw, bg="#1565C0", fg="white", font=("Arial", 10, "bold"))
btn_hitung.place(x=480, y=490, width=280, height=45)

btn_reset = tk.Button(root, text="🔄 Reset Matriks", command=reset_sistem, bg="#C62828", fg="white", font=("Arial", 10, "bold"))
btn_reset.place(x=775, y=490, width=155, height=45)

root.mainloop()
