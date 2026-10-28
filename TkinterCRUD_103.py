import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("prediksi_diabetes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pasien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pasien TEXT NOT NULL,
    usia INTEGER NOT NULL,
    gula_darah REAL NOT NULL,
    bmi REAL NOT NULL,
    riwayat_ortu TEXT NOT NULL,
    hasil_prediksi TEXT NOT NULL
)
""")
conn.commit()


def prediksi_diabetes(gula, bmi, riwayat):
    if gula >= 200:
        if bmi >= 30 and riwayat == "Ya":
            return "Sangat Tinggi"
        return "Tinggi"

    elif gula >= 140:
        if bmi >= 30 and riwayat == "Ya":
            return "Tinggi"
        return "Sedang"

    else:
        if bmi >= 30:
            if riwayat == "Ya":
                return "Sedang"
            return "Waspada"

        elif riwayat == "Ya":
            return "Waspada"

        else:
            return "Rendah"


def simpan_data():
    nama = entry_nama.get().strip()
    usia_text = entry_usia.get().strip()
    gula_text = entry_gula.get().strip()
    bmi_text = entry_bmi.get().strip()
    riwayat = combo_riwayat.get()

    # Validasi input
    if not nama or not usia_text or not gula_text or not bmi_text:
        messagebox.showwarning("Peringatan", "Semua data wajib diisi!")
        return

    if not usia_text.isdigit():
        messagebox.showerror("Error", "Usia harus berupa bilangan bulat!")
        return

    try:
        usia = int(usia_text)
        gula = float(gula_text)
        bmi = float(bmi_text)

        if usia < 1 or usia > 120:
            messagebox.showerror("Error", "Usia harus 1-120 tahun!")
            return

        if gula <= 0 or gula > 1000:
            messagebox.showerror(
                "Error", "Gula darah harus lebih dari 0 hingga 1000!"
            )
            return

        if bmi < 10 or bmi > 100:
            messagebox.showerror("Error", "BMI harus antara 10-100!")
            return

        if riwayat not in ["Ya", "Tidak"]:
            messagebox.showwarning(
                "Peringatan", "Pilih riwayat diabetes orang tua!"
            )
            return

      
        hasil = prediksi_diabetes(gula, bmi, riwayat)

  
        cursor.execute("""
            INSERT INTO pasien
            (nama_pasien, usia, gula_darah, bmi,
             riwayat_ortu, hasil_prediksi)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nama, usia, gula, bmi, riwayat, hasil))

        conn.commit()

        warna = {
            "Rendah": "green",
            "Waspada": "blue",
            "Sedang": "orange",
            "Tinggi": "red",
            "Sangat Tinggi": "darkred"
        }

        label_hasil.config(
            text=f"Hasil Prediksi: {hasil}",
            fg=warna[hasil]
        )

        messagebox.showinfo(
            "Berhasil", "Data pasien berhasil disimpan!"
        )

    except ValueError:
        messagebox.showerror(
            "Error", "Gula darah dan BMI harus berupa angka!"
        )

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def lihat_data():
    jendela = tk.Toplevel(root)
    jendela.title("Riwayat Data Pasien")
    jendela.geometry("950x350")

    kolom = (
        "ID", "Nama", "Usia", "Gula Darah",
        "BMI", "Riwayat Orang Tua", "Hasil Prediksi"
    )

    tabel = ttk.Treeview(
        jendela, columns=kolom, show="headings"
    )

    for nama_kolom in kolom:
        tabel.heading(nama_kolom, text=nama_kolom)
        tabel.column(nama_kolom, width=125, anchor="center")

    tabel.pack(fill="both", expand=True, padx=10, pady=10)
    
    cursor.execute("""
        SELECT id, nama_pasien, usia, gula_darah,
               bmi, riwayat_ortu, hasil_prediksi
        FROM pasien
        ORDER BY id DESC
    """)

    for data in cursor.fetchall():
        tabel.insert("", tk.END, values=data)


root = tk.Tk()
root.title("Aplikasi Prediksi Risiko Diabetes")
root.geometry("500x570")
root.resizable(False, False)

tk.Label(
    root,
    text="PREDIKSI RISIKO DIABETES",
    font=("Arial", 16, "bold")
).pack(pady=20)

# Form input pasien
form = tk.Frame(root)
form.pack(pady=5)

tk.Label(form, text="Nama Pasien").grid(
    row=0, column=0, sticky="w", padx=10, pady=8
)
entry_nama = tk.Entry(form, width=25)
entry_nama.grid(row=0, column=1, pady=8)

tk.Label(form, text="Usia (tahun)").grid(
    row=1, column=0, sticky="w", padx=10, pady=8
)
entry_usia = tk.Entry(form, width=25)
entry_usia.grid(row=1, column=1, pady=8)

tk.Label(form, text="Gula Darah (mg/dL)").grid(
    row=2, column=0, sticky="w", padx=10, pady=8
)
entry_gula = tk.Entry(form, width=25)
entry_gula.grid(row=2, column=1, pady=8)

tk.Label(form, text="BMI").grid(
    row=3, column=0, sticky="w", padx=10, pady=8
)
entry_bmi = tk.Entry(form, width=25)
entry_bmi.grid(row=3, column=1, pady=8)

tk.Label(form, text="Riwayat Diabetes Orang Tua").grid(
    row=4, column=0, sticky="w", padx=10, pady=8
)
combo_riwayat = ttk.Combobox(
    form, values=["Ya", "Tidak"],
    state="readonly", width=22
)
combo_riwayat.grid(row=4, column=1, pady=8)
combo_riwayat.set("Tidak")

tk.Button(
    root,
    text="Prediksi dan Simpan",
    command=simpan_data,
    bg="lightblue",
    width=25
).pack(pady=10)

tk.Button(
    root,
    text="Lihat Data",
    command=lihat_data,
    width=25
).pack(pady=5)

label_hasil = tk.Label(
    root,
    text="Hasil Prediksi: -",
    font=("Arial", 14, "bold")
)
label_hasil.pack(pady=20)

try:
    root.mainloop()
finally:
    conn.close()
