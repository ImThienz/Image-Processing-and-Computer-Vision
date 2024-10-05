"Tạo nhiễu Gauss"
# import cv2
# import f
# import numpy as np
#
# # original image
# f = cv2.imread('miss-1.png', cv2.IMREAD_GRAYSCALE)
# f = f/255s
#
# cv2.imwrite('miss-gray.png',f*255)
#
# cv2.imshow('original image', f)
# cv2.waitKey(0)
#
# # create gaussian noise
# x, y = f.shape
# mean = 0
# var = 0.01
# sigma = np.sqrt(var)
# n = np.random.normal(loc=mean, scale=sigma, size=(x,y))
#
# cv2.imshow('Noise', n)
# cv2.waitKey(0)
#
# print(np.min(n))
# # add a gaussian noise
# g = f + n
#
# cv2.imshow('Image with Noise', g)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# cv2.imwrite('miss-gauss001.png',g*255)

"==========================================================="

"Nhiễu muối tiêu"
# import cv2
# import numpy as np
#
# # orginal image
# img = cv2.imread('girl.jpg', cv2.IMREAD_GRAYSCALE)
# img = img/255
#
# cv2.imshow('original image', img)
# cv2.waitKey(0)
#
# # blank image
# x,y = img.shape
# g = np.zeros((x,y), dtype=np.float32)
#
# # salt and pepper amount
# pepper = 0.1
# salt = 0.95
# "1 là tiêu, 0.95 là muối tiêu"
#
# # create salt and peper noise image
# for i in range(x):
#     for j in range(y):
#         rdn = np.random.random()
#         if rdn < pepper:
#             g[i][j] = 0
#         elif rdn > salt:
#             g[i][j] = 1
#         else:
#             g[i][j] = img[i][j]
#
# cv2.imshow('image with noise', g)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# # (optional) save the image
# # cv2.imwrite('miss-salt-pepper.png',g*255)


"=============================================================="

import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk

screen = tk.Tk()
screen.geometry('400x400')

# tạo title
screen.title('Chương trình')

# Tạo label
label1 = tk.Label(screen, text="Hello",
                  bg="red", fg="white", font=('times', 16, 'bold'))
label1.grid(row=0, column=0, padx=10, pady=10)

label2 = tk.Label(screen, text="Goodbye",
                  bg="red", fg="white", font=('times', 16, 'bold'))
label2.grid(row=1, column=0, padx=10, pady=10)

# Tạo Entry
entry = tk.Entry(screen, width=10, font=("Arial", 18),
                 fg="black", bg="white")
entry.grid(row=0, column=1, sticky="nw", padx=0, pady=10)

entry1 = tk.Entry(screen, width=10, font=("Arial", 18),
                  fg="white", bg="black")
entry1.grid(row=0, column=2, sticky="nw", padx=0, pady=10)

entry2 = tk.Entry(screen, width=10, font=("Arial", 18),
                  fg="yellow", bg="red")
entry2.grid(row=0, column=3, sticky="nw", padx=0, pady=10)

img = Image.open('mario.jpg')
img = img.resize((300, 200))
photo = ImageTk.PhotoImage(img)

# Tạo Label với hình ảnh
labelImg = tk.Label(screen, image=photo)
labelImg.grid(row=2, column=0, columnspan=2, sticky="nw", padx=10, pady=10)

# Hàm lấy dữ liệu từ entry
def get_data():
    data = entry.get()
    print("Dữ liệu đã nhập:", data)


# Hàm thực hiện phép tính căn bậc 3 của (entry^2 + entry1^2)
def calculate_cubic_root():
    try:
        # Lấy giá trị từ entry và entry1
        data1 = float(entry.get())
        data2 = float(entry1.get())

        # Tính căn bậc 3 của (entry^2 + entry1^2)
        result = (data1 ** 2 + data2 ** 2) ** (1 / 3)

        # Xóa nội dung hiện tại của entry2 và hiển thị kết quả
        entry2.delete(0, tk.END)
        entry2.insert(0, round(result, 4))  # Làm tròn kết quả đến 4 chữ số thập phân
    except ValueError:
        entry2.delete(0, tk.END)
        entry2.insert(0, "Lỗi")


# Tạo nút để lấy dữ liệu từ Entry
button = tk.Button(screen, text="Button 1", fg="white", bg="Green",
                   font=('Arial', 12, 'bold'),
                   command=get_data)
button.grid(row=1, column=1, sticky="nw", padx=10, pady=10)

# Nút tính toán căn bậc 3
button1 = tk.Button(screen, text="Button 2", fg="white", bg="Green",
                    font=('Arial', 12, 'bold'),
                    command=calculate_cubic_root)  # Gọi hàm calculate_cubic_root
button1.grid(row=1, column=2, sticky="nw", padx=10, pady=10)

# Vòng lặp chính
screen.mainloop()


