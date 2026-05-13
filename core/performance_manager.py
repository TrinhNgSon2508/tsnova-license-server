from core.app_state import (
    app_state
)


# =========================================================
# AUTO PERFORMANCE
# =========================================================

def auto_optimize_performance():

    # =====================================================
    # HIGH RAM USAGE
    # =====================================================

    if app_state.ram_usage >= 90:

        app_state.max_workers = 1

        return

    # =====================================================
    # HIGH VRAM USAGE
    # =====================================================

    if app_state.vram_usage >= 90:

        app_state.max_workers = 1

        return

    # =====================================================
    # MEDIUM LOAD
    # =====================================================

    if (
        app_state.cpu_usage >= 70 or
        app_state.ram_usage >= 70
    ):

        app_state.max_workers = 2

        return

    # =====================================================
    # LOW LOAD
    # =====================================================

    app_state.max_workers = 4