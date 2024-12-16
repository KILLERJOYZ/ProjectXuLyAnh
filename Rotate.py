from PIL import Image

def rotate_image(image, angle):
    """
    Rotate the image by the specified angle.
    """
    try:
        # Rotate the image by the specified angle
        rotated_image = image.rotate(angle, expand=True)  # expand=True ensures the whole image fits in the frame
        return rotated_image
    except Exception as e:
        raise e