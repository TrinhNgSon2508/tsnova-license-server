# core/preview_manager.py

from PIL import Image
from customtkinter import CTkImage
import customtkinter as ctk


def update_preview(
    files,
    preview_frame,
    preview_images
):

    for widget in preview_frame.winfo_children():

        widget.destroy()

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