import time, requests, os, json, subprocess, re, base64
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.align import Align

console = Console()
MEMORY_FILE = "abyss_memory.json"

# --- CONFIG MESIN (Sistem Ternak Otomatis) ---
def get_farm_engines():
    engines = []
    # Scan 5 Akun Groq dari Termux
    for i in range(1, 6):
        key = os.getenv(f"MY_GROQ_KEY_{i}")
        if key:
            engines.append({
                "name": f"GROQ-ACC-{i}",
                "key": key,
                "url": "https://api.groq.com/openai/v1/chat/completions",
                "model": "llama-3.3-70b-versatile"
            })
    
    # Scan 5 Akun OpenRouter dari Termux
    for i in range(1, 6):
        key = os.getenv(f"MY_OR_KEY_{i}")
        if key:
            engines.append({
                "name": f"OR-ACC-{i}",
                "key": key,
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "model": "google/gemini-2.0-flash-001"
            })
    return engines

CONFIG = get_farm_engines()

# --- FITUR 1: MATA (VISION) ---
def ask_vision(image_path, prompt):
    try:
        if not os.path.exists(image_path): return f"✘ File tidak ditemukan: {image_path}"
        or_acc = [e for e in CONFIG if "OR-ACC" in e['name']]
        if not or_acc: return "✘ Tidak ada akun OpenRouter untuk Vision!"
        
        with open(image_path, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        headers = {"Authorization": f"Bearer {or_acc[0]['key']}", "Content-Type": "application/json"}
        data = {
            "model": or_acc[0]['model'], 
            "messages": [
                {"role": "user", "content": [
                    {"type": "text", "text": prompt}, 
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                ]}
            ]
        }
        res = requests.post(or_acc[0]['url'], headers=headers, json=data, timeout=30)
        return res.json()['choices'][0]['message']['content'] if res.status_code == 200 else f"✘ Error: {res.text}"
    except Exception as e: return f"✘ Error Vision: {str(e)}"

# --- FITUR 2: MEMORI ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f: return json.load(f)
    return []

def save_memory(history):
    with open(MEMORY_FILE, "w") as f: json.dump(history[-20:], f)

chat_history = load_memory()

# --- FITUR 3: DOWNLOADER & RADIO ---
def download_media(url):
    save_path = "/sdcard/Download"
    if not os.path.exists(save_path): save_path = "downloads"
    console.print(f"[bold yellow]⚡ Mendownload...[/bold yellow]")
    try:
        subprocess.run(["yt-dlp", "-o", f"{save_path}/%(title)s.%(ext)s", "--no-playlist", url], check=True)
        return f"✔ Mission Success! Cek folder Download."
    except: return "✘ Gagal! Cek koneksi."

def stream_infinite_music(query):
    console.print(f"[bold magenta]📻 Radio: {query}...[/bold magenta]")
    try:
        subprocess.run(["mpv", "--no-video", "--ytdl-format=worstaudio", f"ytdl://ytsearch20:{query} music"])
        return "✔ Radio dimatikan."
    except: return "✘ MPV bermasalah."

# --- FITUR LOADING: PAMER KANDANG ---
def hacker_loading():
    console.clear()
    total = len(CONFIG)
    tasks = ["INITIALIZING NEURAL LINK", "SYNCING API FARM", "ESTABLISHING PROTOCOL"]
    
    print("\n" * (console.height // 5))
    with console.status("", spinner="aesthetic") as status:
        for t in tasks:
            padding = (console.width - len(t)) // 2
            console.print(" " * padding + f"[bold green]{t}[/bold green]")
            time.sleep(0.5)
            
    console.print(f"\n[bold cyan] 🔎 SCANNING KANDANG API...[/bold cyan]")
    time.sleep(0.3)
    
    for i, engine in enumerate(CONFIG, 1):
        status_ikon = "[bold green]ONLINE[/bold green]"
        console.print(f"  [bold white]├─[/bold white] Engine {i}/{total}: [bold yellow]{engine['name']}[/bold yellow] .... {status_ikon}")
        time.sleep(0.15)
        
    console.print(f"\n[bold green] ✅ {total} SAPI SIAP DIPERAH![/bold green]")
    time.sleep(1.2)
    console.clear()
    
    banner = Panel.fit("[bold green]ABYSS AI[/bold green]\n[dim]Hadi Edition | Farmer Mode Active[/dim]", border_style="green", padding=(1, 5))
    console.print(Align.center(banner))
    time.sleep(1)
    console.clear()

# --- LOGIKA CHAT (DIEM-DIEM PINDAH AKUN) ---
def get_ai_response(user_input):
    chat_history.append({"role": "user", "content": user_input})
    for engine in CONFIG:
        try:
            res = requests.post(
                engine['url'], 
                headers={"Authorization": f"Bearer {engine['key']}"}, 
                json={"messages": chat_history[-10:], "model": engine['model'], "temperature": 0.6}, 
                timeout=15
            )
            if res.status_code == 200:
                answer = res.json()['choices'][0]['message']['content']
                chat_history.append({"role": "assistant", "content": answer})
                save_memory(chat_history)
                return answer, engine['name']
            # Jika limit, loop akan lanjut ke engine berikutnya secara otomatis
        except:
            continue
    return "Semua akun di kandang LIMIT/ERROR!", "FAILED"

def render_response(text, provider):
    full_msg = ""
    title = f"[bold green]💬 Abyss_{provider}[/bold green]"
    with Live(Panel("", title=title, border_style="green"), console=console, transient=True) as live:
        for word in text.split(" "):
            full_msg += word + " "
            live.update(Panel(Markdown(full_msg), title=title, border_style="green", padding=(1,2)))
            time.sleep(0.015)
    console.print(Panel(Markdown(full_msg), title=title, border_style="green", padding=(1,2)))

# --- LOOP UTAMA ---
if __name__ == "__main__":
    hacker_loading()
    try:
        while True:
            msg = Prompt.ask("\n[bold green]>[/bold green]")
            if not msg: continue
            if msg.lower() in ["exit", "quit"]: break
            if msg.lower() == "clear":
                chat_history.clear()
                if os.path.exists(MEMORY_FILE): os.remove(MEMORY_FILE)
                console.clear(); continue
            
            # Fitur: Vision
            if msg.lower().startswith("lihat "):
                parts = msg.split(" ", 2)
                if len(parts) >= 3:
                    with console.status("[bold cyan]Abyss melihat..."):
                        hasil = ask_vision(parts[1].strip("'\""), parts[2])
                    console.print(Panel(hasil, title="👁️ VISION", border_style="cyan"))
                continue
            
            # Fitur: Radio
            if msg.lower().startswith("setel "):
                stream_infinite_music(msg.replace("setel ", "")); continue
            
            # Fitur: Downloader
            if "http" in msg:
                link = re.findall(r'(https?://\S+)', msg)[0]
                console.print(Panel(download_media(link), title="DOWNLOADER", border_style="yellow")); continue
            
            # Fitur: Chat Utama
            with console.status("[bold green]Mengetik..."):
                ans, src = get_ai_response(msg)
            render_response(ans, src)
            
            # Fitur: Simpan Kode
            if "```" in ans:
                if Prompt.ask("\n[yellow]Simpan kodingan? (y/n)[/yellow]", choices=["y", "n"], default="n") == "y":
                    if not os.path.exists("saves"): os.makedirs("saves")
                    fname = f"saves/code_{int(time.time())}.txt"
                    with open(fname, "w") as f: f.write(ans)
                    console.print(f"[bold green]✔ Tersimpan di folder saves/[/bold green]")
    except KeyboardInterrupt:
        pass
