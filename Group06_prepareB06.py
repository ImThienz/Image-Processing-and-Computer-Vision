import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageChops
import numpy as np

original_image = None
processed_image = None

def load_image(default=True):
    global original_image, processed_image
    if default:
        file_path = "VAA.png"
    else:
        file_path = filedialog.askopenfilename()

    # Kiểm tra nếu file ảnh tồn tại
    if file_path:
        img = Image.open(file_path)
        img = img.resize((200, 200))
        original_image = img
        processed_image = img.copy()

        img_tk = ImageTk.PhotoImage(img)
        original_img_label.config(image=img_tk)
        original_img_label.image = img_tk

        after_img_label.config(image='')

# Hàm lọc thông thấp (Low Pass Filter)
def low_pass_filter(image):
    kernel = np.array([[1, 2, 1],
                       [2, 4, 2],
                       [1, 2, 1]]) / 16  # Gaussian kernel
    return image.filter(ImageFilter.Kernel((3, 3), kernel.flatten(), scale=1))

# Hàm lọc thông cao (High Pass Filter)
def high_pass_filter(image):
    low_passed = low_pass_filter(image)
    high_passed = ImageChops.subtract(image, low_passed)
    return high_passed

# Hàm áp dụng bộ lọc lên ảnh
def apply_filter(filter_type):
    global original_image, processed_image
    if original_image:
        try:
            r = float(r_entry.get())

            if filter_type == 'Cao':
                # Áp dụng bộ lọc thông cao
                filtered_img = high_pass_filter(original_image)

            elif filter_type == 'Thấp':
                # Áp dụng bộ lọc thông thấp
                filtered_img = low_pass_filter(original_image)

            # Cập nhật ảnh đã xử lý
            processed_image = filtered_img
            filtered_img_tk = ImageTk.PhotoImage(filtered_img)
            after_img_label.config(image=filtered_img_tk)
            after_img_label.image = filtered_img_tk
        except ValueError:
            print("Vui lòng nhập giá trị hợp lệ cho r.")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Image Processing UI")

# Thêm label "NHÓM 06" ở chính giữa giao diện trên cùng
group_label = tk.Label(root, text="NHÓM 06", font=("Arial", 16))
group_label.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Nút "Load" (Reset ảnh về mặc định)
load_button = tk.Button(root, text="Load", command=lambda: load_image(default=True))
load_button.grid(row=1, column=0, padx=10, pady=10)

# Trường nhập giá trị "r" gần với label "r ="
r_label = tk.Label(root, text="r =")
r_label.grid(row=1, column=1, padx=5)
r_entry = tk.Entry(root)
r_entry.grid(row=1, column=1, padx=5)

# Hai nút "Cao" và "Thấp" để áp dụng bộ lọc
lt_button = tk.Button(root, text="Cao", command=lambda: apply_filter('Cao'))
lt_button.grid(row=2, column=0, padx=10, pady=5)
bw_button = tk.Button(root, text="Thấp", command=lambda: apply_filter('Thấp'))
bw_button.grid(row=3, column=0, padx=10, pady=5)

original_img_label = tk.Label(root, text="Gốc")
original_img_label.grid(row=2, column=1, rowspan=3, padx=10)
after_img_label = tk.Label(root, text="After")
after_img_label.grid(row=2, column=2, rowspan=3, padx=10)

# Tải ảnh mặc định khi khởi động
load_image(default=True)

# Chạy chương trình
root.mainloop()