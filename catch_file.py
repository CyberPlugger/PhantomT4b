"""
catch_file.py
=============

catch_file.py is a helper module for PhantomT4b that is responsible for detecting new completed files in the files directory.

The module was created separately from browser.py to separate responsibilities.
The main project file handles launching Chromium and managing the graphical interface, while this file is responsible exclusively for monitoring the download directory and generating notifications.

When the observer is launched, the contents of the folder are saved. Existing files are not considered new, so when launching PhantomT4b, the user does not receive notifications about all the files that were in the folder before the program was launched.

After that, the module periodically checks the contents of the directory. If a new file appears, it undergoes several checks. First, it is checked whether the object is a temporary file. This is especially important for Chromium, which uses the .crdownload extension during the download. Such files should not be considered completed downloads.

Besides.crdownload, some other common temporary extensions are ignored. This allows you to avoid notifications about files that are still in the process of being created or downloaded.

After detecting a potentially ready file, the module checks its size several times. If the size continues to change, it is considered that the file is still being written. If the size remains the same for a sufficiently long time, the file is considered completed.

The monitoring is performed in a separate daemon thread so that constant directory checking does not block the main Tkinter interface.

The notification window itself is created via root.after(). This is necessary because Tkinter must modify its graphical elements from the application’s main thread. Thus, the background thread only detects the event, and root.after() passes the command to the main Tkinter loop.

The module does not create its own Tkinter window and does not run its own mainloop(). It is intended to be connected to an existing application via the call catch_file.start(root, directory).

This architecture allows catch_file.py to be used as an independent component of PhantomT4b, and in the future, it can be used to replace the notification system, add a download log, or expand the processing of various file types without changing the browser’s core logic.
"""

import os
import time
import threading
from tkinter import messagebox


def start(root, directory="files"):
    os.makedirs(
        directory,
        exist_ok=True
    )

    containing = set(
        os.listdir(directory)
    )

    def is_temporary(filename):
        name = filename.lower()

        return (
            name.endswith(".crdownload")
            or name.endswith(".tmp")
            or name.endswith(".part")
        )

    def wait_until_ready(path):
        last_size = -1
        stable_count = 0

        while True:

            if not os.path.exists(path):
                return False

            try:
                size = os.path.getsize(path)

            except OSError:
                return False

            if size == last_size:
                stable_count += 1
            else:
                stable_count = 0

            last_size = size

            if stable_count >= 3:
                return True

            time.sleep(0.5)

    def watch():
        nonlocal containing

        while True:

            try:
                current = set(
                    os.listdir(directory)
                )

                new_files = current - containing

                for filename in new_files:

                    if is_temporary(filename):
                        continue

                    path = os.path.abspath(
                        os.path.join(
                            directory,
                            filename
                        )
                    )

                    if not os.path.isfile(path):
                        continue

                    if not wait_until_ready(path):
                        continue

                    final_name = os.path.basename(
                        path
                    )

                    if is_temporary(final_name):
                        continue

                    root.after(
                        0,
                        lambda name=final_name,
                        full_path=path:
                            messagebox.showinfo(
                                "PhantomT4b",
                                f"{name} has been added in:\n\n"
                                f"{full_path}"
                            )
                    )

                containing = current

            except Exception:
                pass

            time.sleep(0.5)

    threading.Thread(
        target=watch,
        daemon=True
    ).start()
