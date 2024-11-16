# import libraries
import streamlit as st
import pandas as pd

# Define the main function for the "Modeling" page
def main():
    # - Load data
    data = pd.read_csv('data/hour.csv')
    
    st.title("🛠️ Data Cleaning & Processing")

    # 1. Dataset preview
    st.header("1. Dataset Preview")
    st.write("Here are the first 5 rows of the dataset:")
    st.dataframe(data.head())

    # 2. Data types
    st.header("2. Data Types")
    data_types = pd.DataFrame(data.dtypes, columns=['Data type'])
    st.write(data_types)
    st.info("The data type of `dteday` column should be changed to DateTime format.")

    # Data type conversion and merging date with hour
    st.markdown("#### Steps for Data Type Conversion:")
    st.markdown("""
                1. Change `dteday` column to DateTime format.
                2. Combine `dteday` with `hr` to create a complete timestamp.
                3. Set `dteday` as the index and remove the old index.
                """)
    data["dteday"] = pd.to_datetime(data["dteday"], format='%Y-%m-%d')
    data["dteday"] = data["dteday"] + pd.to_timedelta(data['hr'], unit='h')
    data.set_index('dteday', inplace=True)
    
    # Display the data after transformation
    st.write("#### Data Table after Date Transformation")
    st.dataframe(data.head())

    # 3. Missing values 
    st.header("3. Missing Values")
    null_values = pd.DataFrame(data.isnull().sum(), columns=['# of nulls'])
    if null_values['# of nulls'].sum() == 0:
        st.success("No missing values detected in the dataset.")
    else:
        st.write("Here is the count of missing values per column:")
        fig_nulls = px.bar(null_values[null_values['# of nulls'] > 0], y='# of nulls', title="Missing Values by Column")
        st.plotly_chart(fig_nulls)

    # 4. Dropping irrelevant columns
    st.header("4. Removing Irrelevant Columns")
    st.write("The `instant` column is dropped as it is irrelevant.")
    data = data.drop(columns='instant')
    st.write("#### Data Table after Dropping `instant` Column")
    st.dataframe(data.head())

    # 5. Denormalizing values in certain columns
    st.header("5. Denormalizing Values for Interpretability")
    st.markdown("""
                The following columns are denormalized for easier interpretation:
                - `temp`: Scaled to actual temperature in °C.
                - `atemp`: Scaled to apparent temperature in °C.
                - `hum`: Scaled to represent percentage.
                - `windspeed`: Scaled to represent speed in m/s.
                """)
    data['temp'] = data['temp'] * 41
    data['atemp'] = data['atemp'] * 50
    data['hum'] = data['hum'] * 100
    data['windspeed'] = data['windspeed'] * 67

    # Display the data after denormalization
    st.write("#### Data Table after Denormalization")
    st.dataframe(data[['temp', 'atemp', 'hum', 'windspeed']].head())

    # 6. Deriving new columns from existing columns
    # 6.1 Daylight
    st.header("6. Deriving New Columns")

    st.subheader("DayLight")

    st.markdown("""
                A new column, `daylight`, is added to represent 1 if each timestamp falls within daylight hours based on the season:
                - **Spring and Fall**: 7:00 AM to 7:00 PM
                - **Summer**: 6:00 AM to 9:00 PM
                - **Winter**: 7:00 AM to 5:00 PM
                """)

    def add_daylight_column(data):
        data['daylight'] = 0  # Initialize the daylight column

        daylight_hours = {
            1: (7, 0, 19, 0),  # Spring: 7:00 - 19:00
            2: (6, 0, 21, 0),  # Summer: 6:00 - 21:00
            3: (7, 0, 19, 0),  # Fall: 7:00 - 19:00
            4: (7, 0, 17, 0)   # Winter: 7:00 - 17:00
        }

        # Iterate through the DataFrame using the index
        for i in range(len(data)):
            row = data.iloc[i]
            season = row['season']
            hour = data.index[i].hour
            minute = data.index[i].minute

            # Retrieve start and end times for the current season
            start_hour, start_minute, end_hour, end_minute = daylight_hours[season]

            # Check if the time is within daylight hours
            if ((hour > start_hour or (hour == start_hour and minute >= start_minute)) and
                (hour < end_hour or (hour == end_hour and minute <= end_minute))):
                data.at[data.index[i], 'daylight'] = 1  # Set daylight to 1 if within daylight hours

        return data
    
    data = add_daylight_column(data)
    st.write("#### Data Table after Adding 'Daylight' Column")
    st.dataframe(data[['season', 'daylight']].head())

    st.subheader("Temperature Buckets")

    st.markdown("""
                `temp_buckets` categorizes temperature values into 5-degree buckets, making it easy to analyze data within defined temperature ranges.
                """)
    
    # 6.2 Temperature buckets
    # Define temperature buckets in 5-degree intervals
    bins = [0, 5, 10, 15, 20, 25, 30, 35, 40]
    labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40']

    # Apply the temperature bucketing
    data['temp_buckets'] = pd.cut(data['temp'], bins=bins, labels=labels, right=False)
    st.write("#### Data Table after Adding 'Temperature Buckets' Column")
    st.dataframe(data[['temp', 'temp_buckets']].head())

    st.subheader("Wind Speed Bucketing Analysis")
    st.write("""
            `wind_buckets` categorizes wind speeds into descriptive buckets (e.g., Calm, Moderate, Strong), allowing users to understand wind data within specific ranges.
            """)

    # 6.3 Wind buckets
    # Define wind speed buckets with descriptive labels
    bins = [0, 10, 20, 30, 40, 50, 60]
    labels = ['Calm', 'Light', 'Moderate', 'Fresh', 'Strong', 'Gale']

    # Apply wind speed bucketing
    data['wind_buckets'] = pd.cut(data['windspeed'], bins=bins, labels=labels, right=False)
    
    st.write("#### Data Table after Adding 'Wind Buckets' Column")
    st.dataframe(data[['windspeed', 'wind_buckets']].head())

# Check if the script is being run directly
if __name__ == "__main__":
    main()