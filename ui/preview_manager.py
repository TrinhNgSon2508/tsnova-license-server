import os
import threading

import customtkinter as ctk

from PIL import Image


class PreviewManager:

    def __init__(self):

        # =================================================
        # CONFIG
        # =================================================

        self.thumbnail_size = (
            160,
            160
        )

        # =================================================
        # CACHE
        # =================================================

        self.thumbnail_cache = {}

        self.loading_threads = {}

        self.card_widgets = {}

        # =================================================
        # LOCK
        # =================================================

        self.cache_lock = threading.Lock()

    # =====================================================
    # CREATE THUMBNAIL
    # =====================================================

    def create_thumbnail(
        self,
        parent,
        image_path,
        click_callback=None
    ):

        # =================================================
        # CARD
        # =================================================

        card = ctk.CTkFrame(
            parent,
            width=190,
            height=240,
            corner_radius=12
        )

        card.grid_propagate(False)

        card.pack_propagate(False)

        # =================================================
        # IMAGE FRAME
        # =================================================

        image_frame = ctk.CTkFrame(
            card,
            width=170,
            height=170,
            fg_color="#252525"
        )

        image_frame.pack(
            pady=(10, 5)
        )

        image_frame.pack_propagate(False)

        # =================================================
        # IMAGE LABEL
        # =================================================

        image_label = ctk.CTkLabel(
            image_frame,
            text="Loading..."
        )

        image_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =================================================
        # STATUS LABEL
        # =================================================

        status_label = ctk.CTkLabel(
            image_frame,
            text="WAITING",
            height=22,
            corner_radius=6,
            fg_color="#444444",
            padx=8
        )

        status_label.place(
            relx=0.98,
            rely=0.02,
            anchor="ne"
        )

        # =================================================
        # PROGRESS BAR
        # =================================================

        progress_bar = ctk.CTkProgressBar(
            image_frame,
            width=140,
            height=10
        )

        progress_bar.set(0)

        progress_bar.place(
            relx=0.5,
            rely=0.95,
            anchor="s"
        )

        # =================================================
        # PROGRESS TEXT
        # =================================================

        progress_text = ctk.CTkLabel(
            image_frame,
            text="0%",
            font=("Arial", 11)
        )

        progress_text.place(
            relx=0.5,
            rely=0.82,
            anchor="center"
        )

        # =================================================
        # FILE NAME
        # =================================================

        filename = os.path.basename(
            image_path
        )

        filename_label = ctk.CTkLabel(
            card,
            text=filename,
            wraplength=160,
            justify="center"
        )

        filename_label.pack(
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # CLICK EVENT
        # =================================================

        if click_callback:

            def on_click(event=None):

                click_callback(
                    image_path
                )

            widgets = [

                card,
                image_frame,
                image_label,
                filename_label,
                status_label,
                progress_text
            ]

            for widget in widgets:

                widget.bind(
                    "<Button-1>",
                    on_click
                )

        # =================================================
        # SAVE WIDGETS
        # =================================================

        self.card_widgets[image_path] = {

            "card": card,

            "image_frame": image_frame,

            "image_label": image_label,

            "filename_label": filename_label,

            "status_label": status_label,

            "progress_bar": progress_bar,

            "progress_text": progress_text
        }

        # =================================================
        # ASYNC LOAD
        # =================================================

        self.load_thumbnail_async(
            image_path=image_path,
            image_label=image_label
        )

        return card

    # =====================================================
    # LOAD THUMBNAIL ASYNC
    # =====================================================

    def load_thumbnail_async(
        self,
        image_path,
        image_label
    ):

        with self.cache_lock:

            if image_path in self.loading_threads:
                return

        # =================================================
        # WORKER
        # =================================================

        def worker():

            try:

                # =========================================
                # CACHE HIT
                # =========================================

                with self.cache_lock:

                    cached = self.thumbnail_cache.get(
                        image_path
                    )

                if cached:

                    photo = cached

                else:

                    image = Image.open(
                        image_path
                    )

                    image.thumbnail(
                        self.thumbnail_size
                    )

                    photo = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=image.size
                    )

                    with self.cache_lock:

                        self.thumbnail_cache[
                            image_path
                        ] = photo

                # =========================================
                # UI UPDATE
                # =========================================

                def update_ui():

                    try:

                        image_label.configure(
                            image=photo,
                            text=""
                        )

                        image_label.image = photo

                    except:
                        pass

                image_label.after(
                    0,
                    update_ui
                )

            except Exception as error:

                def show_error():

                    try:

                        image_label.configure(
                            text="Failed"
                        )

                    except:
                        pass

                image_label.after(
                    0,
                    show_error
                )

                print(
                    f"Thumbnail Error: {error}"
                )

            finally:

                with self.cache_lock:

                    if image_path in self.loading_threads:

                        del self.loading_threads[
                            image_path
                        ]

        # =================================================
        # START THREAD
        # =================================================

        thread = threading.Thread(
            target=worker,
            daemon=True
        )

        with self.cache_lock:

            self.loading_threads[
                image_path
            ] = thread

        thread.start()

    # =====================================================
    # UPDATE SELECTION STATE
    # =====================================================

    def update_selection_state(
        self,
        image_path,
        selected
    ):

        if image_path not in self.card_widgets:
            return

        widgets = self.card_widgets[
            image_path
        ]

        card = widgets["card"]

        image_frame = widgets["image_frame"]

        try:

            if selected:

                card.configure(
                    border_width=2,
                    border_color="#3b8cff"
                )

                image_frame.configure(
                    fg_color="#1f3d5c"
                )

            else:

                card.configure(
                    border_width=0
                )

                image_frame.configure(
                    fg_color="#252525"
                )

        except:
            pass

    # =====================================================
    # UPDATE TASK STATUS
    # =====================================================

    def update_task_status(
        self,
        image_path,
        status
    ):

        if image_path not in self.card_widgets:
            return

        widgets = self.card_widgets[
            image_path
        ]

        status_label = widgets[
            "status_label"
        ]

        status_text = str(
            status
        ).upper()

        # =================================================
        # STATUS COLORS
        # =================================================

        color_map = {

            "waiting": "#555555",

            "processing": "#3b82f6",

            "completed": "#16a34a",

            "failed": "#dc2626",

            "cancelled": "#a855f7"
        }

        color = color_map.get(
            status.lower(),
            "#444444"
        )

        try:

            status_label.configure(
                text=status_text,
                fg_color=color
            )

        except:
            pass

    # =====================================================
    # UPDATE TASK PROGRESS
    # =====================================================

    def update_task_progress(
        self,
        image_path,
        progress
    ):

        if image_path not in self.card_widgets:
            return

        widgets = self.card_widgets[
            image_path
        ]

        progress_bar = widgets[
            "progress_bar"
        ]

        progress_text = widgets[
            "progress_text"
        ]

        try:

            normalized = max(
                0,
                min(100, progress)
            ) / 100

            progress_bar.set(
                normalized
            )

            progress_text.configure(
                text=f"{int(progress)}%"
            )

        except:
            pass

    # =====================================================
    # REMOVE THUMBNAIL
    # =====================================================

    def remove_thumbnail(
        self,
        image_path
    ):

        with self.cache_lock:

            if image_path in self.thumbnail_cache:

                del self.thumbnail_cache[
                    image_path
                ]

        if image_path in self.card_widgets:

            try:

                widgets = self.card_widgets[
                    image_path
                ]

                widgets["card"].destroy()

            except:
                pass

            del self.card_widgets[
                image_path
            ]

    # =====================================================
    # CLEAR CACHE
    # =====================================================

    def clear_cache(self):

        with self.cache_lock:

            self.thumbnail_cache.clear()

            self.loading_threads.clear()

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup(self):

        for image_path in list(
            self.card_widgets.keys()
        ):

            self.remove_thumbnail(
                image_path
            )

        self.clear_cache()


preview_manager = PreviewManager()