import customtkinter as ctk


class WidgetPool:

    def __init__(self):

        self.active_widgets = {}

        self.inactive_widgets = []

    # =====================================================
    # ACQUIRE
    # =====================================================

    def acquire(
        self,
        parent,
        create_callback
    ):

        if self.inactive_widgets:

            widget = self.inactive_widgets.pop()

            widget.pack_forget()

            widget.grid_forget()

            return widget

        return create_callback(
            parent
        )

    # =====================================================
    # RELEASE
    # =====================================================

    def release(
        self,
        key
    ):

        if key not in self.active_widgets:
            return

        widget = self.active_widgets.pop(
            key
        )

        try:

            widget.grid_forget()

            widget.pack_forget()

        except:
            pass

        self.inactive_widgets.append(
            widget
        )

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        key,
        widget
    ):

        self.active_widgets[key] = widget

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        key
    ):

        return self.active_widgets.get(
            key
        )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        for widget in self.active_widgets.values():

            try:
                widget.destroy()
            except:
                pass

        for widget in self.inactive_widgets:

            try:
                widget.destroy()
            except:
                pass

        self.active_widgets.clear()

        self.inactive_widgets.clear()