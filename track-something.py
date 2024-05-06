import streamlit as st
import pandas as pd
import csv
import time
import os
from datetime import datetime

st.title("Task Tracker")

tab1, tab2 = st.tabs(["Tracker", "Log"])


# Initialize the CSV file, write headings if the file doesn't exist.
storage_file = 'storage.csv'
try:
    with open(storage_file, 'x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Task", "Start_time", "End_time", "Duration"])
except:
    pass


with tab1:

    task = st.text_input('Enter a task')
    start_button, end_button = st.columns(2)

    start_file = 'time_log.csv'
    # Handle the start of a task
    if start_button.button('Start Task'):
        start_time = time.time()
        st.success('Started %s at %s' % (task, format(start_time)))
        with open(start_file, 'w') as csvfile:
            # Create CSV writer
            writer = csv.writer(csvfile)

            # Write current task
            writer.writerow([task])
            # Write current time
            writer.writerow([start_time])

    if end_button.button('End Task'):
        end_time = time.time()

        if os.path.isfile(start_file):
            # Read the first line of file
            with open(start_file, 'r') as f:
                reader = csv.reader(f)
                task = next(reader)[0]
                start_time = float(next(reader)[0])
                duration = end_time - start_time
                st.success('Ended %s at %s' % (task, end_time))
                st.success('Duration of %s = %s' % (task, duration))
            with open(storage_file, 'a', newline='') as log:
                writer = csv.writer(log)
                writer.writerow([task, start_time, end_time, duration])

            # Delete the file
            os.remove(start_file)


with tab2:

    log_data = pd.read_csv(storage_file)
    st.write(log_data)
