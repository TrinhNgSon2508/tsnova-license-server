# ui/splash_screen.py

import customtkinter as ctk


class SplashScreen:

    def __init__(self):

        self.window = ctk.CTkToplevel(parent)

        self.window.geometry("500x300")

        self.window.title("TSNOVA Loading")

        self.window.resizable(False, False)

        self.window.configure(
            fg_color="#111111"
        )

        # =========================
        # TITLE
        # =========================

        title = ctk.CTkLabel(
            self.window,
            text="TSNOVA",
            font=("Arial", 42, "bold")
        )

        title.pack(pady=(70, 20))

        # =========================
        # STATUS
        # =========================

        self.status_label = ctk.CTkLabel(
            self.window,
            text="Loading AI Models...",
            font=("Arial", 18)
        )

        self.status_label.pack(pady=10)

        # =========================
        # PROGRESS
        # =========================

        self.progress = ctk.CTkProgressBar(
            self.window,
            width=300
        )

        self.progress.pack(pady=20)

        self.progress.set(0)

    def update_progress(
        self,
        value,
        text
    ):

        self.progress.set(value)

        self.status_label.configure(
            text=text
        )

        self.window.update()

    def destroy(self):

        self.window.destroy()

    def run(self):

        self.window.update()