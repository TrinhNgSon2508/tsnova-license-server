import queue


class AppState:

    def __init__(self):

        self.tasks = []

        self.task_status = {}

        self.image_paths = []

        self.selected_images = set()

        self.selected_image = None

        self.is_processing = False

        self.queue_paused = False

        self.queue = []

        self.processing_queue = queue.Queue()

        self.active_workers = 0

        self.max_workers = 4

        self.current_preview = None

        self.preview_cache = {}

        self.stats = {
            "total": 0,
            "waiting": 0,
            "processing": 0,
            "completed": 0,
            "failed": 0
        }

        self.monitor_data = {}

        self.memory_usage = 0

        self.cpu_usage = 0

        self.cache_size = 0

        self.settings = {}

        self.shutdown_requested = False

        self.cancel_requested = set()


app_state = AppState()
