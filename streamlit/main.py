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