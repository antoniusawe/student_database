import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import plotly.express as px
import requests
import os
from datetime import datetime
import pytz
from streamlit_echarts import st_echarts

# sidebar
st.sidebar.title("RYP")  # Judul sidebar
option = st.sidebar.selectbox(  # Dropdown di sidebar
    "Choose HR Option:",  # Teks label dropdown
    ["Select an option", "200HR", "300HR"]  # Opsi dalam dropdown
)

# button "Generate"
generate_button = st.sidebar.button("Generate")

st.image("https://raw.githubusercontent.com/antoniusawe/student_database/main/images/house%20of%20om.png", use_column_width=True)

# home
st.title("RYP Student Database")

local_timezone = pytz.timezone("Asia/Makassar")
last_refresh = datetime.now(local_timezone).strftime("%Y-%m-%d %H:%M:%S")

# Display the last refresh time
st.write(f"Last refresh: {last_refresh}")

# fungsi untuk button "Generate"
if generate_button:
    # Jika belum memilih atau pilihannya masih 'Select an option'
    if option == "Select an option":
        st.write("Silakan pilih opsi dari dropdown untuk melihat data.")
    
    # Jika memilih 200HR, tampilkan data dari file Excel
    elif option == "200HR":
        st.subheader("200HR Students Data")
        
        # URL raw dari file Excel di GitHub untuk 200HR
        url = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_200hr.xlsx"
        
        # Membaca file Excel langsung dari URL
        df_200hr_stud = pd.read_excel(url)
        
         # Drop the 'S.No.', 'All', and 'Period' columns if they exist
        columns_to_drop = ['S.No.', 'All', 'Period']
        df_200hr_stud = df_200hr_stud.drop(columns=[col for col in columns_to_drop if col in df_200hr_stud.columns])

        # Menampilkan data dalam bentuk tabel
        st.dataframe(df_200hr_stud)
        
        df_200hr_stud['Batch start date'] = pd.to_datetime(df_200hr_stud['Batch start date'], format='%B %d, %Y')
        df_200hr_stud['Batch end date'] = pd.to_datetime(df_200hr_stud['Batch end date'], format='%B %d, %Y')
        
        
        # Grouping the data
        batch_booking_source_200hr = df_200hr_stud.groupby(
            ['Batch start date', 'Batch end date', 'Booking source']
        ).agg({
            'Total Payable (in USD or USD equiv)': 'sum',
            'Total paid (as of today)': 'sum',
            'Student still to pay': 'sum'
        }).unstack(fill_value=0)

        batch_booking_source_200hr = batch_booking_source_200hr.sort_index(level='Batch start date', ascending=True)
        batch_booking_source_200hr.index = batch_booking_source_200hr.index.set_levels(
            [batch_booking_source_200hr.index.levels[0].strftime('%B %d, %Y'),
             batch_booking_source_200hr.index.levels[1].strftime('%B %d, %Y')],
            level=['Batch start date', 'Batch end date']
        )
        
        # Menampilkan hasil grouping
        st.subheader("Total Payable x Total Paid x Student still to pay")
        st.dataframe(batch_booking_source_200hr)

        # Chart 
        st.subheader("Chart")

        batch_start_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch start date'))
        batch_end_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch end date'))
        
        # Sort DataFrame berdasarkan periode batch
        batch_booking_source_sorted = batch_booking_source_200hr.copy()
        batch_booking_source_sorted = batch_booking_source_sorted.set_index([batch_start_dates, batch_end_dates])
        batch_booking_source_sorted = batch_booking_source_sorted.sort_index()
        
        # Convert datetime ke string format untuk visualisasi
        batch_start_dates_sorted = batch_booking_source_sorted.index.get_level_values(0).strftime('%B %d, %Y')
        batch_end_dates_sorted = batch_booking_source_sorted.index.get_level_values(1).strftime('%B %d, %Y')
        
        # Combine "Batch start date" dan "Batch end date"
        batch_dates = [f"{start} to {end}" for start, end in zip(batch_start_dates_sorted, batch_end_dates_sorted)]
        
        # Ambil data Total paid and Total payable
        total_payable_all = batch_booking_source_sorted['Total Payable (in USD or USD equiv)'].sum(axis=1).round(2).tolist()
        total_paid_all = batch_booking_source_sorted['Total paid (as of today)'].sum(axis=1).round(2).tolist()
        gap_all = [round(payable - paid, 2) for payable, paid in zip(total_payable_all, total_paid_all)]
        
        # Menyusun data untuk ECharts
        options = {
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "cross"},
                "formatter": """{b0}<br />Total Paid: ${c0}<br />Total Payable: ${c1}<br />Gap: ${c2}"""  # Menampilkan tooltip dengan format sederhana
            },
            "legend": {
                "data": ["Total Paid", "Total Payable", "Gap"]
            },
            "xAxis": {
                "type": "category",
                "data": batch_dates,
                "axisLabel": {
                    "interval": 0,
                    "rotate": 45,
                }
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {
                    "formatter": "${value}"  # Format untuk y-axis sebagai mata uang
                }
            },
            "series": [
                {
                    "name": "Total Paid",
                    "type": "line",
                    "data": total_paid_all,
                    "smooth": True,
                    "symbol": "circle",
                    "symbolSize": 8,
                    "itemStyle": {"color": "blue"},
                    "areaStyle": {"color": "rgba(0, 0, 255, 0.2)"},
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "${@[2]}"  # Format angka pada label sebagai mata uang
                    }
                },
                {
                    "name": "Total Payable",
                    "type": "line",
                    "data": total_payable_all,
                    "smooth": True,
                    "symbol": "circle",
                    "symbolSize": 8,
                    "itemStyle": {"color": "orange"},
                    "lineStyle": {"type": "dashed"},
                    "areaStyle": {"color": "rgba(255, 165, 0, 0.3)"},
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "${@[2]}"  # Format angka pada label sebagai mata uang
                    }
                },
                {
                    "name": "Gap",
                    "type": "line",
                    "data": gap_all,
                    "smooth": True,
                    "lineStyle": {"width": 0},  # Menghilangkan garis, hanya area
                    "areaStyle": {"color": "rgba(128, 128, 128, 0.3)"},  # Area transparan untuk Gap
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "${@[2]}"  # Format angka pada label sebagai mata uang
                    },
                    "tooltip": {"show": False}  # Tidak perlu tooltip terpisah untuk Gap
                }
            ]
        }
        
        # Tampilkan chart di Streamlit
        st_echarts(options=options)

        # ------------------------
        # Checking unique values and counts in the column "What channel, with which student initiated enquiry?"
        st.subheader("Channel Distribution")
        channel_data = df_200hr_stud['What channel, with which student initiated enquiry? (Booking source capture this for their students)'].value_counts()
        channel_data = channel_data[channel_data.index.str.strip() != '']

        # Display the result to the user for analysis
        st.dataframe(channel_data)

        # Menyusun data untuk ECharts
        options = {
            "tooltip": {"trigger": "item"},
            "series": [
                {
                    "name": "Channel Distribution",
                    "type": "pie",
                    "radius": ["50%", "80%"],  # Radius lebih besar untuk ruang tambahan
                    "avoidLabelOverlap": True,
                    "label": {
                        "show": True,
                        "position": "outside",
                        "formatter": "{b|{b}}\n{d}%",  # Pengaturan teks untuk menambah baris baru
                        "rich": {  # Menggunakan rich text untuk mengatur label
                            "b": {
                                "width": 80,
                                "overflow": "break"  # Memaksa teks turun jika terlalu panjang
                            }
                        }
                    },
                    "labelLine": {"show": True},  # Garis penghubung untuk label luar
                    "data": [{"value": int(value), "name": str(name)} for name, value in zip(channel_data.index, channel_data.values)]
                }
            ]
        }
        
        # Menampilkan chart
        st_echarts(options=options)
        
        # Menampilkan Judul
        # st.write("Composition of Channels Used by Students to Initiate Enquiries (Cleaned)")

        # Adding the conclusion text at the bottom
        st.write("""
        **Direct (new student) - Self-aware of RYP or HOM** memiliki jumlah tertinggi, menunjukkan brand awareness yang kuat.
        **Search Engines** seperti Google dan Safari juga cukup signifikan, mengindikasikan pentingnya optimisasi SEO.
        **Instagram** dan rekomendasi langsung memiliki jumlah yang lebih rendah, menunjukkan potensi untuk penguatan di area ini.
        """)

    # Jika memilih 300HR, tampilkan data dari file Excel untuk 300HR
    elif option == "300HR":
        st.subheader("300HR Students Data")
        
        # URL raw dari file Excel di GitHub untuk 300HR
        url = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_300hr.xlsx"
        
        # Membaca file Excel langsung dari URL
        df_300hr_stud = pd.read_excel(url)

        columns_to_drop = ['S.No.', 'All', 'Period']
        df_300hr_stud = df_300hr_stud.drop(columns=[col for col in columns_to_drop if col in df_300hr_stud.columns])

        # Menampilkan data dalam bentuk tabel
        st.dataframe(df_300hr_stud)

        df_300hr_stud['Batch start date'] = pd.to_datetime(df_300hr_stud['Batch start date'], format='%B %d, %Y')
        df_300hr_stud['Batch end date'] = pd.to_datetime(df_300hr_stud['Batch end date'], format='%B %d, %Y')

        # Grouping the data sesuai dengan instruksi Anda
        batch_booking_source_300hr = df_300hr_stud.groupby(
            ['Batch start date', 'Batch end date', 'Booking source']
        ).agg({
            'Total Payable (in USD or USD equiv)': 'sum',
            'Total paid (as of today)': 'sum',
            'Student still to pay': 'sum'
        }).unstack(fill_value=0)

        batch_booking_source_300hr = batch_booking_source_300hr.sort_index(level='Batch start date', ascending=True)
        batch_booking_source_300hr.index = batch_booking_source_300hr.index.set_levels(
            [batch_booking_source_300hr.index.levels[0].strftime('%B %d, %Y'),
             batch_booking_source_300hr.index.levels[1].strftime('%B %d, %Y')],
            level=['Batch start date', 'Batch end date']
        )

        # Menampilkan hasil grouping
        st.subheader("Total Payable x Total Paid x Student still to pay")
        st.dataframe(batch_booking_source_300hr)

        # Chart generation section
        # st.subheader("Chart")

        batch_start_dates = pd.to_datetime(batch_booking_source_300hr.index.get_level_values('Batch start date'))
        batch_end_dates = pd.to_datetime(batch_booking_source_300hr.index.get_level_values('Batch end date'))
        
        # Sort DataFrame berdasarkan periode batch
        batch_booking_source_sorted = batch_booking_source_300hr.copy()
        batch_booking_source_sorted = batch_booking_source_sorted.set_index([batch_start_dates, batch_end_dates])
        batch_booking_source_sorted = batch_booking_source_sorted.sort_index()
        
        # Convert datetime ke string format untuk visualisasi
        batch_start_dates_sorted = batch_booking_source_sorted.index.get_level_values(0).strftime('%B %d, %Y')
        batch_end_dates_sorted = batch_booking_source_sorted.index.get_level_values(1).strftime('%B %d, %Y')
        
        # Combine "Batch start date" dan "Batch end date"
        batch_dates = [f"{start} to {end}" for start, end in zip(batch_start_dates_sorted, batch_end_dates_sorted)]
        
        # Ambil data Total paid and Total payable
        total_payable_all = batch_booking_source_sorted['Total Payable (in USD or USD equiv)'].sum(axis=1).round(2).tolist()
        total_paid_all = batch_booking_source_sorted['Total paid (as of today)'].sum(axis=1).round(2).tolist()
        gap_all = [round(payable - paid, 2) for payable, paid in zip(total_payable_all, total_paid_all)]
        
        # Menyusun data untuk ECharts
        options = {
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "cross"},
                "formatter": """{b0}<br />Total Paid: ${c0}<br />Total Payable: ${c1}<br />Gap: ${c2}"""  # Menampilkan tooltip dengan format sederhana
            },
            "legend": {
                "data": ["Total Paid", "Total Payable", "Gap"]
            },
            "xAxis": {
                "type": "category",
                "data": batch_dates,
                "axisLabel": {
                    "interval": 0,
                    "rotate": 45,
                }
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {
                    "formatter": "${value}"  # Format untuk y-axis sebagai mata uang
                }
            },
            "series": [
                {
                    "name": "Total Paid",
                    "type": "line",
                    "data": total_paid_all,
                    "smooth": True,
                    "symbol": "circle",
                    "symbolSize": 8,
                    "itemStyle": {"color": "blue"},
                    "areaStyle": {"color": "rgba(0, 0, 255, 0.2)"},
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "${@[2]}"  # Format angka pada label sebagai mata uang
                    }
                },
                {
                    "name": "Total Payable",
                    "type": "line",
                    "data": total_payable_all,
                    "smooth": True,
                    "symbol": "circle",
                    "symbolSize": 8,
                    "itemStyle": {"color": "orange"},
                    "lineStyle": {"type": "dashed"},
                    "areaStyle": {"color": "rgba(255, 165, 0, 0.3)"},
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "${@[2]}"  # Format angka pada label sebagai mata uang
                    }
                },
                {
                    "name": "Gap",
                    "type": "line",
                    "data": gap_all,
                    "smooth": True,
                    "lineStyle": {"width": 0},  # Menghilangkan garis, hanya area
                    "areaStyle": {"color": "rgba(128, 128, 128, 0.3)"},  # Area transparan untuk Gap
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "${@[2]}"  # Format angka pada label sebagai mata uang
                    },
                    "tooltip": {"show": False}  # Tidak perlu tooltip terpisah untuk Gap
                }
            ]
        }
        
        # Tampilkan chart di Streamlit
        st_echarts(options=options)

        # ------------------------
        # Checking unique values and counts in the column "What channel, with which student initiated enquiry?"
        st.subheader("Channel Distribution")
        channel_data = df_300hr_stud['What channel, with which student initiated enquiry? (Booking source capture this for their students)'].value_counts()
        channel_data = channel_data[channel_data.index.str.strip() != '']

        # Display the result to the user for analysis
        st.dataframe(channel_data)

        # Menyusun data untuk ECharts
        options = {
            "tooltip": {"trigger": "item"},
            "series": [
                {
                    "name": "Channel Distribution",
                    "type": "pie",
                    "radius": ["50%", "80%"],  # Radius lebih besar untuk ruang tambahan
                    "avoidLabelOverlap": True,
                    "label": {
                        "show": True,
                        "position": "outside",
                        "formatter": "{b|{b}}\n{d}%",  # Pengaturan teks untuk menambah baris baru
                        "rich": {  # Menggunakan rich text untuk mengatur label
                            "b": {
                                "width": 80,
                                "overflow": "break"  # Memaksa teks turun jika terlalu panjang
                            }
                        }
                    },
                    "labelLine": {"show": True},  # Garis penghubung untuk label luar
                    "data": [{"value": int(value), "name": str(name)} for name, value in zip(channel_data.index, channel_data.values)]
                }
            ]
        }
        
        # Menampilkan chart
        st_echarts(options=options)

        # Adding title
        # plt.title("Composition of Channels Used by Students to Initiate Enquiries (Cleaned)")

        # Equal aspect ratio ensures that the pie is drawn as a circle
        plt.ylabel("")  # Removing the default ylabel for a cleaner look


        # Adding the conclusion text at the bottom
        st.write("""
        **Direct (new student) - Self-aware of RYP or HOM** memiliki jumlah tertinggi, menunjukkan brand awareness yang kuat.
        **Search Engines** seperti Google dan Safari juga cukup signifikan, mengindikasikan pentingnya optimisasi SEO.
        **Instagram** dan rekomendasi langsung memiliki jumlah yang lebih rendah, menunjukkan potensi untuk penguatan di area ini.
        """)
