import os

os.system('pip install .')

from pathlib import Path
from playwright.sync_api import sync_playwright

def chromium_installed():
    with sync_playwright() as p:
        path = Path(p.chromium.executable_path)
        return path.exists()

if not chromium_installed():
    from sys import executable
    os.system(f'{executable} -m playwright install chromium')

print('Everything is ready. Launch the project with main.py')
os.startfile('main.py')