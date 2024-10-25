import streamlit as st
import pandas as pd

# Sidebar dengan judul dan dropdown
st.sidebar.title("RYP")  # Judul sidebar
option = st.sidebar.selectbox(  # Dropdown di sidebar
    "Choose HR Option:",  # Teks label dropdown
    ["Select an option", "200HR", "300HR"]  # Opsi dalam dropdown
)

# Tambahkan tombol "Generate" di bawah dropdown
generate_button = st.sidebar.button("Generate")

# Halaman utama
st.title("2025 RYP Student Database")

# Jika tombol "Generate" ditekan
if generate_button:
    # Jika belum memilih atau pilihannya masih 'Select an option'
    if option == "Select an option":
        st.write("Silakan pilih opsi dari dropdown untuk melihat data.")
    
    # Jika memilih 200HR, tampilkan data dari file Excel
    elif option == "200HR":
        st.subheader("Data 200HR Students")
        
        # URL raw dari file Excel di GitHub
        url = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_200hr.xlsx"
        
        # Membaca file Excel langsung dari URL
        df_200hr_stud = pd.read_excel(url)

        # Menampilkan data dalam bentuk tabel
        st.dataframe(df_200hr_stud)

        # Grouping the data sesuai dengan instruksi Anda
        batch_booking_source_200hr = df_200hr_stud.groupby(
            ['Batch start date', 'Batch end date', 'Booking source']
        ).agg({
            'Total Payable (in USD or USD equiv)': 'sum',
            'Total paid (as of today)': 'sum',
            'Student still to pay': 'sum'
        }).unstack(fill_value=0)

        # Menampilkan hasil grouping
        st.subheader("Total Payable x Total Paid x Student still to pay")
        st.dataframe(batch_booking_source_200hr)

    # Jika memilih 300HR, Anda bisa menambahkan logika untuk menampilkan data lainnya
    elif option == "300HR":
        st.subheader("Data untuk 300HR masih belum tersedia.")
