import streamlit as st
import pandas as pd

# Periksa query parameter untuk menentukan halaman yang ditampilkan
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]

# Cek apakah halaman saat ini adalah "home"
if page == "home":
    st.write("Anda berada di halaman utama. Silakan kembali ke home.py.")
else:
    # URL dari file Excel di GitHub
    file_url = 'https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_200hr.xlsx'

    st.title("Student Database Viewer")

    # Membaca file Excel dari URL
    try:
        data = pd.read_excel(file_url)

        # Tampilkan data di Streamlit
        st.write("## Student Database")
        st.dataframe(data)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
