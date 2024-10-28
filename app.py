import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

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
        # st.subheader("Chart")

        # Extract 'Batch start date' and 'Batch end date' dan convert ke bentuk datetime
        batch_start_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch start date'))
        batch_end_dates = pd.to_datetime(batch_booking_source_200hr.index.get_level_values('Batch end date'))

        # sort the DataFrame berdasarkan periode batch
        batch_booking_source_sorted = batch_booking_source_200hr.copy()
        batch_booking_source_sorted = batch_booking_source_sorted.set_index([batch_start_dates, batch_end_dates])
        batch_booking_source_sorted = batch_booking_source_sorted.sort_index()

        # convert datetime ke string format untuk visualisasi
        batch_start_dates_sorted = batch_booking_source_sorted.index.get_level_values(0).strftime('%B %d, %Y')
        batch_end_dates_sorted = batch_booking_source_sorted.index.get_level_values(1).strftime('%B %d, %Y')

        # combine "Batch start date" dan "Batch end date"
        batch_dates = [f"{start} to {end}" for start, end in zip(batch_start_dates_sorted, batch_end_dates_sorted)]

        # ambil data Total paid and Total payable
        total_payable_all = batch_booking_source_sorted['Total Payable (in USD or USD equiv)'].sum(axis=1)
        total_paid_all = batch_booking_source_sorted['Total paid (as of today)'].sum(axis=1)

        # calculate the gap antara Total Payable dan Total Paid
        gap = total_payable_all - total_paid_all

        
        # Plot the lines
        plt.figure(figsize=(10, 6))
        plt.plot(batch_dates, total_paid_all, label="Total Paid (All Sources)", marker='o', color='blue')
        plt.plot(batch_dates, total_payable_all, label="Total Payable (in USD or USD equiv)", marker='o', color='orange', linestyle='--')

        # Add data labels for Total Paid
        for i, txt in enumerate(total_paid_all):
            plt.annotate(f'{txt:.0f}', (batch_dates[i], total_paid_all[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, color='blue')

        # Add data labels for Total Payable
        for i, txt in enumerate(total_payable_all):
            plt.annotate(f'{txt:.0f}', (batch_dates[i], total_payable_all[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, color='orange')

        # Fill the gap between the lines with a color
        plt.fill_between(batch_dates, total_paid_all, total_payable_all, color='#b2b4a3', alpha=0.3)

        # Add data labels for the gap (difference)
        for i, g in enumerate(gap):
            plt.annotate(f'{g:.0f}', (batch_dates[i], (total_paid_all[i] + total_payable_all[i]) / 2), 
                         textcoords="offset points", xytext=(0,0), ha='center', color='red', fontsize=8)

        # Labeling the chart
        wrapped_labels = [label.replace(" to ", "\nto\n") for label in batch_dates]
        wrapped_labels = [label.replace(" ", "\n", 1) for label in wrapped_labels]

        plt.xlabel("Batch Date Range (Start to End)")
        plt.ylabel("Amount")
        plt.xticks(ticks=range(len(batch_dates)), labels=wrapped_labels, rotation=0, ha="center", fontsize=8.3)
        plt.ylim(0, max(total_payable_all) * 1.1)  # Add some padding on top
        plt.legend()

        # Use tight layout
        plt.tight_layout()

        # Show the plot in Streamlit
        st.pyplot(plt)

        # ------------------------
        # Checking unique values and counts in the column "What channel, with which student initiated enquiry?"
        st.subheader("Channel Distribution")
        channel_data = df_200hr_stud['What channel, with which student initiated enquiry? (Booking source capture this for their students)'].value_counts()
        channel_data = channel_data[channel_data.index.str.strip() != '']

        # Display the result to the user for analysis
        st.dataframe(channel_data)

        # Plotting the cleaned channel data in a pie chart
        plt.figure(figsize=(8, 8))
        channel_data.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3'])

        # Adding title
        # plt.title("Composition of Channels Used by Students to Initiate Enquiries (Cleaned)")

        # Equal aspect ratio ensures that the pie is drawn as a circle
        plt.ylabel("")  # Removing the default ylabel for a cleaner look
        plt.tight_layout()

        # Show pie chart in Streamlit
        st.pyplot(plt)

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

        # Extract 'Batch start date' and 'Batch end date' from the index and convert them to datetime
        batch_start_dates = pd.to_datetime(batch_booking_source_300hr.index.get_level_values('Batch start date'))
        batch_end_dates = pd.to_datetime(batch_booking_source_300hr.index.get_level_values('Batch end date'))

        # Sort the DataFrame by the converted datetime index values
        batch_booking_source_sorted = batch_booking_source_300hr.copy()
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

        # Calculate the gap between Total Payable and Total Paid
        gap = total_payable_all - total_paid_all

        # Plot the lines
        plt.figure(figsize=(10, 6))
        plt.plot(batch_dates, total_paid_all, label="Total Paid (All Sources)", marker='o', color='blue')
        plt.plot(batch_dates, total_payable_all, label="Total Payable (in USD or USD equiv)", marker='o', color='orange', linestyle='--')

        # Add data labels for Total Paid
        for i, txt in enumerate(total_paid_all):
            plt.annotate(f'{txt:.0f}', (batch_dates[i], total_paid_all[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, color='blue')

        # Add data labels for Total Payable
        for i, txt in enumerate(total_payable_all):
            plt.annotate(f'{txt:.0f}', (batch_dates[i], total_payable_all[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, color='orange')

        # Fill the gap between the lines with a color
        plt.fill_between(batch_dates, total_paid_all, total_payable_all, color='grey', alpha=0.3)

        # Add data labels for the gap (difference)
        for i, g in enumerate(gap):
            plt.annotate(f'{g:.0f}', (batch_dates[i], (total_paid_all[i] + total_payable_all[i]) / 2), 
                         textcoords="offset points", xytext=(0,0), ha='center', color='red', fontsize=8)

        
        # Labeling the chart
        plt.xlabel("Batch Date Range (Start to End)")
        plt.ylabel("Amount")
        plt.xticks(ticks=range(len(batch_dates)), labels=wrapped_labels, rotation=0, ha="center", fontsize=8)
        plt.ylim(0, max(total_payable_all) * 1.1)  # Add some padding on top
        plt.legend()

        # Use tight layout
        plt.tight_layout()

        # Show the plot in Streamlit
        st.pyplot(plt)

        # ------------------------
        # Checking unique values and counts in the column "What channel, with which student initiated enquiry?"
        st.subheader("Channel Distribution")
        channel_data = df_300hr_stud['What channel, with which student initiated enquiry? (Booking source capture this for their students)'].value_counts()
        channel_data = channel_data[channel_data.index.str.strip() != '']

        # Display the result to the user for analysis
        st.dataframe(channel_data)

        # Plotting the cleaned channel data in a pie chart
        plt.figure(figsize=(8, 8))
        channel_data.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3'])

        # Adding title
        # plt.title("Composition of Channels Used by Students to Initiate Enquiries (Cleaned)")

        # Equal aspect ratio ensures that the pie is drawn as a circle
        plt.ylabel("")  # Removing the default ylabel for a cleaner look
        plt.tight_layout()

        # Show pie chart in Streamlit
        st.pyplot(plt)

        # Adding the conclusion text at the bottom
        st.write("""
        **Direct (new student) - Self-aware of RYP or HOM** memiliki jumlah tertinggi, menunjukkan brand awareness yang kuat.
        **Search Engines** seperti Google dan Safari juga cukup signifikan, mengindikasikan pentingnya optimisasi SEO.
        **Instagram** dan rekomendasi langsung memiliki jumlah yang lebih rendah, menunjukkan potensi untuk penguatan di area ini.
        """)
