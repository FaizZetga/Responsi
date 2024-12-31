# Responsi
## Dokumentasi Aplikasi CRUD Produk dan Transaksi

### 1. Deskripsi Aplikasi
Aplikasi ini adalah sistem manajemen sederhana untuk produk dan transaksi yang terintegrasi dengan database MySQL. Aplikasi ini memiliki dua fitur utama:
- **Manajemen Produk**: Menambah, menghapus, dan menampilkan daftar produk.
- **Manajemen Transaksi**: Menambah, memperbarui, menghapus, dan menampilkan data transaksi berdasarkan produk yang ada.

Aplikasi ini dibangun menggunakan **Python** dengan antarmuka pengguna berbasis **Tkinter**.

### 2. Cara Menjalankan Aplikasi
1. **Persiapan Database**:
   - Buat database baru dengan nama `Toko` di MySQL.
   - Jalankan perintah SQL berikut untuk membuat tabel:
     ```sql
     CREATE DATABASE Toko;
     USE Toko;

     CREATE TABLE Produk (
         id_produk INT AUTO_INCREMENT PRIMARY KEY,
         nama_produk VARCHAR(100) NOT NULL,
         harga_produk DECIMAL(10, 2) NOT NULL
     );

     CREATE TABLE Transaksi (
         id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
         id_produk INT,
         jumlah_produk INT NOT NULL,
         total_harga DECIMAL(10, 2) NOT NULL,
         tanggal_transaksi DATE NOT NULL,
         FOREIGN KEY (id_produk) REFERENCES Produk(id_produk)
     );
     ```

2. **Persiapan Aplikasi**:
   - Pastikan **Python** telah terinstal di komputer Anda.
   - Instal modul yang diperlukan dengan menjalankan:
     ```bash
     pip install mysql-connector-python
     ```
   - Ubah konfigurasi **host**, **user**, dan **password** di bagian koneksi database sesuai dengan pengaturan MySQL Anda.

3. **Menjalankan Aplikasi**:
   - Jalankan file `Responsi.py` menggunakan Python:
     ```bash
     python Responsi.py
     ```

### 3. Struktur Tabel Database

**a. Tabel Produk**

| Nama Kolom   | Tipe Data         | Deskripsi                          |
|--------------|-------------------|------------------------------------|
| id_produk    | INT (Primary Key) | ID unik untuk setiap produk        |
| nama_produk  | VARCHAR(100)      | Nama produk                        |
| harga_produk | DECIMAL(10, 2)    | Harga produk dalam format desimal  |

**b. Tabel Transaksi**

| Nama Kolom        | Tipe Data         | Deskripsi                                   |
|-------------------|-------------------|---------------------------------------------|
| id_transaksi      | INT (Primary Key) | ID unik untuk setiap transaksi             |
| id_produk         | INT               | ID produk terkait transaksi (Foreign Key)  |
| jumlah_produk     | INT               | Jumlah produk yang dibeli                  |
| total_harga       | DECIMAL(10, 2)    | Total harga transaksi                      |
| tanggal_transaksi | DATE              | Tanggal transaksi dilakukan                |
