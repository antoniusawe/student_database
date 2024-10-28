import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sidebar
st.sidebar.title("RYP")  # Judul sidebar
option = st.sidebar.selectbox(
    "Choose HR Option:",
    ["Select an option", "200HR", "300HR"]
)

# Button "Generate"
generate_button = st.sidebar.button("Generate")

st.image("https://raw.githubusercontent.com/antoniusawe/student_database/main/images/house%20of%20om.png", use_column_width=True)

# Home
st.title("2025 RYP Student Database")

# Fungsi untuk button "Generate"
if generate_button:
    if option == "Select an option":
        st.write("Silakan pilih opsi dari dropdown untuk melihat data.")
    
    elif option == "200HR":
        st.subheader("Data 200HR Students")
        
        # URL file Excel untuk 200HR
        url = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_200hr.xlsx"
        
        # Membaca file Excel
        df_200hr_stud = pd.read_excel(url)
        st.dataframe(df_200hr_stud)
                
        # Grouping the data
        batch_booking_source_200hr = df_200hr_stud.groupby(
            ['Batch start date', 'Batch end date', 'Booking source']
        ).agg({
            'Total Payable (in USD or USD equiv)': 'sum',
            'Total paid (as of today)': 'sum',
            'Student still to pay': 'sum'
        })

        # Sorting by 'Batch start date' and 'Batch end date'
        batch_booking_source_200hr = batch_booking_source_200hr.sort_index(level=[0, 1])
        st.subheader("Total Payable x Total Paid x Student still to pay (Sorted)")
        st.dataframe(batch_booking_source_200hr)

        # Mengambil 'Batch start date' dan 'Batch end date' dan konversi ke string
        batch_start_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch start date'))
        batch_end_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch end date'))
        
        # Membuat label tanggal untuk sumbu X
        batch_dates = [f"{start.strftime('%B %d, %Y')} to {end.strftime('%B %d, %Y')}" 
                       for start, end in zip(batch_start_dates, batch_end_dates)]

        # Ambil data Total paid dan Total payable
        total_payable_all = batch_booking_source_200hr['Total Payable (in USD or USD equiv)']
        total_paid_all = batch_booking_source_200hr['Total paid (as of today)']

        # Menghitung selisih antara Total Payable dan Total Paid
        gap = total_payable_all - total_paid_all

        # Membuat Plot
        plt.figure(figsize=(10, 6))
        plt.plot(batch_dates, total_paid_all, label="Total Paid (All Sources)", marker='o', color='blue')
        plt.plot(batch_dates, total_payable_all, label="Total Payable (in USD or USD equiv)", marker='o', color='orange', linestyle='--')

        # Menambahkan data labels untuk Total Paid
        for i, txt in enumerate(total_paid_all):
            plt.annotate(f'{txt:.0f}', (batch_dates[i], total_paid_all[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, color='blue')

        # Menambahkan data labels untuk Total Payable
        for i, txt in enumerate(total_payable_all):
            plt.annotate(f'{txt:.0f}', (batch_dates[i], total_payable_all[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, color='orange')

        # Mengisi selisih antara garis
        plt.fill_between(batch_dates, total_paid_all, total_payable_all, color='#b2b4a3', alpha=0.3)

        # Menambahkan data labels untuk selisih (gap)
        for i, g in enumerate(gap):
            plt.annotate(f'{g:.0f}', (batch_dates[i], (total_paid_all[i] + total_payable_all[i]) / 2), 
                         textcoords="offset points", xytext=(0,0), ha='center', color='red', fontsize=8)

        # Memberi label pada chart
        plt.xlabel("Batch Date Range (Start to End)")
        plt.ylabel("Amount")
        plt.xticks(rotation=45, ha="right")
        plt.ylim(0, max(total_payable_all) * 1.1)
        plt.legend()
        plt.tight_layout()

        # Menampilkan plot di Streamlit
        st.pyplot(plt)

        # Distribusi Channel
        st.subheader("Channel Distribution")
        channel_data = df_200hr_stud['What channel, with which student initiated enquiry? (Booking source capture this for their students)'].value_counts()
        channel_data = channel_data[channel_data.index.str.strip() != '']

        # Menampilkan data channel
        st.dataframe(channel_data)

        # Membuat Pie Chart untuk distribusi channel
        plt.figure(figsize=(8, 8))
        channel_data.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3'])
        plt.ylabel("")
        plt.tight_layout()
        st.pyplot(plt)

        # Menambahkan kesimpulan
        st.write("""
        **Direct (new student) - Self-aware of RYP or HOM** memiliki jumlah tertinggi, menunjukkan brand awareness yang kuat.
        **Search Engines** seperti Google dan Safari juga cukup signifikan, mengindikasikan pentingnya optimisasi SEO.
        **Instagram** dan rekomendasi langsung memiliki jumlah yang lebih rendah, menunjukkan potensi untuk penguatan di area ini.
        """)

    # Jika memilih 300HR, tampilkan data dari file Excel untuk 300HR
    elif option == "300HR":
        st.subheader("Data 300HR Students")
        
        # URL file Excel untuk 300HR
        url = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_300hr.xlsx"
        
        # Membaca file Excel
        df_300hr_stud = pd.read_excel(url)
        st.dataframe(df_300hr_stud)

        # Grouping the data sesuai dengan instruksi Anda
        batch_booking_source_300hr = df_300hr_stud.groupby(
            ['Batch start date', 'Batch end date', 'Booking source']
        ).agg({
            'Total Payable (in USD or USD equiv)': 'sum',
            'Total paid (as of today)': 'sum',
            'Student still to pay': 'sum'
        }).sort_index(level=[0, 1])

        # Menampilkan hasil grouping yang sudah diurutkan
        st.subheader("Total Payable x Total Paid x Student still to pay (Sorted)")
        st.dataframe(batch_booking_source_300hr)
