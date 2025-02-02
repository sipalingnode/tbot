### T3rnBot - Bot Auto Bridge Multi-Chain (Arbitrum Sepolia, OP Sepolia, Blast Sepolia, Base Sepolia)

T3rnBot adalah bot otomatis yang melakukan bridging token di antara beberapa jaringan, termasuk 
Arbitrum Sepolia, OP Sepolia, Blast Sepolia, dan Base Sepolia. Bot ini dirancang untuk memudahkan 
transfer token antarjaringan dengan cepat dan efisien.


### Fitur
- **Auto Bridging Multi-Chain:** Mengotomatisasi proses bridging dari Arbitrum Sepolia, OP Sepolia, 
  Blast Sepolia, dan Base Sepolia.
- **Notifikasi Transaksi Real-Time:** Menampilkan hasil transaksi yang berhasil secara real-time 
  dengan detail seperti hash transaksi, jumlah ETH yang dikirim, dan total transaksi yang sukses.
- **Penandaan Jaringan dengan Warna:** Output menampilkan warna berbeda untuk setiap jaringan 
  (Arbitrum, OP, Blast, Base) agar mudah diidentifikasi.
- **Pengecekan Koneksi Jaringan:** Bot akan memeriksa apakah terhubung ke setiap jaringan sebelum 
  memulai proses bridging.
- **Retry Transaksi:** Jika ada kegagalan dalam perkiraan gas atau pengiriman transaksi, bot akan 
  menampilkan pesan kesalahan.
  
### Instalasi

1. Clone repository ini ke lokal Anda:

   ```bash
   git clone https://github.com/hnfdm/tbot-asc.git
   ```

2. Masuk ke direktori proyek:
   ```bash
   cd tbot-asc
   ```

3. Install dependencies yang diperlukan:
   ```bash
   pip install web3 eth_account
   ```

### Konfigurasi

1. Ganti `private_keys`, `my_addresses`, dan `labels` dengan pk dan address di file `config.py`.

2. Atur rpc dan ca di file `config.py` sesuai dengan jaringan yang ingin Anda gunakan.
   
3. Masukkan data hex pada `config.py` dengan cara lakukan swap manual & copy HEX.

### Cara Penggunaan

1. Jalankan bot dengan perintah berikut:
   
   ```bash
   python t3rn.py
   ```

2. Bot akan secara otomatis melakukan bridging antarjaringan sesuai dengan konfigurasi yang telah diatur.

### FAQ

- Q: "Pip install error?"
- A: "Pake virtual environtment"
   ```bash
   python3 -m venv t3rn
   ```
   ```bash
   source t3rn/bin/activate
   ```

- Q: "Error estimating gas...R07..." / "BRN ga sinkron?"
- A: "Ganti HEX dengan punya kalian & pastikan dari transaksi yang sudah berhasil"

### Catatan
- Jangan lupa pakein screen/tmux.
- Pastikan saldo yang cukup tersedia di setiap jaringan sebelum memulai bridging.

### Acknowledgements
- Inspired by [airdropinsiders](https://github.com/airdropinsiders)
