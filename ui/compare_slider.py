import customtkinter as ctk

from PIL import (
    Image,
    ImageTk
)


class CompareSlider(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        before_path,
        after_path
    ):

        super().__init__(parent)

        self.before_image = Image.open(
            before_path
        )

        self.after_image = Image.open(
            after_path
        )

        self.slider_pos = 0.5

        # =====================================
        # CANVAS
        # =====================================

        self.canvas = ctk.CTkCanvas(
            self,
            bg="#202020",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # =====================================
        # SLIDER
        # =====================================

        self.slider = ctk.CTkSlider(
            self,
            from_=0,
            to=1,
            command=self.update_slider
        )

        self.slider.set(0.5)

        self.slider.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        # =====================================
        # EVENTS
        # =====================================

        self.canvas.bind(
            "<Configure>",
            lambda e: self.draw_images()
        )

    # =========================================
    # UPDATE SLIDER
    # =========================================

    def update_slider(
        self,
        value
    ):

        self.slider_pos = value

        self.draw_images()

    # =========================================
    # DRAW IMAGES
    # =========================================

    def draw_images(self):

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 10:
            return

        if canvas_height < 10:
            return

        before = self.before_image.copy()
        after = self.after_image.copy()

        before.thumbnail(
            (
                canvas_width,
                canvas_height
            )
        )

        after.thumbnail(
            (
                canvas_width,
                canvas_height
            )
        )

        width = min(
            before.width,
            after.width
        )

        height = min(
            before.height,
            after.height
        )

        before = before.resize(
            (
                width,
                height
            )
        )

        after = after.resize(
            (
                width,
                height
            )
        )

        split_x = int(
            width * self.slider_pos
        )

        before_crop = before.crop(
            (
                0,
                0,
                split_x,
                height
            )
        )

        after_crop = after.crop(
            (
                split_x,
                0,
                width,
                height
            )
        )

        combined = Image.new(
            "RGB",
            (
                width,
                height
            )
        )

        combined.paste(
            before_crop,
            (0, 0)
        )

        combined.paste(
            after_crop,
            (split_x, 0)
        )

        self.tk_image = ImageTk.PhotoImage(
            combined
        )

        self.canvas.delete("all")

        x = canvas_width // 2
        y = canvas_height // 2

        self.canvas.create_image(
            x,
            y,
            image=self.tk_image
        )

        line_x = (
            x - width // 2 + split_x
        )

        self.canvas.create_line(
            line_x,
            y - height // 2,
            line_x,
            y + height // 2,
            width=3,
            fill="white"
        )