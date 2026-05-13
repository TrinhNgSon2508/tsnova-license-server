import time
from collections import OrderedDict


class ImageCache:

    def __init__(self, max_items=300):

        self.max_items = max_items

        self.cache = OrderedDict()

    def set(self, key, value):

        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = {
            "value": value,
            "time": time.time()
        }

        self._cleanup_if_needed()

    def get(self, key):

        if key not in self.cache:
            return None

        self.cache.move_to_end(key)

        return self.cache[key]["value"]

    def remove(self, key):

        if key in self.cache:
            del self.cache[key]

    def clear(self):

        self.cache.clear()

    def cleanup_unused(self):

        now = time.time()

        remove_keys = []

        for key, data in self.cache.items():

            age = now - data["time"]

            if age > 300:
                remove_keys.append(key)

        for key in remove_keys:
            del self.cache[key]

    def _cleanup_if_needed(self):

        while len(self.cache) > self.max_items:
            self.cache.popitem(last=False)

    def get_cache_size(self):

        return len(self.cache)


image_cache = ImageCache()
