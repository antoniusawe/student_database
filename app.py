import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# URL raw dari file Excel di GitHub untuk 200HR dan 300HR
url_200hr = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_200hr.xlsx"
url_300hr = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_300hr.xlsx"

# Load CSS untuk styling
st.markdown("""
    <style>
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding: 20px;
    }

    /* Dropdown styling */
    select {
        border: 2px solid #4CAF50;
        padding: 5px;
        font-size: 16px;
    }

    /* Table Styling */
    .responsive-table {
        max-width: 100%;
        overflow-x: auto;
        margin-top: 10px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th, td {
        text-align: left;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }

    th {
        background-color: #4CAF50;
        color: white;
    }

    /* Responsive adjustments */
    @media only screen and (max-width: 600px) {
        td, th {
            font-size: 12px;
            padding: 6px;
        }
    }

    /* Title Styling */
    .main-title {
        font-size: 36px;
        color: #333333;
        text-align: center;
    }

    /* Subheader Styling */
    .sub-header {
        font-size: 24px;
        color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar dengan judul dan dropdown
st.sidebar.title("RYP")  # Judul sidebar
option = st.sidebar.selectbox(
    "Choose HR Option:",
    ["Select an option", "200HR", "300HR"]
)

# Tombol Generate
generate_button = st.sidebar.button("Generate")

# Halaman utama
st.markdown('<h1 class="main-title">2025 RYP Student Database</h1>', unsafe_allow_html=True)

# Jika tombol "Generate" ditekan
if generate_button:
    # Jika belum memilih opsi
    if option == "Select an option":
        st.write("Silakan pilih opsi dari dropdown untuk melihat data.")

    # Menampilkan data 200HR jika dipilih
    elif option == "200HR":
        st.markdown('<h2 class="sub-header">Data 200HR Students</h2>', unsafe_allow_html=True)

        # Membaca file Excel langsung dari URL
        df_200hr_stud = pd.read_excel(url_200hr)
        
        # Menampilkan data dalam bentuk tabel responsif
        st.markdown('<div class="responsive-table">', unsafe_allow_html=True)
        st.write(df_200hr_stud.to_html(index=False), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Mengelompokkan data sesuai instruksi
        batch_booking_source_200hr = df_200hr_stud.groupby(
            ['Batch start date', 'Batch end date', 'Booking source']
        ).agg({
            'Total Payable (in USD or USD equiv)': 'sum',
            'Total paid (as of today)': 'sum',
            'Student still to pay': 'sum'
        }).unstack(fill_value=0)

        # Menampilkan hasil grouping
        st.markdown('<h2 class="sub-header">Total Payable x Total Paid x Student still to pay</h2>', unsafe_allow_html=True)
        st.write(batch_booking_source_200hr)

        # Generate chart
        batch_start_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch start date'))
        batch_end_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch end date'))
        batch_booking_source_sorted = batch_booking_source_200hr.set_index([batch_start_dates, batch_end_dates]).sort_index()

        batch_dates = [f"{start} to {end}" for start, end in zip(
            batch_booking_source_sorted.index.get_level_values(0).strftime('%B %d, %Y'),
            batch_booking_source_sorted.index.get_level_values(1).strftime('%B %d, %Y')
        )]

        total_payable_all = batch_booking_source_sorted['Total Payable (in USD or USD equiv)'].sum(axis=1)
        total_paid_all = batch_booking_source_sorted['Total paid (as of today)'].sum(axis=1)

        plt.figure(figsize=(10, 6))
        plt.plot(batch_dates, total_paid_all, label="Total Paid (All Sources)", marker='o', color='blue')
        plt.plot(batch_dates, total_payable_all, label="Total Payable (in USD or USD equiv)", marker='o', color='orange', linestyle='--')
        plt.fill_between(batch_dates, total_paid_all, total_payable_all, color='grey', alpha=0.3)
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Batch Date Range (Start to End)")
        plt.ylabel("Amount")
        plt.legend()
        plt.tight_layout()

        st.pyplot(plt)

    # Menampilkan data 300HR jika dipilih
    elif option == "300HR":
        st.markdown('<h2 class="sub-header">Data 300HR Students</h2>', unsafe_allow_html=True)
        df_300hr_stud = pd.read_excel(url_300hr)

        st.markdown('<div class="responsive-table">', unsafe_allow_html=True)
        st.write(df_300hr_stud.to_html(index=False), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        batch_booking_source_300hr = df_300hr_stud.groupby(
            ['Batch start date', 'Batch end date', 'Booking source']
        ).agg({
            'Total Payable (in USD or USD equiv)': 'sum',
            'Total paid (as of today)': 'sum',
            'Student still to pay': 'sum'
        }).unstack(fill_value=0)

        st.markdown('<h2 class="sub-header">Total Payable x Total Paid x Student still to pay</h2>', unsafe_allow_html=True)
        st.write(batch_booking_source_300hr)
