import streamlit as st
import pandas as pd

# Fungsi untuk halaman Home
def show_home():
    st.title("RYP Student Database")
    st.write("Selamat datang di RYP Student Database. Silakan klik tombol 'Next' untuk melihat data mahasiswa.")
    
    # Tombol untuk pindah ke halaman berikutnya
    if st.button("Next"):
        st.session_state.page = "app"  # Mengubah session state ke halaman app

# Fungsi untuk halaman App
def show_app():
    st.title("Student Database Viewer")
    
    file_url = 'https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_200hr.xlsx'
    
    try:
        # Membaca file Excel dari URL
        data = pd.read_excel(file_url)

        # Tampilkan data di Streamlit
        st.write("## Student Database")
        st.dataframe(data)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
    
    # Tombol untuk kembali ke halaman Home
    if st.button("Back"):
        st.session_state.page = "home"  # Mengubah session state ke halaman home

# Pengaturan default untuk session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Kondisi untuk menampilkan halaman berdasarkan session state
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'app':
    show_app()
