import tkinter as tk
from tkinter import filedialog
from rembg import remove
from PIL import Image
import os
import requests
import uuid

API_URL = "http://127.0.0.1:8000/verify"

license_key = input("Nhập license key: ")
hwid = hex(uuid.getnode())

r = requests.post(API_URL, json={
    "license_key": license_key,
    "hwid": hwid
})

data = r.json()

if not data["valid"]:
    print("License không hợp lệ")
    exit()

print("License OK")

# ===== CHỈ CHẠY NẾU LICENSE HỢP LỆ =====

print("Bắt đầu tách nền...")

# window
root = tk.Tk()
root.title("TSNOVA Remove")
root.geometry("400x200")

# status label
status_label = tk.Label(
    root,
    text="Waiting...",
    font=("Arial", 10)
)

status_label.pack(pady=10)


def process_images():

    folder = filedialog.askdirectory()

    if not folder:
        return

    output_folder = os.path.join(folder, "output")
    os.makedirs(output_folder, exist_ok=True)

    files = os.listdir(folder)

    for index, filename in enumerate(files, start=1):

        input_path = os.path.join(folder, filename)

        if not os.path.isfile(input_path):
            continue

        try:

            status_label.config(
                text=f"Processing {index}/{len(files)}: {filename}"
            )

            root.update()

            input_image = Image.open(input_path)

            output_image = remove(input_image)

            name = os.path.splitext(filename)[0]

            output_path = os.path.join(
                output_folder,
                f"{name}_no_bg.png"
            )

            output_image.save(output_path)

            status_label.config(
                text=f"Done: {filename}"
            )

            root.update()

        except Exception as e:

            print(f"Error: {e}")

    status_label.config(text="TSNOVA Remove Complete!")

    root.update()


button = tk.Button(
    root,
    text="Remove Background",
    command=process_images,
    width=25,
    height=2
)

button.pack(expand=True)

root.mainloop()