# grayscale.py

from PIL import Image, ImageEnhance

def convert_to_grayscale(image):
    """
    Convert an image to grayscale.
    """
    try:
        # Convert image to grayscale (L mode)
        grayscale_image = image.convert("L")
        return grayscale_image
    except Exception as e:
        raise e

def adjust_grayscale(image, intensity_percentage):
    """
    Adjust the grayscale intensity based on a given percentage.
    0% = completely black, 100% = original grayscale.
    """
    try:
        # Convert image to grayscale first
        grayscale_image = convert_to_grayscale(image)

        # Use ImageEnhance to adjust brightness
        enhancer = ImageEnhance.Brightness(grayscale_image)

        # Convert the intensity percentage to a factor (0 to 1)
        intensity_factor = intensity_percentage / 100.0

        # Enhance the image based on intensity factor
        adjusted_image = enhancer.enhance(intensity_factor)

        return adjusted_image
    except Exception as e:
        raise e
