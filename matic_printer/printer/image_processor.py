import multiprocessing
from PIL import Image
import numpy as np
import io
import config

def process_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    processed_image = image.resize(config.DISPLAY_RESOLUTION, Image.LANCZOS)
    return np.array(processed_image)

class ImageProcessor:
    def __init__(self, num_processes=None):
        self.pool = multiprocessing.Pool(processes=num_processes)

    def process_images(self, image_data_list):
        return self.pool.map(process_image, image_data_list)

    def close(self):
        self.pool.close()
        self.pool.join()