import os
import requests
import pandas as pd
import streamlit as st
import schedule
import time

url = "http://localhost:3000/download"
data_dir = '/Users/yadnesh/yash/streamletEc2Fetch/streamlit/data'
parquet_file_path = os.path.join(data_dir, 'downloaded_file.parquet')
csv_file_path = os.path.join(data_dir, 'downloaded_file.csv')

def download_file():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        if response.status_code == 200:
            os.makedirs(data_dir, exist_ok=True)
            with open(parquet_file_path, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded and saved at {parquet_file_path}")
        else:
            print(f"Failed to download file: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def process_file():
    try:
        df = pd.read_parquet(parquet_file_path)
        df.to_csv(csv_file_path, index=False)
        print(f"File converted to CSV and saved at {csv_file_path}")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

def display_data():
    try:
        df = pd.read_csv(csv_file_path)
        st.write("Data from CSV file:")
        st.dataframe(df)
    except Exception as e:
        print(f"An error occurred while displaying the data: {e}")

def job():
    download_file()
    process_file()
    display_data()

# Fetch data immediately
job()

# Schedule the job to run every 10 minutes
schedule.every(1).minutes.do(job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)

# import streamlit as st
# from streamlit_autorefresh import st_autorefresh
# import time
# import pandas as pd  # Example if you're working with CSV data

# # Function to fetch and process the file
# def fetch_file():
#     # Replace this with the actual logic for fetching the file
#     file_path = "path/to/your/backend_file.csv"  # Example: Replace with your backend file path
#     try:
#         # Example: Reading a CSV file
#         data = pd.read_csv(file_path)
#         return data
#     except Exception as e:
#         return f"Error loading file: {e}"

# # Automatic refresh every 10 minutes (10 minutes = 600 seconds)
# # Use `st_autorefresh` to trigger rerun without full page refresh
# refresh_interval = 10 * 60 * 1000  # 10 minutes in milliseconds
# st_autorefresh(interval=refresh_interval, key="data_refresh")

# # Fetch the data
# st.title("Dynamic File Analysis")
# data = fetch_file()

# # Display the data or analysis
# if isinstance(data, pd.DataFrame):
#     st.write("Updated Data (Every 10 minutes):")
#     st.dataframe(data)
# else:
#     st.error(data)  # Show error if file loading fails

# # Add any additional visualization or analysis logic here
