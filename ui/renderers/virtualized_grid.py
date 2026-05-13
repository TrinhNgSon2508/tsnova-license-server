import math
import threading

from ui.renderers.preview_grid_renderer import (
    PreviewGridRenderer
)


class VirtualizedGrid:

    def __init__(
        self,
        container,
        scroll_widget,
        click_callback=None
    ):
        self.refresh_delay = 30

        self.refresh_timer = None

        self.refresh_lock = threading.Lock()

        self.container = container

        self.scroll_widget = scroll_widget

        self.click_callback = click_callback

        self.grid_renderer = PreviewGridRenderer(
            container=self.container,
            click_callback=self.click_callback
        )

        # =================================================
        # CONFIG
        # =================================================

        self.columns = 4

        self.item_height = 210

        self.buffer_rows = 2

        self.max_visible_rows = 6

        # =================================================
        # STATE
        # =================================================

        self.image_paths = []

        self.visible_start = 0

        self.visible_end = 0

        self.last_scroll_position = 0

        # =================================================
        # BIND
        # =================================================

        self.bind_scroll()

    # =====================================================
    # BIND SCROLL
    # =====================================================

    def bind_scroll(self):

        try:

            self.scroll_widget._parent_canvas.bind(
                "<MouseWheel>",
                self.on_scroll
            )

        except:
            pass

    # =====================================================
    # SET IMAGES
    # =====================================================

    def set_images(
        self,
        image_paths
    ):

        self.image_paths = list(
            image_paths
        )

        self.schedule_refresh()

    # =====================================================
    # ON SCROLL
    # =====================================================

    def on_scroll(
        self,
        event=None
    ):

        self.schedule_refresh()

    # =====================================================
    # GET SCROLL Y
    # =====================================================
    
    def schedule_refresh(self):

        with self.refresh_lock:

            if self.refresh_timer:

                try:
                    self.refresh_timer.cancel()
                except:
                    pass

            self.refresh_timer = threading.Timer(
                self.refresh_delay / 1000,
                self.refresh_visible
            )

            self.refresh_timer.daemon = True

            self.refresh_timer.start()

    def get_scroll_y(self):

        try:

            canvas = self.scroll_widget._parent_canvas

            return canvas.canvasy(0)

        except:
            return 0

    # =====================================================
    # CALCULATE RANGE
    # =====================================================

    def calculate_visible_range(self):

        scroll_y = self.get_scroll_y()

        start_row = max(
            0,
            math.floor(
                scroll_y / self.item_height
            ) - self.buffer_rows
        )

        end_row = start_row + (
            self.max_visible_rows +
            self.buffer_rows
        )

        start_index = start_row * self.columns

        end_index = end_row * self.columns

        return (
            start_index,
            end_index
        )

    # =====================================================
    # GET VISIBLE PATHS
    # =====================================================

    def get_visible_paths(self):

        (
            start_index,
            end_index
        ) = self.calculate_visible_range()

        self.visible_start = start_index

        self.visible_end = end_index

        return self.image_paths[
            start_index:end_index
        ]

    # =====================================================
    # REFRESH VISIBLE
    # =====================================================

    def refresh_visible(self):

        visible_paths = self.get_visible_paths()

        self.grid_renderer.refresh(
            visible_paths
        )

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        self.schedule_refresh()

    # =====================================================
    # REMOVE ITEM
    # =====================================================

    def remove_item(
        self,
        image_path
    ):

        if image_path in self.image_paths:

            self.image_paths.remove(
                image_path
            )

        self.grid_renderer.remove_item(
            image_path
        )

        self.schedule_refresh()

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.image_paths.clear()

        self.grid_renderer.clear()

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup(self):

        self.clear()