import threading
from PIL import Image
import customtkinter as ctk

from services.image_cache import image_cache


class PreviewService:

    def __init__(self):

        self.current_request_id = 0

        self.lock = threading.Lock()

    def request_preview(
        self,
        image_path,
        callback,
        size=(300, 300)
    ):

        if not image_path:
            return

        with self.lock:

            self.current_request_id += 1

            request_id = self.current_request_id

        cache_key = f"{image_path}_{size}"

        cached = image_cache.get(cache_key)

        if cached:

            callback(cached)

            return

        threading.Thread(
            target=self._load_preview,
            args=(
                request_id,
                image_path,
                size,
                callback,
                cache_key
            ),
            daemon=True
        ).start()

    def _load_preview(
        self,
        request_id,
        image_path,
        size,
        callback,
        cache_key
    ):

        try:

            image = Image.open(image_path)

            image.thumbnail(size)

            preview = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )

            image_cache.set(cache_key, preview)

            with self.lock:

                if request_id != self.current_request_id:
                    return

            callback(preview)

        except Exception as error:

            print(f"[PreviewService] {error}")

    def clear_cache(self):

        image_cache.clear()

    def cleanup(self):

        image_cache.cleanup_unused()


preview_service = PreviewService()
