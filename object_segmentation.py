import cv2
from PIL import Image
import numpy as np

def segment_objects(image):
    # PIL image to CV2
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Grayscale
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # Segment the object via threshold function
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # find contour of the object
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # mask
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, contours, -1, 255, thickness=cv2.FILLED)

    # apply mask in the og image
    segmented = cv2.bitwise_and(open_cv_image, open_cv_image, mask=mask)

    # Switch back to PIL
    return Image.fromarray(cv2.cvtColor(segmented, cv2.COLOR_BGR2RGB))
