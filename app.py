import streamlit as st
import pandas as pd

# Menambahkan Sidebar untuk navigasi
st.sidebar.title("Configuration")
st.sidebar.subheader("Choose your preferred API:")

# Pilihan API dalam bentuk dropdown atau selectbox
api_choice = st.sidebar.selectbox("Select API:", ["API 1", "API 2", "API 3"])

# Tampilkan pilihan API yang dipilih
st.write(f"You selected {api_choice}")

# Fungsi untuk halaman Home
def show_home():
    st.title("2025 RYP Student Database")
    st.write("Selamat datang di RYP Student Database. Silakan klik tombol di sidebar untuk melihat data mahasiswa atau melakukan konfigurasi.")

# Fungsi untuk halaman Data Mahasiswa
def show_student_data():
    st.title("Data Mahasiswa 2025 RYP")

    # Memuat data dari file CSV (ganti 'data_mahasiswa.csv' dengan file yang sesuai)
    try:
        data = pd.read_csv('data_mahasiswa.csv')
        st.write("Berikut adalah data mahasiswa:")
        st.dataframe(data)

        # Filter data berdasarkan nama atau NIM
        search_term = st.text_input("Cari berdasarkan Nama atau NIM:")
        if search_term:
            filtered_data = data[data.apply(lambda row: search_term.lower() in row.to_string().lower(), axis=1)]
            st.write(f"Hasil pencarian untuk '{search_term}':")
            st.dataframe(filtered_data)
    except FileNotFoundError:
        st.error("File data_mahasiswa.csv tidak ditemukan. Pastikan file berada di direktori yang benar.")

# Menampilkan halaman sesuai pilihan di sidebar
page = st.sidebar.selectbox("Pilih Halaman", ["Home", "Data Mahasiswa"])

if page == "Home":
    show_home()
elif page == "Data Mahasiswa":
    show_student_data()
