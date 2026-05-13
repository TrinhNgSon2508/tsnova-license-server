from core.constants import (
    TASK_WAITING,
    TASK_PROCESSING,
    TASK_DONE,
    TASK_FAILED,
    TASK_CANCELLED
)


# =========================================================
# TASK CHECKS
# =========================================================

def is_task_waiting(
    status
):

    return status == TASK_WAITING


def is_task_processing(
    status
):

    return status == TASK_PROCESSING


def is_task_done(
    status
):

    return status == TASK_DONE


def is_task_failed(
    status
):

    return status == TASK_FAILED


def is_task_cancelled(
    status
):

    return status == TASK_CANCELLED


# =========================================================
# TASK FINAL
# =========================================================

def is_task_finished(
    status
):

    return status in [

        TASK_DONE,

        TASK_FAILED,

        TASK_CANCELLED
    ]