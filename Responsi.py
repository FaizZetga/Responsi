import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date

# Koneksi ke Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Ganti dengan username MySQL Anda
    password="",  # Ganti dengan password MySQL Anda
    database="Toko"
)
cursor = conn.cursor()

# Fungsi CRUD Produk
def fetch_produk():
    """Mengambil data produk dari database dan menampilkannya di tabel."""
    for row in table_produk.get_children():
        table_produk.delete(row)
    cursor.execute("SELECT * FROM Produk")
    for data in cursor.fetchall():
        table_produk.insert("", END, values=data)

def add_produk():
    """Menambah produk ke database."""
    nama = name_produk_var.get()
    harga = harga_produk_var.get()
    if nama and harga:
        try:
            cursor.execute("INSERT INTO Produk (nama_produk, harga_produk) VALUES (%s, %s)", (nama, harga))
            conn.commit()
            messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
            clear_produk()
            fetch_produk()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    else:
        messagebox.showwarning("Input Error", "Nama dan harga produk harus diisi.")

def delete_produk():
    """Menghapus produk yang dipilih di database."""
    try:
        selected_item = table_produk.selection()[0]
        id_selected = table_produk.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM Produk WHERE id_produk = %s", (id_selected,))
        conn.commit()
        messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
        fetch_produk()
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data dari tabel terlebih dahulu.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

def clear_produk():
    """Menghapus input di form produk."""
    name_produk_var.set("")
    harga_produk_var.set("")

# Fungsi Manajemen Transaksi
def fetch_transaksi():
    """Mengambil data transaksi dari database dan menampilkannya di tabel."""
    for row in table_transaksi.get_children():
        table_transaksi.delete(row)
    cursor.execute("""
        SELECT Transaksi.id_transaksi, Produk.nama_produk, Transaksi.jumlah_produk, 
               Transaksi.total_harga, Transaksi.tanggal_transaksi
        FROM Transaksi
        JOIN Produk ON Transaksi.id_produk = Produk.id_produk
    """)
    for data in cursor.fetchall():
        table_transaksi.insert("", END, values=data)

def add_transaksi():
    """Menambah transaksi ke database."""
    id_produk = id_produk_var.get()
    jumlah = jumlah_var.get()
    if id_produk and jumlah:
        try:
            cursor.execute("SELECT harga_produk FROM Produk WHERE id_produk = %s", (id_produk,))
            harga_produk = cursor.fetchone()
            if harga_produk:
                total_harga = int(jumlah) * harga_produk[0]
                tanggal = date.today()
                cursor.execute(
                    "INSERT INTO Transaksi (id_produk, jumlah_produk, total_harga, tanggal_transaksi) VALUES (%s, %s, %s, %s)",
                    (id_produk, jumlah, total_harga, tanggal)
                )
                conn.commit()
                messagebox.showinfo("Sukses", f"Transaksi berhasil ditambahkan! Total Harga: {total_harga}")
                fetch_transaksi()
            else:
                messagebox.showwarning("Produk Tidak Ditemukan", "ID Produk tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    else:
        messagebox.showwarning("Input Error", "ID Produk dan Jumlah harus diisi.")

def update_transaksi():
    """Memperbarui data transaksi yang sudah ada."""
    try:
        selected_item = table_transaksi.selection()[0]
        id_transaksi = table_transaksi.item(selected_item)['values'][0]
        jumlah = jumlah_var.get()

        if not jumlah or not jumlah.isdigit():
            messagebox.showwarning("Input Error", "Jumlah harus diisi dengan angka.")
            return

        cursor.execute("SELECT id_produk, jumlah_produk FROM Transaksi WHERE id_transaksi = %s", (id_transaksi,))
        transaksi = cursor.fetchone()
        if transaksi:
            id_produk = transaksi[0]
            cursor.execute("SELECT harga_produk FROM Produk WHERE id_produk = %s", (id_produk,))
            harga_produk = cursor.fetchone()
            if harga_produk:
                total_harga = int(jumlah) * harga_produk[0]
                cursor.execute(
                    "UPDATE Transaksi SET jumlah_produk = %s, total_harga = %s WHERE id_transaksi = %s",
                    (jumlah, total_harga, id_transaksi)
                )
                conn.commit()
                messagebox.showinfo("Sukses", f"Transaksi dengan ID {id_transaksi} berhasil diperbarui!")
                fetch_transaksi()
            else:
                messagebox.showwarning("Produk Tidak Ditemukan", "ID Produk tidak ditemukan.")
        else:
            messagebox.showwarning("Transaksi Tidak Ditemukan", "ID Transaksi tidak ditemukan.")
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data dari tabel terlebih dahulu.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

def delete_transaksi():
    """Menghapus transaksi yang dipilih di database."""
    try:
        selected_item = table_transaksi.selection()[0]
        id_selected = table_transaksi.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM Transaksi WHERE id_transaksi = %s", (id_selected,))
        conn.commit()
        messagebox.showinfo("Sukses", "Transaksi berhasil dihapus!")
        fetch_transaksi()
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data dari tabel terlebih dahulu.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Fungsi Navigasi
def show_produk_tab():
    tab_control.select(tab_produk)

def show_transaksi_tab():
    tab_control.select(tab_transaksi)

# GUI Utama
app = Tk()
app.title("Aplikasi CRUD Produk dan Transaksi")
app.geometry("900x600")

# Menu Utama
menu_frame = Frame(app, pady=10)
menu_frame.pack(fill=X)

Button(menu_frame, text="Manajemen Produk", command=show_produk_tab, bg="blue", fg="white", width=20).pack(side=LEFT, padx=10)
Button(menu_frame, text="Manajemen Transaksi", command=show_transaksi_tab, bg="green", fg="white", width=20).pack(side=LEFT, padx=10)

# Tab Control
tab_control = ttk.Notebook(app)
tab_produk = Frame(tab_control)
tab_transaksi = Frame(tab_control)
tab_control.add(tab_produk, text="Manajemen Produk")
tab_control.add(tab_transaksi, text="Manajemen Transaksi")
tab_control.pack(expand=1, fill="both")

# Tab Produk
Label(tab_produk, text="Nama Produk:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
name_produk_var = StringVar()
Entry(tab_produk, textvariable=name_produk_var, width=30).grid(row=0, column=1, padx=10, pady=5)

Label(tab_produk, text="Harga Produk:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
harga_produk_var = StringVar()
Entry(tab_produk, textvariable=harga_produk_var, width=30).grid(row=1, column=1, padx=10, pady=5)

Button(tab_produk, text="Tambah", command=add_produk, bg="green", fg="white", width=10).grid(row=2, column=0, padx=10, pady=10)
Button(tab_produk, text="Hapus", command=delete_produk, bg="red", fg="white", width=10).grid(row=2, column=1, padx=10, pady=10)
Button(tab_produk, text="Clear", command=clear_produk, bg="yellow", fg="black", width=10).grid(row=2, column=2, padx=10, pady=10)

table_produk = ttk.Treeview(tab_produk, columns=("ID", "Nama", "Harga"), show="headings")
table_produk.heading("ID", text="ID")
table_produk.heading("Nama", text="Nama Produk")
table_produk.heading("Harga", text="Harga Produk")
table_produk.column("ID", width=50)
table_produk.column("Nama", width=200)
table_produk.column("Harga", width=100)
table_produk.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
fetch_produk()

# Tab Transaksi
Label(tab_transaksi, text="ID Produk:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
id_produk_var = StringVar()
Entry(tab_transaksi, textvariable=id_produk_var, width=30).grid(row=0, column=1, padx=10, pady=5)

Label(tab_transaksi, text="Jumlah:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
jumlah_var = StringVar()
Entry(tab_transaksi, textvariable=jumlah_var, width=30).grid(row=1, column=1, padx=10, pady=5)

Button(tab_transaksi, text="Tambah Transaksi", command=add_transaksi, bg="green", fg="white", width=20).grid(row=2, column=0, columnspan=2, pady=10)
Button(tab_transaksi, text="Update Transaksi", command=update_transaksi, bg="blue", fg="white", width=20).grid(row=3, column=0, pady=10)
Button(tab_transaksi, text="Hapus Transaksi", command=delete_transaksi, bg="red", fg="white", width=20).grid(row=3, column=1, pady=10)

table_transaksi = ttk.Treeview(tab_transaksi, columns=("ID", "Nama Produk", "Jumlah", "Total Harga", "Tanggal"), show="headings")
table_transaksi.heading("ID", text="ID Transaksi")
table_transaksi.heading("Nama Produk", text="Nama Produk")
table_transaksi.heading("Jumlah", text="Jumlah")
table_transaksi.heading("Total Harga", text="Total Harga")
table_transaksi.heading("Tanggal", text="Tanggal Transaksi")
table_transaksi.column("ID", width=50)
table_transaksi.column("Nama Produk", width=200)
table_transaksi.column("Jumlah", width=100)
table_transaksi.column("Total Harga", width=100)
table_transaksi.column("Tanggal", width=150)
table_transaksi.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
fetch_transaksi()

# Jalankan Aplikasi
app.mainloop()

# Membuat Databasenya

# CREATE DATABASE Toko;

# USE Toko;

# CREATE TABLE Produk (
#     id_produk INT AUTO_INCREMENT PRIMARY KEY,
#     nama_produk VARCHAR(100) NOT NULL,
#     harga_produk DECIMAL(10, 2) NOT NULL
# );

# CREATE TABLE Transaksi (
#     id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
#     id_produk INT,
#     jumlah_produk INT NOT NULL,
#     total_harga DECIMAL(10, 2) NOT NULL,
#     tanggal_transaksi DATE NOT NULL,
#     FOREIGN KEY (id_produk) REFERENCES Produk(id_produk)
# );
