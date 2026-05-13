# tsnova_ui.py

import os
import time
import threading
import tkinter as tk

import customtkinter as ctk
import torch

from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

from PIL import (
    Image,
    ImageGrab
)

from customtkinter import CTkImage
from torchvision import transforms

from license.activate_client import (
    verify_license_key,
    save_license,
    load_license
)

from usage_manager import (
    can_use,
    add_usage,
    get_remaining
)

from model_loader import (
    load_hd_model,
    load_fast_model,
    device
)

from core.image_processor import (
    remove_background_image
)

from core.file_manager import (
    scan_images_from_drop
)

from ui.preview_manager  import (
    update_preview
)

from config import *

# =========================
# CONFIG
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

current_mode = "fast"

CURRENT_PLAN = "FREE"
IS_PRO = False

selected_files = set()
preview_images = []

stop_requested = False

# =========================
# LOAD MODELS
# =========================


# =========================
# LICENSE WINDOW
# =========================

license_window = ctk.CTkToplevel(parent)

license_window.title("TSNOVA License")
license_window.geometry("350x180")
license_window.resizable(False, False)

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

# =========================
# MAIN APP
# =========================

def start_main_app():

    global stop_requested

    app = ctk.CTkToplevel(parent)
    app.iconbitmap("assets/icon.ico")

    app.title(APP_NAME)
    app.geometry(
    f"{APP_WIDTH}x{APP_HEIGHT}"
)
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

    sidebar.pack(
        side="left",
        fill="y"
    )

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

    footer.pack(
        side="bottom",
        pady=20
    )

    # =========================
    # MAIN CONTENT
    # =========================

    main_frame = ctk.CTkScrollableFrame(
        app,
        fg_color="#111111"
    )

    main_frame.pack(
        side="right",
        fill="both",
        expand=True
    )

    content_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )

    content_frame.pack(
        anchor="n",
        pady=20
    )

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

    usage_label = ctk.CTkLabel(
        content_frame,
        text=f"Free Uses Left Today: {get_remaining()}",
        font=("Arial", 16)
    )

    usage_label.pack(pady=(0, 10))

    # =========================
    # MODE SWITCH
    # =========================

    def set_mode(mode):

        global current_mode

        if mode == "hd" and not IS_PRO:

            messagebox.showwarning(
                "PRO Required",
                "HD Mode is available for PRO users only."
            )

            return

        current_mode = mode

        if mode == "fast":

            fast_button.configure(
                fg_color="#3b82f6"
            )

            hd_button.configure(
                fg_color="#2a2a2a"
            )

            status_label.configure(
                text="Fast Remove Mode ⚡"
            )

        else:

            hd_button.configure(
                fg_color="#3b82f6"
            )

            fast_button.configure(
                fg_color="#2a2a2a"
            )

            status_label.configure(
                text="HD Remove Mode ✨"
            )

    mode_frame = ctk.CTkFrame(
        content_frame,
        fg_color="transparent"
    )

    mode_frame.pack(pady=(0, 20))

    fast_button = ctk.CTkButton(
        mode_frame,
        text="⚡ Fast Remove\nQuick processing",
        width=220,
        height=70,
        font=("Arial", 16, "bold"),
        command=lambda: set_mode("fast")
    )

    fast_button.grid(
        row=0,
        column=0,
        padx=10
    )

    hd_button = ctk.CTkButton(
        mode_frame,
        text="✨ HD Remove\nBest quality",
        width=220,
        height=70,
        font=("Arial", 16, "bold"),
        command=lambda: set_mode("hd")
    )

    hd_button.grid(
        row=0,
        column=1,
        padx=10
    )

    set_mode("fast")

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

    preview_frame.pack(pady=(0, 5))

    compare_frame = ctk.CTkFrame(
        content_frame,
        fg_color="transparent"
    )

    compare_frame.pack(pady=(0, 10))

    before_label = ctk.CTkLabel(
        compare_frame,
        text=""
    )

    before_label.grid(
        row=0,
        column=0,
        padx=20
    )

    after_label = ctk.CTkLabel(
        compare_frame,
        text=""
    )

    after_label.grid(
        row=0,
        column=1,
        padx=20
    )

    # =========================
    # FUNCTIONS
    # =========================

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

            from core.error_handler import (
                handle_error
            )

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

        files = scan_images_from_drop(data)

        selected_files.update(files)

        if selected_files:

            status_label.configure(
                text=f"{len(selected_files)} images selected"
            )

            update_preview(
                list(selected_files)
            )

            remove_button.configure(
                state="normal"
            )

    def process_images():

        start_time = time.time()

        processed_count = 0

        selected_files_list = sorted(
            selected_files,
            key=lambda x: os.path.basename(x).lower()
        )

        output_folder = os.path.join(
            os.getcwd(),
            OUTPUT_FOLDER
        )

        os.makedirs(
            output_folder,
            exist_ok=True
        )

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

                image, image_rgba = remove_background_image(
                    file,
                    current_mode,
                    fast_model,
                    hd_model,
                    device
                )

                filename = os.path.basename(file)

                name, _ = os.path.splitext(filename)

                output_path = os.path.join(
                    output_folder,
                    f"{name}_removed.png"
                )
                if os.path.exists(output_path):

                    print(f"Skipped: {filename}")

                    processed_count += 1

                    continue

                image_rgba.save(output_path)
                image.close()
                image_rgba.close()

                processed_count += 1

                elapsed = time.time() - start_time

                avg_time = elapsed / processed_count

                remaining = total - processed_count

                eta = round(
                    avg_time * remaining,
                    1
                )

                preview_before = image.copy()

                preview_before.thumbnail(
                    (250, 250),
                    Image.LANCZOS
                )

                preview_after = image_rgba.copy()

                preview_after.thumbnail(
                    (250, 250),
                    Image.LANCZOS
                )

                before_ctk = CTkImage(
                    light_image=preview_before,
                    dark_image=preview_before,
                    size=preview_before.size
                )

                after_ctk = CTkImage(
                    light_image=preview_after,
                    dark_image=preview_after,
                    size=preview_after.size
                )

                app.after(
                    0,
                    lambda b=before_ctk:
                    before_label.configure(
                        image=b,
                        text="Before"
                    )
                )

                app.after(
                    0,
                    lambda a=after_ctk:
                    after_label.configure(
                        image=a,
                        text="After"
                    )
                )

                if device == "cuda":

                    torch.cuda.empty_cache()
                    import gc
                    gc.collect()

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
                lambda i=index, t=total, e=eta, a=avg_time:
                status_label.configure(
                    text=f"Processing {i+1}/{t} | ETA: {e}s | Speed: {round(a,2)}s/img"
                )
            )

        elapsed = round(
            time.time() - start_time,
            2
        )

        app.after(
            0,
            lambda:
            status_label.configure(
                text=f"TSNOVA Remove Complete! ({elapsed}s)"
            )
        )

        app.after(
            0,
            lambda:
            remove_button.configure(
                state="normal"
            )
        )

        app.after(
            0,
            lambda:
            output_button.configure(
                state="normal"
            )
        )

        app.after(
            0,
            lambda:
            delete_button.configure(
                state="normal"
            )
        )

        app.after(
            0,
            lambda:
            os.startfile(output_folder)
        )

    def stop_processing():

        global stop_requested

        stop_requested = True

    def remove_background():

        global stop_requested

        if not IS_PRO:

            if not can_use():

                messagebox.showerror(
                    "Limit Reached",
                    "Daily free limit reached."
                )

                return

            add_usage()

            usage_label.configure(
                text=f"Free Uses Left Today: {get_remaining()}"
            )

        if not selected_files:

            status_label.configure(
                text="No images selected"
            )

            return

        stop_requested = False

        progressbar.set(0)

        remove_button.configure(
            state="disabled"
        )

        output_button.configure(
            state="disabled"
        )

        delete_button.configure(
            state="disabled"
        )

        threading.Thread(
            target=process_images,
            daemon=True
        ).start()

    def open_output_folder():

        output_folder = os.path.join(
            os.getcwd(),
            OUTPUT_FOLDER
        )

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        os.startfile(output_folder)

    def clear_selected_images():

        selected_files.clear()

        preview_images.clear()

        clear_preview()

        progressbar.set(0)

        status_label.configure(
            text="Selection cleared"
        )

        remove_button.configure(
            state="disabled"
        )

    def paste_image(event=None):

        image = ImageGrab.grabclipboard()

        if image is None:

            return

        input_folder = os.path.join(
            os.getcwd(),
            INPUT_FOLDER
        )

        os.makedirs(
            input_folder,
            exist_ok=True
        )

        temp_path = os.path.join(
            input_folder,
            "pasted_image.png"
        )

        image.save(temp_path)

        selected_files.clear()

        preview_images.clear()

        clear_preview()

        selected_files.add(temp_path)

        update_preview(
            list(selected_files)
        )

        status_label.configure(
            text="Pasted image from clipboard"
        )

        remove_button.configure(
            state="normal"
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

    app.dnd_bind(
        "<<Drop>>",
        drop
    )

    # =========================
    # RUN
    # =========================

    app.bind(
        "<Control-v>",
        paste_image
    )

    app.mainloop()

# =========================
# VERIFY LICENSE
# =========================

def verify_license():

    global CURRENT_PLAN
    global IS_PRO

    key = license_entry.get().strip()

    if not key:

        messagebox.showerror(
            "Error",
            "Please enter license key"
        )

        return

    try:

        data = verify_license_key(key)

        if not data.get("success"):

            messagebox.showerror(
                "Error",
                data.get(
                    "message",
                    "Invalid License"
                )
            )

            return

        CURRENT_PLAN = data.get(
            "plan",
            "FREE"
        )

        IS_PRO = CURRENT_PLAN in [
            "PRO",
            "PREMIUM"
        ]

        save_license(
            key,
            CURRENT_PLAN
        )

        messagebox.showinfo(
            "Success",
            f"License Activated ({CURRENT_PLAN})"
        )

        license_window.destroy()

        start_main_app()

    except Exception as e:

        messagebox.showerror(
            "Connection Error",
            str(e)
        )

# =========================
# LICENSE BUTTON
# =========================

verify_button = tk.Button(
    license_window,
    text="Verify License",
    command=verify_license
)

verify_button.pack(pady=20)

# =========================
# AUTO LOGIN
# =========================

def launch_app(
    fast_model,
    hd_model
):

    global CURRENT_PLAN
    global IS_PRO

    saved = load_license()

    if saved:

        try:

            data = verify_license_key(
                saved["key"]
            )

            if data.get("success"):

                CURRENT_PLAN = data.get(
                    "plan",
                    "FREE"
                )

                IS_PRO = CURRENT_PLAN in [
                    "PRO",
                    "PREMIUM"
                ]

                license_window.destroy()

                start_main_app()

                return

        except:
            pass

    license_window.mainloop()

# =========================
# START
# =========================
