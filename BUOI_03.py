import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, fftshift
from PIL import Image

def process_image(image_path):
    # Đọc ảnh
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)

    # Biến đổi Fourier rời rạc bằng fft2
    G_uv = fft2(image_array)

    # Tính ma trận độ lớn của số phức
    magnitude = np.abs(G_uv)

    # Chuyển trục tọa độ 0,0 vào giữa
    magnitude_shifted = fftshift(magnitude)

    # Dùng hàm logarit để biểu diễn biên độ
    log_magnitude = np.log1p(magnitude_shifted)

    return image_array, log_magnitude

# Các đường dẫn đến ảnh
image_paths = ['mario.jpg', 'girl.jpg', 'monkey.jpg']

# Khởi tạo một figure với kích thước phù hợp
plt.figure(figsize=(15, 10))

for i, image_path in enumerate(image_paths):
    # Xử lý từng ảnh
    image_array, log_magnitude = process_image(image_path)

    # Hiển thị ảnh gốc
    plt.subplot(3, 2, 2 * i + 1)
    plt.title(f'Image: {image_path}')
    plt.imshow(image_array, cmap='gray')
    plt.axis('off')

    # Hiển thị phổ theo thang logarit
    plt.subplot(3, 2, 2 * i + 2)
    plt.title(f'Log Magnitude Spectrum: {image_path}')
    plt.imshow(log_magnitude, cmap='hot')
    plt.axis('off')

# Hiển thị toàn bộ hình ảnh
plt.tight_layout()
plt.show()
