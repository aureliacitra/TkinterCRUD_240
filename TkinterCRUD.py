import tkinter as tk
import tkinter.messagebox as msg
import sqlite3

def db():
    c = sqlite3.connect("tutorial.db")
    c.execute("""CREATE TABLE IF NOT EXISTS nilai_siswa(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nama TEXT, bio INT, fis INT, ing INT, prediksi TEXT)""")
    return c

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Prediksi Fakultas")
root.geometry("300x300")

labels = ["Nama", "Biologi", "Fisika", "Inggris"]
entries = {}

for i, t in enumerate(labels):
    tk.Label(root, text=t).pack()
    e = tk.Entry(root)
    e.pack()
    entries[t] = e

def submit():
    try:
        nama = entries["Nama"].get()
        b = int(entries["Biologi"].get())
        f = int(entries["Fisika"].get())
        g = int(entries["Inggris"].get())
    except:
        return msg.showerror("Error", "Nilai harus angka!")

    # Prediksi
    tertinggi = max(b, f, g)
    prediksi = "Kedokteran" if tertinggi == b else "Teknik" if tertinggi == f else "Bahasa"

    # Simpan ke DB
    conn = db()
    conn.execute("INSERT INTO nilai_siswa(nama, bio, fis, ing, prediksi) VALUES (?,?,?,?,?)",
                 (nama, b, f, g, prediksi))
    conn.commit()
    conn.close()

    msg.showinfo("Hasil", f"Prediksi Fakultas: {prediksi}")
    hasil_label.config(text=f"Hasil: {prediksi}")

tk.Button(root, text="Submit", command=submit).pack(pady=10)
hasil_label = tk.Label(root, text="Hasil akan muncul di sini")
hasil_label.pack()

root.mainloop()