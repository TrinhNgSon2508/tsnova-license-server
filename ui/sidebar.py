import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        on_page_change=None
    ):

        super().__init__(
            parent,
            width=220
        )

        self.pack_propagate(False)

        self.on_page_change = on_page_change

        # =================================================
        # TITLE
        # =================================================

        title = ctk.CTkLabel(

            self,

            text="TSNOVA",

            font=(
                "Arial",
                28,
                "bold"
            )
        )

        title.pack(
            pady=(30, 40)
        )

        # =================================================
        # NAV BUTTONS
        # =================================================

        self.create_nav_button(
            "Preview",
            "preview"
        )

        self.create_nav_button(
            "Queue",
            "queue"
        )

        self.create_nav_button(
            "Performance",
            "performance"
        )

        self.create_nav_button(
            "Settings",
            "settings"
        )

    # =====================================================
    # NAV BUTTON
    # =====================================================

    def create_nav_button(
        self,
        text,
        page_name
    ):

        button = ctk.CTkButton(

            self,

            text=text,

            height=45,

            command=lambda: self.change_page(
                page_name
            )
        )

        button.pack(
            fill="x",
            padx=20,
            pady=8
        )

    # =====================================================
    # CHANGE PAGE
    # =====================================================

    def change_page(
        self,
        page_name
    ):

        if self.on_page_change:

            self.on_page_change(
                page_name
            )