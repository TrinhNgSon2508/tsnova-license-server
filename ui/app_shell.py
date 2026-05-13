import customtkinter as ctk

from ui.sidebar import Sidebar

from ui.pages.dashboard_page import DashboardPage
from ui.pages.preview_page import PreviewPage
from ui.pages.queue_page import QueuePage
from ui.pages.settings_page import SettingsPage


class AppShell(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)

        # SIDEBAR

        self.sidebar = Sidebar(
            self,
            self.switch_page
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # CONTENT AREA

        self.content = ctk.CTkFrame(self)

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        # PAGES

        self.pages = {

            "dashboard": DashboardPage(
                self.content
            ),

            "preview": PreviewPage(
                self.content
            ),

            "queue": QueuePage(
                self.content
            ),

            "settings": SettingsPage(
                self.content
            )
        }

        self.current_page = None

        self.switch_page("preview")

    def switch_page(self, page_name):

        if self.current_page:
            self.current_page.pack_forget()

        self.current_page = self.pages[page_name]

        self.current_page.pack(
            fill="both",
            expand=True
        )