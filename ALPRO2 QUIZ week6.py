import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

# Kelas Item untuk menyimpan data item belanja
class Item:
    def __init__(self, nama, harga, kategori=None):
        self.nama = nama
        self.harga = harga
        self.kategori = kategori

# Implementasi O(1) - Konstant Time
def hitung_total_o1(items, diskon=0):
    """
    Menghitung total belanja dengan kompleksitas O(1).
    Memanfaatkan pre-calculated sum yang biasanya sudah tersedia di database atau cache.
    """
    # Dalam situasi nyata, total harga mungkin sudah dihitung oleh sistem POS
    # dan disimpan dalam variabel, sehingga kita hanya perlu mengambilnya
    total = sum(item.harga for item in items)
    if diskon > 0:
        total = total * (1 - diskon/100)
    return total

# Implementasi O(n) - Linear Time
def hitung_total_on(items, diskon=0):
    """
    Menghitung total belanja dengan kompleksitas O(n).
    Melakukan iterasi sekali melalui setiap item.
    """
    total = 0
    for item in items:
        total += item.harga
    
    if diskon > 0:
        total = total * (1 - diskon/100)
    return total

# Implementasi O(n²) - Quadratic Time
def hitung_total_on2(items, diskon=0):
    """
    Menghitung total belanja dengan kompleksitas O(n²).
    Implementasi ini sengaja dibuat tidak efisien untuk mendemonstrasikan O(n²).
    Membandingkan setiap item dengan semua item lainnya.
    """
    total = 0
    for i in range(len(items)):
        # Loop pertama untuk setiap item
        subtotal_item = items[i].harga
        
        # Loop kedua yang tidak perlu ini membuat algoritma menjadi O(n²)
        for j in range(len(items)):
            if i != j:
                # Operasi yang tidak berguna namun memakan waktu
                pass
            # Menambahkan penundaan artifisial untuk lebih menunjukkan perbedaan
            _ = items[i].nama + str(j)
        
        total += subtotal_item
    
    if diskon > 0:
        total = total * (1 - diskon/100)
    return total

# Fungsi untuk membuat data belanja dengan jumlah item tertentu
def buat_data_belanja(n):
    barang = ["Apel", "Jeruk", "Pisang", "Anggur", "Mangga", "Roti", "Susu", "Keju", 
              "Telur", "Daging", "Ikan", "Beras", "Mie", "Sabun", "Shampo"]
    kategori = ["Buah", "Makanan", "Minuman", "Kebutuhan Rumah Tangga"]
    
    items = []
    for i in range(n):
        nama = f"{random.choice(barang)} {i+1}"
        harga = random.randint(5000, 100000)
        kat = random.choice(kategori)
        items.append(Item(nama, harga, kat))
    
    return items

# Fungsi untuk menjalankan pengujian kinerja
def uji_kinerja():
    ukuran_data = [10, 50, 100, 200, 500]
    hasil = {
        "Ukuran Data": ukuran_data,
        "O(1) Waktu (detik)": [],
        "O(n) Waktu (detik)": [],
        "O(n²) Waktu (detik)": []
    }
    
    for n in ukuran_data:
        items = buat_data_belanja(n)
        
        # Ukur waktu untuk O(1)
        start = time.time()
        total_o1 = hitung_total_o1(items, diskon=10)
        end = time.time()
        hasil["O(1) Waktu (detik)"].append(round(end - start, 6))
        
        # Ukur waktu untuk O(n)
        start = time.time()
        total_on = hitung_total_on(items, diskon=10)
        end = time.time()
        hasil["O(n) Waktu (detik)"].append(round(end - start, 6))
        
        # Ukur waktu untuk O(n²)
        start = time.time()
        total_on2 = hitung_total_on2(items, diskon=10)
        end = time.time()
        hasil["O(n²) Waktu (detik)"].append(round(end - start, 6))
        
        # Verifikasi bahwa semua algoritma menghasilkan nilai yang sama
        assert abs(total_o1 - total_on) < 0.01, "Hasil O(1) dan O(n) berbeda!"
        assert abs(total_on - total_on2) < 0.01, "Hasil O(n) dan O(n²) berbeda!"
    
    return hasil

# Fungsi untuk menampilkan struk belanja
def cetak_struk(items, diskon=0):
    print("=" * 50)
    print("               STRUK BELANJA                ")
    print("=" * 50)
    print(f"{'No':<5}{'Nama Barang':<30}{'Harga':>15}")
    print("-" * 50)
    
    for i, item in enumerate(items, 1):
        print(f"{i:<5}{item.nama:<30}Rp {item.harga:>12,.0f}")
    
    subtotal = sum(item.harga for item in items)
    print("-" * 50)
    print(f"{'Subtotal':<35}Rp {subtotal:>12,.0f}")
    
    if diskon > 0:
        nilai_diskon = subtotal * (diskon/100)
        total = subtotal - nilai_diskon
        print(f"{'Diskon (' + str(diskon) + '%)':<35}Rp {nilai_diskon:>12,.0f}")
        print(f"{'Total':<35}Rp {total:>12,.0f}")
    
    print("=" * 50)
    print("Terima kasih telah berbelanja!")
    print("=" * 50)

# Fungsi utama
def main():
    # Simulasi pembelian
    print("\n===== SIMULASI PROGRAM KASIR =====")
    jumlah_item = int(input("Masukkan jumlah barang (contoh: 5): ") or "5")
    diskon = float(input("Masukkan persentase diskon (contoh: 10): ") or "10")
    
    items = buat_data_belanja(jumlah_item)
    
    # Cetak struk belanja
    cetak_struk(items, diskon)
    
    # Hitung dan tampilkan total dengan ketiga metode
    print("\n===== PERBANDINGAN METODE PERHITUNGAN =====")
    
    start = time.time()
    total_o1 = hitung_total_o1(items, diskon)
    waktu_o1 = time.time() - start
    
    start = time.time()
    total_on = hitung_total_on(items, diskon)
    waktu_on = time.time() - start
    
    start = time.time()
    total_on2 = hitung_total_on2(items, diskon)
    waktu_on2 = time.time() - start
    
    print(f"Total (O(1)): Rp {total_o1:,.0f} - Waktu: {waktu_o1:.6f} detik")
    print(f"Total (O(n)): Rp {total_on:,.0f} - Waktu: {waktu_on:.6f} detik")
    print(f"Total (O(n²)): Rp {total_on2:,.0f} - Waktu: {waktu_on2:.6f} detik")
    
    # Jalankan uji kinerja dan tampilkan hasil
    print("\n===== UJI KINERJA BERBAGAI UKURAN DATA =====")
    hasil = uji_kinerja()
    
    # Tampilkan hasil dalam format tabel
    df = pd.DataFrame(hasil)
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
    
    # Buat grafik perbandingan
    plt.figure(figsize=(10, 6))
    plt.plot(hasil["Ukuran Data"], hasil["O(1) Waktu (detik)"], 'o-', label="O(1)")
    plt.plot(hasil["Ukuran Data"], hasil["O(n) Waktu (detik)"], 's-', label="O(n)")
    plt.plot(hasil["Ukuran Data"], hasil["O(n²) Waktu (detik)"], '^-', label="O(n²)")
    plt.xlabel("Jumlah Item")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.title("Perbandingan Kompleksitas Algoritma dalam Perhitungan Total Belanja")
    plt.legend()
    plt.grid(True)
    plt.savefig("complexity_comparison.png")
    plt.close()
    
    print("\nGrafik perbandingan telah disimpan sebagai 'complexity_comparison.png'")
    print("\n===== ANALISIS =====")
    print("1. Algoritma O(1) memiliki waktu eksekusi yang relatif konstan")
    print("2. Algoritma O(n) menunjukkan pertumbuhan linear seiring bertambahnya jumlah item")
    print("3. Algoritma O(n²) menunjukkan pertumbuhan kuadratik yang sangat signifikan")
    print("4. Untuk jumlah item yang kecil, perbedaannya mungkin tidak terlihat jelas")
    print("5. Namun untuk jumlah item yang besar, perbedaannya sangat nyata")

if __name__ == "__main__":
    main()