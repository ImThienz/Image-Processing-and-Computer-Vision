"Lọc mean (trung bình)"
# import cv2
# import matplotlib.pyplot as plt

# # Đọc ảnh gốc
# image = cv2.imread('doraemon.jpg')
# image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Chuyển ảnh sang không gian màu xám
#
# # Lọc trung bình với kernel 3x3
# mean_3x3 = cv2.blur(image_gray, (3, 3))
#
# # Lọc trung bình với kernel 9x9
# mean_9x9 = cv2.blur(image_gray, (9, 9))
#
# # Lọc trung bình với kernel 15x15
# mean_15x15 = cv2.blur(image_gray, (15, 15))
#
# # Hiển thị ảnh
# plt.figure(figsize=(20, 5))  # Tăng chiều rộng cho các hình
#
# # Sắp xếp các ảnh theo hàng ngang (1 hàng, 4 cột)
# plt.subplot(1, 4, 1)  # 1 hàng, 4 cột, vị trí 1
# plt.imshow(image_gray, cmap='gray')  # Hiển thị ảnh gốc màu xám
# plt.title('Original Grayscale Image')
# plt.axis('off')
#
# plt.subplot(1, 4, 2)  # 1 hàng, 4 cột, vị trí 2
# plt.imshow(mean_3x3, cmap='gray')  # Hiển thị ảnh sau khi áp dụng lọc 3x3
# plt.title('Mean Filter (3x3)')
# plt.axis('off')
#
# plt.subplot(1, 4, 3)  # 1 hàng, 4 cột, vị trí 3
# plt.imshow(mean_9x9, cmap='gray')  # Hiển thị ảnh sau khi áp dụng lọc 9x9
# plt.title('Mean Filter (9x9)')
# plt.axis('off')
#
# plt.subplot(1, 4, 4)  # 1 hàng, 4 cột, vị trí 4
# plt.imshow(mean_15x15, cmap='gray')  # Hiển thị ảnh sau khi áp dụng lọc 15x15
# plt.title('Mean Filter (15x15)')
# plt.axis('off')
#
# plt.tight_layout()
# plt.show()


"Lọc median (trung vị)"
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Đọc ảnh gốc
# image = cv2.imread('pikachu.jpg')  # Thay 'doramon.jpg' bằng đường dẫn tới ảnh của bạn
#
# # Chuyển sang không gian màu xám
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#
# # Thêm nhiễu muối tiêu
# def salt_and_pepper_noise(image, prob):
#     noisy_image = np.copy(image)
#     # Tạo ngẫu nhiên các điểm ảnh để thay thế thành muối (trắng)
#     num_salt = np.ceil(prob * image.size * 0.5)
#     coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
#     noisy_image[coords[0], coords[1]] = 255  # Thay đổi màu trắng cho muối
#
#     # Tạo ngẫu nhiên các điểm ảnh để thay thế thành tiêu (đen)
#     num_pepper = np.ceil(prob * image.size * 0.5)
#     coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
#     noisy_image[coords[0], coords[1]] = 0  # Thay đổi màu đen cho tiêu
#
#     return noisy_image
#
#
# # Thêm nhiễu muối tiêu với xác suất 0.02
# noisy_gray_image = salt_and_pepper_noise(gray_image, 0.02)
#
# # Lọc trung vị với các kernel 3x3, 9x9, và 15x15
# median_3x3 = cv2.medianBlur(noisy_gray_image, 3)
# median_9x9 = cv2.medianBlur(noisy_gray_image, 9)
# median_15x15 = cv2.medianBlur(noisy_gray_image, 15)
#
# # Hiển thị ảnh
# plt.figure(figsize=(20, 5))  # Tăng chiều rộng cho các hình
#
# # Sắp xếp các ảnh theo hàng ngang (1 hàng, 5 cột)
# plt.subplot(1, 5, 1)  # 1 hàng, 5 cột, vị trí 1
# plt.imshow(gray_image, cmap='gray')
# plt.title('Original Gray Image')
# plt.axis('off')
#
# plt.subplot(1, 5, 2)  # 1 hàng, 5 cột, vị trí 2
# plt.imshow(noisy_gray_image, cmap='gray')
# plt.title('Salt & Pepper Noise')
# plt.axis('off')
#
# plt.subplot(1, 5, 3)  # 1 hàng, 5 cột, vị trí 3
# plt.imshow(median_3x3, cmap='gray')
# plt.title('Median Filter (3x3)')
# plt.axis('off')
#
# plt.subplot(1, 5, 4)  # 1 hàng, 5 cột, vị trí 4
# plt.imshow(median_9x9, cmap='gray')
# plt.title('Median Filter (9x9)')
# plt.axis('off')
#
# plt.subplot(1, 5, 5)  # 1 hàng, 5 cột, vị trí 5
# plt.imshow(median_15x15, cmap='gray')
# plt.title('Median Filter (15x15)')
# plt.axis('off')
#
# plt.tight_layout()
# plt.show()


"Nhiễu muối & tiêu: Lọc max-min"
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh gốc
img = cv2.imread('pikachu.jpg', cv2.IMREAD_GRAYSCALE)

# Tạo nhiễu muối
def add_salt_noise(image, amount=0.05):
    row, col = image.shape
    num_salt = np.ceil(amount * image.size)

    # Tạo nhiễu muối
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    image[coords[0], coords[1]] = 255

    return image

# Tạo nhiễu tiêu
def add_pepper_noise(image, amount=0.05):
    row, col = image.shape
    num_pepper = np.ceil(amount * image.size)

    # Tạo nhiễu tiêu
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    image[coords[0], coords[1]] = 0

    return image

# Tạo ảnh nhiễu muối và tiêu
salt_img = add_salt_noise(img.copy(), amount=0.05)
pepper_img = add_pepper_noise(img.copy(), amount=0.05)

# Áp dụng lọc Max (Dilation) và Min (Erosion) cho nhiễu muối
salt_max_filtered = cv2.dilate(salt_img, np.ones((3, 3), np.uint8))
salt_min_filtered = cv2.erode(salt_img, np.ones((3, 3), np.uint8))

# Áp dụng lọc Max (Dilation) và Min (Erosion) cho nhiễu tiêu
pepper_max_filtered = cv2.dilate(pepper_img, np.ones((3, 3), np.uint8))
pepper_min_filtered = cv2.erode(pepper_img, np.ones((3, 3), np.uint8))

# Hiển thị ảnh gốc, ảnh lọc max/min của nhiễu muối và tiêu
plt.figure(figsize=(10, 8))

# Ảnh lọc Max của nhiễu muối
plt.subplot(2, 2, 1)
plt.imshow(salt_max_filtered, cmap='gray')
plt.title('Lọc Max - Nhiễu Muối')

# Ảnh lọc Min của nhiễu muối
plt.subplot(2, 2, 2)
plt.imshow(salt_min_filtered, cmap='gray')
plt.title('Lọc Min - Nhiễu Muối')

# Ảnh lọc Max của nhiễu tiêu
plt.subplot(2, 2, 3)
plt.imshow(pepper_max_filtered, cmap='gray')
plt.title('Lọc Max - Nhiễu Tiêu')

# Ảnh lọc Min của nhiễu tiêu
plt.subplot(2, 2, 4)
plt.imshow(pepper_min_filtered, cmap='gray')
plt.title('Lọc Min - Nhiễu Tiêu')

plt.tight_layout()
plt.show()

