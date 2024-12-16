#superres.py

from PIL import Image, ImageEnhance, ImageFilter

def upscale_image(image, factor):
    global current_image
    current_image = image
    try:
        # Upscale the image
        width, height = image.size
        new_width = int(width * factor)
        new_height = int(height * factor)

        # Resize the image
        upscale_image = image.resize((new_width, new_height), Image.LANCZOS)

        # Apply sharpening filter
        upscale_image = upscale_image.filter(ImageFilter.SHARPEN)

        return upscale_image
    except Exception as e:
        raise e