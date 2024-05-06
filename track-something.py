import streamlit as st
import pandas as pd
import csv
import time
import os
from datetime import datetime
import altair as alt

# Title of app
st.title("Task Tracker")

# This app consists of three tabs
tab1, tab2, tab3 = st.tabs(["Tracker", "Overview", "Visuals"])

# Name of main database file
storage_file = 'storage.csv'

# Initialize the CSV file, write headings if the file doesn't exist.
try:
    with open(storage_file, 'x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Task", "Start_time", "End_time", "Duration"])
except:
    pass

# This determines the content of tab1
with tab1:


    # Ask user for the name of the task
    task = st.text_input('Enter a task')

    # This tab has two columns, called start_button and end_button
    start_button, end_button = st.columns(2)

    # Every time you click a button, this script runs again
    # To remember the start time, we need to (temporarily) store it
    # This is where I define the name of that file.
    start_file = 'time_log.csv'

    # This creates a button (on the column "start_button") with the text "Start Task"
    # And checks if the button is pressed.
    if start_button.button('Start Task'):

        # If that button is pressed...
        # Get the time of that moment
        start_time = time.time()

        # Turn that time in a human readable format
        form_start_time = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

        # Show (in green) a statement indicating success
        st.success('Started %s at %s' % (task, format(form_start_time)))


        # Write the start time to the above-mentioned file
        with open(start_file, 'w') as csvfile:
            # Create CSV writer
            writer = csv.writer(csvfile)

            # Write current task
            writer.writerow([task])
            # Write current time
            writer.writerow([start_time])


    # This creates a button on the "end_button" column, and checks if it is pressed.
    if end_button.button('End Task'):

        # if it is pressed, get the end time
        end_time = time.time()
        # Get the end time in a human readable format
        form_end_time = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')


        # if there is a file with a start time
        if os.path.isfile(start_file):
            # Read the first line of file
            with open(start_file, 'r') as f:
                reader = csv.reader(f)

                # "next" is the "cursor" going down in the csv
                task = next(reader)[0]

                start_time = float(next(reader)[0])
                form_start_time = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

                duration = end_time - start_time

                # see p. 117 of Downey what divmod does 
                hours, rem = divmod(duration, 3600)
                minutes, seconds = divmod(rem, 60)

                # This a new way of formatting a string
                form_duration = "%02d:%02d:%05.2f" % (int(hours), int(minutes), seconds)

                # 
                st.success('Ended %s at %s' % (task, form_end_time))
                st.success('Duration of %s = %s' % (task, form_duration))

                form_end_time = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

            with open(storage_file, 'a', newline='') as log:
                writer = csv.writer(log)
                writer.writerow([task, form_start_time, form_end_time, form_duration])

            # Delete the file that kept the starting time
            os.remove(start_file)

# this describes what happens in tab 2
with tab2:

    # To view the contents of the storage file we use pandas
    log_data = pd.read_csv(storage_file)
    st.write(log_data)

    # This is to delete all entries
    if st.button("Delete all entries"):
        os.remove(storage_file)

        # This is to rerun the page after all entries are deleted
        st.rerun()
        
# This describes what happens in tab 3
with tab3:

    # Read data
    log_data = pd.read_csv(storage_file)

    # Convert string to datetime (datetime is a special type/class).
    log_data["Start_time"] = pd.to_datetime(log_data["Start_time"])
    log_data["End_time"] = pd.to_datetime(log_data["End_time"])
    log_data["Duration"] = log_data["Duration"]

    # The visualization uses a libraray called altair. See documentation.
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
    
