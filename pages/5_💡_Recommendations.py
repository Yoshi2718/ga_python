# impport libraries
import streamlit as st

# Define the main function for the "Modeling" page
def main():
    st.title("Recommendations")
    
    st.write("##### Based on the analysis and modelling results, the following recommendations are proposed to optimize the bike-sharing service:")

    # Recommendation 1: Optimize Bike Availability
    st.subheader("1️⃣ Optimize Bike Availability with Real-Time Demand Insights")
    st.write("""
    - Enhance predictive analytics with more reliable data.
    - Improve peak-hour forecasts to ensure better bike availability.
    - Increase ridership and drive business growth.
    """)

    # Recommendation 2: Improve Service Efficiency
    st.subheader("2️⃣ Improve Service Efficiency in High-Demand Areas")
    st.write("""
    - Utilize data to identify high-demand locations.
    - Prioritize new bike stations or increased availability.
    - Ensure efficient resource allocation and enhance customer satisfaction.
    """)

    # Recommendation 3: Introduce Dynamic Pricing
    st.subheader("3️⃣ Introduce Dynamic Pricing Strategies")
    st.write("""
    - Analyse demand patterns to adjust rates during:
        - Peak hours
        - Favourable weather
        - Events
    - Optimize bike utilization while maximizing revenue and user satisfaction.
    """)

    # Recommendation 4: Strengthen Maintenance Strategies
    st.subheader("4️⃣ Strengthen Maintenance Strategies")
    st.write("""
    - Use predictive models to analyze bike usage patterns.
    - Forecast maintenance needs to:
        - Reduce downtime
        - Ensure bikes remain operational
    - Enhance user satisfaction and operational efficiency.
    """)

    # Recommendation 5: Introduce Advanced Reservation Systems
    st.subheader("5️⃣ Introduce Advanced Reservation Systems")
    st.write("""
    - Leverage predictive models to anticipate demand.
    - Allow users to book bikes in advance during:
        - Peak hours
        - Special occasions
    - Improve convenience and reduce unavailability.
    """)

    # Call to Action
    st.info("##### These recommendations aim to optimize resource allocation, maximize revenue, and enhance the customer experience.")
    

# Check if the script is being run directly
if __name__ == "__main__":
    main()