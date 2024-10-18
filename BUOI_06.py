"Lọc thông thấp"
# # libraries
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # original image
# f = cv2.imread('./pic/mario.jpg', 0)
#
# plt.imshow(f, cmap='gray')
# plt.axis('off')
# plt.show()
#
# # image in frequency domain
# F = np.fft.fft2(f)
# Fshift = np.fft.fftshift(F)
#
# # Filter: Low pass filter
# M, N = f.shape
# H = np.zeros((M, N), dtype=np.float32)
"Bộ lọc D0=20"
# # D0 = 20
# # for u in range(M):
# #     for v in range(N):
# #         D = np.sqrt((u - M / 2) ** 2 + (v - N / 2) ** 2)
# #         if D <= D0:
# #             H[u, v] = 1
# #         else:
# #             H[u, v] = 0
"Bộ lạc D0=50"
# D0 = 50
# n = 2
# for u in range(M):
#     for v in range(N):
#         D = np.sqrt((u - M / 2) ** 2 + (v - N / 2) ** 2)
#         H[u, v] = 1 / (1 + (D / D0) ** n)
#
# Gshift = Fshift * H
#
# # Inverse Fourier Transform
# G = np.fft.ifftshift(Gshift)
# g = np.abs(np.fft.ifft2(G))
# plt.imshow(g, cmap='gray')
# plt.axis('off')
# plt.show()

"=========================================================="
"=========================================================="

"ảnh gốc - D=30 n=1 - D=30 n=5 - D=30 n=40"
# # Hàm tạo bộ lọc Butterworth bậc n
# def butterworth_low_pass_filter(M, N, D0, n):
#     H = np.zeros((M, N), dtype=np.float32)
#     for u in range(M):
#         for v in range(N):
#             D = np.sqrt((u - M / 2) ** 2 + (v - N / 2) ** 2)
#             H[u, v] = 1 / (1 + (D / D0) ** (2 * n))
#     return H
#
# # original image
# f = cv2.imread('./pic/girl.jpg', 0)
#
# # image in frequency domain
# F = np.fft.fft2(f)
# Fshift = np.fft.fftshift(F)
#
# # Filter: Low pass Butterworth filter with different n
# M, N = f.shape
# D0 = 30  # Đặt D0 = 30
#
# # Tạo các bộ lọc Butterworth với bậc n = 1, n = 6, n = 40
# H1 = butterworth_low_pass_filter(M, N, D0, 1)
# H6 = butterworth_low_pass_filter(M, N, D0, 6)
# H40 = butterworth_low_pass_filter(M, N, D0, 40)
#
# # Áp dụng các bộ lọc cho ảnh
# Gshift1 = Fshift * H1
# Gshift6 = Fshift * H6
# Gshift40 = Fshift * H40
#
# # Inverse Fourier Transform để đưa ảnh về không gian thời gian
# G1 = np.fft.ifftshift(Gshift1)
# g1 = np.abs(np.fft.ifft2(G1))
#
# G6 = np.fft.ifftshift(Gshift6)
# g6 = np.abs(np.fft.ifft2(G6))
#
# G40 = np.fft.ifftshift(Gshift40)
# g40 = np.abs(np.fft.ifft2(G40))
#
# # Hiển thị ảnh gốc và các ảnh lọc
# plt.figure(figsize=(20, 5))  # Kích thước hình
#
# # Ảnh gốc
# plt.subplot(1, 4, 1)
# plt.imshow(f, cmap='gray')
# plt.title('Original Image')
# plt.axis('off')
#
# # Ảnh lọc với D=30, n=1
# plt.subplot(1, 4, 2)
# plt.imshow(g1, cmap='gray')
# plt.title('Butterworth (D=30, n=1)')
# plt.axis('off')
#
# # Ảnh lọc với D=30, n=6
# plt.subplot(1, 4, 3)
# plt.imshow(g6, cmap='gray')
# plt.title('Butterworth (D=30, n=6)')
# plt.axis('off')
#
# # Ảnh lọc với D=30, n=40
# plt.subplot(1, 4, 4)
# plt.imshow(g40, cmap='gray')
# plt.title('Butterworth (D=30, n=40)')
# plt.axis('off')
#
# plt.tight_layout()
# plt.show()

"=========================================================="
"=========================================================="

"Lọc thông thấp"
import tkinter as tk
from tkinter import filedialog
from tkinter import Label, Button, Entry
import cv2
import numpy as np
from PIL import Image, ImageTk


# Hàm tạo bộ lọc Butterworth bậc n
def butterworth_low_pass_filter(M, N, D0, n):
    H = np.zeros((M, N), dtype=np.float32)
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u - M / 2) ** 2 + (v - N / 2) ** 2)
            H[u, v] = 1 / (1 + (D / D0) ** (2 * n))
    return H


# Hàm để load ảnh
def load_image():
    global img, img_original, panel_orig
    filepath = filedialog.askopenfilename()
    img = cv2.imread(filepath)  # Giữ nguyên ảnh màu
    img_resized = cv2.resize(img, (200, 200))  # Resize cho hiển thị dễ dàng
    img_original = ImageTk.PhotoImage(
        image=Image.fromarray(cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)))  # Đổi từ BGR sang RGB
    panel_orig.config(image=img_original)
    panel_orig.image = img_original


# Hàm áp dụng bộ lọc Butterworth
def apply_butterworth():
    global img, img_filtered, panel_filtered
    D0 = int(entry_D.get())
    n = int(entry_n.get())

    if img is None:
        return

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Chuyển sang ảnh xám để xử lý Fourier
    # Image in frequency domain
    F = np.fft.fft2(img_gray)
    Fshift = np.fft.fftshift(F)

    M, N = img_gray.shape
    H = butterworth_low_pass_filter(M, N, D0, n)

    Gshift = Fshift * H

    # Inverse Fourier Transform to bring the image back
    G = np.fft.ifftshift(Gshift)
    g = np.abs(np.fft.ifft2(G))

    # Resize and display the filtered image
    g_resized = cv2.resize(g, (200, 200))
    img_filtered = ImageTk.PhotoImage(image=Image.fromarray(g_resized))
    panel_filtered.config(image=img_filtered)
    panel_filtered.image = img_filtered


# Giao diện Tkinter
root = tk.Tk()
root.title("Butterworth Filter - Nhóm 06")

# Label nhóm ở vị trí giữa
label_group = Label(root, text="NHÓM 06", font=("Arial", 24))
label_group.grid(row=0, column=1)

# Button load ảnh
btn_load = Button(root, text="Load", command=load_image)
btn_load.grid(row=1, column=0)

# Button Butterworth
btn_butterworth = Button(root, text="Butterworth", command=apply_butterworth)
btn_butterworth.grid(row=2, column=0)

# Entry để nhập giá trị D
label_D = Label(root, text="D:")
label_D.grid(row=3, column=0)
entry_D = Entry(root)
entry_D.grid(row=3, column=1)

# Entry để nhập giá trị n
label_n = Label(root, text="n:")
label_n.grid(row=4, column=0)
entry_n = Entry(root)
entry_n.grid(row=4, column=1)

# Hiển thị ảnh gốc và ảnh đã lọc
panel_orig = Label(root)
panel_orig.grid(row=2, column=1)

panel_filtered = Label(root)
panel_filtered.grid(row=2, column=2)

root.mainloop()




