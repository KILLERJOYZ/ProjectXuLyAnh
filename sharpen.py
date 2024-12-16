from PIL import Image, ImageEnhance, ImageFilter


def sharpen_image(image, sharpness_level=2.0):

    try:
        #Sharpening filter
        sharpened_image = image.filter(ImageFilter.SHARPEN)

        # Enhance the sharpness via Sharpness function in PIL
        enhancer = ImageEnhance.Sharpness(sharpened_image)
        sharpened_image = enhancer.enhance(sharpness_level)

        return sharpened_image
    except Exception as e:
        print(f"Lỗi khi làm nét ảnh: {e}")
        raise
