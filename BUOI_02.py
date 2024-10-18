"CHẬP 1 CHIỀU"
# import numpy as np
# import cv2
#
# f = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype='float')
# g = np.array([1/5, 1/5, 1/5], dtype='float')
# h = np.convolve(f, g, mode='full')
# print(h)


"CHẬP 2 CHIỀU"
# import numpy as np
# import scipy as sp
# from scipy import signal
#
# f = np.array([[1, 8, 9, 10],
#               [2, 5, 12, 14],
#               [11, 7, 6, 5],
#               [13, 4, 2, 1]], dtype='float')
#
# g = np.array([[0, 1, 0],
#               [0, 0, 1],
#               [1, 1, 1]], dtype='float')
#
# h = sp.signal.convolve2d(f, g, mode='same')s
#
# print("Convolve:", h)

"LÀM MỜ HÌNH ẢNH"
import cv2
import numpy as np

image=cv2.imread('pic/cameraman.tif')

kernel=np.array([[0,0,0],
                [0,1,0],
                [0,0,0]], dtype=np.float32)
blur=np.array([[1,1,1],
                [1,1,1],
                [1,1,1]], dtype=np.float32)
sharp=np.array([[-1,-1,-1],
                [-1,9,-1],
                [-1,-1,-1]], dtype=np.float32)
edge=np.array([[0,-1,0],
                [-1,5,-1],
                [0,-1,0]], dtype=np.float32)
blur = blur / 9.0

output=cv2.filter2D(image,-1,kernel)
cv2.imshow("Original", output)

output=cv2.filter2D(image,-1,blur)
cv2.imshow("Blur", output)

output1=cv2.filter2D(image,-1,sharp)
cv2.imshow("Sharp", output1)

output2=cv2.filter2D(image,-1,edge)
cv2.imshow("Edge", output2)

cv2.waitKey(0)


"TÍNH FURIER"
# import numpy as np
#
# g=np.array([[0,0,0,0],
#             [0,1,1,0],
#             [0,1,1,0],
#             [0,0,0,0]], dtype='float')
# G=np.fft.fft2(g)
# print(G)
#
# g1=np.array([[0,0,1,0],
#             [0,0,1,0],
#             [0,0,1,0],
#             [0,0,1,0]], dtype='float')
# G1=np.fft.fft2(g1)
# print(G1)

"ĐỀ TÀI: NHẬN DIỆN BIỂN SỐ XE / PCA / KHUÔN MẶT / VGG16...YOLO...CNN"
