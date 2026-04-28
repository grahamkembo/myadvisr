"""
GOOGLE COLAB LAUNCH CELL — myAdvisr with RAG
=============================================
Run this single cell in Google Colab after uploading myadvisr_rag.zip.
It installs all dependencies, patches the API key, and launches the app.
"""

# ── Step 1: Unzip ──────────────────────────────────────────────────────────
import os, subprocess, threading, time, re

os.system("unzip -o myadvisr_rag.zip 2>/dev/null || echo 'Zip already extracted'")
print("Files:", os.listdir("myadvisr_rag"))

# ── Step 2: Install dependencies (takes 2-3 min on first run) ──────────────
print("\nInstalling dependencies (this takes ~2-3 minutes on first run)...")
os.system("pip install streamlit anthropic sentence-transformers chromadb -q")
print("Dependencies installed.")

# ── Step 3: Patch API key ──────────────────────────────────────────────────
API_KEY = "sk-ant-..."   # <-- paste your Anthropic API key here

with open("myadvisr_rag/app.py", "r") as f:
    code = f.read()

code = re.sub(
    r'client\s*=\s*Anthropic\([^)]*\)',
    f'client = Anthropic(api_key="{API_KEY}")',
    code
)

with open("myadvisr_rag/app.py", "w") as f:
    f.write(code)

check = subprocess.run(["grep", "Anthropic(", "myadvisr_rag/app.py"],
                       capture_output=True, text=True)
print("Key patch:", check.stdout.strip())

# ── Step 4: Kill old instances ──────────────────────────────────────────────
os.system("pkill -f streamlit 2>/dev/null || true")
os.system("pkill -f cloudflared 2>/dev/null || true")
time.sleep(2)

# ── Step 5: Download cloudflared tunnel ────────────────────────────────────
if not os.path.exists("cloudflared"):
    os.system("wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared")
    os.system("chmod +x cloudflared")

# ── Step 6: Launch Streamlit ───────────────────────────────────────────────
def run_streamlit():
    subprocess.run(
        ["streamlit", "run", "myadvisr_rag/app.py",
         "--server.port=8501",
         "--server.headless=true",
         "--server.enableCORS=false",
         "--server.enableXsrfProtection=false"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

threading.Thread(target=run_streamlit, daemon=True).start()
print("\nStarting Streamlit (RAG index builds on first load, ~30 seconds)...")
time.sleep(10)

# ── Step 7: Open tunnel ────────────────────────────────────────────────────
tunnel = subprocess.Popen(
    ["./cloudflared", "tunnel", "--url", "http://localhost:8501"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
)

url = None
for _ in range(60):
    line = tunnel.stdout.readline().decode("utf-8", errors="ignore").strip()
    if line: print("tunnel:", line)
    match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", line)
    if match:
        url = match.group(0)
        break
    time.sleep(1)

if url:
    print("\n" + "="*56)
    print("  myAdvisr + RAG is LIVE:")
    print(f"  {url}")
    print("="*56)
    print("\n  On first load, the RAG index builds (~20-30 seconds).")
    print("  You will see 'Loading knowledge base...' in the app.")
    print("  After that, every AI response is grounded in real Clarkson data.")
else:
    print("\nCheck tunnel lines above for the URL.")
