import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide")

def fetch_and_save_data_dob_now(selected_date):
    # Base URL for the selected date
    base_url = f"https://data.cityofnewyork.us/resource/rbx6-tga4.json?$where=issued_date >= '{selected_date}T00:00:00' AND issued_date < '{selected_date}T23:59:59'"
    
    try:
        # Fetching the data
        response = requests.get(base_url)
        data = response.json()

        # Converting the data into a pandas DataFrame
        df = pd.DataFrame(data)

        # If 'issued_date' exists, process and save
        if 'issued_date' in df.columns:
            df['issued_date'] = pd.to_datetime(df['issued_date'], errors='coerce')
            df['modified_issued_date'] = df['issued_date'].dt.date
            df = df[['modified_issued_date'] + [col for col in df.columns if col != 'modified_issued_date']]

            # Display the data as a table
            st.dataframe(df)

            # Save the Excel file in the current folder
            filename = f"NYC_DOB_NOW_{selected_date}.xlsx"
            filepath = os.path.join(os.getcwd(), filename)
            df.to_excel(filepath, index=False)

            # Success message
            st.success(f"Data saved to {filename}")
        else:
            st.warning(f"No 'issued_date' data available for {selected_date}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

def fetch_and_save_data_dob_permits(selected_date):
    # Format the date in MM/DD/YYYY format (for the API query)
    formatted_date = selected_date.strftime("%m/%d/%Y")

    # Modify the API URL to apply the specific date filter
    base_url = f"https://data.cityofnewyork.us/resource/ipu4-2q9a.json?$where=issuance_date = '{formatted_date}'"

    try:
        # Fetching the data from the API for the selected date
        response = requests.get(base_url)
        data = response.json()

        # Convert the data to a DataFrame
        df = pd.DataFrame(data)

        # Check if the filtered data is not empty
        if not df.empty:
            # Display the data as a table
            st.dataframe(df)

            # Save the data to an Excel file
            filename = f"DOB_permits_data_{selected_date.strftime('%Y-%m-%d')}.xlsx"
            filepath = os.path.join(os.getcwd(), filename)
            df.to_excel(filename, index=False)

            # Success message
            st.success(f"Data saved to {filename}")
        else:
            st.warning(f"No records found for {selected_date.strftime('%Y-%m-%d')}")

    except KeyError as e:
        st.error(f"A KeyError occurred: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    st.markdown("<h1 style='text-align: center;'>HIRANI ENGINEERING</h1>", unsafe_allow_html=True)
    st.title("NYC DOB Data Fetcher")
    st.subheader("Select which data you would like to explore:")

    # Center align buttons using HTML
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

    # Buttons for selecting DOB NOW or DOB Permits
    selected_option = st.radio("Choose Data Type", ("DOB NOW", "DOB Permits"))
    selected_date = st.date_input("Select Date", value=datetime.now())

    # Button to fetch data
    if st.button("Get Data"):
        formatted_date = selected_date.strftime('%Y-%m-%d')
        if selected_option == "DOB NOW":
            fetch_and_save_data_dob_now(formatted_date)
        elif selected_option == "DOB Permits":
            fetch_and_save_data_dob_permits(selected_date)

    st.markdown("</div>", unsafe_allow_html=True)

# Main entry point
if __name__ == "__main__":
    main()