# core/file_manager.py

import os


IMAGE_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
)


def scan_images_from_drop(data_list):

    selected_files = set()

    for item in data_list:

        item = item.strip("{}")

        # Folder
        if os.path.isdir(item):

            for root, dirs, files in os.walk(item):

                for file in files:

                    if file.lower().endswith(
                        IMAGE_EXTENSIONS
                    ):

                        full_path = os.path.join(
                            root,
                            file
                        )

                        selected_files.add(full_path)

        # Single file
        elif item.lower().endswith(
            IMAGE_EXTENSIONS
        ):

            selected_files.add(item)

    return sorted(selected_files)