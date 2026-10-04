"""
PhantomT4b
==========

browser.py is the main file of the PhantomT4b project. It is responsible for creating the application’s graphical user interface, launching Chromium via Playwright, managing the browser session, and navigating between pages.

The main idea behind PhantomT4b is that Chromium is launched not with a permanent user profile, but with a separate temporary directory. Thanks to this, each new session gets its own browser environment, which exists only during the session’s operation.

When the application is launched, a files directory is created, intended for storing files downloaded via Chromium. A separate module, catch_file.py, monitors this directory and informs the user when completed downloads appear.

The graphical part of the application is built on Tkinter. The interface is designed in a terminal style: it uses a black background, green monospaced text, green control elements, and a status console. This appearance is part of the visual concept of PhantomT4b.

Playwright is used as a tool for controlling Chromium. It allows you to launch the browser, open the required address, create pages, and perform basic navigation actions. When the session ends, the temporary Chromium profile is deleted, after which the next session is created anew.

The file architecture is divided into several logical parts. First, the main paths and application settings are created, then the browser states and Chromium control functions are defined. After that, the graphical interface, address bar, navigation buttons, status console, and bottom status bar are created.

Chromium is launched in a separate thread so that long‑running Playwright operations do not block the Tkinter interface. To modify interface elements from a background thread, root.after() is used, which passes the execution back to the main Tkinter thread.

The file does not contain its own logic for analyzing downloaded files. This task is handled by catch_file.py. Thanks to the division of responsibilities, browser.py handles the browser and the interface, while catch_file.py monitors the files folder and handles notifications.

PhantomT4b, in its current architecture, is a Chromium launcher with temporary browser sessions and a separate system for monitoring completed downloads. Further development of the project may include tabs, additional Chromium settings, enhanced profile management, event logging, and more complex interface elements.
"""

import os
import shutil
import tempfile
import threading
import tkinter as tk

from tkinter import messagebox
from playwright.sync_api import sync_playwright

import catch_file


APP_NAME = "PhantomT4b"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")

os.makedirs(FILES_DIR, exist_ok=True)


BLACK = "#000000"
GREEN = "#00FF41"
DARK_GREEN = "#008F11"
BRIGHT_GREEN = "#39FF14"

FONT = ("Courier New", 10)
FONT_BOLD = ("Courier New", 10, "bold")
FONT_TITLE = ("Courier New", 16, "bold")


playwright = None
context = None
page = None
profile_dir = None


root = tk.Tk()

root.title(APP_NAME)
root.geometry("950x620")
root.minsize(800, 500)
root.configure(bg=BLACK)


def log(text):
    console.config(state="normal")

    console.insert(
        "end",
        f"[ {APP_NAME} ] {text}\n"
    )

    console.see("end")
    console.config(state="disabled")


def set_status(text):
    status_label.config(
        text=f"STATUS :: {text}"
    )


def get_url():
    url = url_entry.get().strip()

    if not url:
        return "https://example.com"

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def launch_browser():
    global playwright
    global context
    global page
    global profile_dir

    url = get_url()

    launch_button.config(
        state="disabled"
    )

    set_status("INITIALIZING")
    log("Starting Chromium engine...")

    def worker():
        global playwright
        global context
        global page
        global profile_dir

        try:
            profile_dir = tempfile.mkdtemp(
                prefix="PhantomT4b_"
            )

            log(
                f"Temporary profile: {profile_dir}"
            )

            playwright = sync_playwright().start()

            log("Chromium engine loaded.")

            context = playwright.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                headless=False,
                viewport={
                    "width": 1280,
                    "height": 800
                },
                locale="ru-RU",
                timezone_id="Europe/Berlin",
                accept_downloads=True,
                downloads_path=FILES_DIR,
                args=[
                    "--start-maximized"
                ]
            )

            if context.pages:
                page = context.pages[0]
            else:
                page = context.new_page()

            log(f"Opening: {url}")

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            root.after(
                0,
                lambda: set_status(
                    "CHROMIUM RUNNING"
                )
            )

            root.after(
                0,
                lambda: log(
                    "Browser session started."
                )
            )

        except Exception as error:
            root.after(
                0,
                lambda: messagebox.showerror(
                    APP_NAME,
                    str(error)
                )
            )

            root.after(
                0,
                lambda: set_status(
                    "ERROR"
                )
            )

        finally:
            root.after(
                0,
                lambda: launch_button.config(
                    state="normal"
                )
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


def back():
    if page:
        try:
            page.go_back()
        except Exception as error:
            log(
                f"BACK ERROR :: {error}"
            )


def forward():
    if page:
        try:
            page.go_forward()
        except Exception as error:
            log(
                f"FORWARD ERROR :: {error}"
            )


def reload():
    if page:
        try:
            page.reload()
        except Exception as error:
            log(
                f"RELOAD ERROR :: {error}"
            )


def navigate():
    if page:
        try:
            url = get_url()

            log(
                f"Navigate: {url}"
            )

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

        except Exception as error:
            log(
                f"NAVIGATION ERROR :: {error}"
            )
    else:
        launch_browser()


def new_session():
    close_browser()

    root.after(
        500,
        launch_browser
    )


def close_browser():
    global playwright
    global context
    global page
    global profile_dir

    log("Closing browser...")

    try:
        if context:
            context.close()
    except Exception:
        pass

    context = None
    page = None

    try:
        if playwright:
            playwright.stop()
    except Exception:
        pass

    playwright = None

    if profile_dir:
        try:
            shutil.rmtree(
                profile_dir,
                ignore_errors=True
            )

            log(
                "Temporary profile deleted."
            )

        except Exception as error:
            log(
                f"PROFILE DELETE ERROR :: {error}"
            )

    profile_dir = None

    set_status("READY")


def cyber_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=BLACK,
        fg=GREEN,
        activebackground=DARK_GREEN,
        activeforeground=BRIGHT_GREEN,
        relief="solid",
        borderwidth=1,
        font=FONT_BOLD,
        padx=10,
        pady=4
    )


header = tk.Frame(
    root,
    bg=BLACK
)

header.pack(
    fill="x",
    padx=15,
    pady=(15, 5)
)


title = tk.Label(
    header,
    text="PHANTOMT4B",
    bg=BLACK,
    fg=GREEN,
    font=FONT_TITLE
)

title.pack(
    side="left"
)


version = tk.Label(
    header,
    text=" :: CHROMIUM LAUNCHER",
    bg=BLACK,
    fg=DARK_GREEN,
    font=FONT_BOLD
)

version.pack(
    side="left"
)


separator = tk.Label(
    root,
    text="============================================================",
    bg=BLACK,
    fg=DARK_GREEN,
    font=FONT
)

separator.pack(
    fill="x",
    padx=15
)


url_frame = tk.Frame(
    root,
    bg=BLACK
)

url_frame.pack(
    fill="x",
    padx=15,
    pady=12
)


url_label = tk.Label(
    url_frame,
    text="TARGET ::",
    bg=BLACK,
    fg=GREEN,
    font=FONT_BOLD
)

url_label.pack(
    side="left"
)


url_entry = tk.Entry(
    url_frame,
    bg=BLACK,
    fg=GREEN,
    insertbackground=GREEN,
    selectbackground=DARK_GREEN,
    selectforeground=GREEN,
    relief="solid",
    borderwidth=1,
    font=FONT
)

url_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10
)

url_entry.insert(
    0,
    "https://example.com"
)

url_entry.bind(
    "<Return>",
    lambda event: navigate()
)


launch_button = cyber_button(
    url_frame,
    "[ LAUNCH ]",
    launch_browser
)

launch_button.pack(
    side="right"
)


nav_frame = tk.Frame(
    root,
    bg=BLACK
)

nav_frame.pack(
    fill="x",
    padx=15
)


cyber_button(
    nav_frame,
    "[ < ]",
    back
).pack(
    side="left",
    padx=3
)


cyber_button(
    nav_frame,
    "[ > ]",
    forward
).pack(
    side="left",
    padx=3
)


cyber_button(
    nav_frame,
    "[ REFRESH ]",
    reload
).pack(
    side="left",
    padx=3
)


cyber_button(
    nav_frame,
    "[ NEW SESSION ]",
    new_session
).pack(
    side="left",
    padx=3
)


cyber_button(
    nav_frame,
    "[ CLOSE ]",
    close_browser
).pack(
    side="right",
    padx=3
)


console_frame = tk.Frame(
    root,
    bg=BLACK
)

console_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)


console = tk.Text(
    console_frame,
    bg=BLACK,
    fg=GREEN,
    insertbackground=GREEN,
    selectbackground=DARK_GREEN,
    selectforeground=GREEN,
    relief="solid",
    borderwidth=1,
    font=FONT,
    wrap="word"
)

console.pack(
    fill="both",
    expand=True
)

console.config(
    state="disabled"
)


status_label = tk.Label(
    root,
    text="STATUS :: READY",
    bg=BLACK,
    fg=GREEN,
    anchor="w",
    font=FONT_BOLD
)

status_label.pack(
    fill="x",
    padx=15,
    pady=(0, 12)
)


log("PhantomT4b initialized.")
log("Chromium launcher ready.")
log(f"Download directory: {FILES_DIR}")
log("File watcher initialized.")
log("Waiting for target...")


catch_file.start(
    root,
    FILES_DIR
)


def on_close():
    close_browser()
    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    on_close
)


root.mainloop()
