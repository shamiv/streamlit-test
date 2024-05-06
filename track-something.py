import streamlit as st
import pandas as pd
import csv
import time
import os
from datetime import datetime
import altair as alt

st.title("Task Tracker")

tab1, tab2, tab3 = st.tabs(["Tracker", "Overview", "Visuals"])

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
        form_start_time = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        st.success('Started %s at %s' % (task, format(form_start_time)))
        with open(start_file, 'w') as csvfile:
            # Create CSV writer
            writer = csv.writer(csvfile)

            # Write current task
            writer.writerow([task])
            # Write current time
            writer.writerow([start_time])

    if end_button.button('End Task'):
        end_time = time.time()
        form_end_time = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

        if os.path.isfile(start_file):
            # Read the first line of file
            with open(start_file, 'r') as f:
                reader = csv.reader(f)
                task = next(reader)[0]

                start_time = float(next(reader)[0])
                form_start_time = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

                duration = end_time - start_time
                hours, rem = divmod(duration, 3600)
                minutes, seconds = divmod(rem, 60)
                form_duration = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)


                st.success('Ended %s at %s' % (task, form_end_time))
                st.success('Duration of %s = %s' % (task, form_duration))

                form_end_time = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

            with open(storage_file, 'a', newline='') as log:
                writer = csv.writer(log)
                writer.writerow([task, form_start_time, form_end_time, form_duration])

            # Delete the file
            os.remove(start_file)


with tab2:

    log_data = pd.read_csv(storage_file)
    st.write(log_data)
    if st.button("Delete all entries"):
        os.remove(storage_file)
        st.rerun()
        
with tab3:

    # Read data
    log_data = pd.read_csv(storage_file)

    # Convert string to datetime
    log_data["Start_time"] = pd.to_datetime(log_data["Start_time"])
    log_data["End_time"] = pd.to_datetime(log_data["End_time"])
    log_data["Duration"] = log_data["Duration"]



    log_data
    # Build chart
    timeline_chart = alt.Chart(log_data).mark_bar().encode(
        x=alt.X('Start_time:T', axis=alt.Axis(format="%Y-%m-%d %H:%M")),
        x2='End_time:T',
        y='Task:N',
        color='Task:N',
        tooltip=[alt.Tooltip('Task:N'),
                alt.Tooltip('Start_time:T', format='%Y-%m-%d %H:%M'),
                alt.Tooltip('End_time:T', format='%Y-%m-%d %H:%M'),
                'Duration']
    )
    st.altair_chart(timeline_chart, use_container_width=True)
    
