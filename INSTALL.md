# PhantomT4b — Installation

## Requirements

Before installing PhantomT4b, make sure you have:

* Windows 10 or Windows 11
* Python 3.10 or newer
* Internet access for installing dependencies and Chromium

PhantomT4b uses Python, Tkinter, and Playwright. Tkinter provides the graphical interface, while Playwright is used to launch and control Chromium.

## Clone the Repository

Open PowerShell or Command Prompt and run:

```powershell
git clone https://github.com/CyberPlugger/PhantomT4b.git
cd PhantomT4b
```

If the repository has a different name, replace `PhantomT4b` with the correct repository name.

## Create a Virtual Environment

It is recommended to use a separate Python virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

After successful activation, you should see `(.venv)` at the beginning of the terminal prompt.

## Install Dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

The main external dependency used by PhantomT4b is Playwright.

Tkinter does not need to be installed through `pip` when using a standard Python installation on Windows.

## Install Chromium

After installing Playwright, download the Chromium browser:

```powershell
playwright install chromium
```

This downloads the Chromium build used by PhantomT4b.

## Run PhantomT4b

After completing the installation, start the application with:

```powershell
python browser.py
```

The PhantomT4b graphical interface should open.

Enter a website address in the `TARGET ::` field and press:

```text
[ LAUNCH ]
```

If the address does not contain `http://` or `https://`, PhantomT4b automatically adds `https://`.

## Download Directory

PhantomT4b automatically creates the following directory:

```text
files/
```

This directory is used to store files downloaded through Chromium.

The basic project structure looks like this:

```text
PhantomT4b/
│
├── browser.py
├── catch_file.py
├── pyproject.toml
├── requirements.txt
├── install.md
├── README.md
│
└── files/
```

The `catch_file.py` module monitors the `files/` directory and notifies the user when a completed download is detected.

Temporary Chromium download files such as `.crdownload`, `.tmp`, and `.part` are ignored.

## Browser Sessions

The:

```text
[ NEW SESSION ]
```

button closes the current browser session and creates a new one.

Each PhantomT4b session uses its own temporary Chromium profile.

When the browser session is closed, the temporary profile directory is removed.

## Navigation

The interface provides basic browser navigation controls:

```text
[ < ]             Back
[ > ]             Forward
[ REFRESH ]       Reload the current page
[ NEW SESSION ]   Start a new browser session
[ CLOSE ]         Close the browser
```

You can also enter a new URL in the `TARGET ::` field and press `Enter`.

## Troubleshooting

### `ModuleNotFoundError: No module named 'playwright'`

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

### Playwright is installed, but Chromium does not start

Run:

```powershell
playwright install chromium
```

### `python` is not recognized

Make sure Python is installed and added to your system `PATH`.

Check your Python installation with:

```powershell
python --version
```

### Tkinter is not available

On Windows, Tkinter is normally included with the standard Python installer.

If Tkinter is missing, reinstall Python using the official Windows installer and make sure the standard Python components are enabled.

## Updating PhantomT4b

To update the source code from GitHub:

```powershell
git pull
```

After updating, reinstall the Python dependencies if necessary:

```powershell
pip install -r requirements.txt
```

If the Playwright version was updated, you may also need to run:

```powershell
playwright install chromium
```

## Fresh Installation

The complete installation process can be performed with:

```powershell
git clone https://github.com/CyberPlugger/PhantomT4b.git
cd PhantomT4b
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
python browser.py
```

PhantomT4b should now be ready to use.
