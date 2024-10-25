import streamlit as st

# Sidebar dengan judul dan dropdown
st.sidebar.title("RYP")  # Judul sidebar
option = st.sidebar.selectbox(  # Dropdown di sidebar
    "Pilih Kategori:",  # Teks untuk dropdown
    ["200HR", "300HR"]  # Opsi dalam dropdown
)

# Halaman utama
st.title("2025 RYP Student Database")

# Menampilkan pilihan dropdown yang dipilih
# st.sidebar.write(f"Selected: {option}")
