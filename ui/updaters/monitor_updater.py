from core.app_state import (
    app_state
)


# =========================================================
# UPDATE MONITOR LABELS
# =========================================================

def update_monitor_labels(
    panel
):

    # =====================================================
    # WORKERS
    # =====================================================

    panel.worker_label.configure(

        text=(
            f"Workers: "
            f"{app_state.active_workers}"
        )
    )

    # =====================================================
    # QUEUE
    # =====================================================

    panel.queue_label.configure(

        text=(
            f"Queue: "
            f"{len(app_state.processing_queue)}"
        )
    )

    # =====================================================
    # DONE
    # =====================================================

    panel.done_label.configure(

        text=(
            f"Done: "
            f"{app_state.completed_tasks}"
        )
    )

    # =====================================================
    # FAILED
    # =====================================================

    panel.failed_label.configure(

        text=(
            f"Failed: "
            f"{app_state.failed_tasks}"
        )
    )

    # =====================================================
    # CPU
    # =====================================================

    panel.cpu_label.configure(

        text=(
            f"CPU: "
            f"{app_state.cpu_usage:.0f}%"
        )
    )

    # =====================================================
    # RAM
    # =====================================================

    panel.ram_label.configure(

        text=(
            f"RAM: "
            f"{app_state.ram_usage:.0f}%"
        )
    )

    # =====================================================
    # GPU
    # =====================================================

    panel.gpu_label.configure(

        text=(
            f"GPU: "
            f"{app_state.gpu_usage:.0f}%"
        )
    )

    # =====================================================
    # VRAM
    # =====================================================

    panel.vram_label.configure(

        text=(
            f"VRAM: "
            f"{app_state.vram_usage:.0f}%"
        )
    )

    # =====================================================
    # SPEED
    # =====================================================

    panel.speed_label.configure(

        text=(
            f"Speed: "
            f"{app_state.processing_speed:.1f} "
            f"file/min"
        )
    )

    # =====================================================
    # AVG
    # =====================================================

    panel.avg_label.configure(

        text=(
            f"Avg: "
            f"{app_state.average_processing_time:.1f}s/file"
        )
    )