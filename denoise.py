from PIL import Image, ImageFilter

def denoise_image(image, filter_strength=2):

    try:
        # Denoise the image via Gaussian Blur
        denoised_image = image.filter(ImageFilter.GaussianBlur(radius=filter_strength))
        return denoised_image
    except Exception as e:
        print(f"Lỗi khi khử nhiễu ảnh: {e}")
        raise
