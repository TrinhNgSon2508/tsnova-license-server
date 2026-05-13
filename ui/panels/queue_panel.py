import customtkinter as ctk

from core.app_state import (
    app_state
)

from core.constants import (
    QUEUE_REFRESH_MS,
    QUEUE_ITEM_HEIGHT
)

from core.processing_worker import (
    start_processing_worker
)

from core.queue_storage import (
    save_queue
)

from core.system_monitor import (
    start_system_monitor
)

from core.queue_manager import (
    remove_item,
    retry_item,
    cancel_queue_item,
    clear_queue
)

from core.queue_sync import (
    rebuild_processing_queue
)

from core.preset_manager import (
    PRESETS
)

from ui.builders.queue_item_builder import (
    create_queue_item
)

from ui.renderers.queue_renderer import (
    build_eta_text,
    build_label_text,
    get_status_color
)

from ui.updaters.monitor_updater import (
    update_monitor_labels
)

from ui.updaters.summary_updater import (
    update_summary
)

from ui.updaters.queue_item_updater import (
    update_queue_item
)

from utils.task_utils import (
    is_task_waiting
)

from ui.updaters.queue_item_updater import (
    update_queue_item
)

from ui.updaters.summary_updater import (
    update_summary
)

# =========================================================
# QUEUE PANEL
# =========================================================

class QueuePanel(ctk.CTkFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(parent)

        # =================================================
        # DRAG STATE
        # =================================================

        self.dragging_item = None

        # =================================================
        # UI REFERENCES
        # =================================================

        self.queue_frames = {}

        self.queue_labels = {}

        self.queue_progressbars = {}

        # =================================================
        # LAYOUT
        # =================================================

        self.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =================================================
        # TITLE
        # =================================================

        self.title_label = ctk.CTkLabel(

            self,

            text="Task Queue",

            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.title_label.pack(
            pady=(10, 15)
        )

        # =================================================
        # PRESET FRAME
        # =================================================

        self.preset_frame = ctk.CTkFrame(
            self
        )

        self.preset_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.preset_label = ctk.CTkLabel(
            self.preset_frame,
            text="Preset"
        )

        self.preset_label.pack(
            side="left",
            padx=10
        )

        self.preset_menu = ctk.CTkOptionMenu(

            self.preset_frame,

            values=list(
                PRESETS.keys()
            ),

            command=self.apply_preset
        )

        self.preset_menu.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =================================================
        # CONTROL FRAME
        # =================================================

        self.control_frame = ctk.CTkFrame(
            self
        )

        self.control_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # PAUSE BUTTON
        # =================================================

        self.pause_button = ctk.CTkButton(

            self.control_frame,

            text="Pause",

            command=self.pause_queue
        )

        self.pause_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        # =================================================
        # RESUME BUTTON
        # =================================================

        self.resume_button = ctk.CTkButton(

            self.control_frame,

            text="Resume",

            command=self.resume_queue
        )

        self.resume_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        # =================================================
        # CLEAR BUTTON
        # =================================================

        self.clear_button = ctk.CTkButton(

            self.control_frame,

            text="Clear Queue",

            command=self.clear_queue
        )

        self.clear_button.pack(
            side="right",
            padx=5,
            pady=5
        )

        # =================================================
        # MONITOR FRAME
        # =================================================

        self.monitor_frame = ctk.CTkFrame(
            self
        )

        self.monitor_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # MONITOR LABELS
        # =================================================

        self.worker_label = ctk.CTkLabel(
            self.monitor_frame,
            text="Workers: 0"
        )

        self.worker_label.pack(
            side="left",
            padx=10
        )

        self.queue_label = ctk.CTkLabel(
            self.monitor_frame,
            text="Queue: 0"
        )

        self.queue_label.pack(
            side="left",
            padx=10
        )

        self.done_label = ctk.CTkLabel(
            self.monitor_frame,
            text="Done: 0"
        )

        self.done_label.pack(
            side="left",
            padx=10
        )

        self.failed_label = ctk.CTkLabel(
            self.monitor_frame,
            text="Failed: 0"
        )

        self.failed_label.pack(
            side="left",
            padx=10
        )

        self.cpu_label = ctk.CTkLabel(
            self.monitor_frame,
            text="CPU: 0%"
        )

        self.cpu_label.pack(
            side="left",
            padx=10
        )

        self.ram_label = ctk.CTkLabel(
            self.monitor_frame,
            text="RAM: 0%"
        )

        self.ram_label.pack(
            side="left",
            padx=10
        )

        self.gpu_label = ctk.CTkLabel(
            self.monitor_frame,
            text="GPU: 0%"
        )

        self.gpu_label.pack(
            side="left",
            padx=10
        )

        self.vram_label = ctk.CTkLabel(
            self.monitor_frame,
            text="VRAM: 0%"
        )

        self.vram_label.pack(
            side="left",
            padx=10
        )

        self.speed_label = ctk.CTkLabel(
            self.monitor_frame,
            text="Speed: 0 file/min"
        )

        self.speed_label.pack(
            side="left",
            padx=10
        )

        self.avg_label = ctk.CTkLabel(
            self.monitor_frame,
            text="Avg: 0s/file"
        )

        self.avg_label.pack(
            side="left",
            padx=10
        )

        # =================================================
        # SUMMARY FRAME
        # =================================================

        self.summary_frame = ctk.CTkFrame(
            self
        )

        self.summary_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.summary_label = ctk.CTkLabel(
            self.summary_frame,
            text="0 / 0 completed"
        )

        self.summary_label.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.summary_progressbar = (
            ctk.CTkProgressBar(
                self.summary_frame,
                height=14
            )
        )

        self.summary_progressbar.pack(
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        self.summary_progressbar.set(0)

        # =================================================
        # SCROLL FRAME
        # =================================================

        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            height=QUEUE_ITEM_HEIGHT
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =================================================
        # START SERVICES
        # =================================================

        start_processing_worker()

        start_system_monitor()

        # =================================================
        # AUTO REFRESH
        # =================================================

        self.auto_refresh()

    # =====================================================
    # AUTO REFRESH
    # =====================================================

    def auto_refresh(
        self
    ):
        from core.state_validator import (
            validate_app_state
        )
        update_monitor_labels(
            self
        )

        update_summary(
            self
        )
        
        validate_app_state()
        self.refresh_queue()


    # =====================================================
    # REFRESH QUEUE
    # =====================================================

    def refresh_queue(
        self
    ):

        existing_paths = set(
            self.queue_frames.keys()
        )

        current_paths = set(
            app_state.image_paths
        )

        # =================================================
        # REMOVE OLD ITEMS
        # =================================================

        removed_paths = (
            existing_paths - current_paths
        )

        for path in removed_paths:

            self.queue_frames[path].destroy()

            self.queue_frames.pop(
                path,
                None
            )

            self.queue_labels.pop(
                path,
                None
            )

            self.queue_progressbars.pop(
                path,
                None
            )

        # =================================================
        # BUILD / UPDATE ITEMS
        # =================================================

        for image_path in app_state.image_paths:

            status = app_state.task_status.get(
                image_path,
                "waiting"
            )

            progress = app_state.task_progress.get(
                image_path,
                0
            )

            filename = image_path.split(
                "/"
            )[-1].split("\\")[-1]

            eta_text = build_eta_text(
                image_path=image_path,
                status=status,
                progress=progress
            )

            label_text = build_label_text(
                filename=filename,
                status=status,
                eta_text=eta_text
            )

            status_color = get_status_color(
                status
            )

            # =================================================
            # UPDATE EXISTING
            # =================================================

            if image_path in self.queue_labels:

                update_queue_item(
                    label=self.queue_labels[
                        image_path
                    ],
                    progressbar=self.queue_progressbars[
                        image_path
                    ],
                    label_text=label_text,
                    status_color=status_color,
                    progress=progress
                )

                continue

            # =================================================
            # CREATE ITEM
            # =================================================

            item_frame, label, progressbar = (
                create_queue_item(
                    panel=self,
                    image_path=image_path,
                    label_text=label_text,
                    status_color=status_color,
                    progress=progress
                )
            )

            self.queue_frames[
                image_path
            ] = item_frame

            update_queue_item(
                label=self.queue_labels[
                    image_path
                ],
                progressbar=self.queue_progressbars[
                    image_path
                ],
                label_text=label_text,
                status_color=status_color,
                progress=progress
            )

    # =====================================================
    # START DRAG
    # =====================================================

    def start_drag(
        self,
        image_path
    ):

        self.dragging_item = image_path

    # =====================================================
    # END DRAG
    # =====================================================

    def end_drag(
        self,
        target_path
    ):

        if not self.dragging_item:
            return

        source_path = self.dragging_item

        if source_path == target_path:
            return

        queue = app_state.image_paths

        if (
            source_path not in queue or
            target_path not in queue
        ):

            return

        source_index = queue.index(
            source_path
        )

        target_index = queue.index(
            target_path
        )

        queue.insert(
            target_index,
            queue.pop(source_index)
        )

        app_state.image_paths = list(
            queue
        )

        rebuild_processing_queue()

        self.dragging_item = None

        self.refresh_queue()

    # =====================================================
    # PAUSE QUEUE
    # =====================================================

    def pause_queue(
        self
    ):

        app_state.queue_paused = True

    # =====================================================
    # RESUME QUEUE
    # =====================================================

    def resume_queue(
        self
    ):

        app_state.queue_paused = False

    # =====================================================
    # CLEAR QUEUE
    # =====================================================

    def clear_queue(
        self
    ):

        clear_queue()

        self.refresh_queue()

    # =====================================================
    # REMOVE ITEM
    # =====================================================

    def remove_item(
        self,
        image_path
    ):

        remove_item(
            image_path
        )

        self.refresh_queue()

    # =====================================================
    # RETRY ITEM
    # =====================================================

    def retry_item(
        self,
        image_path
    ):

        retry_item(
            image_path
        )

        self.refresh_queue()

    # =====================================================
    # CANCEL ITEM
    # =====================================================

    def cancel_item(
        self,
        image_path
    ):

        cancel_queue_item(
            image_path
        )

        self.refresh_queue()

    # =====================================================
    # APPLY PRESET
    # =====================================================

    def apply_preset(
        self,
        preset_name
    ):

        preset = PRESETS.get(
            preset_name
        )

        if not preset:
            return

        app_state.max_workers = (
            preset["workers"]
        )

        app_state.upscale_factor = (
            preset["upscale_factor"]
        )

        app_state.output_format = (
            preset["output_format"]
        )

        app_state.current_model = (
            preset["model"]
        )

        app_state.denoise_strength = (
            preset["denoise"]
        )