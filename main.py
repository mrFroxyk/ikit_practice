import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from backend import *


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.image = None
        self.original_image = None

        # Получаем размеры окна
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Создаем фрейм для панели справа
        self.side_panel = tk.Frame(root, width=int(screen_width * 0.3), height=screen_height)
        self.side_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.side_panel.pack_propagate(False)

        # Создаем холст для изображения, занимающий 70% ширины
        self.canvas = tk.Canvas(root, width=int(screen_width * 0.7), height=screen_height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        button_font = ('Arial', 14)

        # Размещение кнопок и элементов управления на панели справа
        self.btn_load = tk.Button(self.side_panel, text="Load Image", command=self.load_image, font=button_font)
        self.btn_load.pack(fill=tk.X, padx=10, pady=5)

        self.btn_capture = tk.Button(self.side_panel, text="Capture from Webcam", command=self.capture_image, font=button_font)
        self.btn_capture.pack(fill=tk.X, padx=10, pady=5)

        self.line_thickness_label = tk.Label(self.side_panel, text="Enter x1 y1 x2 y2 coords:", font=button_font)
        self.line_thickness_label.pack(fill=tk.X, padx=10, pady=5)

        self.line_x1_entry = tk.Entry(self.side_panel, font=button_font)
        self.line_x1_entry.pack(fill=tk.X, padx=10, pady=5)

        self.line_y1_entry = tk.Entry(self.side_panel, font=button_font)
        self.line_y1_entry.pack(fill=tk.X, padx=10, pady=5)

        self.line_x2_entry = tk.Entry(self.side_panel, font=button_font)
        self.line_x2_entry.pack(fill=tk.X, padx=10, pady=5)

        self.line_y2_entry = tk.Entry(self.side_panel, font=button_font)
        self.line_y2_entry.pack(fill=tk.X, padx=10, pady=5)

        self.line_thickness_label = tk.Label(self.side_panel, text="Line Thickness (in pixel):", font=button_font)
        self.line_thickness_label.pack(fill=tk.X, padx=10, pady=5)
        self.line_thickness_entry = tk.Entry(self.side_panel, font=button_font)
        self.line_thickness_entry.pack(fill=tk.X, padx=10, pady=5)

        self.btn_draw_line = tk.Button(self.side_panel, text="Draw Line", command=self.draw_line, font=button_font)
        self.btn_draw_line.pack(fill=tk.X, padx=10, pady=5)

        self.blur_button = tk.Button(self.side_panel, text="Open Blur Setting", command=self.open_blur_form, font=button_font)
        self.blur_button.pack(fill=tk.X, padx=10, pady=5)

        self.btn_gray = tk.Button(self.side_panel, text="Convert to Gray", command=self.convert_to_gray, font=button_font)
        self.btn_gray.pack(fill=tk.X, padx=10, pady=5)

        self.red_button = tk.Button(self.side_panel, text="Red Channel", command=lambda: self.update_image("red"), font=button_font)
        self.red_button.pack(fill=tk.X, padx=10, pady=5)

        self.green_button = tk.Button(self.side_panel, text="Green Channel", command=lambda: self.update_image("green"), font=button_font)
        self.green_button.pack(fill=tk.X, padx=10, pady=5)

        self.blue_button = tk.Button(self.side_panel, text="Blue Channel", command=lambda: self.update_image("blue"), font=button_font)
        self.blue_button.pack(fill=tk.X, padx=10, pady=5)

        self.btn_reset = tk.Button(self.side_panel, text="Reset Image", command=self.reset_image, font=button_font)
        self.btn_reset.pack(fill=tk.X, padx=10, pady=5)

    def open_blur_form(self):
        def accept():
            if self.image is not None:
                try:
                    kernel_size = int(entry.get())
                    self.image = get_image_with_gaussian_blur(self.image, kernel_size)
                    self.display_image(self.image)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            form.destroy()

        def cancel():
            form.destroy()

        form = tk.Toplevel(self.root)
        form.title("Input Form")
        label = tk.Label(form, text="Enter an integer blur value:")
        label.pack(padx=10, pady=10)
        entry = tk.Entry(form)
        entry.pack(padx=10, pady=10)
        accept_button = tk.Button(form, text="Accept", command=accept)
        accept_button.pack(side=tk.LEFT, padx=10, pady=10)
        cancel_button = tk.Button(form, text="Cancel", command=cancel)
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.image = load_image_from_disk(file_path)
                self.original_image = self.image.copy()
                self.display_image(self.image)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def capture_image(self):
        try:
            self.image = capture_image_from_webcam()
            self.original_image = self.image.copy()
            self.display_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_image(self, channel):
        if self.image is not None:
            try:
                img = get_image_with_channels(self.image, channel)
                self.display_image(img)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def apply_blur(self):
        if self.image is not None:
            try:
                kernel_size = int(self.blur_entry.get())
                self.image = get_image_with_gaussian_blur(self.image, kernel_size)
                self.display_image(self.image)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def convert_to_gray(self):
        if self.image is not None:
            try:
                self.image = get_grey_channel_img(self.image)
                self.display_image(self.image)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def draw_line(self):
        if self.image is not None:
            try:
                x1 = int(self.line_x1_entry.get())
                y1 = int(self.line_y1_entry.get())
                x2 = int(self.line_x2_entry.get())
                y2 = int(self.line_y2_entry.get())
                thickness = int(self.line_thickness_entry.get())
                self.image = get_image_with_line(self.image, (x1, y1), (x2, y2), thickness)
                self.display_image(self.image)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def reset_image(self):
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.display_image(self.image)

    def display_image(self, img):
        if len(img.shape) == 2:  # Grayscale image
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
