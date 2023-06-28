import requests
import os
import shutil
from zipfile import ZipFile
import io
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk
import subprocess
import webbrowser
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# repo selection was from previous project, just rolled with it and kept it...update this later
def check_updates(user, repo_name):
    url = f"https://api.github.com/repos/{user}/{repo_name}/releases"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    if 'created_at' in data[0]:
        latest_release_date = datetime.strptime(data[0]['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        diff = datetime.now() - latest_release_date
        if diff.days < 2:
            latest_release_name = data[0]['name'] if data[0]['name'] else data[0]['tag_name']
            repo = data[0]['html_url'].split('/')[-3] 
            messagebox.showinfo("Update available!", f"A new release ({latest_release_name}) has been posted in the last 48 hours. Please update. Github Source: {user}/{repo_name}")
        else:
            messagebox.showinfo("No updates", "There have been no releases in the past 48 hours.")

def install_updates():
    os.system(f'python {get_resource_path("YuzuEAUpdater.py")}')

def restore_previous(version_entry, url_mapping):
    if version_entry:
        selected_version = version_entry.get()
        if selected_version in url_mapping:
            download_url = url_mapping[selected_version]
            subprocess.run(['python', get_resource_path('RestorePrevious.py'), 'pineappleEA', 'pineapple-src', selected_version, download_url], check=True)
        else:
            messagebox.showinfo("Invalid Version", "The entered version is not available for restoration.")

def fetch_recent_updates(user, repo_name):
    url = f"https://api.github.com/repos/{user}/{repo_name}/releases"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 1
    url_mapping = {}
    for release in data[:30]:
        tag_name = release['tag_name']
        version_number = tag_name.split('-')[-1]
        assets = release['assets']
        for asset in assets:
            if asset['browser_download_url'].endswith('.zip'):
                url_mapping[version_number] = asset['browser_download_url']
                break
    return url_mapping

def open_repo():
    webbrowser.open_new("https://github.com/pineappleEA/pineapple-src")

def view_releases():
    webbrowser.open_new("https://github.com/pineappleEA/pineapple-src/releases")

def repo_support():
    webbrowser.open_new("https://github.com/ib4error")

def main_window(user, repo_name):
    root = tk.Tk()
    root.title(f"Yuzu Early Release Updater || Updates Source: {user}/{repo_name} ")
    root.resizable(False, False)

    body_color = "#111111"
    button_color = "#111111"
    button_text_color = "#ffffff"

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 650
    window_height = 350

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    image_path = get_resource_path("backg.png") 
    bg_image = Image.open(image_path)
    bg_image = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=window_width, height=window_height, bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    myFont = font.Font(family="Arial", size=12, weight="bold")

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Menu", menu=file_menu)
    file_menu.add_command(label="Open EA Repo", command=open_repo)
    file_menu.add_command(label="View EA Releases", command=view_releases)
    file_menu.add_command(label="Updater Repo & Support", command=repo_support)

    button_canvas = tk.Canvas(root, bg=body_color, width=window_width, height=100, bd=0, highlightthickness=0)
    button_canvas.pack()

    check_button = tk.Button(button_canvas, text="Check Updates", command=lambda: check_updates(user, repo_name), font=myFont, bg=button_color, fg=button_text_color)
    check_button.pack(side='left', padx=20)

    install_button = tk.Button(button_canvas, text="Install Updates", command=install_updates, font=myFont, bg=button_color, fg=button_text_color)
    install_button.pack(side='left', padx=20)

    frame_input = tk.Frame(root, bg=body_color)
    input_label = tk.Label(frame_input, text="Type Previous EA Version Number | 4 Digit Number Only | Click Restore Previous", bg=body_color, fg="white")
    input_label.grid(row=0, column=0, columnspan=2, sticky="w")

    version_entry = tk.Entry(frame_input, width=50, font=myFont)
    version_entry.grid(row=1, column=0, columnspan=2)

    restore_button = tk.Button(button_canvas, text="Restore Previous", command=lambda: restore_previous(version_entry, url_mapping), font=myFont, bg=button_color, fg=button_text_color)
    restore_button.pack(side='left', padx=20)

    canvas.create_window(window_width/2, 100, window=button_canvas)
    canvas.create_window(window_width/2, 250, window=frame_input)

    url_mapping = fetch_recent_updates(user, repo_name)

    root.mainloop()

main_window('pineappleEA', 'pineapple-src')
