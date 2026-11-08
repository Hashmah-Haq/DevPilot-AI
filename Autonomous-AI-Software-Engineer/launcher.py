"""Local-first one-click launcher. No Colab, tunnels or public links required."""
from __future__ import annotations
import os
import socket
import subprocess
import sys
import time
import urllib.request
import venv
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV = ROOT / '.venv'
PYTHON = ENV / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
LOG = ROOT / 'launcher_error.log'

def run(command):
    subprocess.run([str(x) for x in command], cwd=ROOT, check=True)

def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]

def main():
    if sys.version_info < (3, 10):
        raise RuntimeError('Python 3.10 or newer is required.')
    print('\n=== DevPilot AI Local Dashboard ===', flush=True)
    if not PYTHON.exists():
        print('First launch: creating isolated Python environment...', flush=True)
        venv.EnvBuilder(with_pip=True).create(ENV)
    print('Checking/installing dashboard dependencies (internet required first time)...', flush=True)
    run([PYTHON, '-m', 'pip', 'install', '-r', 'requirements.txt', '--disable-pip-version-check'])
    port = free_port()
    url = f'http://127.0.0.1:{port}'
    command = [str(PYTHON), '-m', 'streamlit', 'run', 'frontend/app.py',
               '--server.address=127.0.0.1', f'--server.port={port}',
               '--server.headless=true', '--browser.gatherUsageStats=false']
    print('Starting local server...', flush=True)
    with LOG.open('w', encoding='utf-8') as log:
        server = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    for _ in range(90):
        if server.poll() is not None:
            raise RuntimeError(f'Streamlit exited early. See {LOG.name}.')
        try:
            with urllib.request.urlopen(url + '/_stcore/health', timeout=1) as response:
                if response.status == 200:
                    break
        except (OSError, TimeoutError):
            time.sleep(1)
    else:
        server.terminate()
        raise RuntimeError(f'Server did not become ready. See {LOG.name}.')
    print(f'\nDashboard ready: {url}', flush=True)
    print('Opening your browser automatically...', flush=True)
    webbrowser.open(url)
    print('Keep this window open while using DevPilot AI. Press Ctrl+C to stop.\n', flush=True)
    try:
        server.wait()
    except KeyboardInterrupt:
        server.terminate()
        try:
            server.wait(timeout=8)
        except subprocess.TimeoutExpired:
            server.kill()
    return server.returncode or 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        with LOG.open('a', encoding='utf-8') as file:
            file.write(f'\nLAUNCHER ERROR: {type(exc).__name__}: {exc}\n')
        print(f'\nStartup error: {exc}\nSee {LOG} for details.', file=sys.stderr)
        sys.exit(1)
