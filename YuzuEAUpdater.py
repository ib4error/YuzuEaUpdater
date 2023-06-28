import os
import requests
import pathlib
from zipfile import ZipFile
import shutil
import tkinter as tk

def update_application(user, repo_name):

    # repo selection was from previous project, just rolled with it and kept it...update this later
    url = f"https://api.github.com/repos/{user}/{repo_name}/releases"

    response = requests.get(url)

    # check successful
    assert response.status_code == 200

    # parse JSON
    data = response.json()

    # check at atleast one new release
    assert len(data) > 0

    # get latest url
    asset_url = data[0]['assets'][1]['browser_download_url']

    # get latest version name
    version = data[0]['tag_name']

    # download zip
    response = requests.get(asset_url, stream=True)

    # check successful
    assert response.status_code == 200

    # save zip
    downloaded_file_path = os.path.join(pathlib.Path().resolve(), "downloaded_file.zip")
    with open(downloaded_file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    # extract zip
    with ZipFile(downloaded_file_path, "r") as zip_ref:
        zip_ref.extractall()

    # rename extracted
    os.rename("yuzu-windows-msvc-early-access", "yuzu-windows-msvc")

    # rm current yuzu-windows msvc instance
    yuzu_dir_path = os.path.join(os.environ['LOCALAPPDATA'], "yuzu", "yuzu-windows-msvc")
    if os.path.exists(yuzu_dir_path):
        shutil.rmtree(yuzu_dir_path)

    # replace yuzu-windows-msvc
    shutil.move("yuzu-windows-msvc", yuzu_dir_path)

    # rm zip
    os.remove(downloaded_file_path)

    create_popup(f"You have updated Yuzu to {version}")

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

update_application('pineappleEA', 'pineapple-src')
