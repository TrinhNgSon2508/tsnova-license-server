# core/system_monitor.py

import time
import threading

import psutil

from core.app_state import (
    app_state
)


class SystemMonitor:

    def __init__(self):

        # =================================================
        # STATE
        # =================================================

        self.running = False

        self.thread = None

        # =================================================
        # METRICS
        # =================================================

        self.cpu_usage = 0

        self.ram_usage = 0

        self.ram_used_gb = 0

        self.ram_total_gb = 0

        self.gpu_usage = 0

        self.vram_usage = 0

        self.active_workers = 0

        self.queue_size = 0

        self.completed_tasks = 0

        self.failed_tasks = 0

        self.tasks_per_minute = 0

        self.eta_seconds = 0

        # =================================================
        # INTERNAL
        # =================================================

        self.last_completed = 0

        self.last_time = time.time()

    # =====================================================
    # START
    # =====================================================

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(

            target=self.monitor_loop,

            daemon=True
        )

        self.thread.start()

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        self.running = False

    # =====================================================
    # LOOP
    # =====================================================

    def monitor_loop(self):

        while self.running:

            try:

                self.update_metrics()

            except Exception as error:

                print(
                    f"Monitor Error: {error}"
                )

            time.sleep(1)

    # =====================================================
    # UPDATE METRICS
    # =====================================================

    def update_metrics(self):

        # =================================================
        # CPU
        # =================================================

        self.cpu_usage = psutil.cpu_percent()

        # =================================================
        # RAM
        # =================================================

        ram = psutil.virtual_memory()

        self.ram_usage = ram.percent

        self.ram_used_gb = round(

            ram.used / (1024 ** 3),

            2
        )

        self.ram_total_gb = round(

            ram.total / (1024 ** 3),

            2
        )

        # =================================================
        # GPU PLACEHOLDER
        # =================================================

        self.gpu_usage = 0

        self.vram_usage = 0

        # =================================================
        # TASK STATS
        # =================================================

        self.active_workers = (
            app_state.active_workers
        )

        self.queue_size = (
            app_state.processing_queue.qsize()
        )

        # =================================================
        # TASK COUNTS
        # =================================================

        completed = 0

        failed = 0

        for status in app_state.task_status.values():

            if status == "completed":

                completed += 1

            elif status == "failed":

                failed += 1

        self.completed_tasks = completed

        self.failed_tasks = failed

        # =================================================
        # THROUGHPUT
        # =================================================

        now = time.time()

        elapsed = now - self.last_time

        if elapsed >= 60:

            delta = (
                completed -
                self.last_completed
            )

            self.tasks_per_minute = delta

            self.last_completed = completed

            self.last_time = now

        # =================================================
        # ETA
        # =================================================

        if self.tasks_per_minute > 0:

            self.eta_seconds = int(

                (
                    self.queue_size /

                    self.tasks_per_minute
                ) * 60
            )

        else:

            self.eta_seconds = 0

    # =====================================================
    # ETA STRING
    # =====================================================

    def get_eta_string(self):

        seconds = self.eta_seconds

        hours = seconds // 3600

        minutes = (
            seconds % 3600
        ) // 60

        secs = seconds % 60

        if hours > 0:

            return (
                f"{hours}h "
                f"{minutes}m "
                f"{secs}s"
            )

        if minutes > 0:

            return (
                f"{minutes}m "
                f"{secs}s"
            )

        return f"{secs}s"

    # =====================================================
    # EXPORT
    # =====================================================

    def export_metrics(self):

        return {

            "cpu_usage": self.cpu_usage,

            "ram_usage": self.ram_usage,

            "ram_used_gb": self.ram_used_gb,

            "ram_total_gb": self.ram_total_gb,

            "gpu_usage": self.gpu_usage,

            "vram_usage": self.vram_usage,

            "active_workers": self.active_workers,

            "queue_size": self.queue_size,

            "completed_tasks": self.completed_tasks,

            "failed_tasks": self.failed_tasks,

            "tasks_per_minute": self.tasks_per_minute,

            "eta_seconds": self.eta_seconds,

            "eta_string": self.get_eta_string()
        }


# =========================================================
# GLOBAL INSTANCE
# =========================================================

system_monitor = SystemMonitor()