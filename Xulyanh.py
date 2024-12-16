import tkinter as tk
from tkinter import Menu, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import grayscale  # Import module grayscale
import superres  #import module superres
import Rotate #import module rotate
import dynamicrange #import module hdr
from applysegmentation import adaptive_segmentation  #import module segmentation
from crop import crop_image
from splashscreen import show_splash_screen
from flip import flip_image
from sharpen import sharpen_image
from denoise import denoise_image
from object_segmentation import segment_objects
from autoedit import (auto_edit_image)  # Import custom auto-edit module


r = tk.Tk()
r.title('Ứng dụng xử lí ảnh')

# Set window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
r.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# Global variable to hold the current image
current_image = None


# Greeting
greeting_label = tk.Label(r, text="Chào mừng bạn đến với ứng dụng xử lý ảnh!", font=("Arial", 14))
greeting_label.pack(pady=20)

def apply_object_segmentation():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để tách vật thể!")
        return

    try:
        # Call the segmentation function
        segmented_image = segment_objects(current_image)

        # Show the segmented image
        tk_img = ImageTk.PhotoImage(segmented_image)
        img_label.config(image=tk_img)
        img_label.image = tk_img

        # Update the segmented image back to current image to display
        current_image = segmented_image
    except Exception as e:
        messagebox.showerror("Error", f"Không thể tách vật thể: {e}")

def apply_auto_edit():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để chỉnh sửa tự động!")
        return

    try:
        # Define actions for auto-editing
        actions = [
            {'type': 'rotate', 'angle': 45},
            {'type': 'crop', 'box': (50, 50, current_image.width - 50, current_image.height - 50)},
            {'type': 'flip', 'direction': 'horizontal'}  # Lật ngang
        ]

        # Apply auto-editing
        edited_image = auto_edit_image(current_image, actions)

        # Display the edited image
        tk_img = ImageTk.PhotoImage(edited_image)
        img_label.config(image=tk_img)
        img_label.image = tk_img  # Keep reference to prevent garbage collection

        # Update the current image
        current_image = edited_image
    except Exception as e:
        messagebox.showerror("Error", f"Không thể chỉnh sửa tự động: {e}")

def apply_denoise():
    global current_image

    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để khử nhiễu!")
        return

    # Create a popup window for denoising
    denoise_window = tk.Toplevel(r)
    denoise_window.title("Khử nhiễu ảnh")
    denoise_window.geometry("500x400")  # Đảm bảo cửa sổ đủ lớn để chứa cả ảnh và nút

    # Label
    label = tk.Label(denoise_window, text="Chọn mức độ khử nhiễu:", font=("Arial", 12))
    label.pack(pady=10)

    # Create a slider for applying denoising.
    slider = tk.Scale(
        denoise_window,
        from_=1,
        to=10,
        orient=tk.HORIZONTAL,
        label="Mức độ (1-10)",
        length=300
    )
    slider.pack(pady=10)

    # Preview image
    img_preview_label = tk.Label(denoise_window)
    img_preview_label.pack(pady=10, side=tk.TOP)

    # Function to update the preview after sliding.
    def update_preview():
        global current_image
        try:
            filter_strength = slider.get()
            # Denoise the image via slider
            denoised_image = denoise_image(current_image, filter_strength)

            # Display the denoised image in denoise window
            tk_img = ImageTk.PhotoImage(denoised_image)
            img_preview_label.config(image=tk_img)
            img_preview_label.image = tk_img  # Maintain the old img to compare and contrast.
        except Exception as e:
            messagebox.showerror("Error", f"Không thể khử nhiễu ảnh: {e}")

    # Callback the function of denoising
    slider.bind("<Motion>", lambda event: update_preview())

    # Confirmation and application of denosing in the image
    def confirm_and_apply():
        global current_image
        try:
            filter_strength = slider.get()
            # Denoise the final img
            denoised_image = denoise_image(current_image, filter_strength)

            # Display the denoised img in the GUI
            tk_img = ImageTk.PhotoImage(denoised_image)
            img_label.config(image=tk_img)
            img_label.image = tk_img

            # Update the current image to denoised one
            current_image = denoised_image

            # Close the denoise window
            denoise_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Không thể khử nhiễu ảnh: {e}")

    # Confirm button
    confirm_button = tk.Button(
        denoise_window, text="Xác nhận", command=confirm_and_apply, font=("Arial", 12), bg="lightgreen"
    )
    confirm_button.pack(pady=20, side=tk.BOTTOM)

    # Loop
    denoise_window.mainloop()


def apply_sharpen():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để làm nét!")
        return

    try:
        # Sharpness collection
        sharpness_level = simpledialog.askfloat("Làm nét ảnh", "Nhập mức độ làm nét (1.0 đến 5.0):", minvalue=1.0, maxvalue=5.0)

        if sharpness_level is not None:
            # Sharpen image
            sharpened_image = sharpen_image(current_image, sharpness_level)

            # Display the sharpened one.
            tk_img = ImageTk.PhotoImage(sharpened_image)
            img_label.config(image=tk_img)
            img_label.image = tk_img  # Maintain the old one for comparison and contrast.

            # Update to current image
            current_image = sharpened_image
    except Exception as e:
        messagebox.showerror("Error", f"Không thể làm nét ảnh: {e}")



def apply_segmentation():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "No image available to process!")
        return

    try:
        # Prompt the user to input block_size and C parameters
        block_size = simpledialog.askinteger("Phân đoạn", "Gõ block size, lớn hơn 1:", minvalue=3)
        C = simpledialog.askinteger("Phân đoạn", "Nhập hằng số trừ (giá trị C):", minvalue=0)

        if block_size is not None and C is not None:
            # Ensure block_size is an odd number
            if block_size % 2 == 0:
                messagebox.showerror("Error", "Giá trị phải là số lẻ")
                return

            # Call the adaptive_segmentation function
            segmented_image = adaptive_segmentation(current_image, block_size, C)

            # Display the segmented image
            tk_img = ImageTk.PhotoImage(segmented_image)
            img_label.config(image=tk_img)
            img_label.image = tk_img  # Keep a reference to prevent garbage collection
            img_label.pack(expand=True)
    except Exception as e:
        messagebox.showerror("Error", f"Không thể phân tách hình ảnh này: {e}")

def crop_image_with_gui():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "No image available to crop!")
        return

    # Open a new window for cropping
    crop_window = tk.Toplevel(r)
    crop_window.title("Crop Image")

    # Create a Canvas to display the image
    canvas = tk.Canvas(crop_window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    canvas.pack()

    # Convert the PIL image to PhotoImage for tkinter
    tk_img = ImageTk.PhotoImage(current_image)
    canvas_image = canvas.create_image(0, 0, anchor="nw", image=tk_img)

    # Variables to store the rectangle coordinates
    rect_id = None
    start_x, start_y = None, None
    end_x, end_y = None, None

    def on_mouse_press(event):
        nonlocal start_x, start_y, rect_id
        # Record the starting point
        start_x, start_y = event.x, event.y
        # Create a rectangle
        rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def on_mouse_drag(event):
        nonlocal rect_id
        # Update the rectangle as the mouse is dragged
        canvas.coords(rect_id, start_x, start_y, event.x, event.y)

    def on_mouse_release(event):
        nonlocal end_x, end_y
        # Record the ending point
        end_x, end_y = event.x, event.y

    def crop_and_close():
        global current_image
        nonlocal start_x, start_y, end_x, end_y

        if None in (start_x, start_y, end_x, end_y):
            messagebox.showerror("Error", "No crop region selected!")
            return

        # Ensure coordinates are valid and in the correct order
        left, right = sorted([start_x, end_x])
        top, bottom = sorted([start_y, end_y])

        left = max(0, left)
        right = min(current_image.width, right)
        top = max(0, top)
        bottom = min(current_image.height, bottom)

        if left >= right or top >= bottom:
            messagebox.showerror("Error", "Invalid crop region!")
            return

        # Crop the image
        cropped_image = current_image.crop((left, top, right, bottom))

        # Display the cropped image in the main app
        tk_img_cropped = ImageTk.PhotoImage(cropped_image)
        img_label.config(image=tk_img_cropped)
        img_label.image = tk_img_cropped
        img_label.pack(expand=True)

        # Update the global current image

        current_image = cropped_image

        # Close the crop window
        crop_window.destroy()

    # Bind mouse events
    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    # Add a button to confirm cropping
    confirm_button = tk.Button(crop_window, text="Crop", command=crop_and_close)
    confirm_button.pack(pady=10)

    # Run the crop window
    crop_window.mainloop()

# Function to import and display an image
def import_image():
    global current_image, greeting_label, add_image_button
    # Open file dialog to select an image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")],
        title="Chọn một hình ảnh"
    )

    if file_path:
        try:
            # Load the image using PIL
            img = Image.open(file_path)

            # Get image dimensions
            img_width, img_height = img.size

            # Calculate scaling factor to fit image into the window
            scale_factor = min(WINDOW_WIDTH / img_width, WINDOW_HEIGHT / img_height)

            # Calculate new dimensions while maintaining the aspect ratio
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)

            # Resize the image while maintaining aspect ratio
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img_resized)

            # Save the resized image in the global variable
            current_image = img_resized

            # Display the image in the app
            img_label.config(image=tk_img)
            img_label.image = tk_img  # Keep a reference to prevent garbage collection
            img_label.pack(expand=True)

            # Remove greeting label if it exists
            if greeting_label:
                greeting_label.pack_forget()
                greeting_label = None

            # Change the "Thêm ảnh" button to "Thay thế ảnh"
            add_image_button.config(text="Thay thế ảnh")

        except Exception as e:
            messagebox.showerror("Error", f"Không thể tải hình ảnh: {e}")

def upscale_image():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để xử lý!")
        return

    try:
        # Call the upscale_image function from the superres module
        factor = simpledialog.askfloat("Siêu phân giải", "Bạn muốn bức ảnh phóng to như thế nào:")

        if factor is not None:
            upscaled_image = superres.upscale_image(current_image, factor)
            # Display the upscaled image
            tk_img = ImageTk.PhotoImage(upscaled_image)
            img_label.config(image=tk_img)
            img_label.image = tk_img  # Keep a reference to prevent garbage collection
            img_label.pack(expand=True)
    except Exception as e:
        messagebox.showerror("Error", f"Không thể nâng cấp hình ảnh: {e}")


# Function to rotate the image
def rotate_image_ui():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để xoay!")
        return

    try:
        # Ask the user for the rotation angle
        angle = simpledialog.askinteger("Xoay ảnh", "Nhập góc xoay (độ):")

        if angle is not None:
            # Rotate the image using the rotate module's function
            rotated_image = Rotate.rotate_image(current_image, angle)

            # Display the rotated image
            tk_img = ImageTk.PhotoImage(rotated_image)
            img_label.config(image=tk_img)
            img_label.image = tk_img  # Keep a reference to prevent garbage collection
    except Exception as e:
        messagebox.showerror("Error", f"Không thể xoay hình ảnh: {e}")


# Function to adjust grayscale intensity based on percentage
def adjust_grayscale():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để chuyển đổi!")
        return

    # Prompt user for intensity percentage
    intensity_percentage = simpledialog.askinteger("Điều chỉnh mức độ đen trắng", "Bạn muốn bức ảnh trắng đen như thế nào:", minvalue=0,
                                                   maxvalue=100)

    if intensity_percentage is not None:
        # Call the adjust_grayscale function from the grayscale module
        adjusted_image = grayscale.adjust_grayscale(current_image, intensity_percentage)

        # Display the adjusted grayscale image
        tk_img = ImageTk.PhotoImage(adjusted_image)
        img_label.config(image=tk_img)
        img_label.image = tk_img  # Keep a reference to prevent garbage collection
        img_label.pack(expand=True)


# Function to export the current image
def export_image():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để xuất!")
        return

    # Open file dialog to save the image
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg"), ("Bitmap Files", "*.bmp")],
        title="Lưu hình ảnh"
    )

    if file_path:
        try:
            # Save the image to the selected path
            current_image.save(file_path)
            messagebox.showinfo("Success", "Hình ảnh đã được lưu thành công!")
        except Exception as e:
            messagebox.showerror("Error", f"Không thể lưu hình ảnh: {e}")

def apply_hdr():
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "Không có hình ảnh nào để xử lý")
        return

    try:
        strength = simpledialog.askinteger("HDR", "Nhập độ mạnh HDR từ 0 đến 5:", minvalue=0, maxvalue=5)
        if strength is not None:
            hdr_image = dynamicrange.enhance_hdr(current_image, strength)

    # Display the HDR-enhanced image
            tk_img = ImageTk.PhotoImage(hdr_image)
            img_label.config(image=tk_img)
            img_label.image = tk_img  # Keep a reference to prevent garbage collection

    except Exception as e:
        messagebox.showerror("Error", f"Không thể áp dụng HDR: {e}")
# Add img button
add_image_button = tk.Button(r, text="Thêm ảnh", command=import_image, font=("Arial", 12), bg="lightblue")
add_image_button.pack(pady=10)

def flip_image_ui(direction):

    global current_image
    flipped_image = flip_image(current_image, direction)
    if flipped_image:
        # Display the flipped image
        tk_img = ImageTk.PhotoImage(flipped_image)
        img_label.config(image=tk_img)
        img_label.image = tk_img  # Saved the old one to compare and contrast
        current_image = flipped_image  # Update back to the old one.



# Menu configuration
menu = Menu(r)
r.config(menu=menu)

# File menu
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Tệp tin', menu=filemenu)
filemenu.add_command(label='Nhập ảnh', command=import_image)
filemenu.add_command(label='Xuất hình ảnh', command=export_image)
filemenu.add_separator()
filemenu.add_command(label='Thoát', command=r.quit)

# Tools Menu
filetoolbox = Menu(menu, tearoff=0)
menu.add_cascade(label='Công cụ', menu=filetoolbox)
filetoolbox.add_command(label='Đen trắng', command=adjust_grayscale)
filetoolbox.add_command(label='Siêu phân giải', command=upscale_image)
filetoolbox.add_command(label='Xoay ảnh', command=rotate_image_ui)
filetoolbox.add_command(label='tăng cường HDR', command=apply_hdr)
filetoolbox.add_command(label='Làm nét ảnh', command=apply_sharpen)
filetoolbox.add_command(label='Khử nhiễu ảnh', command=apply_denoise)



#segmentation menu
filesegmentation = Menu(menu, tearoff=0)
menu.add_cascade(label='Công cụ phân tách', menu=filesegmentation)
filesegmentation.add_command(label='Phân tích', command=apply_segmentation)
filesegmentation.add_command(label='Tách vật thể', command=apply_object_segmentation)


#image menu
imageedit = Menu(menu, tearoff=0)
menu.add_cascade(label = 'Công cụ chỉnh sửa hình ảnh', menu = imageedit)
imageedit.add_command(label='Chỉnh sửa ma thuật', command=apply_auto_edit)
imageedit.add_command(label = 'Cắt', command = crop_image_with_gui)
imageflip = Menu(menu, tearoff=0)
imageedit.add_cascade(label = 'lật ảnh', menu = imageflip)
imageflip.add_command(label='Lật ngang', command=lambda: flip_image_ui("horizontal"))
imageflip.add_command(label='Lật dọc', command=lambda: flip_image_ui("vertical"))

# About Menu
filehelp = Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=filehelp)
filehelp.add_command(label='Help')


# Add About menu item with a callback
def show_about():
    messagebox.showinfo("About", "Ứng dụng xử lí ảnh Beta\nVersion 0.1")


filehelp.add_command(label='About', command=show_about)

# Label to display images
img_label = tk.Label(r)
img_label.pack()

if __name__ == "__main__":
    # Create the main app window
    r.title('Ứng dụng xử lí ảnh')

    # Set window size
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    r.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # Show splash screen
    show_splash_screen(r)

    # Add main application logic here (menu, buttons, etc.)
    tk.Label(r, text="Main Application", font=("Arial", 24), pady=50).pack()

    # Run the main loop
    r.mainloop()


