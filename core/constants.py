# =========================================================
# TASK STATUS
# =========================================================

TASK_WAITING = "waiting"

TASK_PROCESSING = "processing"

TASK_DONE = "done"

TASK_FAILED = "failed"

TASK_CANCELLED = "cancelled"


# =========================================================
# UI REFRESH
# =========================================================

QUEUE_REFRESH_MS = 500

PREVIEW_REFRESH_MS = 300


# =========================================================
# UI SIZE
# =========================================================

QUEUE_ITEM_HEIGHT = 300

PREVIEW_SIZE = (300, 300)


# =========================================================
# WORKER
# =========================================================

WORKER_SLEEP_EMPTY = 0.2

WORKER_SLEEP_LIMIT = 0.1

WORKER_SLEEP_START = 0.05


# =========================================================
# COLORS
# =========================================================

COLOR_WAITING = "#E6A700"

COLOR_PROCESSING = "#3B82F6"

COLOR_DONE = "#22C55E"

COLOR_FAILED = "#EF4444"

COLOR_CANCELLED = "#6B7280"

COLOR_DEFAULT = "#888888"


# =========================================================
# EXPORT
# =========================================================

SUPPORTED_EXPORT_FORMATS = [

    "png",

    "jpg",

    "jpeg",

    "webp"
]


# =========================================================
# PRESETS
# =========================================================

DEFAULT_WORKERS = 2

DEFAULT_UPSCALE_FACTOR = 2

DEFAULT_OUTPUT_FORMAT = "png"

DEFAULT_DENOISE = 0.3