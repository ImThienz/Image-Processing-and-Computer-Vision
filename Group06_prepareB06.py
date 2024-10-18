import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

# Khởi tạo biến img
img = None

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Xử lý ảnh và thị giác máy tính")
root.configure(bg="#D3A399")

# Tạo tiêu đề chính "NHÓM..." với định dạng và vị trí giống yêu cầu
heading = tk.Label(root, text="NHÓM 06", font=('Arial', 25, 'bold'), bg="#D3A399", fg="#5E35B1")
heading.place(x=10, y=10)  # Đặt tiêu đề ở góc trên bên trái, cách 10px từ trên và trái

# Thêm Label chỉ dẫn nhập kích thước bộ lọc
size_label = tk.Label(root, text="Hãy nhập N để tạo kích thước bộ lọc NxN", bg="#D3A399", fg="black",
                      font=("Arial", 12))
size_label.grid(row=1, column=0, padx=5, pady=5)

# Nhập kích thước lọc
size_entry = tk.Entry(root)
size_entry.grid(row=2, column=0, padx=10, pady=5)

# Khung hiển thị ảnh gốc và text "Ảnh gốc"
original_label_text = tk.Label(root, text="Ảnh gốc", bg="#D3A399", fg="red", font=("Arial", 16))
original_label_text.grid(row=2, column=1, padx=10, pady=10)

original_label = tk.Label(root, bg="#D3A399")
original_label.grid(row=3, column=1, padx=10, pady=10)

# Khung hiển thị kết quả và text "Kết quả ảnh"
result_label_text = tk.Label(root, text="Kết quả ảnh", bg="#D3A399", fg="red", font=("Arial", 16))
result_label_text.grid(row=2, column=2, padx=10, pady=10)

result_label = tk.Label(root, bg="#D3A399")
result_label.grid(row=3, column=2, padx=10, pady=10)


# Hàm hiển thị ảnh với kích thước cố định
def display_image(image, label, width=300, height=300, to_grayscale=False):
    if image is None:
        print("No image to display.")
        return

    # Resize ảnh
    image_resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    # Chuyển ảnh sang grayscale nếu cần
    if to_grayscale:
        image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)

    # Kiểm tra số chiều của ảnh
    if len(image_resized.shape) == 2:  # Ảnh grayscale
        image_display = Image.fromarray(image_resized)
    elif len(image_resized.shape) == 3:  # Ảnh màu
        image_display = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
        image_display = Image.fromarray(image_display)
    else:
        print("Invalid image format.")
        return

    image_display = ImageTk.PhotoImage(image_display)
    label.config(image=image_display)
    label.image = image_display


# Label để hiển thị trạng thái loading
loading_label = tk.Label(root, text="Đang tải ảnh...", bg="#D3A399", fg="red", font=("Arial", 14))


# Hàm hiển thị loading
def show_loading():
    loading_label.grid(row=4, column=1, columnspan=2, pady=10)  # Hiển thị ở giữa giao diện
    root.update_idletasks()  # Cập nhật giao diện ngay lập tức


# Hàm ẩn loading
def hide_loading():
    loading_label.grid_forget()  # Ẩn label loading

# Hàm mở ảnh từ file với loading
def load_image():
    file_path = filedialog.askopenfilename()  # Chọn file ảnh từ hệ thống
    if file_path:
        show_loading()  # Hiển thị "Đang tải ảnh..." sau khi chọn ảnh
        reset_result_image()  # Xóa kết quả hình ảnh cũ trước khi tải ảnh mới
        root.after(100, process_image, file_path)  # Đảm bảo trạng thái giao diện hiển thị trước khi xử lý


def reset_result_image():
    # Xóa hình ảnh cũ trên kết quả
    result_label.config(image='')
    result_label.image = None


def process_image(file_path):
    global img
    img = cv2.imread(file_path)  # Tải ảnh

    if img is not None:
        display_image(img, original_label, to_grayscale=True)  # Hiển thị ảnh gốc dưới dạng grayscale
    hide_loading()  # Ẩn thông báo "Đang tải ảnh..." sau khi ảnh đã được hiển thị


# Hàm thêm nhiễu Gauss
def add_gaussian_noise():
    global img
    if img is None:
        print("Please load an image first.")
        return
    row, col, ch = img.shape
    mean = 0
    sigma = 25  # Điều chỉnh sigma để quan sát rõ nhiễu
    gauss = np.random.normal(mean, sigma, (row, col, ch)).astype('float32')
    noisy = img.astype('float32') + gauss

    # Đảm bảo giá trị pixel nằm trong khoảng [0, 255]
    noisy = np.clip(noisy, 0, 255).astype('uint8')

    display_result(noisy)


# Hàm thêm nhiễu muối tiêu
def add_salt_pepper_noise():
    global img
    if img is None:
        print("Please load an image first.")
        return
    s_vs_p = 0.8
    amount = 0.006
    noisy = np.copy(img)

    # Salt mode
    num_salt = np.ceil(amount * img.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img.shape]
    noisy[tuple(coords)] = 1

    # Pepper mode
    num_pepper = np.ceil(amount * img.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img.shape]
    noisy[tuple(coords)] = 0
    display_result(noisy)


# Hàm hiển thị ảnh kết quả
def display_result(result_img):
    if result_img is None:
        print("No result image to display.")
        return
    display_image(result_img, result_label, to_grayscale=True)  # Hiển thị ảnh kết quả dưới dạng grayscale


# Hàm lọc trung bình
def average_filter():
    global img
    if img is None:
        print("Please load an image first.")
        return

    ksize = size_entry.get()
    if not ksize.isdigit() or int(ksize) <= 0:
        print("Please enter a valid positive integer.")
        return

    ksize = int(ksize)

    # Áp dụng lọc trung bình
    filtered_img = cv2.blur(img, (ksize, ksize))
    display_result(filtered_img)


# Hàm lọc trung vị
def median_filter():
    global img
    if img is None:
        print("Please load an image first.")
        return

    ksize = size_entry.get()

    # Kiểm tra xem giá trị nhập có phải là số không
    if not ksize.isdigit():
        print("Please enter a valid number.")
        return

    ksize = int(ksize)

    # Kiểm tra ksize có lớn hơn 1 và là số lẻ không
    if ksize < 1 or ksize % 2 == 0:
        print("Kernel size must be an odd number greater than 1.")
        return

    # Áp dụng bộ lọc trung vị
    filtered_img = cv2.medianBlur(img, ksize)
    display_result(filtered_img)


# Hàm lọc max
def max_filter():
    global img
    if img is None:
        print("Please load an image first.")
        return
    ksize = size_entry.get()
    if not ksize.isdigit() or int(ksize) <= 0:
        print("Please enter a valid positive integer.")
        return
    ksize = int(ksize)
    filtered_img = cv2.dilate(img, np.ones((ksize, ksize), np.uint8))
    display_result(filtered_img)


# Hàm lọc min
def min_filter():
    global img
    if img is None:
        print("Please load an image first.")
        return
    ksize = size_entry.get()
    if not ksize.isdigit() or int(ksize) <= 0:
        print("Please enter a valid positive integer.")
        return
    ksize = int(ksize)
    filtered_img = cv2.erode(img, np.ones((ksize, ksize), np.uint8))
    display_result(filtered_img)


# Tạo frame cho các nút chức năng phía trên
top_button_frame = tk.Frame(root, bg="#D3A399")
top_button_frame.grid(row=0, column=1, columnspan=2, pady=10, sticky="ew")

# Nút tải ảnh
load_btn = tk.Button(top_button_frame, text="Load ảnh", bg="#6C63FF", fg="white", command=load_image, width=15,
                     height=2, font=("Arial", 12))
load_btn.pack(side="left", padx=10, pady=5)

# Nút thêm nhiễu Gauss
gauss_btn = tk.Button(top_button_frame, text="Tạo nhiễu gauss", bg="#8D7961", fg="white", command=add_gaussian_noise,
                      width=15, height=2, font=("Arial", 12))
gauss_btn.pack(side="left", padx=10, pady=5)

# Nút thêm nhiễu muối tiêu
sp_btn = tk.Button(top_button_frame, text="Tạo nhiễu muối tiêu", bg="#DE6349", fg="white",
                   command=add_salt_pepper_noise, width=15, height=2, font=("Arial", 12))
sp_btn.pack(side="left", padx=10, pady=5)

# Tạo frame để nhóm các nút lọc
filter_frame = tk.Frame(root, bg="#D3A399")
filter_frame.grid(row=3, column=0, padx=10, pady=5, sticky="n")

# Nút lọc trung bình
avg_filter_btn = tk.Button(filter_frame, text="Lọc trung bình", bg="#6C63FF", fg="white", command=average_filter,
                           width=15, height=2, font=("Arial", 12))
avg_filter_btn.pack(pady=5, fill="x")

# Nút lọc trung vị
median_filter_btn = tk.Button(filter_frame, text="Lọc trung vị", bg="#8D7961", fg="white", command=median_filter,
                              width=15, height=2, font=("Arial", 12))
median_filter_btn.pack(pady=5, fill="x")

# Nút lọc max
max_filter_btn = tk.Button(filter_frame, text="Lọc MAX", bg="#DE6349", fg="white", command=max_filter, width=15,
                           height=2, font=("Arial", 12))
max_filter_btn.pack(pady=5, fill="x")


# Nút lọc min
min_filter_btn = tk.Button(filter_frame, text="Lọc MIN", bg="#6C63FF", fg="white", command=min_filter, width=15,
                           height=2, font=("Arial", 12))
min_filter_btn.pack(pady=5, fill="x")

root.mainloop()