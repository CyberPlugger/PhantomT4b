# PhantomT4b

**PhantomT4b** is a lightweight Chromium launcher built with Python, Tkinter, and Playwright.

The project provides isolated temporary browser sessions, a dedicated download directory, and a simple hacker-style graphical interface.

Each browser session uses a temporary Chromium profile. When the session is closed, the temporary profile is removed.

## Features

* Temporary isolated Chromium sessions
* Playwright-based browser control
* Automatic Chromium installation
* Dedicated `files/` download directory
* Download completion notifications
* Browser navigation controls
* Refresh and new-session controls
* Terminal-style activity console
* Dark hacker-style interface
* Windows-friendly setup
* No permanent browser profile data

## Project Structure

```text
PhantomT4b/
├── launch.py
├── browser.py
├── catch_file.py
├── pyproject.toml
├── requirements.txt
├── install.md
├── README.md
└── files/
```

### `launch.py`

The main entry point.

It checks whether the Playwright Chromium browser is installed. If Chromium is missing, it installs it automatically and then starts the application.

Run the project with:

```bash
python launch.py
```

### `browser.py`

Contains the main PhantomT4b graphical interface and Chromium launcher.

It is responsible for:

* Starting Chromium
* Creating temporary browser profiles
* Opening websites
* Navigation
* Browser session management
* Download configuration
* GUI controls
* Application status messages

### `catch_file.py`

Monitors the `files/` directory for newly completed downloads.

Temporary browser download files such as:

```text
.crdownload
.tmp
.part
```

are ignored.

When a real file has finished downloading, PhantomT4b displays a notification containing the file name and its location.

### `files/`

All browser downloads are stored in this directory.

Example:

```text
PhantomT4b/
└── files/
    ├── example.zip
    ├── image.png
    └── document.pdf
```

## Requirements

* Windows 10 or Windows 11
* Python 3.10 or newer
* Internet connection for the initial Chromium installation

Python dependencies:

```text
playwright>=1.50,<2.0
```

## Installation

Clone the repository:

```bash
git clone https://github.com/CyberPlugger/PhantomT4b.git
cd PhantomT4b
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

You can also install the project using:

```bash
pip install .
```

## Chromium

PhantomT4b uses Playwright's Chromium build.

Normally, `launch.py` checks whether Chromium is already installed.

If it is missing, the launcher automatically runs:

```bash
python -m playwright install chromium
```

You can also install Chromium manually:

```bash
playwright install chromium
```

## Running

Start PhantomT4b:

```bash
python launch.py
```

The launcher will:

```text
Check Playwright
       |
       v
Check Chromium
       |
       +---- installed ----> Start PhantomT4b
       |
       +---- missing ------> Install Chromium
                                  |
                                  v
                           Start PhantomT4b
```

## Browser Sessions

Every new session creates a temporary browser profile.

The profile is stored temporarily on the local machine while Chromium is running.

When PhantomT4b closes the session, the temporary profile is removed.

This means normal browsing data from the temporary session is not reused by the next session.

PhantomT4b does not modify your regular Chrome or Chromium profile.

## Downloads

Downloads are redirected to:

```text
PhantomT4b/files/
```

The download monitor waits until a file is finished before displaying a notification.

For example:

```text
example.zip
```

will trigger a notification similar to:

```text
PhantomT4b

example.zip was added to:

C:\...\PhantomT4b\files\example.zip
```

## Interface

The application uses a terminal-inspired visual style:

```text
PHANTOMT4B
────────────────────────────────────────

[ URL / SEARCH ]

[ LAUNCH ] [ < ] [ > ] [ REFRESH ]
[ NEW SESSION ]          [ CLOSE ]

────────────────────────────────────────
SYSTEM CONSOLE

[STATUS] Chromium session initialized
[INFO] Temporary profile created
[INFO] Browser ready
```

The interface is intentionally minimal and uses a dark background with green terminal-style text.

## Configuration

The main browser configuration is located in `browser.py`.

The application uses:

```text
Locale:       ru-RU
Timezone:     Europe/Berlin
Viewport:     1280x800
Downloads:    files/
Headless:     False
```

The browser runs in visible mode so the user can interact with Chromium normally.

## Troubleshooting

### `ModuleNotFoundError: No module named 'playwright'`

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Chromium is missing

Run:

```bash
playwright install chromium
```

or simply start:

```bash
python launch.py
```

`launch.py` is designed to install Chromium automatically when it is missing.

### `python` is not recognized

Make sure Python is installed and added to the Windows PATH.

Check:

```bash
python --version
```

The project requires Python 3.10 or newer.

### Downloads are not appearing

Make sure the application has permission to write to the project directory.

The expected directory is:

```text
PhantomT4b/files/
```

## Updating

Pull the latest version:

```bash
git pull
```

Update Python dependencies:

```bash
pip install -r requirements.txt --upgrade
```

If Playwright has been updated, reinstall Chromium:

```bash
playwright install chromium
```

## Development

The project is intentionally kept small and modular.

The main responsibilities are separated into:

```text
launch.py      -> startup and Chromium check
browser.py     -> browser and GUI
catch_file.py  -> download monitoring
```

This makes it possible to modify the browser interface, startup logic, or download monitoring independently.

## Safety and Usage

PhantomT4b is designed for ordinary browser use, isolated temporary sessions, testing, and development workflows.

It does not attempt to bypass authentication systems, CAPTCHAs, anti-bot protections, rate limits, or other access controls.

Users are responsible for complying with the terms and policies of the websites they access.

## License

This project is released under the MIT License.

See the `LICENSE` file for details.

## Author

**CyberPlugger**

GitHub:

https://github.com/CyberPlugger

## Project

**PhantomT4b**

A small temporary-session Chromium launcher with a terminal-inspired interface.
