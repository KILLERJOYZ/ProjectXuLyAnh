import tkinter as tk
from tkinter import Label

def show_splash_screen(root):
    """
    Display the splash screen for a few seconds before the main app starts.
    """
    # Create the splash screen as a Toplevel window
    splash = tk.Toplevel()
    splash.title("Welcome")
    splash.geometry("400x300")  # Set size of splash screen
    splash.resizable(False, False)  # Disable resizing

    # Center the splash screen on the screen
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x_cord = int((screen_width / 2) - (400 / 2))
    y_cord = int((screen_height / 2) - (300 / 2))
    splash.geometry(f"+{x_cord}+{y_cord}")

    # Add a label or image to the splash screen
    Label(splash, text="ỨNG DỤNG XỬ LÍ ẢNH", font=("Segoe UI", 22), pady=50).pack()
    Label(splash, text="Phiên bản V0.1 Beta", font=("Segoe UI", 14), pady=50).pack()
    Label(splash, text="Đang khởi chạy", font=("Segoe UI", 12), pady=20).pack()

    # Show the splash screen for 2 seconds and then destroy it
    splash.after(2000, splash.destroy)  # 2000 milliseconds = 2 seconds

    # Block further execution until the splash is closed
    splash.grab_set()  # This ensures that no other interaction can happen with other windows
    splash.mainloop()  # This blocks the execution until the splash is destroyed

    # Once the splash screen is closed, show the main window
    root.deiconify()  # This will make the main window visible after splash screen closes


def main_app():
    # Create the main application window
    root = tk.Tk()
    root.title("Ứng dụng Xử Lý Ảnh")

    # Set window size
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # Hide the main window initially
    root.withdraw()  # Hide the main window so only the splash screen is shown

    # Show splash screen
    show_splash_screen(root)

    # Main app content
    Label(root, text="Main Application Window", font=("Segoe UI", 24), pady=50).pack()

    # Run the main application
    root.mainloop()


if __name__ == "__main__":
    main_app()
