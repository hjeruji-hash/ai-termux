[readme.md](https://github.com/user-attachments/files/25445208/readme.md)
# 🌌 Abyss AI Assistant (v5.0) - Termux Edition

Asisten pribadi canggih untuk Termux yang menggabungkan kecerdasan buatan, multimedia, dan alat bantu hacker dalam satu interface terminal yang keren.

---

## 🚀 Fitur Utama
- **🤖 Dual Engine AI**: Menggunakan Groq (Llama 3.3) dan OpenRouter (Gemini 2.0).
- **👁️ Abyss Vision**: AI bisa "melihat" dan menjelaskan isi foto atau screenshot.
- **📻 Infinite Radio**: Putar musik YouTube non-stop dengan fitur **Bass Boost**.
- **📥 Media Downloader**: Ambil video TikTok (No WM), IG, dan YouTube langsung ke folder Download.
- **💾 Code Manager**: Fitur simpan kodingan otomatis ke folder `saves/`.
- **🧠 Smart Memory**: AI yang ingat konteks obrolan sebelumnya.

---

## 🛠️ Persiapan & Instalasi (Tutorial)

Buka Termux kamu dan jalankan perintah di bawah ini secara berurutan untuk menginstal semua tools yang dibutuhkan:

### 1. Update Sistem & Install Package Utama
```bash
pkg update && pkg upgrade -y
pkg install python git mpv ffmpeg -y
termux-setup-storage

#### install library pendukung [tools]
pip install requests rich google-generativeai pillow yt-dlp

##### konfigurasi apikei 
Buka file abyss_ai.py menggunakan nano dan masukkan API Key milikmu pada bagian CONFIG dan genai.configure.

    Groq API: Bikin di sini

    Gemini API: Bikin di sini

###### cara menjalannkanya 
python abyss_ai.py

###### panduan perintah chat
Perintah,Contoh Penggunaan
Setel Musik,setel lagu peterpan
Gunakan Mata,lihat /sdcard/Download/foto.jpg ini foto apa?
Download,Langsung tempel link TikTok/IG/YouTube
Bersihkan,clear (Menghapus memori & layar)
Keluar,exit atau quit

