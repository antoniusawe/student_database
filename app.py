import streamlit as st
import pandas as pd

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
