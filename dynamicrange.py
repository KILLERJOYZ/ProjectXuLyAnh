from PIL import Image, ImageEnhance, ImageFilter

def enhance_hdr(image, strength=2.0):


    try:
        # Convert to RGB (if not already in that mode)
        image = image.convert("RGB")

        # Apply enhancement to simulate HDR effect
        enhancer = ImageEnhance.Contrast(image)
        enhanced_image = enhancer.enhance(strength)  # Increase contrast for HDR look

        # Optionally apply some sharpening to simulate HDR clarity
        enhanced_image = enhanced_image.filter(ImageFilter.SHARPEN)

        return enhanced_image
    except Exception as e:
        raise e
