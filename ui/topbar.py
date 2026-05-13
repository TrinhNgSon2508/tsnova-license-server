import customtkinter as ctk


class Topbar(ctk.CTkFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent,
            height=60
        )

        self.pack_propagate(False)

        title = ctk.CTkLabel(

            self,

            text="TSNOVA",

            font=(
                "Arial",
                24,
                "bold"
            )
        )

        title.pack(

            side="left",

            padx=20,
            pady=10
        )