import streamlit as st
import mysql.connector
import pandas as pd
from io import BytesIO

# Kết nối tới cơ sở dữ liệu MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Clock_in"
    )

# Lấy dữ liệu từ bảng attendance
def fetch_attendance_data():
    conn = get_connection()
    query = "SELECT name, time FROM attendance"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Chức năng xuất dữ liệu ra file Excel
def to_excel(dataframe):
    output = BytesIO()  # Sử dụng BytesIO để lưu file Excel vào bộ nhớ
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, sheet_name='Attendance', index=False)
    processed_data = output.getvalue()  # Lấy nội dung của file Excel từ bộ nhớ
    return processed_data

# Xóa tất cả dữ liệu trong bảng attendance
def delete_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    delete_query = "DELETE FROM attendance"
    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()

# Thiết kế giao diện với Streamlit
st.title("BẢNG CHẤM CÔNG ")

# Lấy dữ liệu từ cơ sở dữ liệu
try:
    data = fetch_attendance_data()
    if not data.empty:
        # Lọc theo tên
        search_name = st.text_input("Nhập tên để lọc", "")
        if search_name:
            data_filtered = data[data['name'].str.contains(search_name, case=False, na=False)]
        else:
            data_filtered = data

        # Hiển thị dữ liệu đã lọc
        if not data_filtered.empty:
            st.write("Dữ liệu sau khi lọc:")
            st.dataframe(data_filtered)
        else:
            st.write("Không có dữ liệu phù hợp.")

        # Xuất dữ liệu ra file Excel
        if st.button("Xuất dữ liệu ra Excel"):
            excel_data = to_excel(data_filtered)  # Tạo file Excel
            st.download_button(label="Tải xuống file Excel", data=excel_data, file_name="attendance_data.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # Chức năng xóa tất cả dữ liệu
        if st.button("Xóa tất cả dữ liệu"):
            delete_all_data()
            st.success("Tất cả bản ghi đã được xóa thành công.")

    else:
        st.write("Không có dữ liệu nào trong bảng attendance.")
except Exception as e:
    st.error("Không thể kết nối đến cơ sở dữ liệu.")
    st.write(e)
