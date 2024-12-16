from PIL import Image

def auto_edit_image(image, actions):

    try:
        # Automatic actions in toolbox. Under development.
        for action in actions:
            if action['type'] == 'rotate':
                angle = action.get('angle', 0)
                image = image.rotate(angle, expand=True)
            elif action['type'] == 'crop':
                crop_box = action.get('box', (0, 0, image.width, image.height))
                image = image.crop(crop_box)
            elif action['type'] == 'flip':
                direction = action.get('direction', 'horizontal')
                if direction == 'horizontal':
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                elif direction == 'vertical':
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)

        return image
    except Exception as e:
        print(f"Lỗi khi chỉnh sửa ảnh: {e}")
        return None
