import streamlit as st
import pandas as pd

# Sidebar dengan judul dan dropdown
st.sidebar.title("RYP")  # Judul sidebar
option = st.sidebar.selectbox(  # Dropdown di sidebar
    "Choose HR Option:",  # Teks untuk dropdown
    ["200HR", "300HR"]  # Opsi dalam dropdown
)

# Halaman utama
st.title("2025 RYP Student Database")

# Jika memilih 200HR, tampilkan data dari file Excel
if option == "200HR":
    st.subheader("Data 200HR Students")
    
    # URL raw dari file Excel di GitHub
    url = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_200hr.xlsx"
    
    # Membaca file Excel langsung dari URL
    data = pd.read_excel(url)

    # Menampilkan data dalam bentuk tabel
    st.dataframe(data)
else:
    st.write("Silakan pilih opsi dari dropdown.")
