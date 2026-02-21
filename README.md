# 🌌 ABYSS AI v5.0 - HADI EDITION
**Abyss AI** adalah asisten multifungsi berbasis terminal (Termux) yang menggabungkan kecerdasan buatan, hiburan musik, dan alat pengunduh media dalam satu sistem terpadu.

---

## 🚀 Fitur Utama
* **🤖 Otak Ganda (Multi-Engine)**: Menggunakan **GROQ (Llama 3.3)** untuk chat super cepat dan **OpenRouter (Gemini 2.0)** sebagai cadangan.
* **👁️ Abyss Vision**: Mampu menganalisis dan membaca gambar langsung dari penyimpanan HP.
* **📻 Infinite Radio**: Streaming musik YouTube tanpa henti dengan kualitas hemat kuota dan efek *Bass Boost*.
* **📥 Universal Downloader**: Download video dari TikTok (No WM), Instagram, dan YouTube langsung ke `/sdcard/Download`.
* **💾 Auto Code Saver**: Menyimpan snippet kodingan dari AI secara otomatis ke folder `saves/`.
* **🧠 Smart Memory**: Mengingat konteks percakapan hingga 20 pesan terakhir.

---

## 🛠️ Langkah-Langkah Instalasi

### 1. Update & Install Package Pendukung
Pastikan Termux kamu sudah memiliki alat-alat dasar:
```bash
pkg update && pkg upgrade -y
pkg install python mpv ffmpeg rust binutils build-essential -y
termux-setup-storage
2. Install Library Utama
Bash

pip install requests rich pillow yt-dlp

### 3. Clone & Jalankan
Bash

git clone [https://github.com/USERNAME_KAMU/NAMA_REPO_KAMU.git](https://github.com/USERNAME_KAMU/NAMA_REPO_KAMU.git)
cd NAMA_REPO_KAMU
python abyss_ai.py

🎮 Panduan Perintah
Perintah	Deskripsi	Contoh
apa itu AI?	Chat biasa dengan AI	jelaskan cara kerja mesin
lihat [path]	Menyuruh AI melihat gambar	lihat /sdcard/foto.jpg ini siapa?
setel [judul]	Putar musik YouTube	setel lagu denny caknan
[Link URL]	Download Video otomatis	https://vt.tiktok.com/xxxx/
clear	Hapus semua memori chat	clear
🤝 Kontribusi

Project ini dikembangkan oleh Hadi dengan bantuan Gemini AI. Jangan ragu untuk melakukan Fork atau memberikan Star ⭐ jika kamu suka project ini!

<p align="center">Built with ❤️ for Termux Users</p>


-----
