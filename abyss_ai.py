import time, requests, os, json, subprocess, re, base64
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.align import Align

# --- CONFIG MESIN (Ninja Mode) ---
CONFIG = [
    {
        "name": "GROQ",
        "key": os.getenv("MY_GROQ_KEY"),
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "llama-3.3-70b-versatile"
    },
    {
        "name": "ABYSS-EYES",
        "key": os.getenv("MY_OR_KEY"),
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "model": "google/gemini-2.0-flash-001"
    }
]

console = Console()
MEMORY_FILE = "abyss_memory.json"

# --- FITUR 1: MATA (VISION) ---
def ask_vision(image_path, prompt):
    try:
        if not os.path.exists(image_path): return f"✘ File tidak ditemukan: {image_path}"
        with open(image_path, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        headers = {"Authorization": f"Bearer {CONFIG[1]['key']}", "Content-Type": "application/json"}
        data = {"model": CONFIG[1]['model'], "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}]}]}
        res = requests.post(CONFIG[1]['url'], headers=headers, json=data, timeout=30)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        return f"✘ Error Mesin: {res.text}"
    except Exception as e: return f"✘ Error Vision: {str(e)}"

# --- FITUR 2: MEMORI ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f: return json.load(f)
    return []

def save_memory(history):
    with open(MEMORY_FILE, "w") as f: json.dump(history[-20:], f)

chat_history = load_memory()

# --- FITUR 3: DOWNLOADER ---
def download_media(url):
    save_path = "/sdcard/Download"
    if not os.path.exists(save_path): save_path = "downloads"
    console.print(f"[bold yellow]⚡ Mendownload ke Folder Download...[/bold yellow]")
    try:
        subprocess.run(["yt-dlp", "-o", f"{save_path}/%(title)s.%(ext)s", "--no-playlist", url], check=True)
        return f"✔ **Mission Success!** Cek folder Download HP."
    except: return "✘ **Gagal!** Coba cek koneksi atau yt-dlp."

# --- FITUR 4: RADIO ---
def stream_infinite_music(query):
    console.print(f"[bold magenta]📻 Abyss Radio: {query}...[/bold magenta]")
    try:
        subprocess.run(["mpv", "--no-video", "--ytdl-format=worstaudio", f"ytdl://ytsearch20:{query} music"])
        return "✔ Radio dimatikan."
    except: return "✘ MPV bermasalah."

# --- FITUR 5: LOADING HACKER (YANG KAMU SUKA) ---
def hacker_loading():
    console.clear()
    width = console.width
    tasks = ["INITIALIZING NEURAL LINK", "BYPASSING CRYPTOGRAPHY", "OPENING ABYSS EYES", "SYNCING ENGINES", "ESTABLISHING PROTOCOL"]
    print("\n" * (console.height // 4))
    with console.status("", spinner="aesthetic") as status:
        for task in tasks:
            padding = (width - len(task)) // 2
            console.print(" " * padding + f"[bold green]{task}[/bold green]")
            time.sleep(0.6)
    console.clear()
    banner = Panel.fit("[bold green]ABYSS AI[/bold green]\n[dim]Hadi Edition | Vision Active[/dim]", border_style="green", padding=(1, 5))
    console.print(Align.center(banner))
    time.sleep(1.5)
    console.clear()

def get_ai_response(user_input):
    chat_history.append({"role": "user", "content": user_input})
    for engine in CONFIG:
        if not engine['key']: continue
        try:
            res = requests.post(engine['url'], headers={"Authorization": f"Bearer {engine['key']}"}, json={"messages": chat_history[-10:], "model": engine['model'], "temperature": 0.6}, timeout=20)
            if res.status_code == 200:
                answer = res.json()['choices'][0]['message']['content']
                chat_history.append({"role": "assistant", "content": answer})
                save_memory(chat_history)
                return answer, engine['name']
        except: continue
    return "Jalur Terputus. Cek API Key di Termux!", "None"

def render_response(text, provider):
    full_msg = ""
    title = f"[bold green]💬 Abyss_{provider}[/bold green]"
    with Live(Panel("", title=title, border_style="green"), console=console, transient=True) as live:
        for word in text.split(" "):
            full_msg += word + " "
            live.update(Panel(Markdown(full_msg), title=title, border_style="green", padding=(1,2)))
            time.sleep(0.015)
    console.print(Panel(Markdown(full_msg), title=title, border_style="green", padding=(1,2)))

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
            
            # Lihat Foto
            if msg.lower().startswith("lihat "):
                parts = msg.split(" ", 2)
                if len(parts) >= 3:
                    with console.status("[bold cyan]Abyss sedang melihat..."):
                        hasil = ask_vision(parts[1].strip("'\""), parts[2])
                    console.print(Panel(hasil, title="👁️ VISION", border_style="cyan"))
                continue
            
            # Setel Musik
            if msg.lower().startswith("setel "):
                stream_infinite_music(msg.replace("setel ", "")); continue
            
            # Link Downloader
            if "http" in msg:
                link = re.findall(r'(https?://\S+)', msg)[0]
                console.print(Panel(download_media(link), title="DOWNLOADER", border_style="yellow")); continue
            
            # Chat Biasa
            with console.status("[bold green]Mengetik..."):
                ans, src = get_ai_response(msg)
            render_response(ans, src)
            
            # FITUR SIMPAN KODINGAN (Balik lagi!)
            if "```" in ans:
                if Prompt.ask("\n[yellow]Simpan kodingan? (y/n)[/yellow]", choices=["y", "n"], default="n") == "y":
                    if not os.path.exists("saves"): os.makedirs("saves")
                    fname = f"saves/code_{int(time.time())}.txt"
                    with open(fname, "w") as f: f.write(ans)
                    console.print(f"[bold green]✔ Tersimpan di folder saves/[/bold green]")
    except KeyboardInterrupt: pass
