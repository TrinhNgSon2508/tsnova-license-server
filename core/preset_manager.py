PRESETS = {

    "Anime Upscale": {

        "workers": 2,
        "upscale_factor": 4,
        "output_format": "png",
        "model": "realesrgan-anime",
        "denoise": 0.3
    },

    "Photo Restore": {

        "workers": 1,
        "upscale_factor": 2,
        "output_format": "png",
        "model": "gfpgan",
        "denoise": 0.6
    },

    "4K Batch": {

        "workers": 4,
        "upscale_factor": 4,
        "output_format": "jpg",
        "model": "realesrgan-x4",
        "denoise": 0.2
    }
}