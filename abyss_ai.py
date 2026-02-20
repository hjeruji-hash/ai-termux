import time, requests, os, json, subprocess, re
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.prompt import Prompt
import google.generativeai as genai
import PIL.Image # Pastikan sudah install: pip install pillow

# --- CONFIG API GEMINI (Untuk Vision) ---
# Masukkan API Key Gemini kamu di sini
genai.configure(api_key="ISI_API_KEY_GEMINI_KAMU_DI_SINI")

def ask_vision(image_path, prompt):
    """Fungsi untuk membuat AI 'melihat' gambar"""
    try:
        # Load model vision Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Buka gambar
        img = PIL.Image.open(image_path)
        
        # Tanya ke AI
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"✘ Mata Abyss Error: {str(e)}"

console = Console()
MEMORY_FILE = "abyss_memory.json"

# --- CONFIG MESIN ---
CONFIG = [
    {"name": "GROQ", "key": "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", "url": "https://api.groq.com/openai/v1/chat/completions", "model": "llama-3.3-70b-versatile"},
    {"name": "OPENROUTER", "key": "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", "url": "https://openrouter.ai/api/v1/chat/completions", "model": "google/gemini-2.0-flash-001"}
]

# --- FITUR 1: MEMORI ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f: return json.load(f)
    return []

def save_memory(history):
    with open(MEMORY_FILE, "w") as f: json.dump(history[-20:], f)

chat_history = load_memory()

# --- FITUR 2: DOWNLOADER VIDEO ---
def download_media(url):
    save_path = "/sdcard/Download"
    if not os.path.exists(save_path): save_path = "downloads"
    
    console.print(f"[bold yellow]⚡ Mendownload ke Folder Download...[/bold yellow]")
    try:
        subprocess.run(["yt-dlp", "-o", f"{save_path}/%(title)s.%(ext)s", "--no-playlist", url], check=True)
        return f"✔ **Mission Success!** File ada di folder Download HP kamu."
    except:
        return "✘ **Gagal!** Cek izin storage (`termux-setup-storage`) atau linknya."

# --- FITUR 3: STREAMING MUSIK (HEMAT KUOTA) ---
def stream_infinite_music(query):
    """Memutar musik tanpa henti (Infinite Radio) kualitas paling hemat"""
    console.print(f"[bold magenta]📻 Abyss Radio: Menyiarkan {query} Tanpa Henti...[/bold magenta]")
    console.print("[dim]KONTROL: [ENTER] Next | [P] Pause | [Q] Stop[/dim]")
    
    cmd = [
        "mpv",
        "--no-video",
        "--ytdl-format=worstaudio/worst",
        "--loop-playlist=inf",
        "--shuffle",
        "--tls-verify=no",
        "--af=equalizer=f=60:w=100:g=10", 
        f"ytdl://ytsearch20:{query} music" 
    ]
    
    try:
        subprocess.run(cmd)
        return "✔ Radio dimatikan."
    except:
        return "✘ Gagal memulai radio."

# --- FITUR 4: TAMPILAN ---
def hacker_loading():
    console.clear()
    for task in ["LOADING KERNEL", "SYNCING MEMORY", "READYING DOWNLOADER", "TUNING RADIO"]:
        console.print(f"[bold green][#] {task}...", end="\r"); time.sleep(0.4)
        console.print(f"[bold green][OK] {task}          ")
    time.sleep(0.5); console.clear()
    console.print(Panel.fit("[bold green]Asisten Hadi[/bold green]\n[dim]HACKER | MUSIC | DOWNLOADER | AI[/dim]", border_style="green", padding=(1, 5)))

def get_ai_response(user_input):
    chat_history.append({"role": "user", "content": user_input})
    for engine in CONFIG:
        try:
            res = requests.post(engine['url'], headers={"Authorization": f"Bearer {engine['key']}"}, json={"messages": chat_history[-10:], "model": engine['model'], "temperature": 0.6}, timeout=20)
            if res.status_code == 200:
                answer = res.json()['choices'][0]['message']['content']
                chat_history.append({"role": "assistant", "content": answer})
                save_memory(chat_history)
                return answer, engine['name']
        except: continue
    return "Neural Link Severed.", "None"

def render_response(text, provider):
    full_msg = ""
    title = f"[bold green]💬 Abyss_{provider}[/bold green]"
    with Live(Panel("", title=title, border_style="green"), console=console, transient=True) as live:
        words = text.split(" ")
        for word in words:
            full_msg += word + " "
            live.update(Panel(Markdown(full_msg), title=title, border_style="green", padding=(1,2)))
            time.sleep(0.015)
    console.print(Panel(Markdown(full_msg), title=title, border_style="green", padding=(1,2)))

# --- LOGIKA UTAMA ---
if __name__ == "__main__":
    try:
        hacker_loading()
        while True:
            msg = Prompt.ask("\n[bold green]>[/bold green]")
            if not msg: continue
            
            # Perintah Keluar/Clear
            if msg.lower() in ["exit", "quit", "clear"]:
                if msg.lower() == "clear":
                    chat_history.clear(); os.remove(MEMORY_FILE) if os.path.exists(MEMORY_FILE) else None
                    console.clear(); console.print("[yellow]Memory wiped."); continue
                break

            # --- FITUR MATA (VISION) ---
            if msg.lower().startswith("lihat "):
                # Cara pakai: lihat /sdcard/foto.jpg apa isi foto ini?
                parts = msg.split(" ", 2)
                if len(parts) >= 3:
                    path = parts[1]
                    tanya = parts[2]
                    with console.status("[bold cyan]Abyss sedang melihat..."):
                        hasil = ask_vision(path, tanya)
                    console.print(Panel(hasil, title="👁️ ABYSS VISION", border_style="cyan"))
                else:
                    console.print("[red]Format salah! Contoh: lihat [jalur_foto] [pertanyaan][/red]")
                continue

            # LOGIKA 1: Streaming Musik
            if msg.lower().startswith("setel "):
                search = msg.lower().replace("setel ", "")
                status = stream_infinite_music(search)
                console.print(Panel(status, border_style="magenta"))
                continue

            # LOGIKA 2: Download Video
            if "http" in msg and any(x in msg for x in ["tiktok", "instagram", "youtube", "youtu", "vt"]):
                with console.status("[bold cyan]Bypassing Server..."):
                    link = re.findall(r'(https?://\S+)', msg)[0]
                    status = download_media(link)
                    console.print(Panel(status, title="SYSTEM LOG", border_style="yellow"))
                continue

            # LOGIKA 3: Tanya AI
            with console.status("[bold green]Mengetik..."):
                ans, src = get_ai_response(msg)
            render_response(ans, src)
            
            # Fitur Simpan Code (Tetap Pakai Konfirmasi y/n sesuai request)
            if "```" in ans:
                if Prompt.ask("\n[yellow]Simpan kodingan? (y/n)[/yellow]", choices=["y", "n"], default="n") == "y":
                    if not os.path.exists("saves"): os.makedirs("saves")
                    fname = f"saves/code_{int(time.time())}.txt"
                    with open(fname, "w") as f: f.write(ans)
                    console.print(f"[bold green]✔ Tersimpan: {fname}[/bold green]")

    except KeyboardInterrupt: pass
