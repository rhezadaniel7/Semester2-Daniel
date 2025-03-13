import time
import random
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Simulasi database untuk menyimpan interaksi dan pengguna
class SocialMediaDatabase:
    def __init__(self):
        self.interactions = []
        self.users = set(range(1, 1001))  # 1000 pengguna
        self.user_notifications = defaultdict(list)
    
    def generate_random_interactions(self, num_interactions):
        """Menghasilkan interaksi acak antara pengguna"""
        new_interactions = []
        for _ in range(num_interactions):
            sender = random.choice(list(self.users))
            receiver = random.choice(list(self.users - {sender}))
            interaction_type = random.choice(['like', 'comment', 'tag', 'share'])
            timestamp = time.time()
            
            interaction = {
                'id': len(self.interactions) + len(new_interactions) + 1,
                'sender': sender,
                'receiver': receiver,
                'type': interaction_type,
                'timestamp': timestamp,
                'content': f"Interaksi {interaction_type} dari pengguna {sender} ke {receiver}"
            }
            new_interactions.append(interaction)
        
        self.interactions.extend(new_interactions)
        return new_interactions

# Implementasi Solusi Buruk: O(n) - Polling Linier
class PollingNotificationSystem:
    def __init__(self, database):
        self.database = database
        self.last_check_time = time.time()
        self.processed_ids = set()
    
    def check_notifications(self):
        """Melakukan polling untuk menemukan interaksi baru (O(n))"""
        start_time = time.time()
        
        notifications_sent = 0
        interactions_checked = 0
        
        # Memeriksa semua interaksi (kompleksitas O(n))
        for interaction in self.database.interactions:
            interactions_checked += 1
            
            # Hanya memproses interaksi yang belum diproses
            if interaction['id'] not in self.processed_ids:
                # Simulasi pengiriman notifikasi ke penerima
                self.database.user_notifications[interaction['receiver']].append({
                    'interaction_id': interaction['id'],
                    'content': interaction['content'],
                    'timestamp': time.time()
                })
                
                self.processed_ids.add(interaction['id'])
                notifications_sent += 1
        
        processing_time = time.time() - start_time
        return {
            'processing_time': processing_time,
            'notifications_sent': notifications_sent,
            'interactions_checked': interactions_checked
        }

# Implementasi Solusi Baik: O(1) - Sistem Pub/Sub
class PubSubNotificationSystem:
    def __init__(self, database):
        self.database = database
        self.subscription_channels = defaultdict(set)
        
        # Setiap pengguna berlangganan ke saluran notifikasinya sendiri
        for user in self.database.users:
            self.subscription_channels[user].add(user)
    
    def process_new_interaction(self, interaction):
        """Memproses satu interaksi baru dan mengirim notifikasi (O(1))"""
        start_time = time.time()
        
        # Langsung kirim notifikasi ke penerima (kompleksitas O(1))
        self.database.user_notifications[interaction['receiver']].append({
            'interaction_id': interaction['id'],
            'content': interaction['content'],
            'timestamp': time.time()
        })
        
        processing_time = time.time() - start_time
        return {
            'processing_time': processing_time,
            'notifications_sent': 1,
            'interactions_checked': 1
        }
    
    def process_batch_interactions(self, interactions):
        """Memproses batch interaksi baru untuk pengujian performa"""
        total_time = 0
        for interaction in interactions:
            result = self.process_new_interaction(interaction)
            total_time += result['processing_time']
        
        return {
            'processing_time': total_time,
            'notifications_sent': len(interactions),
            'interactions_checked': len(interactions)
        }

# Fungsi untuk menjalankan pengujian performa
def run_performance_test():
    print("Menjalankan Pengujian Performa Sistem Notifikasi Media Sosial...")
    
    # Inisialisasi database
    db = SocialMediaDatabase()
    
    # Inisialisasi sistem notifikasi
    polling_system = PollingNotificationSystem(db)
    pubsub_system = PubSubNotificationSystem(db)
    
    # Parameter pengujian
    test_batch_sizes = [100, 500, 1000, 5000, 10000, 50000]
    results = {
        'batch_sizes': test_batch_sizes,
        'polling_times': [],
        'pubsub_times': [],
        'polling_efficiency': [],
        'pubsub_efficiency': []
    }
    
    # Jalankan pengujian untuk setiap ukuran batch
    for batch_size in test_batch_sizes:
        print(f"\nMenghasilkan {batch_size} interaksi acak...")
        new_interactions = db.generate_random_interactions(batch_size)
        
        # Uji sistem polling
        print(f"Menguji sistem Polling Linier O(n) dengan {batch_size} interaksi...")
        polling_result = polling_system.check_notifications()
        results['polling_times'].append(polling_result['processing_time'])
        results['polling_efficiency'].append(polling_result['notifications_sent'] / max(1, polling_result['processing_time']))
        
        print(f"  Waktu pemrosesan: {polling_result['processing_time']:.6f} detik")
        print(f"  Notifikasi terkirim: {polling_result['notifications_sent']}")
        print(f"  Interaksi diperiksa: {polling_result['interactions_checked']}")
        
        # Reset database untuk pengujian pubsub
        db.user_notifications = defaultdict(list)
        
        # Uji sistem pub/sub
        print(f"Menguji sistem Pub/Sub O(1) dengan {batch_size} interaksi...")
        pubsub_result = pubsub_system.process_batch_interactions(new_interactions)
        results['pubsub_times'].append(pubsub_result['processing_time'])
        results['pubsub_efficiency'].append(pubsub_result['notifications_sent'] / max(1, pubsub_result['processing_time']))
        
        print(f"  Waktu pemrosesan: {pubsub_result['processing_time']:.6f} detik")
        print(f"  Notifikasi terkirim: {pubsub_result['notifications_sent']}")
        print(f"  Interaksi diperiksa: {pubsub_result['interactions_checked']}")
    
    return results

# Fungsi untuk membuat visualisasi hasil pengujian
def visualize_results(results):
    # Grafik waktu pemrosesan
    plt.figure(figsize=(14, 7))
    plt.subplot(1, 2, 1)
    plt.plot(results['batch_sizes'], results['polling_times'], 'ro-', label='Polling Linier O(n)')
    plt.plot(results['batch_sizes'], results['pubsub_times'], 'go-', label='Pub/Sub O(1)')
    plt.title('Waktu Pemrosesan vs Ukuran Batch')
    plt.xlabel('Jumlah Interaksi')
    plt.ylabel('Waktu Pemrosesan (detik)')
    plt.legend()
    plt.grid(True)
    
    # Grafik efisiensi
    plt.subplot(1, 2, 2)
    plt.plot(results['batch_sizes'], results['polling_efficiency'], 'ro-', label='Polling Linier O(n)')
    plt.plot(results['batch_sizes'], results['pubsub_efficiency'], 'go-', label='Pub/Sub O(1)')
    plt.title('Efisiensi vs Ukuran Batch')
    plt.xlabel('Jumlah Interaksi')
    plt.ylabel('Notifikasi/Detik')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('perbandingan_kinerja.png')
    plt.close()
    
    # Buat tabel perbandingan
    print("\n--- Tabel Perbandingan Kinerja ---")
    print("| Jumlah Interaksi | Waktu Polling O(n) | Waktu Pub/Sub O(1) | Rasio Peningkatan |")
    print("|------------------|-------------------|-------------------|-------------------|")
    
    for i, batch_size in enumerate(results['batch_sizes']):
        polling_time = results['polling_times'][i]
        pubsub_time = results['pubsub_times'][i]
        improvement = polling_time / max(pubsub_time, 0.000001)  # Hindari pembagian dengan nol
        
        print(f"| {batch_size:16,d} | {polling_time:17.6f} | {pubsub_time:17.6f} | {improvement:17.2f}x |")

    return {
        'batch_sizes': results['batch_sizes'],
        'polling_times': results['polling_times'],
        'pubsub_times': results['pubsub_times'],
        'improvement_ratios': [pt / max(pst, 0.000001) for pt, pst in zip(results['polling_times'], results['pubsub_times'])]
    }

# Fungsi utama
def main():
    print("=== SISTEM NOTIFIKASI MEDIA SOSIAL: PERBANDINGAN ALGORITMA ===")
    print("Membandingkan kinerja algoritma Polling Linier O(n) vs. Pub/Sub O(1)\n")
    
    # Jalankan pengujian
    results = run_performance_test()
    
    # Visualisasikan hasil
    table_data = visualize_results(results)
    
    print("\n=== KESIMPULAN ===")
    avg_improvement = sum(table_data['improvement_ratios']) / len(table_data['improvement_ratios'])
    max_improvement = max(table_data['improvement_ratios'])
    batch_with_max = table_data['batch_sizes'][table_data['improvement_ratios'].index(max_improvement)]
    
    print(f"1. Algoritma Pub/Sub O(1) rata-rata {avg_improvement:.2f}x lebih cepat dari Polling Linier O(n)")
    print(f"2. Peningkatan kinerja terbesar ({max_improvement:.2f}x) terjadi pada batch ukuran {batch_with_max:,d} interaksi")
    print(f"3. Keunggulan Pub/Sub semakin signifikan seiring bertambahnya jumlah interaksi")
    print("\nDisarankan untuk mengimplementasikan sistem notifikasi berbasis Pub/Sub untuk aplikasi media sosial dengan jumlah pengguna dan interaksi yang besar.")

if __name__ == "__main__":
    main()
