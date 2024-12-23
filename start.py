from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import mysql.connector
import os
import subprocess
import sys

# Đặt nền trắng
Window.clearcolor = (1, 1, 1, 1)
Window.size = (800, 600)


# Function to check login credentials from the database
def check_credentials(admin, password):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Clock_in"
        )
        cursor = db.cursor()
        query = "SELECT * FROM admin WHERE admin = %s AND pass = %s"
        cursor.execute(query, (admin, password))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result is not None
    except mysql.connector.Error as e:
        show_popup("Lỗi kết nối", f"Không thể kết nối tới cơ sở dữ liệu: {e}")
        return False


# Function to run a specified Python file
def run_file(filename, is_streamlit=False):
    if os.path.exists(filename):
        if is_streamlit:
            subprocess.Popen(["streamlit", "run", filename])
        else:
            subprocess.Popen([sys.executable, filename])
    else:
        show_popup("Lỗi", f"File {filename} không tồn tại trong thư mục hiện tại.")


# Function to show popup messages
def show_popup(title, message):
    popup_layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
    popup_label = Label(
        text=message,
        halign="center",
        valign="middle",
        font_size=24,  # Kích thước chữ lớn hơn
        color=(0, 0, 0, 1)  # Text color: Black
    )
    close_button = Button(
        text="Đóng",
        size_hint=(1, 0.2),
        font_size=20,  # Chữ to hơn
        background_color=(0.2, 0.6, 0.8, 1)
    )
    popup_layout.add_widget(popup_label)
    popup_layout.add_widget(close_button)

    popup = Popup(title=title, content=popup_layout, size_hint=(0.7, 0.4))
    close_button.bind(on_release=popup.dismiss)
    popup.open()


# Main app class
class MainApp(App):
    def build(self):
        # Root layout
        root_layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Title
        title_label = Label(
            text="HỆ THỐNG CHẤM CÔNG TỰ ĐỘNG",
            font_size=42,  # Kích thước chữ lớn hơn
            color=(0.2, 0.5, 0.7, 1),
            bold=True,
            halign="center",
            valign="middle"
        )
        title_label.bind(size=title_label.setter('text_size'))
        root_layout.add_widget(title_label)

        # Main buttons layout
        buttons_layout = GridLayout(cols=2, spacing=20, padding=20, size_hint_y=0.7)
        buttons_data = [
            ("Nhận diện khuôn mặt", (0.2, 0.7, 0.4, 1), lambda x: run_file("nhan_dien.py")),
            ("Thêm khuôn mặt mới", (0.1, 0.5, 0.9, 1), lambda x: self.prompt_login("them_khuan_mat.py")),
            ("Xem dữ liệu trực tuyến", (0.9, 0.5, 0.0, 1), lambda x: self.prompt_login("web.py", is_streamlit=True)),
            ("Thoát", (0.9, 0.2, 0.2, 1), self.stop)
        ]

        for text, color, callback in buttons_data:
            button = Button(
                text=text,
                font_size=27,  # Chữ to hơn
                background_color=color,
                color=(1, 1, 1, 1),  # White text color
                size_hint=(1, 0.6),
                halign="center",
                valign="middle"
            )
            button.bind(on_release=callback)
            buttons_layout.add_widget(button)
        root_layout.add_widget(buttons_layout)

        # Footer message
        footer_label = Label(
            text="Chúc bạn một ngày làm việc hiệu quả và năng suất!",
            font_size=27,  # Chữ to hơn
            color=(0.2, 0.2, 0.2, 1),
            italic=True,
            halign="center",
            valign="middle"
        )
        footer_label.bind(size=footer_label.setter('text_size'))
        root_layout.add_widget(footer_label)

        return root_layout

    # Function to prompt login
    def prompt_login(self, filename, is_streamlit=False):
        login_layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Username input
        login_layout.add_widget(Label(text="Tên đăng nhập:", font_size=27, color=(0.2, 0.2, 0.2, 1)))
        username_input = TextInput(multiline=False, font_size=27, size_hint_y=None, height=50)
        login_layout.add_widget(username_input)

        # Password input
        login_layout.add_widget(Label(text="Mật khẩu:", font_size=27, color=(0.2, 0.2, 0.2, 1)))
        password_input = TextInput(password=True, multiline=False, font_size=27, size_hint_y=None, height=50)
        login_layout.add_widget(password_input)

        # Login button
        btn_login = Button(
            text="Đăng nhập",
            font_size=30,  # Chữ to hơn
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_login.bind(on_release=lambda instance: self.login_action(username_input.text, password_input.text, filename,
                                                                     is_streamlit))
        login_layout.add_widget(btn_login)

        # Popup for login
        popup = Popup(title="Đăng nhập hệ thống", content=login_layout, size_hint=(0.6, 0.6))
        popup.open()

    def login_action(self, username, password, filename, is_streamlit):
        if check_credentials(username, password):
            run_file(filename, is_streamlit)
        else:
            show_popup("Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại.")


# Run the app
if __name__ == "__main__":
    MainApp().run()
