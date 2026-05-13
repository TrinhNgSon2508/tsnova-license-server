# ui/performance_panel.py

import customtkinter as ctk

from core.system_monitor import (
    system_monitor
)


class PerformancePanel(ctk.CTkFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(parent)

        # =================================================
        # START MONITOR
        # =================================================

        system_monitor.start()

        # =================================================
        # UI
        # =================================================

        self.build_ui()

        # =================================================
        # LOOP
        # =================================================

        self.update_loop()

    # =====================================================
    # BUILD UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # TITLE
        # =================================================

        title = ctk.CTkLabel(

            self,

            text="Performance",

            font=("Arial", 20, "bold")
        )

        title.pack(
            pady=(10, 15)
        )

        # =================================================
        # METRICS FRAME
        # =================================================

        self.metrics_frame = (
            ctk.CTkFrame(self)
        )

        self.metrics_frame.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=(0, 10)
        )

        # =================================================
        # LABELS
        # =================================================

        self.cpu_label = self.create_metric(
            "CPU"
        )

        self.ram_label = self.create_metric(
            "RAM"
        )

        self.gpu_label = self.create_metric(
            "GPU"
        )

        self.vram_label = self.create_metric(
            "VRAM"
        )

        self.worker_label = self.create_metric(
            "Workers"
        )

        self.queue_label = self.create_metric(
            "Queue"
        )

        self.completed_label = (
            self.create_metric(
                "Completed"
            )
        )

        self.failed_label = self.create_metric(
            "Failed"
        )

        self.throughput_label = (
            self.create_metric(
                "Tasks/Min"
            )
        )

        self.eta_label = self.create_metric(
            "ETA"
        )

    # =====================================================
    # CREATE METRIC
    # =====================================================

    def create_metric(
        self,
        name
    ):

        row = ctk.CTkFrame(
            self.metrics_frame
        )

        row.pack(

            fill="x",

            padx=10,

            pady=5
        )

        name_label = ctk.CTkLabel(

            row,

            text=name,

            width=120,

            anchor="w"
        )

        name_label.pack(
            side="left"
        )

        value_label = ctk.CTkLabel(

            row,

            text="-",

            anchor="e"
        )

        value_label.pack(
            side="right"
        )

        return value_label

    # =====================================================
    # UPDATE LOOP
    # =====================================================

    def update_loop(self):

        try:

            metrics = (
                system_monitor.export_metrics()
            )

            # =============================================
            # CPU
            # =============================================

            self.cpu_label.configure(

                text=f"{metrics['cpu_usage']}%"
            )

            # =============================================
            # RAM
            # =============================================

            self.ram_label.configure(

                text=(
                    f"{metrics['ram_usage']}% "
                    f"({metrics['ram_used_gb']}GB/"
                    f"{metrics['ram_total_gb']}GB)"
                )
            )

            # =============================================
            # GPU
            # =============================================

            self.gpu_label.configure(

                text=f"{metrics['gpu_usage']}%"
            )

            # =============================================
            # VRAM
            # =============================================

            self.vram_label.configure(

                text=f"{metrics['vram_usage']}%"
            )

            # =============================================
            # WORKERS
            # =============================================

            self.worker_label.configure(

                text=str(
                    metrics['active_workers']
                )
            )

            # =============================================
            # QUEUE
            # =============================================

            self.queue_label.configure(

                text=str(
                    metrics['queue_size']
                )
            )

            # =============================================
            # COMPLETED
            # =============================================

            self.completed_label.configure(

                text=str(
                    metrics['completed_tasks']
                )
            )

            # =============================================
            # FAILED
            # =============================================

            self.failed_label.configure(

                text=str(
                    metrics['failed_tasks']
                )
            )

            # =============================================
            # THROUGHPUT
            # =============================================

            self.throughput_label.configure(

                text=str(
                    metrics['tasks_per_minute']
                )
            )

            # =============================================
            # ETA
            # =============================================

            self.eta_label.configure(

                text=metrics['eta_string']
            )

        except Exception as error:

            print(
                f"Performance UI Error: {error}"
            )

        self.after(
            1000,
            self.update_loop
        )