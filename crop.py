from PIL import Image

def crop_image(image, left, top, right, bottom):

    try:
        # Crop the image using the specified boundaries
        cropped_image = image.crop((left, top, right, bottom))
        return cropped_image
    except Exception as e:
        raise e
