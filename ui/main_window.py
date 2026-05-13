import customtkinter as ctk

from ui.sidebar import (
    Sidebar
)

from ui.pages.preview_page import (
    PreviewPage
)

from ui.pages.queue_page import (
    QueuePage
)

from ui.pages.settings_page import (
    SettingsPage
)


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        # =================================================
        # WINDOW
        # =================================================

        self.title(
            "TSNOVA"
        )

        self.geometry(
            "1400x900"
        )

        self.minsize(
            1200,
            800
        )

        # =================================================
        # GRID
        # =================================================

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # =================================================
        # SIDEBAR
        # =================================================

        self.sidebar = Sidebar(

            self,

            on_page_change=self.show_page
        )

        self.sidebar.grid(

            row=0,
            column=0,

            sticky="ns"
        )

        # =================================================
        # PAGE CONTAINER
        # =================================================

        self.page_container = (
            ctk.CTkFrame(
                self
            )
        )

        self.page_container.grid(

            row=0,
            column=1,

            sticky="nsew"
        )

        self.page_container.grid_rowconfigure(
            0,
            weight=1
        )

        self.page_container.grid_columnconfigure(
            0,
            weight=1
        )

        # =================================================
        # PAGES
        # =================================================

        self.pages = {}

        self.pages["preview"] = (
            PreviewPage(
                self.page_container
            )
        )

        self.pages["queue"] = (
            QueuePage(
                self.page_container
            )
        )

        self.pages["settings"] = (
            SettingsPage(
                self.page_container
            )
        )

        # =================================================
        # GRID ALL PAGES
        # =================================================

        for page in self.pages.values():

            page.grid(

                row=0,
                column=0,

                sticky="nsew"
            )

        # =================================================
        # DEFAULT PAGE
        # =================================================

        self.show_page(
            "preview"
        )

    # =====================================================
    # SHOW PAGE
    # =====================================================

    def show_page(
        self,
        page_name
    ):

        page = self.pages.get(
            page_name
        )

        if page:

            page.tkraise()