import customtkinter as ctk

from core.app_state import (
    app_state
)


# =========================================================
# SYSTEM STATS
# =========================================================

class SystemStats(ctk.CTkFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(parent)

        # =================================================
        # LAYOUT
        # =================================================

        self.pack_propagate(False)

        # =================================================
        # WORKER
        # =================================================

        self.worker_label = ctk.CTkLabel(
            self,
            text="Workers: 0"
        )

        self.worker_label.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =================================================
        # QUEUE
        # =================================================

        self.queue_label = ctk.CTkLabel(
            self,
            text="Queue: 0"
        )

        self.queue_label.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =================================================
        # DONE
        # =================================================

        self.done_label = ctk.CTkLabel(
            self,
            text="Done: 0"
        )

        self.done_label.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =================================================
        # FAILED
        # =================================================

        self.failed_label = ctk.CTkLabel(
            self,
            text="Failed: 0"
        )

        self.failed_label.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =================================================
        # CPU
        # =================================================

        self.cpu_label = ctk.CTkLabel(
            self,
            text="CPU: 0%"
        )

        self.cpu_label.pack(
            side="left",
            padx=10
        )

        # =================================================
        # RAM
        # =================================================

        self.ram_label = ctk.CTkLabel(
            self,
            text="RAM: 0%"
        )

        self.ram_label.pack(
            side="left",
            padx=10
        )

        # =================================================
        # GPU
        # =================================================

        self.gpu_label = ctk.CTkLabel(
            self,
            text="GPU: 0%"
        )

        self.gpu_label.pack(
            side="left",
            padx=10
        )

        # =================================================
        # VRAM
        # =================================================

        self.vram_label = ctk.CTkLabel(
            self,
            text="VRAM: 0%"
        )

        self.vram_label.pack(
            side="left",
            padx=10
        )

        # =================================================
        # SPEED
        # =================================================

        self.speed_label = ctk.CTkLabel(
            self,
            text="Speed: 0 file/min"
        )

        self.speed_label.pack(
            side="left",
            padx=10
        )

        # =================================================
        # AVG
        # =================================================

        self.avg_label = ctk.CTkLabel(
            self,
            text="Avg: 0s/file"
        )

        self.avg_label.pack(
            side="left",
            padx=10
        )

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(
        self
    ):

        self.worker_label.configure(
            text=(
                f"Workers: "
                f"{app_state.active_workers}"
            )
        )

        self.queue_label.configure(
            text=(
                f"Queue: "
                f"{len(app_state.processing_queue)}"
            )
        )

        self.done_label.configure(
            text=(
                f"Done: "
                f"{app_state.completed_tasks}"
            )
        )

        self.failed_label.configure(
            text=(
                f"Failed: "
                f"{app_state.failed_tasks}"
            )
        )

        self.cpu_label.configure(
            text=(
                f"CPU: "
                f"{app_state.cpu_usage:.0f}%"
            )
        )

        self.ram_label.configure(
            text=(
                f"RAM: "
                f"{app_state.ram_usage:.0f}%"
            )
        )

        self.gpu_label.configure(
            text=(
                f"GPU: "
                f"{app_state.gpu_usage:.0f}%"
            )
        )

        self.vram_label.configure(
            text=(
                f"VRAM: "
                f"{app_state.vram_usage:.0f}%"
            )
        )

        self.speed_label.configure(
            text=(
                f"Speed: "
                f"{app_state.processing_speed:.1f} "
                f"file/min"
            )
        )

        self.avg_label.configure(
            text=(
                f"Avg: "
                f"{app_state.average_processing_time:.1f}s/file"
            )
        )