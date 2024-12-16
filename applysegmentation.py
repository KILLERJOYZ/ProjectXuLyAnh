import cv2
import numpy as np
from PIL import Image

def adaptive_segmentation(image, block_size=11, C=2):

    try:
        # Convert the image to grayscale
        gray = np.array(image.convert("L"))

        # Apply adaptive thresholding
        segmented = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)

        # Convert the segmented image back to a PIL Image
        return Image.fromarray(segmented)
    except Exception as e:
        raise e
