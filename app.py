import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

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
        st.subheader("Grouped Data by 'Batch start date', 'Batch end date', and 'Booking source'")
        st.dataframe(batch_booking_source_200hr)

        # Extract 'Batch start date' and 'Batch end date' from the index and convert them to datetime
        batch_start_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch start date'))
        batch_end_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch end date'))

        # Sort the DataFrame by the converted datetime index values
        batch_booking_source_sorted = batch_booking_source_200hr.copy()
        batch_booking_source_sorted = batch_booking_source_sorted.set_index([batch_start_dates, batch_end_dates])
        batch_booking_source_sorted = batch_booking_source_sorted.sort_index()

        # Convert the sorted dates back to the desired string format for display purposes
        batch_start_dates_sorted = batch_booking_source_sorted.index.get_level_values(0).strftime('%B %d, %Y')
        batch_end_dates_sorted = batch_booking_source_sorted.index.get_level_values(1).strftime('%B %d, %Y')

        # Combine start and end dates for x-axis labels
        batch_dates = [f"{start} to {end}" for start, end in zip(batch_start_dates_sorted, batch_end_dates_sorted)]

        # Extract the data for Total paid and Total payable across all sources
        total_payable_all = batch_booking_source_sorted['Total Payable (in USD or USD equiv)'].sum(axis=1)
        total_paid_all = batch_booking_source_sorted['Total paid (as of today)'].sum(axis=1)

        # Data untuk ECharts
        option_chart = {
            "xAxis": {
                "type": "category",
                "data": batch_dates,
            },
            "yAxis": {
                "type": "value",
            },
            "series": [
                {
                    "data": total_paid_all.tolist(),
                    "type": "line",
                    "smooth": True,
                    "name": "Total Paid (All Sources)",
                },
                {
                    "data": total_payable_all.tolist(),
                    "type": "line",
                    "smooth": True,
                    "name": "Total Payable (in USD or USD equiv)",
                },
            ],
            "tooltip": {
                "trigger": "axis",
            },
            "legend": {
                "data": ["Total Paid (All Sources)", "Total Payable (in USD or USD equiv)"],
            },
        }

        # Tampilkan ECharts di Streamlit
        st_echarts(option_chart)

    # Jika memilih 300HR, Anda bisa menambahkan logika untuk menampilkan data lainnya
    elif option == "300HR":
        st.subheader("Data untuk 300HR masih belum tersedia.")
