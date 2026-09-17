from PIL import Image
import cv2
import numpy as np


class ImageProcessor:

    @staticmethod
    def load_image(image_file):
        return Image.open(image_file).convert("RGB")

    @staticmethod
    def get_image_details(image):
        image_array = np.array(image)
        height, width, channels = image_array.shape
        return {
            "width": width,
            "height": height,
            "channels": channels
        }

    @staticmethod
    def process_with_opencv(image):
        image_array = np.array(image)
        return cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
