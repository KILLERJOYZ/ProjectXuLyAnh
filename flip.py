from PIL import Image, ImageTk
from tkinter import messagebox

def flip_image(current_image, direction):

    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để lật!")
        return None

    try:
        if direction == "horizontal":
            flipped_image = current_image.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == "vertical":
            flipped_image = current_image.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            messagebox.showerror("Error", "Chiều lật không hợp lệ!")
            return None

        return flipped_image
    except Exception as e:
        messagebox.showerror("Error", f"Không thể lật ảnh: {e}")
        return None

