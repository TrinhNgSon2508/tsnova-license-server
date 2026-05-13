import math

import customtkinter as ctk

from ui.preview_manager import (
    preview_manager
)

from ui.renderers.widget_pool import (
    WidgetPool
)


class PreviewGridRenderer:

    def __init__(
        self,
        container,
        click_callback=None
    ):

        self.container = container

        self.click_callback = click_callback

        self.columns = 4

        self.cell_padding = 10

        self.thumbnail_widgets = {}

        self.visible_paths = []

        self.widget_pool = WidgetPool()

    # =====================================================
    # CLEAR GRID
    # =====================================================

    def clear(self):

        self.widget_pool.clear()

        self.thumbnail_widgets.clear()

        self.visible_paths.clear()

    # =====================================================
    # REMOVE ITEM
    # =====================================================

    def remove_item(
        self,
        image_path
    ):

        self.widget_pool.release(
            image_path
        )

        self.thumbnail_widgets.pop(
            image_path,
            None
        )

        if image_path in self.visible_paths:

            self.visible_paths.remove(
                image_path
            )

    # =====================================================
    # CREATE THUMBNAIL
    # =====================================================

    def create_thumbnail_widget(
        self,
        image_path
    ):

        def create_widget(parent):

            return preview_manager.create_thumbnail(
                parent=parent,
                image_path=image_path,
                click_callback=self.click_callback
            )

        thumbnail = self.widget_pool.acquire(
            self.container,
            create_widget
        )

        return thumbnail

    # =====================================================
    # POSITION WIDGET
    # =====================================================

    def position_widget(
        self,
        widget,
        index
    ):

        row = math.floor(
            index / self.columns
        )

        column = index % self.columns

        widget.grid(
            row=row,
            column=column,
            padx=self.cell_padding,
            pady=self.cell_padding,
            sticky="n"
        )

    # =====================================================
    # RENDER GRID
    # =====================================================

    def render(
        self,
        image_paths
    ):

        new_paths = set(image_paths)

        current_paths = set(
            self.visible_paths
        )

        removed_paths = current_paths - new_paths

        # =================================================
        # REMOVE OLD
        # =================================================

        for path in removed_paths:

            self.remove_item(path)

        # =================================================
        # RENDER CURRENT
        # =================================================

        for index, image_path in enumerate(image_paths):

            # =============================================
            # REUSE EXISTING
            # =============================================

            if image_path in self.thumbnail_widgets:

                widget = self.thumbnail_widgets[
                    image_path
                ]

                self.position_widget(
                    widget,
                    index
                )

                continue

            # =============================================
            # CREATE NEW
            # =============================================

            thumbnail = self.create_thumbnail_widget(
                image_path
            )

            self.position_widget(
                thumbnail,
                index
            )

            self.thumbnail_widgets[
                image_path
            ] = thumbnail

            self.widget_pool.register(
                image_path,
                thumbnail
            )

        # =================================================
        # SAVE STATE
        # =================================================

        self.visible_paths = list(
            image_paths
        )

    # =====================================================
    # REFRESH GRID
    # =====================================================

    def refresh(
        self,
        image_paths
    ):

        self.render(
            image_paths
        )

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup(self):

        self.clear()