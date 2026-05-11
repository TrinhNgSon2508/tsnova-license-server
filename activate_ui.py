import customtkinter as ctk

from activate_client import activate_license
from license_manager import save_license_key
from tsnova_ui import TSNovaApp


class ActivateWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("TSNOVA Activation")

        self.geometry("400x250")

        # title
        self.label = ctk.CTkLabel(
            self,
            text="Enter License Key",
            font=("Arial", 20)
        )

        self.label.pack(pady=20)

        # input
        self.entry = ctk.CTkEntry(
            self,
            width=250
        )

        self.entry.pack(pady=10)

        # result label
        self.result_label = ctk.CTkLabel(
            self,
            text=""
        )

        self.result_label.pack(pady=10)

        # button
        self.button = ctk.CTkButton(
            self,
            text="Activate",
            command=self.activate
        )

        self.button.pack(pady=20)

    def activate(self):

        key = self.entry.get()

        result = activate_license(key)

        if result["success"]:

            save_license_key(key)

            self.destroy()

            app = TSNovaApp()

            app.mainloop()

        else:

            self.result_label.configure(
                text=result["message"]
            )


if __name__ == "__main__":

    app = ActivateWindow()

    app.mainloop()