# tsnova_ui.py

import os
import threading
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
from customtkinter import CTkImage
from transformers import AutoModelForImageSegmentation
from torchvision import transforms
import torch.nn.functional as F
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"

from PIL import ImageGrab
import time
import requests
import uuid
import subprocess
import tkinter as tk

API_URL = "https://tsnova-license-server.onrender.com/verify"

from tkinter import messagebox

hwid = subprocess.check_output(
    "wmic csproduct get uuid"
).decode().split("\n")[1].strip()


license_window = tk.Tk()

license_window.title("TSNOVA License")
license_window.geometry("350x180")


label = tk.Label(
    license_window,
    text="Enter License Key"
)

label.pack(pady=10)


license_entry = tk.Entry(
    license_window,
    width=35
)

license_entry.pack(pady=5)

def verify_license():

    key = license_entry.get()

    try:

        r = requests.post(
            API_URL,
            json={
                "license_key": key,
                "hwid": hwid
            },
            timeout=15
        )

        print("STATUS:", r.status_code)
        print("TEXT:", r.text)

        data = r.json()

        if not data.get("valid"):

            messagebox.showerror(
                "Error",
                data.get("reason", "Invalid License")
            )

            return

        messagebox.showinfo(
            "Success",
            "License OK"
        )

        license_window.destroy()

        start_main_app()

    except Exception as e:

        print(e)

        messagebox.showerror(
            "Connection Error",
            str(e)
        )

        key = license_entry.get()

        r = requests.post(
            API_URL,
            json={
                "license_key": key,
                "hwid": hwid
            },
            timeout=10
        )
        
        data = r.json()

        print(r.text)
        print(r.status_code)

        data = r.json()

        print(data)
        if not data["valid"]:

            messagebox.showerror(
                "Error",
                "Invalid License"
            )

            return

        messagebox.showinfo(
            "Success",
            "License OK"
        )

        license_window.destroy()

        start_main_app()


verify_button = tk.Button(
    license_window,
    text="Verify License",
    command=verify_license
)

verify_button.pack(pady=20) 

print("Loading BiRefNet...")

from model_loader import model, device


model.to(device)

if device == "cuda":
    model.half()

model.eval()

transform_image = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])


# =========================
# AI MODEL
# =========================

print("Loading BiRefNet...")


print("BiRefNet loaded!")

# =========================
# CONFIG
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

selected_files = set()
preview_images = []
stop_requested = False
# =========================
# APP
# =========================

def start_main_app():

    app = TkinterDnD.Tk()
    app.title("TSNOVA Remove")
    app.geometry("1200x700")
    app.configure(bg="#111111")

    # =========================
    # SIDEBAR
    # =========================

    sidebar = ctk.CTkFrame(
        app,
        width=140,
        corner_radius=0,
        fg_color="#1e1e1e"
    )

    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    logo = ctk.CTkLabel(
        sidebar,
        text="TSNOVA",
        font=("Arial", 24, "bold")
    )

    logo.pack(pady=(30, 20))

    remove_tab = ctk.CTkButton(
        sidebar,
        text="Remove",
        width=110,
        height=40
    )

    remove_tab.pack(pady=10)

    footer = ctk.CTkLabel(
        sidebar,
        text="TSNOVA AI POWERED",
        font=("Arial", 12)
    )

    footer.pack(side="bottom", pady=20)

    # =========================
    # MAIN CONTENT
    # =========================

    main_frame = ctk.CTkScrollableFrame(
        app,
        fg_color="#111111"
    )

    main_frame.pack(side="right", fill="both", expand=True)

    content_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )

    content_frame.pack(anchor="n", pady=20)

    # =========================
    # TITLE
    # =========================

    title = ctk.CTkLabel(
        content_frame,
        text="TSNOVA Remove",
        font=("Arial", 42, "bold")
    )

    title.pack(pady=(10, 15))

    # =========================
    # STATUS
    # =========================

    status_label = ctk.CTkLabel(
        content_frame,
        text="Drag images or folders into the app",
        font=("Arial", 18)
    )

    status_label.pack(pady=(0, 10))

    # =========================
    # PROGRESS BAR
    # =========================

    progressbar = ctk.CTkProgressBar(
        content_frame,
        width=500
    )

    progressbar.pack(pady=(0, 20))
    progressbar.set(0)

    # =========================
    # PREVIEW
    # =========================

    preview_frame = ctk.CTkFrame(
        content_frame,
        fg_color="transparent"
    )

    preview_frame.pack(pady=(0, 20))


            
    # =========================
    # FUNCTIONS
    # =========================
    

    def clear_preview():

        for widget in preview_frame.winfo_children():
            widget.destroy()


    def update_preview(files):

        global preview_images

        clear_preview()
        preview_images.clear()

        max_preview = min(len(files), 8)

        for index, file in enumerate(files[:max_preview]):

            try:

                image = Image.open(file)
                image.thumbnail((120, 120))

                background = Image.new(
                    "RGB",
                    (120, 120),
                    (25, 25, 25)
                )

                x = (120 - image.width) // 2
                y = (120 - image.height) // 2

                background.paste(image, (x, y))

                image = background

                ctk_img = CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=image.size
                )

                preview_images.append(ctk_img)

                label = ctk.CTkLabel(
                    preview_frame,
                    image=ctk_img,
                    text=""
                )

                row = index // 4
                col = index % 4

                label.grid(
                    row=row,
                    column=col,
                    padx=10,
                    pady=10
                )

            except Exception as e:
                print(e)
        remaining = len(files) - max_preview

        if remaining > 0:

            more_label = ctk.CTkLabel(
                preview_frame,
                text=f"+{remaining} more images",
                font=("Arial", 18, "bold")
            )

            more_label.grid(
                row=2,
                column=0,
                columnspan=4,
                pady=(10, 0)
            )

    def drop(event):
        selected_files.clear()

        preview_images.clear()

        clear_preview()

        progressbar.set(0)
        

        data = app.tk.splitlist(event.data)

        image_ext = (".png", ".jpg", ".jpeg", ".webp")

        for item in data:

            item = item.strip("{}")

            # Folder
            if os.path.isdir(item):

                for root, dirs, files in os.walk(item):

                    for file in files:

                        if file.lower().endswith(image_ext):

                            full_path = os.path.join(root, file)

                            if full_path not in selected_files:
                                selected_files.add(full_path)

            # Single file
            elif item.lower().endswith(image_ext):

                if item not in selected_files:
                    selected_files.append(item)

        if selected_files:

            status_label.configure(
                text=f"{len(selected_files)} images selected"
            )

            update_preview(list(selected_files))

            remove_button.configure(state="normal")


    def process_images():
        start_time = time.time()

        selected_files_list = sorted(
            selected_files,
            key=lambda x: os.path.basename(x).lower()
        )

        output_folder = os.path.join(
            os.getcwd(),
            "output"
        )

        os.makedirs(output_folder, exist_ok=True)

        total = len(selected_files)

        for index, file in enumerate(selected_files_list):
            if stop_requested:

                app.after(
                    0,
                    lambda:
                    status_label.configure(
                        text="Processing stopped"
                    )
                )

                break
            try:

                test_image = Image.open(file)
                test_image.verify()

                image = Image.open(file).convert("RGB")

                original_size = image.size

                input_tensor = transform_image(image).unsqueeze(0).to(device)

                if device == "cuda":
                    input_tensor = input_tensor.half()

                with torch.no_grad():
                    preds = model(input_tensor)[-1].sigmoid().cpu()

                mask = preds[0].squeeze()

                mask = transforms.ToPILImage()(mask)

                mask = mask.resize(original_size)

                image_rgba = image.convert("RGBA")
                image_rgba.putalpha(mask)

                filename = os.path.basename(file)
                name, _ = os.path.splitext(filename)

                output_path = os.path.join(
                    output_folder,
                    f"{name}_removed.png"
                )
                if os.path.exists(output_path):

                    print(f"Skipped: {filename}")

                    continue

                image_rgba.save(output_path)

                if device == "cuda":
                    torch.cuda.empty_cache()

            except Exception as e:

                print("ERROR:", e)

            progress = (index + 1) / total

            app.after(
                0,
                lambda p=progress:
                progressbar.set(p)
            )

            app.after(
                0,
                lambda i=index, t=total:
                status_label.configure(
                    text=f"Processing {i+1}/{t} : {os.path.basename(selected_files_list[i])}"
                )
            )

        app.after(
            0,
            lambda:
            status_label.configure(
                text=f"TSNOVA Remove Complete! ({elapsed}s)"
            ))
        app.after(
        0,
        lambda: remove_button.configure(state="normal")
        )

        app.after(
            0,
            lambda: output_button.configure(state="normal")
        )

        app.after(
            0,
            lambda: delete_button.configure(state="normal")
        )
        
        app.after(0, lambda: os.startfile(output_folder))
        elapsed = round(time.time() - start_time, 2)

    def stop_processing():

        global stop_requested

        stop_requested = True
    def remove_background():

        global stop_requested
        stop_requested = False

        if not selected_files:

            status_label.configure(
                text="No images selected"
            )

            return

        progressbar.set(0)

        remove_button.configure(state="disabled")
        output_button.configure(state="disabled")
        delete_button.configure(state="disabled")
        
        threading.Thread(
            target=process_images
        ).start()


    def open_output_folder():

        output_folder = os.path.join(
            os.getcwd(),
            "output"
        )

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        os.startfile(output_folder)

    def clear_selected_images():

        selected_files.clear()

        preview_images.clear()

        clear_preview()

        progressbar.set(0)

        status_label.configure(
            text="Selection cleared"
        )
        remove_button.configure(state="disabled")


        output_folder = os.path.join(
            os.getcwd(),
            "output"
        )

        if os.path.exists(output_folder):

            for file in os.listdir(output_folder):

                file_path = os.path.join(output_folder, file)

                if os.path.isfile(file_path):
                    os.remove(file_path)

        remove_button.configure(state="disabled")
        # clear selected images
        selected_files.clear()

        # clear preview UI
        clear_preview()

        # clear cached previews
        preview_images.clear()

        # reset progress
        progressbar.set(0)

        status_label.configure(
            text="All images cleared"
        )

        output_folder = os.path.join(
            os.getcwd(),
            "output"
        )

        if not os.path.exists(output_folder):
            return

        deleted = 0

        for file in os.listdir(output_folder):

            file_path = os.path.join(output_folder, file)

            if os.path.isfile(file_path):

                os.remove(file_path)
                deleted += 1

        status_label.configure(
            text=f"Deleted {deleted} images"
        )

    def paste_image(event=None):

        global selected_files

        image = ImageGrab.grabclipboard()

        if image is None:
            return

        input_folder = os.path.join(
            os.getcwd(),
            "input"
        )

        os.makedirs(input_folder, exist_ok=True)

        temp_path = os.path.join(
            input_folder,
            "pasted_image.png"
        )

        image.save(temp_path)

        selected_files.clear()

        preview_images.clear()

        clear_preview()

        selected_files.add(temp_path)

        update_preview(list(selected_files))

        status_label.configure(
            text="Pasted image from clipboard"
        )
    # =========================
    # BUTTONS
    # =========================

    remove_button = ctk.CTkButton(
        content_frame,
        text="Remove Background",
        width=320,
        height=55,
        font=("Arial", 20, "bold"),
        command=remove_background,
        state="disabled"
    )

    remove_button.pack(pady=(0, 15))

    output_button = ctk.CTkButton(
        content_frame,
        text="Open Output Folder",
        width=220,
        height=40,
        fg_color="#2a2a2a",
        hover_color="#333333",
        command=open_output_folder
    )

    output_button.pack(pady=(0, 20))

    stop_button = ctk.CTkButton(
        content_frame,
        text="Stop Processing",
        width=220,
        height=40,
        fg_color="#e67e22",
        hover_color="#ca6f1e",
        command=stop_processing
    )

    stop_button.pack(pady=(0, 20))

    delete_button = ctk.CTkButton(
        content_frame,
        text="Clear Selected Images",
        width=220,
        height=40,
        fg_color="#c0392b",
        hover_color="#a93226",
        command=clear_selected_images
    )

    delete_button.pack(pady=(0, 20))

    # =========================
    # DRAG DROP
    # =========================

    app.drop_target_register(DND_FILES)
    app.dnd_bind("<<Drop>>", drop)

    # =========================
    # RUN
    # =========================

    app.bind("<Control-v>", paste_image)
    app.mainloop()

license_window.mainloop()