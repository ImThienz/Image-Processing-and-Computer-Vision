import cv2
import pickle
import numpy as np
import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.core.window import Window

class FaceCaptureApp(App):
    def build(self):
        self.capture = None
        self.facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        self.faces_data = []
        self.i = 0

        # Đặt màu nền cho toàn bộ ứng dụng
        Window.clearcolor = (0.2, 0.3, 0.4, 1)  # Màu nền tối hơn

        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Khung ảnh để hiển thị video
        self.image_widget = Image(size_hint=(1, 0.7))
        self.main_layout.add_widget(self.image_widget)

        # Khung nhập tên và nhãn
        self.label_layout = GridLayout(cols=2, size_hint=(1, 0.1), spacing=10)
        self.name_label = Label(text="Tiêu đề:", color=(1, 1, 1, 1), size_hint=(0.4, 1))  # Đặt màu chữ cho nhãn
        self.name_input = TextInput(hint_text="Nhập tên", multiline=False, size_hint=(0.6, 1), background_color=(1, 1, 1, 0.8))
        self.label_layout.add_widget(self.name_label)
        self.label_layout.add_widget(self.name_input)
        self.main_layout.add_widget(self.label_layout)

        # Nút bắt đầu và kết thúc ở dưới cùng
        self.button_layout = GridLayout(cols=2, size_hint=(1, 0.2), spacing=20)
        self.start_button = Button(text="Bắt đầu", size_hint=(0.5, 0.5), background_color=(0.1, 0.6, 0.3, 1), color=(1, 1, 1, 1))
        self.start_button.bind(on_press=self.start_capture)
        self.button_layout.add_widget(self.start_button)

        self.quit_button = Button(text="Kết thúc", size_hint=(0.5, 0.5), background_color=(0.8, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        self.quit_button.bind(on_press=self.stop_app)
        self.button_layout.add_widget(self.quit_button)

        # Thêm các phần vào layout chính
        self.main_layout.add_widget(self.button_layout)

        return self.main_layout

    def start_capture(self, instance):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # Cập nhật khung hình với 30 FPS

    def update_frame(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.facedetect.detectMultiScale(gray, 1.1, 3)

        # Xử lý mỗi khuôn mặt được phát hiện
        for (x, y, w, h) in faces:
            crop_img = frame[y:y + h, x:x + w]
            resized_img = cv2.resize(crop_img, (50, 50))

            # Lưu mỗi khung hình thứ 10 cho đến khi có 50 hình ảnh
            if len(self.faces_data) < 50 and self.i % 10 == 0:
                self.faces_data.append(resized_img)
            self.i += 1

            # Vẽ khung hình chữ nhật và cập nhật số khung
            cv2.putText(frame, str(len(self.faces_data)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cập nhật hình ảnh Kivy
        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image_widget.texture = texture

        # Dừng bắt hình nếu có đủ khuôn mặt
        if len(self.faces_data) >= 50:
            self.save_data()
            Clock.unschedule(self.update_frame)
            self.capture.release()

    def save_data(self):
        name = self.name_input.text.strip()
        if not name:
            name = "Không biết"

        # Chuyển đổi và thay đổi kích thước dữ liệu khuôn mặt
        faces_data = np.asarray(self.faces_data)
        faces_data = faces_data.reshape(50, -1)

        # Lưu dữ liệu tên
        if 'name.pkl' not in os.listdir('data/'):
            names = [name] * 50
            with open('data/name.pkl', 'wb') as f:
                pickle.dump(names, f)
        else:
            with open('data/name.pkl', 'rb') as f:
                names = pickle.load(f)
            names.extend([name] * 50)
            with open('data/name.pkl', 'wb') as f:
                pickle.dump(names, f)

        # Lưu dữ liệu khuôn mặt
        if 'anh.pkl' not in os.listdir('data/'):
            with open('data/anh.pkl', 'wb') as f:
                pickle.dump(faces_data, f)
        else:
            with open('data/anh.pkl', 'rb') as f:
                faces = pickle.load(f)
            faces = np.append(faces, faces_data, axis=0)
            with open('data/anh.pkl', 'wb') as f:
                pickle.dump(faces, f)

        self.faces_data = []
        self.i = 0
        self.name_input.text = ""
        self.start_button.text = "Bắt đầu"
        self.start_button.disabled = False

    def stop_app(self, instance):
        if self.capture:
            self.capture.release()
        self.stop()

if __name__ == "__main__":
    FaceCaptureApp().run()
