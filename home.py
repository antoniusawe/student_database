import streamlit as st

# Judul halaman
st.title("RYP Student Database")

# Deskripsi singkat
st.write("Selamat datang di RYP Student Database. Silakan klik tombol 'Next' untuk melihat data mahasiswa.")

# Tombol Next
if st.button("Next"):
    # Arahkan pengguna ke app.py (hanya berfungsi di deployment multi-file Streamlit)
    st.experimental_set_query_params(page="app")
