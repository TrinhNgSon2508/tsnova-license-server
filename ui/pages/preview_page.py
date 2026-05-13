import customtkinter as ctk


class PreviewPage(ctk.CTkFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent
        )

        # =================================================
        # TITLE
        # =================================================

        title = ctk.CTkLabel(

            self,

            text="Preview",

            font=(
                "Arial",
                26,
                "bold"
            )
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # =================================================
        # DROP AREA
        # =================================================

        self.drop_area = ctk.CTkFrame(
            self,
            height=220
        )

        self.drop_area.pack(

            fill="x",

            padx=20,
            pady=10
        )

        self.drop_area.pack_propagate(
            False
        )

        drop_label = ctk.CTkLabel(

            self.drop_area,

            text=(
                "Drag & Drop Images Here\n\n"
                "or click Import"
            ),

            font=(
                "Arial",
                20
            )
        )

        drop_label.place(

            relx=0.5,
            rely=0.5,

            anchor="center"
        )

        # =================================================
        # THUMBNAIL AREA
        # =================================================

        self.thumbnail_scroll = (
            ctk.CTkScrollableFrame(
                self
            )
        )

        self.thumbnail_scroll.pack(

            fill="both",
            expand=True,

            padx=20,
            pady=(10, 20)
        )