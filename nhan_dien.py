import cv2
import pickle
import numpy as np
import time
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
import mysql.connector
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup

class FaceRecognitionApp(App):
    def build(self):
        self.capture = None
        self.facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

        # Nạp dữ liệu từ file pickle
        with open('data/name.pkl', 'rb') as f:
            self.LABELS = pickle.load(f)
        with open('data/anh.pkl', 'rb') as f:
            self.FACES = pickle.load(f)

        # Huấn luyện mô hình KNN
        self.knn = KNeighborsClassifier(n_neighbors=5)
        self.knn.fit(self.FACES, self.LABELS)

        # Kết nối đến MySQL
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="Clock_in"
        )
        self.cursor = self.conn.cursor()

        # Tạo giao diện
        Window.clearcolor = (0.2, 0.3, 0.4, 1)  # Màu nền tối hơn
        Window.size = (1024, 768)  # Tăng kích thước cửa sổ ứng dụng
        self.main_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        # Khung ảnh video
        self.image_widget = Image(size_hint=(1, 0.6))
        self.main_layout.add_widget(self.image_widget)

        # Layout thông tin
        self.info_layout = GridLayout(cols=2, size_hint=(1, 0.15), spacing=10, padding=10)
        self.name_label = Label(
            text="Tên:",
            color=(1, 1, 1, 1),
            font_size=28,  # Tăng kích thước chữ
        )
        self.name_display = Label(
            text="Chưa nhận diện",
            color=(1, 1, 1, 1),
            font_size=28,  # Tăng kích thước chữ
        )
        self.info_layout.add_widget(self.name_label)
        self.info_layout.add_widget(self.name_display)
        self.main_layout.add_widget(self.info_layout)

        # Nút lưu thông tin và thoát
        self.button_layout = GridLayout(cols=2, size_hint=(1, 0.2), spacing=20, padding=20)
        self.save_button = Button(
            text="Lưu thông tin",
            size_hint=(0.5, 0.5),
            background_color=(0.1, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=24,  # Tăng kích thước chữ
        )
        self.save_button.bind(on_press=self.save_attendance)
        self.quit_button = Button(
            text="Thoát",
            size_hint=(0.5, 0.5),
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=24,  # Tăng kích thước chữ
        )
        self.quit_button.bind(on_press=self.stop_app)
        self.button_layout.add_widget(self.save_button)
        self.button_layout.add_widget(self.quit_button)

        self.main_layout.add_widget(self.button_layout)

        # Mở camera và bắt đầu quét khuôn mặt
        self.start_capture()

        return self.main_layout

    def start_capture(self):
        # Khởi tạo camera
        self.capture = cv2.VideoCapture(0)

        if not self.capture.isOpened():
            print("Không thể mở camera.")
            return

        # Lên lịch cập nhật khung hình (30 FPS)
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)

    def update_frame(self, dt):
        # Đọc khung hình từ camera
        ret, frame = self.capture.read()
        if not ret:
            print("Không thể lấy khung hình từ camera.")
            return

        # Chuyển sang ảnh xám
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.facedetect.detectMultiScale(gray, 1.1, 3)

        for (x, y, w, h) in faces:
            # Cắt và thay đổi kích thước ảnh khuôn mặt
            crop_img = frame[y:y + h, x:x + w]
            resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)

            # Dự đoán nhãn (tên) của khuôn mặt
            output = self.knn.predict(resized_img)

            # Cập nhật tên người nhận diện
            self.name_display.text = output[0]

            # Vẽ khung quanh khuôn mặt và hiển thị tên
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, str(output[0]), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        # Cập nhật hình ảnh trên giao diện Kivy
        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image_widget.texture = texture

    def save_attendance(self, instance):
        name = self.name_display.text
        if name == "Chưa nhận diện":
            return

        tg = time.time()
        attendance_time = datetime.fromtimestamp(tg).strftime("%Y-%m-%d %H:%M:%S")
        attendance = (name, attendance_time)

        # Lưu vào cơ sở dữ liệu MySQL
        self.cursor.execute("INSERT INTO attendance (name, time) VALUES (%s, %s)", attendance)
        self.conn.commit()
        print(f"Thông tin đã được lưu vào cơ sở dữ liệu: {attendance}")

        # Hiển thị Popup thông báo cho người dùng
        self.show_popup("Thông báo", "Thông tin đã được ghi nhận!")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, font_size=24), size_hint=(None, None), size=(400, 200))
        popup.open()

    def stop_app(self, instance):
        if self.capture:
            self.capture.release()
        self.cursor.close()
        self.conn.close()
        self.stop()

if __name__ == "__main__":
    FaceRecognitionApp().run()
