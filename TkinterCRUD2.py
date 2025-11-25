import tkinter as tk
import tkinter.messagebox as msg
import sqlite3

# ---------------- DB ----------------
def db():
    c = sqlite3.connect("tutorial.db")
    c.execute("""CREATE TABLE IF NOT EXISTS nilai_siswa(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nama TEXT, bio INT, fis INT, ing INT, prediksi TEXT)""")
    return c

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Prediksi Fakultas")
root.geometry("300x420")

# ENTRY ID UNTUK UPDATE / DELETE
tk.Label(root, text="ID (untuk Update / Delete)").pack()
e_id = tk.Entry(root)
e_id.pack()

labels = ["Nama", "Biologi", "Fisika", "Inggris"]
entries = {}

for t in labels:
    tk.Label(root, text=t).pack()
    e = tk.Entry(root)
    e.pack()
    entries[t] = e

# ---------------- PREDIKSI ----------------
def prediksi_fakultas(b, f, g):
    tertinggi = max(b, f, g)
    if tertinggi == b:
        return "Kedokteran"
    elif tertinggi == f:
        return "Teknik"
    else:
        return "Bahasa"

# ---------------- SUBMIT ----------------
def submit():
    try:
        nama = entries["Nama"].get()
        b = int(entries["Biologi"].get())
        f = int(entries["Fisika"].get())
        g = int(entries["Inggris"].get())
    except:
        return msg.showerror("Error", "Nilai harus angka!")

    prediksi = prediksi_fakultas(b, f, g)

    conn = db()
    conn.execute("INSERT INTO nilai_siswa(nama, bio, fis, ing, prediksi) VALUES (?,?,?,?,?)",
                 (nama, b, f, g, prediksi))
    conn.commit()
    conn.close()

    msg.showinfo("Hasil", f"Prediksi Fakultas: {prediksi}")
    hasil_label.config(text=f"Hasil: {prediksi}")

# ---------------- UPDATE ----------------
def update_data():
    try:
        id_data = int(e_id.get())
    except:
        return msg.showerror("Error", "ID harus angka!")

    try:
        nama = entries["Nama"].get()
        b = int(entries["Biologi"].get())
        f = int(entries["Fisika"].get())
        g = int(entries["Inggris"].get())
    except:
        return msg.showerror("Error", "Nilai harus angka!")

    prediksi = prediksi_fakultas(b, f, g)

    conn = db()
    cursor = conn.cursor()
    cursor.execute("""UPDATE nilai_siswa
                       SET nama=?, bio=?, fis=?, ing=?, prediksi=?
                       WHERE id=?""",
                   (nama, b, f, g, prediksi, id_data))
    conn.commit()

    if cursor.rowcount == 0:
        msg.showerror("Error", "ID tidak ditemukan!")
    else:
        msg.showinfo("Sukses", "Data berhasil diupdate!")

    conn.close()

# ---------------- DELETE ----------------
def delete_data():
    try:
        id_data = int(e_id.get())
    except:
        return msg.showerror("Error", "ID harus angka!")

    conn = db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nilai_siswa WHERE id=?", (id_data,))
    conn.commit()

    if cursor.rowcount == 0:
        msg.showerror("Error", "ID tidak ditemukan!")
    else:
        msg.showinfo("Sukses", "Data berhasil dihapus!")

    conn.close()

# ---------------- BUTTONS ----------------
tk.Button(root, text="Submit", command=submit).pack(pady=10)
tk.Button(root, text="Update", command=update_data).pack(pady=5)
tk.Button(root, text="Delete", command=delete_data).pack(pady=5)

hasil_label = tk.Label(root, text="Hasil akan muncul di sini")
hasil_label.pack(pady=10)

root.mainloop()