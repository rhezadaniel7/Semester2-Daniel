def rencana_liburan_korea(budget_total=50000000):
    # Definisi kategori pengeluaran dan opsi-opsinya
    pesawat = [19000000]  # harga pesawat per orang
    komunikasi = [250000, 500000, 800000]  # pilihan paket komunikasi
    hotel = [7000000, 10000000, 14000000]  # pilihan harga hotel di Hotel Shilla Stay
    
    # Opsi tempat makan
    tempat_makan = [
        {"nama": "Tosokchon Samgyetan", "harga": 300000},
        {"nama": "Samyukga", "harga": 400000},
        {"nama": "Osege Hyang", "harga": 350000},
        {"nama": "Mouse Rabbit Coffee", "harga": 150000},
        {"nama": "Cloudy Sky", "harga": 200000}
    ]
    
    # Opsi transportasi
    transportasi = [{"nama": "Taxi", "harga": 500000}]
    
    # Opsi tempat wisata
    tempat_wisata = [
        {"nama": "Lotte World", "harga": 800000},
        {"nama": "Myeongdong Street", "harga": 0},
        {"nama": "Pulau Nami", "harga": 600000},
        {"nama": "N Seoul Tower", "harga": 700000}
    ]
    
    # Opsi tempat belanja
    tempat_belanja = [
        {"nama": "Myeongdong Street", "harga": 1000000},
        {"nama": "Olive Young", "harga": 500000},
        {"nama": "Gotto Mall", "harga": 800000},
        {"nama": "Music Korea", "harga": 700000}
    ]
    
    # Inisialisasi hasil terbaik
    rencana_terbaik = {
        "pesawat": 0,
        "komunikasi": 0,
        "hotel": 0,
        "makan": [],
        "transportasi": [],
        "wisata": [],
        "belanja": [],
        "total_biaya": 0,
        "sisa_budget": budget_total
    }
    
    # Fungsi backtracking untuk menghasilkan rencana liburan
    def backtrack(rencana_saat_ini, kategori_saat_ini=0):
        nonlocal rencana_terbaik
        
        # Kategori: 0=pesawat, 1=komunikasi, 2=hotel, 3=makan, 4=transportasi, 5=wisata, 6=belanja
        if kategori_saat_ini > 6:
            # Rencana lengkap, periksa apakah ini lebih baik
            if rencana_saat_ini["total_biaya"] > rencana_terbaik["total_biaya"] and rencana_saat_ini["sisa_budget"] >= 0:
                rencana_terbaik = rencana_saat_ini.copy()
                rencana_terbaik["makan"] = rencana_saat_ini["makan"].copy()
                rencana_terbaik["transportasi"] = rencana_saat_ini["transportasi"].copy()
                rencana_terbaik["wisata"] = rencana_saat_ini["wisata"].copy()
                rencana_terbaik["belanja"] = rencana_saat_ini["belanja"].copy()
            return
        
        # Kategori Pesawat
        if kategori_saat_ini == 0:
            for biaya in pesawat:
                if biaya <= rencana_saat_ini["sisa_budget"]:
                    rencana_baru = rencana_saat_ini.copy()
                    rencana_baru["pesawat"] = biaya
                    rencana_baru["total_biaya"] += biaya
                    rencana_baru["sisa_budget"] -= biaya
                    backtrack(rencana_baru, kategori_saat_ini + 1)
        
        # Kategori Komunikasi
        elif kategori_saat_ini == 1:
            for biaya in komunikasi:
                if biaya <= rencana_saat_ini["sisa_budget"]:
                    rencana_baru = rencana_saat_ini.copy()
                    rencana_baru["komunikasi"] = biaya
                    rencana_baru["total_biaya"] += biaya
                    rencana_baru["sisa_budget"] -= biaya
                    backtrack(rencana_baru, kategori_saat_ini + 1)
        
        # Kategori Hotel
        elif kategori_saat_ini == 2:
            for biaya in hotel:
                if biaya <= rencana_saat_ini["sisa_budget"]:
                    rencana_baru = rencana_saat_ini.copy()
                    rencana_baru["hotel"] = biaya
                    rencana_baru["total_biaya"] += biaya
                    rencana_baru["sisa_budget"] -= biaya
                    backtrack(rencana_baru, kategori_saat_ini + 1)
        
        # Kategori Makan (bisa pilih beberapa tempat makan)
        elif kategori_saat_ini == 3:
            # Coba semua kombinasi tempat makan dalam batas anggaran 2 juta
            makan_backtrack(rencana_saat_ini, 0, 0, 2000000)
        
        # Kategori Transportasi
        elif kategori_saat_ini == 4:
            for opsi in transportasi:
                if opsi["harga"] <= rencana_saat_ini["sisa_budget"]:
                    rencana_baru = rencana_saat_ini.copy()
                    rencana_baru["transportasi"] = rencana_saat_ini["transportasi"].copy()
                    rencana_baru["transportasi"].append(opsi)
                    rencana_baru["total_biaya"] += opsi["harga"]
                    rencana_baru["sisa_budget"] -= opsi["harga"]
                    backtrack(rencana_baru, kategori_saat_ini + 1)
        
        # Kategori Wisata (bisa pilih beberapa tempat wisata)
        elif kategori_saat_ini == 5:
            # Coba semua kombinasi tempat wisata dalam batas anggaran 2.1 juta
            wisata_backtrack(rencana_saat_ini, 0, 0, 2100000)
        
        # Kategori Belanja (bisa pilih beberapa tempat belanja)
        elif kategori_saat_ini == 6:
            # Coba semua kombinasi tempat belanja dalam batas anggaran 3 juta
            belanja_backtrack(rencana_saat_ini, 0, 0, 3000000)
    
    # Fungsi backtracking untuk tempat makan
    def makan_backtrack(rencana, index, total_makan, batas_makan):
        # Jika sudah melampaui batas anggaran makan atau sudah mencoba semua tempat makan
        if total_makan > batas_makan or index >= len(tempat_makan):
            # Lanjutkan ke kategori berikutnya jika sudah memilih setidaknya satu tempat makan
            if rencana["makan"] and total_makan <= batas_makan:
                backtrack(rencana, 4)  # Lanjut ke transportasi
            return
        
        # Pilihan 1: Pilih tempat makan saat ini
        tempat = tempat_makan[index]
        if tempat["harga"] + total_makan <= batas_makan and tempat["harga"] <= rencana["sisa_budget"]:
            rencana_baru = rencana.copy()
            rencana_baru["makan"] = rencana["makan"].copy()
            rencana_baru["makan"].append(tempat)
            rencana_baru["total_biaya"] += tempat["harga"]
            rencana_baru["sisa_budget"] -= tempat["harga"]
            makan_backtrack(rencana_baru, index + 1, total_makan + tempat["harga"], batas_makan)
        
        # Pilihan 2: Tidak pilih tempat makan saat ini
        makan_backtrack(rencana, index + 1, total_makan, batas_makan)
    
    # Fungsi backtracking untuk tempat wisata
    def wisata_backtrack(rencana, index, total_wisata, batas_wisata):
        # Jika sudah melampaui batas anggaran wisata atau sudah mencoba semua tempat wisata
        if total_wisata > batas_wisata or index >= len(tempat_wisata):
            # Lanjutkan ke kategori berikutnya jika sudah memilih setidaknya satu tempat wisata
            if rencana["wisata"] and total_wisata <= batas_wisata:
                backtrack(rencana, 6)  # Lanjut ke belanja
            return
        
        # Pilihan 1: Pilih tempat wisata saat ini
        tempat = tempat_wisata[index]
        if tempat["harga"] + total_wisata <= batas_wisata and tempat["harga"] <= rencana["sisa_budget"]:
            rencana_baru = rencana.copy()
            rencana_baru["wisata"] = rencana["wisata"].copy()
            rencana_baru["wisata"].append(tempat)
            rencana_baru["total_biaya"] += tempat["harga"]
            rencana_baru["sisa_budget"] -= tempat["harga"]
            wisata_backtrack(rencana_baru, index + 1, total_wisata + tempat["harga"], batas_wisata)
        
        # Pilihan 2: Tidak pilih tempat wisata saat ini
        wisata_backtrack(rencana, index + 1, total_wisata, batas_wisata)
    
    # Fungsi backtracking untuk tempat belanja
    def belanja_backtrack(rencana, index, total_belanja, batas_belanja):
        # Jika sudah melampaui batas anggaran belanja atau sudah mencoba semua tempat belanja
        if total_belanja > batas_belanja or index >= len(tempat_belanja):
            # Evaluasi rencana final jika sudah memilih setidaknya satu tempat belanja
            if rencana["belanja"] and total_belanja <= batas_belanja:
                # Cek rencana final
                if rencana["total_biaya"] > rencana_terbaik["total_biaya"] and rencana["sisa_budget"] >= 0:
                    rencana_terbaik.update(rencana)
                    rencana_terbaik["makan"] = rencana["makan"].copy()
                    rencana_terbaik["transportasi"] = rencana["transportasi"].copy()
                    rencana_terbaik["wisata"] = rencana["wisata"].copy()
                    rencana_terbaik["belanja"] = rencana["belanja"].copy()
            return
        
        # Pilihan 1: Pilih tempat belanja saat ini
        tempat = tempat_belanja[index]
        if tempat["harga"] + total_belanja <= batas_belanja and tempat["harga"] <= rencana["sisa_budget"]:
            rencana_baru = rencana.copy()
            rencana_baru["belanja"] = rencana["belanja"].copy()
            rencana_baru["belanja"].append(tempat)
            rencana_baru["total_biaya"] += tempat["harga"]
            rencana_baru["sisa_budget"] -= tempat["harga"]
            belanja_backtrack(rencana_baru, index + 1, total_belanja + tempat["harga"], batas_belanja)
        
        # Pilihan 2: Tidak pilih tempat belanja saat ini
        belanja_backtrack(rencana, index + 1, total_belanja, batas_belanja)
    
    # Mulai backtracking dari rencana kosong
    rencana_awal = {
        "pesawat": 0,
        "komunikasi": 0,
        "hotel": 0,
        "makan": [],
        "transportasi": [],
        "wisata": [],
        "belanja": [],
        "total_biaya": 0,
        "sisa_budget": budget_total
    }
    
    backtrack(rencana_awal)
    
    # Tampilkan hasil rencana terbaik
    print("=== RENCANA LIBURAN KOREA SELATAN ===")
    print(f"Budget Total: Rp {budget_total:,}")
    print("\nPerincian Biaya:")
    print(f"1. Pesawat: Rp {rencana_terbaik['pesawat']:,}")
    print(f"2. Komunikasi: Rp {rencana_terbaik['komunikasi']:,}")
    print(f"3. Hotel (Hotel Shilla Stay): Rp {rencana_terbaik['hotel']:,}")
    
    print("\n4. Tempat Makan:")
    total_makan = 0
    for tempat in rencana_terbaik["makan"]:
        print(f"   - {tempat['nama']}: Rp {tempat['harga']:,}")
        total_makan += tempat["harga"]
    print(f"   Total Makan: Rp {total_makan:,}")
    
    print("\n5. Transportasi:")
    total_transportasi = 0
    for tempat in rencana_terbaik["transportasi"]:
        print(f"   - {tempat['nama']}: Rp {tempat['harga']:,}")
        total_transportasi += tempat["harga"]
    print(f"   Total Transportasi: Rp {total_transportasi:,}")
    
    print("\n6. Tempat Wisata:")
    total_wisata = 0
    for tempat in rencana_terbaik["wisata"]:
        print(f"   - {tempat['nama']}: Rp {tempat['harga']:,}")
        total_wisata += tempat["harga"]
    print(f"   Total Wisata: Rp {total_wisata:,}")
    
    print("\n7. Tempat Belanja:")
    total_belanja = 0
    for tempat in rencana_terbaik["belanja"]:
        print(f"   - {tempat['nama']}: Rp {tempat['harga']:,}")
        total_belanja += tempat["harga"]
    print(f"   Total Belanja: Rp {total_belanja:,}")
    
    print("\n=== RINGKASAN ===")
    print(f"Total Biaya: Rp {rencana_terbaik['total_biaya']:,}")
    print(f"Sisa Budget: Rp {rencana_terbaik['sisa_budget']:,}")
    
    return rencana_terbaik

# Jalankan fungsi
hasil = rencana_liburan_korea(50000000)

# 3. Logika Backtracking yang Digunakan dalam Program

"""
Logika backtracking dalam program ini digunakan untuk mencari kombinasi terbaik dari berbagai kategori pengeluaran 
(pesawat, komunikasi, hotel, makan, transportasi, wisata, dan belanja) yang memaksimalkan penggunaan budget 
tanpa melebihi batas yang ditentukan. Berikut adalah penjelasan logika backtracking yang digunakan:

- **Inisialisasi**: Program dimulai dengan rencana kosong (tidak ada pengeluaran) dan budget penuh.
- **Rekursi dan Pencabangan**: 
  - Untuk setiap kategori pengeluaran (misalnya, pesawat, komunikasi, hotel), program mencoba semua opsi yang tersedia.
  - Jika opsi tersebut masih dalam batas budget, program akan melanjutkan ke kategori berikutnya.
  - Jika budget terlampaui, program akan "mundur" (backtrack) dan mencoba opsi lain.
- **Kombinasi Tempat Makan, Wisata, dan Belanja**:
  - Untuk kategori yang memungkinkan pemilihan beberapa item (seperti tempat makan, wisata, dan belanja), 
    program menggunakan fungsi backtracking khusus untuk mencoba semua kombinasi yang mungkin.
  - Misalnya, untuk tempat makan, program mencoba semua kombinasi tempat makan yang total harganya tidak melebihi batas tertentu.
- **Evaluasi Rencana**:
  - Setiap kali rencana lengkap terbentuk (semua kategori telah diproses), program memeriksa apakah rencana tersebut 
    lebih baik dari rencana terbaik yang telah ditemukan sebelumnya (dalam hal total biaya yang mendekati budget).
  - Jika ya, rencana tersebut disimpan sebagai rencana terbaik.
- **Penghentian**: Proses berakhir ketika semua kombinasi telah dicoba.

Contoh:
- Untuk kategori pesawat, program mencoba semua opsi harga pesawat yang tersedia.
- Jika opsi pertama (Rp 19.000.000) dipilih, program melanjutkan ke kategori komunikasi.
- Jika opsi komunikasi yang dipilih melebihi budget, program akan mundur dan mencoba opsi komunikasi yang lebih murah.
- Proses ini berlanjut hingga semua kategori terpenuhi atau semua kombinasi telah dicoba.
"""

# 4. Analisis Kelebihan dan Kekurangan Pendekatan Backtracking

"""
**Kelebihan:**
1. **Menemukan Solusi Optimal**:
   - Backtracking memastikan bahwa semua kemungkinan kombinasi dicoba, sehingga solusi yang ditemukan adalah yang terbaik 
     dalam batasan yang diberikan (dalam hal ini, memaksimalkan penggunaan budget).
   
2. **Fleksibel**:
   - Pendekatan ini dapat menangani berbagai batasan dan aturan, seperti batasan budget untuk kategori tertentu 
     (misalnya, batas maksimal untuk makan atau wisata).

3. **Mudah Dikembangkan**:
   - Jika ada kategori pengeluaran baru atau opsi baru dalam kategori yang sudah ada, program dapat dengan mudah 
     diperluas tanpa mengubah struktur utama.

**Kekurangan:**
1. **Kompleksitas Waktu Tinggi**:
   - Karena backtracking mencoba semua kemungkinan kombinasi, kompleksitas waktu program bisa sangat tinggi, terutama 
     jika ada banyak opsi dalam setiap kategori. Ini bisa menjadi masalah jika budget atau jumlah opsi sangat besar.

2. **Penggunaan Memori**:
   - Proses rekursi dalam backtracking dapat menggunakan banyak memori, terutama jika kedalaman rekursi sangat dalam 
     (misalnya, banyak kategori atau banyak opsi dalam kategori).

3. **Tidak Efisien untuk Masalah Besar**:
   - Untuk masalah dengan skala besar (misalnya, budget sangat besar atau banyak opsi), pendekatan backtracking 
     mungkin tidak praktis karena waktu eksekusi yang lama.

4. **Kesulitan dalam Debugging**:
   - Karena sifat rekursif dan banyaknya kombinasi yang dicoba, debugging bisa menjadi sulit jika terjadi kesalahan 
     dalam logika program.

**Contoh Analisis:**
- Jika budget sangat besar (misalnya, Rp 100.000.000) dan ada banyak opsi dalam setiap kategori, program mungkin 
  membutuhkan waktu yang sangat lama untuk menyelesaikan pencarian.
- Namun, untuk budget yang relatif kecil (misalnya, Rp 50.000.000) dan jumlah opsi yang terbatas, backtracking 
  adalah pendekatan yang efektif untuk menemukan solusi optimal.
"""
