# run_all.py
import os
import sys
import time
import socket
import subprocess
from pathlib import Path
from sandbox_setup import init_sandbox

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def main():
    if not Path(".env").exists() and Path(".env.example").exists():
        Path(".env").write_text(Path(".env.example").read_text(encoding="utf-8"), encoding="utf-8")
        print("[HYDRA] Created .env from .env.example. Populate ARMORIQ_API_KEY and GEMINI_API_KEY before running.")
        sys.exit(1)

    print("[HYDRA] Initializing sandbox environment...")
    init_sandbox()

    mcp_proc = None
    if not is_port_in_use(8000):
        print("[HYDRA] Starting FastMCP Server (hydra-mcp) on port 8000...")
        mcp_proc = subprocess.Popen([sys.executable, "mcp_server.py"])
        time.sleep(1.2)
    else:
        print("[HYDRA] Port 8000 already active — reusing running FastMCP server.")

    try:
        print("[HYDRA] Launching Retro OS Command Center...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n[HYDRA] Shutting down...")
    finally:
        if mcp_proc:
            mcp_proc.terminate()

if __name__ == "__main__":
    main()