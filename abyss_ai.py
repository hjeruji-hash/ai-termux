import time, requests, os, json, subprocess, re, base64
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.align import Align

# --- CONFIG MESIN ---
# Saya sudah set OpenRouter sebagai mesin utama untuk Chat dan Vision (Mata)
CONFIG = [
    {"name": "GROQ", "key": "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", "url": "https://api.groq.com/openai/v1/chat/completions", "model": "llama-3.3-70b-versatile"},
    {"name": "ABYSS-EYES", "key": "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", "url": "https://openrouter.ai/api/v1/chat/completions", "model": "google/gemini-2.0-flash-001"}
]

console = Console()
MEMORY_FILE = "abyss_memory.json"

# --- FITUR 1: MATA (VISION) VIA OPENROUTER ---
def ask_vision(image_path, prompt):
    """Fungsi Vision Anti-Error (Tanpa library Google)"""
    try:
        if not os.path.exists(image_path):
            return f"✘ File tidak ditemukan: {image_path}"
            
        with open(image_path, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Gunakan API Key OpenRouter yang tadi ijo/online
        headers = {
            "Authorization": f"Bearer {CONFIG[1]['key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": CONFIG[1]['model'],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]
                }
            ]
        }

        res = requests.post(CONFIG[1]['url'], headers=headers, json=data, timeout=30)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        else:
            return f"✘ Error Mesin ({res.status_code}): {res.text}"
    except Exception as e:
        return f"✘ Mata Abyss Error: {str(e)}"

# --- FITUR 2: MEMORI ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f: return json.load(f)
    return []

def save_memory(history):
    with open(MEMORY_FILE, "w") as f: json.dump(history[-20:], f)

chat_history = load_memory()

# --- FITUR 3: DOWNLOADER VIDEO ---
def download_media(url):
    save_path = "/sdcard/Download"
    if not os.path.exists(save_path): save_path = "downloads"
    
    console.print(f"[bold yellow]⚡ Mendownload ke Folder Download...[/bold yellow]")
    try:
        # Memastikan yt-dlp ada
        subprocess.run(["yt-dlp", "-o", f"{save_path}/%(title)s.%(ext)s", "--no-playlist", url], check=True)
        return f"✔ **Mission Success!** Cek folder Download HP."
    except:
        return "✘ **Gagal!** Coba ketik: pkg install ffmpeg -y"

# --- FITUR 4: STREAMING MUSIK ---
def stream_infinite_music(query):
    console.print(f"[bold magenta]📻 Abyss Radio: {query}...[/bold magenta]")
    cmd = [
        "mpv", "--no-video", "--ytdl-format=worstaudio/worst",
        "--loop-playlist=inf", "--shuffle", "--tls-verify=no",
        "--af=equalizer=f=60:w=100:g=10", 
        f"ytdl://ytsearch20:{query} music" 
    ]
    try:
        subprocess.run(cmd)
        return "✔ Radio dimatikan."
    except:
        return "✘ MPV belum terinstall. Ketik: pkg install mpv -y"

# --- FITUR 5: TAMPILAN ---
def hacker_loading():
    console.clear()
    width = console.width
    height = console.height
    
    tasks = [
        "INITIALIZING NEURAL LINK", 
        "BYPASSING CRYPTOGRAPHY", 
        "OPENING ABYSS EYES", 
        "SYNCING OPENROUTER ENGINE", 
        "ESTABLISHING PROTOCOL"
    ]
    
    # Jarak vertikal (ke tengah layar)
    print("\n" * (height // 4))
    
    # Animasi loading tanpa [OK]
    with console.status("", spinner="aesthetic") as status:
        for task in tasks:
            # Hitung jarak spasi agar teks pas di tengah horizontal
            padding = (width - len(task)) // 2
            # Cetak teks task saja
            console.print(" " * padding + f"[bold green]{task}[/bold green]")
            time.sleep(0.7)
    
    time.sleep(0.5)
    console.clear()
    
    # Jarak vertikal untuk Banner utama
    print("\n" * (height // 3))
    
    # Banner utama tetap di tengah
    from rich.align import Align
    banner = Panel.fit(
        "[bold green]ABYSS AI[/bold green]\n[dim]Hadi Edition | Vision Active[/dim]", 
        border_style="green", 
        padding=(1, 5)
    )
    console.print(Align.center(banner))
    time.sleep(1.5)
    console.clear()
    
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
    return "Jalur Terputus.", "None"

def render_response(text, provider):
    full_msg = ""
    title = f"[bold green]💬 Abyss_{provider}[/bold green]"
    with Live(Panel("", title=title, border_style="green"), console=console, transient=True) as live:
        for word in text.split(" "):
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
            
            if msg.lower() in ["exit", "quit", "clear"]:
                if msg.lower() == "clear":
                    chat_history.clear()
                    if os.path.exists(MEMORY_FILE): os.remove(MEMORY_FILE)
                    console.clear(); continue
                break

            # FITUR MATA (VISION)
            if msg.lower().startswith("lihat "):
                parts = msg.split(" ", 2)
                if len(parts) >= 3:
                    # Ini bagian kuncinya: .strip akan hapus tanda petik otomatis
                    path = parts[1].strip("'").strip('"')
                    tanya = parts[2]
                    
                    # Tambahan: Cek folder internal juga otomatis
                    if not os.path.exists(path):
                        internal_path = f"/data/data/com.termux/files/home/screenshot/{path}"
                        if os.path.exists(internal_path):
                            path = internal_path

                    with console.status("[bold cyan]Abyss sedang melihat..."):
                        hasil = ask_vision(path, tanya)
                    console.print(Panel(hasil, title="👁️ ABYSS VISION", border_style="cyan"))
                else:
                    console.print("[red]Format: lihat [jalur_foto] [pertanyaan][/red]")
                continue

            # Musik & Download
            if msg.lower().startswith("setel "):
                stream_infinite_music(msg.replace("setel ", ""))
                continue

            if "http" in msg:
                link = re.findall(r'(https?://\S+)', msg)[0]
                console.print(Panel(download_media(link), title="DOWNLOADER", border_style="yellow"))
                continue

            # Chat Biasa
            with console.status("[bold green]Mengetik..."):
                ans, src = get_ai_response(msg)
            render_response(ans, src)
            
            if "```" in ans:
                if Prompt.ask("\n[yellow]Simpan kodingan? (y/n)[/yellow]", choices=["y", "n"], default="n") == "y":
                    if not os.path.exists("saves"): os.makedirs("saves")
                    fname = f"saves/code_{int(time.time())}.txt"
                    with open(fname, "w") as f: f.write(ans)
                    console.print(f"[bold green]✔ Tersimpan di folder saves/[/bold green]")

    except KeyboardInterrupt: pass
