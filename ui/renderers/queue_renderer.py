import os
import time

from core.app_state import (
    app_state
)

from core.constants import (
    TASK_WAITING,
    TASK_PROCESSING,
    TASK_DONE,
    TASK_FAILED,
    TASK_CANCELLED,

    COLOR_WAITING,
    COLOR_PROCESSING,
    COLOR_DONE,
    COLOR_FAILED,
    COLOR_CANCELLED,
    COLOR_DEFAULT
)


# =========================================================
# STATUS ICON
# =========================================================

def get_status_icon(
    status
):

    if status == TASK_PROCESSING:
        return "⏳"

    if status == TASK_DONE:
        return "✅"

    if status == TASK_FAILED:
        return "❌"

    if status == TASK_CANCELLED:
        return "🛑"

    return "🕒"


# =========================================================
# STATUS COLOR
# =========================================================

def get_status_color(
    status
):

    if status == TASK_WAITING:
        return COLOR_WAITING

    if status == TASK_PROCESSING:
        return COLOR_PROCESSING

    if status == TASK_DONE:
        return COLOR_DONE

    if status == TASK_FAILED:
        return COLOR_FAILED

    if status == TASK_CANCELLED:
        return COLOR_CANCELLED

    return COLOR_DEFAULT


# =========================================================
# ETA TEXT
# =========================================================

def build_eta_text(
    image_path,
    status,
    progress
):

    if status != TASK_PROCESSING:
        return ""

    if progress <= 0:
        return ""

    start_time = app_state.task_start_time.get(
        image_path
    )

    if not start_time:
        return ""

    elapsed = (
        time.time() - start_time
    )

    estimated_total = (
        elapsed / (progress / 100)
    )

    remaining = max(
        0,
        estimated_total - elapsed
    )

    return (
        f" • ETA {remaining:.1f}s"
    )


# =========================================================
# LABEL TEXT
# =========================================================

def build_label_text(
    filename,
    status,
    eta_text=""
):

    icon = get_status_icon(
        status
    )

    return (
        f"{icon} "
        f"[{status.upper()}] "
        f"{filename}"
        f"{eta_text}"
    )


# =========================================================
# FILENAME
# =========================================================

def get_filename(
    image_path
):

    return os.path.basename(
        image_path
    )