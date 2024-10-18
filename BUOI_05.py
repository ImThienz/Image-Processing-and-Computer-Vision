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
image = cv2.imread('pic/pikachu.jpg', cv2.IMREAD_GRAYSCALE)  # Đọc ảnh dưới dạng màu xám (grayscale)

# Hàm thêm nhiễu muối
def salt_noise(image, prob):
    noisy_image = np.copy(image)
    num_salt = np.ceil(prob * image.size)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 255  # Thêm nhiễu muối (trắng)
    return noisy_image

# Hàm thêm nhiễu tiêu
def pepper_noise(image, prob):
    noisy_image = np.copy(image)
    num_pepper = np.ceil(prob * image.size)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 0  # Thêm nhiễu tiêu (đen)
    return noisy_image

# Thêm nhiễu muối và tiêu với xác suất 0.02
salt_image = salt_noise(image, 0.02)
pepper_image = pepper_noise(image, 0.02)

# Áp dụng bộ lọc Max (maximum filter) và Min (minimum filter)
max_filter_salt = cv2.dilate(salt_image, np.ones((3, 3), np.uint8))  # Bộ lọc Max cho nhiễu muối
min_filter_salt = cv2.erode(salt_image, np.ones((3, 3), np.uint8))   # Bộ lọc Min cho nhiễu muối

max_filter_pepper = cv2.dilate(pepper_image, np.ones((3, 3), np.uint8))  # Bộ lọc Max cho nhiễu tiêu
min_filter_pepper = cv2.erode(pepper_image, np.ones((3, 3), np.uint8))   # Bộ lọc Min cho nhiễu tiêu

# Hiển thị ảnh
plt.figure(figsize=(12, 10))

plt.subplot(2, 3, 1)
plt.imshow(salt_image, cmap='gray')
plt.title('Salt Noise')

plt.subplot(2, 3, 2)
plt.imshow(max_filter_salt, cmap='gray')
plt.title('Max Filter (Salt Noise)')

plt.subplot(2, 3, 3)
plt.imshow(min_filter_salt, cmap='gray')
plt.title('Min Filter (Salt Noise)')

plt.subplot(2, 3, 4)
plt.imshow(pepper_image, cmap='gray')
plt.title('Pepper Noise')

plt.subplot(2, 3, 5)
plt.imshow(max_filter_pepper, cmap='gray')
plt.title('Max Filter (Pepper Noise)')

plt.subplot(2, 3, 6)
plt.imshow(min_filter_pepper, cmap='gray')
plt.title('Min Filter (Pepper Noise)')

plt.tight_layout()
plt.show()
