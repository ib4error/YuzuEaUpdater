import os
import requests
import pathlib
from zipfile import ZipFile
import shutil
import sys
import tkinter as tk

def restore_previous_version(user, repo_name, selected_version, download_url):
    # download latest
    response = requests.get(download_url, stream=True)

    # check successful
    assert response.status_code == 200

    # save zip
    downloaded_file_path = os.path.join(pathlib.Path().resolve(), "downloaded_file.zip")
    with open(downloaded_file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    # extract files
    with ZipFile(downloaded_file_path, "r") as zip_ref:
        zip_ref.extractall()

    # rename extracted
    extracted_dir = "yuzu-windows-msvc-early-access"
    os.rename(extracted_dir, "yuzu-windows-msvc")

    # rm existing yuzu-windows-msvc instance
    yuzu_dir_path = os.path.join(os.environ['LOCALAPPDATA'], "yuzu", "yuzu-windows-msvc")
    if os.path.exists(yuzu_dir_path):
        shutil.rmtree(yuzu_dir_path)

    # replace yuzu-windows-msvc
    shutil.move("yuzu-windows-msvc", yuzu_dir_path)

    # rm download
    os.remove(downloaded_file_path)

    create_popup(f"You have restored Yuzu to version {selected_version}")

def create_popup(message):
    popup = tk.Tk()
    popup.title(message)

    popup.configure(bg="#000000") 
    body_color = "#222222"

    window_width = 300
    window_height = 100
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

    label = tk.Label(popup, text=message, bg=body_color, fg="white")
    label.pack(side="top", fill="x", pady=10)
    close_button = tk.Button(popup, text="Close", command=popup.destroy, bg="#306daf", fg="white")
    close_button.pack()
    popup.mainloop()

# command-line arguments !exist
if len(sys.argv) >= 5:
    user = sys.argv[1]
    repo_name = sys.argv[2]
    selected_version = sys.argv[3]
    download_url = sys.argv[4]
    restore_previous_version(user, repo_name, selected_version, download_url)
else:
    print("Has the repo disappeared? Cannot find the user, repo_name, selected_version, and download_url as command-line arguments.")