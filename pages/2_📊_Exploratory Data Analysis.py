# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns


# Define the main function for the "Modeling" page
def main():
    # Load data 
    data_cleaned = pd.read_csv('data/data_cleaned.csv')

    # Define mappings for different groupings
    month_mapping = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Autumn', 4: 'Winter'}
    weekday_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
    workingday_mapping = {0: 'Non-Working Day', 1: 'Working Day'}

    st.title("Analyzing Bike-Sharing Trends")
    st.write("### Seasonal Patterns, User Behavior, and Weather Impact")

    # 1. Total Rentals for 2011 and 2012
    st.header("1. Total rentals per year (2011 vs. 2012)")
    st.info(
    """
    ##### Key Insights:
    - The provided dataset covers bike rentals from 2011 and 2012.
    - A comparison between the two years reveals a **clear upward trend** in bike rentals.
    """)

    # Group and plot total rentals by year
    rental_summary = data_cleaned.groupby('yr')['cnt'].sum()
    fig = go.Figure(data=[go.Bar(x=['2011', '2012'], 
                                y=rental_summary.values / 1_000_000, 
                                marker=dict(color='skyblue'))])

    # Add total annotations and layout customization
    for i, value in enumerate(rental_summary.values / 1_000_000):
        fig.add_annotation(
            x=i,
            y=value + 0.1,
            text=f"<b>Total: {value:.2f}M</b>",
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center"
        )

    fig.update_layout(
        title='Total Rentals for the Year 2011 and 2012',
        xaxis_title='Year',
        yaxis_title='Total Rentals (in millions)',
        template='plotly_white'
    )

    st.plotly_chart(fig)

    # 2. Total Rentals for each month in 2011 and 2012
    st.header("2. Seasonal Surplus in 2012")
    st.info(
    """
    ##### Key Insights:
    - The increase in bike rentals is spread across the entire year.
    - Notable peaks observed:
        - **March / April**
        - **August to October**
    """)

    monthly_delta = (data_cleaned[data_cleaned['yr'] == 1].groupby('mnth')['cnt'].sum()) - (data_cleaned[data_cleaned['yr'] == 0]
                                                                                            .groupby('mnth')['cnt'].sum())

    # Create the bar chart with all months including January
    fig = go.Figure(data=[go.Bar(
        x=monthly_delta.index,  # Use the month index directly for x-axis
        y=monthly_delta.values / 10_000,  # Convert to 10k
        hoverinfo='none',  # No hover text on the bars
        marker=dict(color='skyblue')
    )])

    # Add annotations for the total values above each bar
    for i, value in enumerate(monthly_delta.values / 10_000):  # Convert to 10k
        fig.add_annotation(
            x=monthly_delta.index[i],  # Use the correct x-value from the month index
            y=value + 1,  # Add a small offset above the bar for visibility
            text=f"<b>{value:.1f}k</b>",  # Bold value text with 'k'
            showarrow=False,
            font=dict(size=12, color="black", family="Arial"),
            align="center")

    # Customize layout
    fig.update_layout(
        title='Monthly Rental Surplus 2012',
        xaxis_title='Month',
        yaxis_title='Total Rentals (in 10k)',
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext=['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']),
        template='plotly_white')
    st.plotly_chart(fig)
    

    # 3. Number of Bikes Rented per Week
    st.header("3. Yearly Patterns & User Trends")
    st.info(
    """
    ##### Key Insights:
    - The yearly pattern remains similar with **the peak in summer** and **the bottom in winter**.
    - Both casual and registered users use bike-sharing year-round, with **registered users** being the **majority**.
    """)

    # Ensure datetime index and resample weekly
    if 'dteday' in data_cleaned.columns:
        data_cleaned['dteday'] = pd.to_datetime(data_cleaned['dteday'])
        data_cleaned.set_index('dteday', inplace=True)

        # Resample monthly, summing rentals for each month
        data_cleaned['cnt'].resample('M').sum().plot(linewidth=6, label='Total', color = 'skyblue')
        data_cleaned['casual'].resample('M').sum().plot(linewidth=2, label='Casual', color= 'magenta')
        data_cleaned['registered'].resample('M').sum().plot(linewidth=2, label='Registered', color = 'lightgreen')

    # Resample monthly, summing rentals for each month
    monthly_data = pd.DataFrame({
        'Total': data_cleaned['cnt'].resample('M').sum(),
        'Casual': data_cleaned['casual'].resample('M').sum(),
        'Registered': data_cleaned['registered'].resample('M').sum()
    })

    # Melt the DataFrame to have a long format suitable for Plotly Express
    monthly_data = monthly_data.reset_index().melt(
        id_vars='dteday', value_vars=['Total', 'Casual', 'Registered'],
        var_name='User Type', value_name='Bike Rentals'
    )

    # Create the line chart with Plotly Express
    fig = px.line(
        monthly_data,
        x='dteday',
        y='Bike Rentals',
        color='User Type',
        title='Monthly Trends by User Type',
        labels={'dteday': 'Months', 'Bike Rentals': 'Bike Rentals'}
    )

    # Generate tick values for every 3 months
    start_date = monthly_data['dteday'].min()
    end_date = monthly_data['dteday'].max()
    tickvals = pd.date_range(start=start_date, end=end_date, freq='3MS')  # '3MS' for 3-month start frequency


    # Update layout for cleaner appearance
    fig.update_layout(
        plot_bgcolor='white'
    )

    # Customize the x-axis to show both month and year
    fig.update_xaxes(
        tickformat="%b\n%Y",  # Format as abbreviated month and year with a line break
        tickangle=0,  # No rotation of the ticks
        tickvals=tickvals
    )

    # Set specific colors for each trace   
    color_map = {'Total': 'skyblue', 'Casual': 'magenta', 'Registered': 'lightgreen'}
    for trace in fig.data:
        trace.marker.color = color_map[trace.name]  # Set the line color based on trace name
        trace.line.color = color_map[trace.name]  # Apply color to the line

    st.plotly_chart(fig)

    # 4.1 Rentals by Season, Month, Weekday, and Working/Non-Working Day
    st.header("4 Monthly & Seasonal Trends")
    st.info(
    """
    ##### Key Insights:
    - Rentals increase from March, peaking in summer, with a **higher proportion of casual users**, indicating increased tourist activity during these months.
    """)

    view_option = st.selectbox("Select View", ["Month", "Season", "Weekday", "Working/Non-Working Day"])

    col1, col2 = st.columns(2)

    # 4.1.1 Season Analysis
    with col1:
        if view_option == "Season":
            season_distribution = data_cleaned.groupby('season')[['registered', 'casual']].mean().reset_index()
            season_distribution['season'] = season_distribution['season'].replace(season_mapping)

            # Melt the data for stacked plotting
            season_distribution = season_distribution.melt(id_vars='season', 
                                                        value_vars=['registered', 'casual'], 
                                                        var_name='user_type', 
                                                        value_name='count')
            # Create the stacked bar chart
            fig = px.bar(season_distribution, 
                        x='season', 
                        y='count', 
                        color='user_type', 
                        labels={'season': 'Season', 'count': 'Average Rentals'}, 
                        color_discrete_map={'registered': 'lightgreen', 'casual': 'magenta'}, 
                        title='Average Bike Rentals by Season')
            fig.update_xaxes(categoryorder='array', categoryarray=['Spring', 'Summer', 'Autumn', 'Winter'])
            st.plotly_chart(fig)

        # 4.1.2 Month Analysis
        elif view_option == "Month":
            month_distribution = data_cleaned.groupby('mnth')[['registered', 'casual']].mean().reset_index()
            month_distribution['mnth'] = month_distribution['mnth'].replace(month_mapping)

            # Melt the data for stacked plotting
            month_distribution = month_distribution.melt(id_vars='mnth', 
                                                        value_vars=['registered', 'casual'], 
                                                        var_name='user_type', 
                                                        value_name='count')
            
            # Create the stached bar chart
            fig = px.bar(month_distribution, 
                        x='mnth', 
                        y='count', 
                        color='user_type', 
                        labels={'mnth': 'Month', 'count': 'Average Rentals'}, 
                        color_discrete_map={'registered': 'lightgreen', 'casual': 'magenta'}, 
                        title='Average Bike Rentals per Month')
            fig.update_xaxes(categoryorder='array', categoryarray=list(month_mapping.values()))
            st.plotly_chart(fig)

        # 4.1.3 Weekday Analysis
        elif view_option == "Weekday":
            weekday_distribution = data_cleaned.groupby('weekday')[['registered', 'casual']].mean().reset_index()
            weekday_distribution['weekday'] = weekday_distribution['weekday'].replace(weekday_mapping)
            weekday_distribution = weekday_distribution.melt(id_vars='weekday', value_vars=['registered', 'casual'], var_name='user_type', value_name='count')
            fig = px.bar(weekday_distribution, 
                        x='weekday', 
                        y='count', 
                        color='user_type', 
                        labels={'weekday': 'Weekday', 'count': 'Average Rentals'}, 
                        color_discrete_map={'registered': 'lightgreen', 'casual': 'magenta'}, 
                        title='Average Bike Rentals per Weekday')
            fig.update_xaxes(categoryorder='array', categoryarray=list(weekday_mapping.values()))
            st.plotly_chart(fig)

        # 4.1.4 Working/Non-Working Day Analysis
        elif view_option == "Working/Non-Working Day":
            workingday_distribution = data_cleaned.groupby('workingday')[['registered', 'casual']].mean().reset_index()
            workingday_distribution['workingday'] = workingday_distribution['workingday'].replace(workingday_mapping)

            # Melt the data for stacked plotting
            workingday_distribution = workingday_distribution.melt(id_vars='workingday', 
                                                                value_vars=['registered', 'casual'], 
                                                                var_name='user_type', 
                                                                value_name='count')
            
            # Create the stached bar chart
            fig = px.bar(workingday_distribution, 
                        x='workingday', 
                        y='count', 
                        color='user_type', 
                        labels={'workingday': 'Day Type', 'count': 'Average Rentals'}, 
                        color_discrete_map={'registered': 'lightgreen', 'casual': 'magenta'}, 
                        title='Average Bike Rentals by Working/Non-Working Day')
            st.plotly_chart(fig)

    with col2:
        # Function to generate line chart based on selected view option
        def generate_share_chart(data, view_option):
            if view_option == "Month":
                # Group by month and calculate share of casual users
                grouped_data = (data.groupby('mnth')['casual'].sum() / data.groupby('mnth')['cnt'].sum()).reset_index()
                grouped_data.columns = ['mnth', 'share_of_casual_users']
                grouped_data['share_of_casual_users'] *= 100
                grouped_data['mnth'] = grouped_data['mnth'].replace(month_mapping)

                x_title = 'Month'
                x_order = list(month_mapping.values())

            elif view_option == "Season":
                # Group by season and calculate share of casual users
                grouped_data = (data.groupby('season')['casual'].sum() / data.groupby('season')['cnt'].sum()).reset_index()
                grouped_data.columns = ['season', 'share_of_casual_users']
                grouped_data['share_of_casual_users'] *= 100
                grouped_data['season'] = grouped_data['season'].replace(season_mapping)

                x_title = 'Season'
                x_order = ['Spring', 'Summer', 'Autumn', 'Winter']

            elif view_option == "Weekday":
                # Group by weekday and calculate share of casual users
                grouped_data = (data.groupby('weekday')['casual'].sum() / data.groupby('weekday')['cnt'].sum()).reset_index()
                grouped_data.columns = ['weekday', 'share_of_casual_users']
                grouped_data['share_of_casual_users'] *= 100
                grouped_data['weekday'] = grouped_data['weekday'].replace(weekday_mapping)

                x_title = 'Weekday'
                x_order = list(weekday_mapping.values())

            elif view_option == "Working/Non-Working Day":
                # Group by working day and calculate share of casual users
                grouped_data = (data.groupby('workingday')['casual'].sum() / data.groupby('workingday')['cnt'].sum()).reset_index()
                grouped_data.columns = ['workingday', 'share_of_casual_users']
                grouped_data['share_of_casual_users'] *= 100
                grouped_data['workingday'] = grouped_data['workingday'].replace(workingday_mapping)

                x_title = 'Day Type'
                x_order = ['Non-Working Day', 'Working Day']

            # Create the line chart
            fig = px.line(
                grouped_data,
                x=grouped_data.columns[0],
                y='share_of_casual_users',
                title=f'Share of Casual Bike Rentals by {view_option} (%)',
                labels={grouped_data.columns[0]: x_title, 'share_of_casual_users': 'Share of Casual Users (%)'}
            )

            fig.update_traces(line=dict(color='magenta'))
            fig.update_xaxes(categoryorder='array', categoryarray=x_order)
            fig.update_layout(plot_bgcolor='white')

            st.plotly_chart(fig, key=f"{view_option}_chart")

        generate_share_chart(data_cleaned, view_option)

    # 5. Hourly Rental Patterns Based on Day Type
    st.header("5. Impact of Weekends & Holidays")
    st.info(
    """
    ##### Key Insights:
    - Bike rentals peak during **rush hours** (8 am, 5 pm, and 6 pm) on workdays and in the **early afternoon** on holidays.
    """)

    day_type_option = st.selectbox("Select Day Type", ["Working Days", "Holidays", "All Days"])

    # Filter the data by day type
    if day_type_option == "Working Days":
        filtered_data = data_cleaned[data_cleaned['workingday'] == 1]
    elif day_type_option == "Holidays":
        filtered_data = data_cleaned[data_cleaned['workingday'] == 0]
    else:
        filtered_data = data_cleaned
    
    # Create the distribution for each data type
    hourly_distribution = filtered_data.groupby('hr')['cnt'].mean().reset_index()
    
    # Calculate the Mean of Bike Rentals for 'All Days'
    overall_avg_rentals = hourly_distribution['cnt'].mean()

    # Create the bar charts
    fig = px.bar(hourly_distribution, 
                x='hr', 
                y='cnt', 
                labels={'hr': 'Hour of Day', 'cnt': 'Average Rentals'}, 
                color_discrete_sequence=['skyblue'], 
                title=f'Average Bike Rentals per Hour ({day_type_option})')
    
    # Create an average line
    fig.add_scatter(x=hourly_distribution['hr'], 
                    y=[overall_avg_rentals] * len(hourly_distribution), 
                    mode='lines', 
                    name='Overall Average', 
                    line=dict(color='red', dash='dash'))
    st.plotly_chart(fig)

    # 6. Heatmaps for Weather, Temperature, and Wind Condition
    st.header("6. Weather Impact on Rentals")
    st.info(
    """
    ##### Key Insights:
    - Bike rentals **increase with temperature** but drop in extreme heat.
    - Sunny days boost rentals, while rain and strong wind deter them.
    """)

    analysis_option = st.selectbox("Select Analysis Type", ["Temperature Buckets", "Weather Condition", "Wind Condition"])

    # 6.1 Weather Condition Analysis
    if analysis_option == "Weather Condition":
        heatmap_data = data_cleaned.groupby(['hr', 'weathersit'])['cnt'].mean().reset_index()
        heatmap_data['weathersit'] = heatmap_data['weathersit'].replace({1: 'Sunny', 2: 'Cloudy', 3: 'Light Rain', 4: 'Heavy Rain'})
        fig = px.density_heatmap(heatmap_data, 
                                x='hr', 
                                y='weathersit', 
                                z='cnt', 
                                color_continuous_scale='Viridis', 
                                labels={'hr': 'Hour of Day', 'weathersit': 'Weather Condition', 'cnt': 'Average Rentals'}, 
                                title='Average Hourly Bike Rentals by Weather Condition')
        st.plotly_chart(fig)

    # 6.2 Temperature Buckets Analysis
    elif analysis_option == "Temperature Buckets":
        bins = [0, 5, 10, 15, 20, 25, 30, 35, 40]
        labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40']

        # Create a new column called 'temp_buckets'
        data_cleaned['temp_buckets'] = pd.cut(data_cleaned['temp'], bins=bins, labels=labels, right=False)

        # Prepare the data for heatmap
        heatmap_data = data_cleaned.groupby(['hr', 'temp_buckets'])['cnt'].mean().reset_index()
        
        # Create the heatmaps
        fig = px.density_heatmap(heatmap_data, 
                                x='hr', 
                                y='temp_buckets', 
                                z='cnt', 
                                color_continuous_scale='Viridis', 
                                labels={'hr': 'Hour of Day', 'temp_buckets': 'Temperature Buckets', 'cnt': 'Average Rentals'}, 
                                title='Average Hourly Bike Rentals by Temperature Buckets')
        st.plotly_chart(fig)

    # 6.3 Wind Condition Analysis
    elif analysis_option == "Wind Condition":
        bins = [0, 10, 20, 30, 40, 50, 60]
        labels = ['Calm', 'Light', 'Moderate', 'Fresh', 'Strong', 'Gale']

        # Create a new column called 'wind_buckets'
        data_cleaned['wind_buckets'] = pd.cut(data_cleaned['windspeed'], bins=bins, labels=labels, right=False)

        # Prepare the data for heatmap
        heatmap_data = data_cleaned.groupby(['hr', 'wind_buckets'])['cnt'].mean().reset_index()

        # Create the heatmaps
        fig = px.density_heatmap(heatmap_data, 
                                x='hr', 
                                y='wind_buckets', 
                                z='cnt', 
                                color_continuous_scale='Viridis', 
                                labels={'hr': 'Hour of Day', 'wind_buckets': 'Wind Condition', 'cnt': 'Average Rentals'}, 
                                title='Average Hourly Bike Rentals by Wind Condition')
        st.plotly_chart(fig)

# Check if the script is being run directly
if __name__ == "__main__":
    main()