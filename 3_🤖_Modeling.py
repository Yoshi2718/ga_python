# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import set_config
from sklearn.utils import estimator_html_repr
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Define the main function for the "Modeling" page
def main():    
    # - Load data and model
    data_cleaned = pd.read_csv('data/data_cleaned.csv')
    linear_model = joblib.load('data/trained_linear_model.pkl')
    rf_model = joblib.load('data/trained_rf_model.pkl')
    xgb_model = joblib.load('data/trained_xgb_model.pkl')
    catboost_model = joblib.load('data/trained_catboost_model.pkl')
    
    st.title("Modeling")

    # 1. Explanation of Model Building Flow
    st.header("1. Flow for Building the Model")

    # Describe each step involved in the model building process
    st.write("""
    The following steps outline the process used to build and evaluate the models in this analysis:

    1. **Data Preprocessing**:
       - Removed columns: `casual`, `registered`, `atemp`, `daylight`, `temp_buckets`, amd `wind_buckets`.
       - One-hot encoding for categorical columns `season`, `weathersit`, and `weekday`, using numerical encoding to transform numerical values that correspond to categorical data (e.g. season, weathersit, month)

    2. **Data Splitting**:
       - 80-20 split for training and testing sets.

    3. **Pipeline Setup**:
       - Included `StandardScaler`, `SelectKBest` (feature selection).
       - Chose 4 models: `LinearRegression`, `RandomForest`, `XG Boost`, and `Cat Boost`.

    4. **Hyperparameter Tuning**:
       - Used `SelectKBest` to find optimal `k` values (5, 10, all).
       - Cross-validation with 5-folds to maximize R².

    5. **Model Training and Selection**:
       - Compared 4 models based on performance metrics.

    6. **Model Evaluation**:
       - Evaluated models using **MAE**, **MSE**, and **R²** scores.
    """)

    # Configure sklearn to display pipelines as diagrams
    set_config(display='diagram')

    # 2. Pipeline visualization
    st.header("2. Pipeline Visualization")

    linear_pipeline_html = estimator_html_repr(linear_model)
    rf_pipeline_html = estimator_html_repr(rf_model)
    xgb_pipeline_html = estimator_html_repr(xgb_model)
    catboost_pipeline_html = estimator_html_repr(catboost_model)

    # Create columns for each model pipeline to display them side-by-side
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Linear Regression")
        st.components.v1.html(linear_pipeline_html, height=250, scrolling=True)

    with col2:
        st.write("#### Random Forest")
        st.components.v1.html(rf_pipeline_html, height=250, scrolling=True)

    col3, col4 = st.columns(2)

    with col3:
        st.write("#### XG Boost")
        st.components.v1.html(xgb_pipeline_html, height=250, scrolling=True)

    with col4:
        st.write("#### Cat Boost")
        st.components.v1.html(catboost_pipeline_html, height=250, scrolling=True)

    # 3. Visualize the Model Performance
    st.header("3. Model Performance")

    # Define target variable and features
    data_cleaned = pd.get_dummies(data_cleaned, columns=['weathersit'], drop_first=True)
    data_cleaned = data_cleaned.set_index('dteday')
    
    #total number of hours, months, weeks and seasons
    h = 24 
    m = 12
    w = 7
    s = 4

    data_cleaned['hr_sin'] = np.sin(2 * np.pi * data_cleaned['hr'] / h)
    data_cleaned['hr_cos'] = np.cos(2 * np.pi * data_cleaned['hr'] / h)

    data_cleaned['mnth_sin'] = np.sin(2 * np.pi * data_cleaned['mnth'] / m)
    data_cleaned['mnth_cos'] = np.cos(2 * np.pi * data_cleaned['mnth'] / m)

    data_cleaned['weekday_sin'] = np.sin(2 * np.pi * data_cleaned['weekday'] / w)
    data_cleaned['weekday_cos'] = np.cos(2 * np.pi * data_cleaned['weekday'] / w)

    data_cleaned['season_sin'] = np.sin(2 * np.pi * data_cleaned['season'] / s)
    data_cleaned['season_cos'] = np.cos(2 * np.pi * data_cleaned['season'] / s)
    
    X = data_cleaned.drop(columns=['casual', 'registered', 'atemp', 'cnt', 'yr', 'daylight'], axis=1)
    y = data_cleaned['cnt']

    # Split data into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Use pre-trained models to make predictions
    y_pred_linear = linear_model.predict(X_test)
    y_pred_rf = rf_model.predict(X_test)
    y_pred_xgb = xgb_model.predict(X_test)
    y_pred_catboost = catboost_model.predict(X_test)

    # Calculate metrics for Linear Regression
    mae_linear = mean_absolute_error(y_test, y_pred_linear)
    mse_linear = mean_squared_error(y_test, y_pred_linear)
    r2_linear = r2_score(y_test, y_pred_linear)

    # Calculate metrics for Random Forest
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    mse_rf = mean_squared_error(y_test, y_pred_rf)
    r2_rf = r2_score(y_test, y_pred_rf)

    # Calculate metrics for XG Boost
    mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
    mse_xgb = mean_squared_error(y_test, y_pred_xgb)
    r2_xgb = r2_score(y_test, y_pred_xgb)

    # Calculate metrics for Cat Boost
    mae_catboost = mean_absolute_error(y_test, y_pred_catboost)
    mse_catboost = mean_squared_error(y_test, y_pred_catboost)
    r2_catboost = r2_score(y_test, y_pred_catboost)

    # 3.1 Display metrics in a table format
    st.subheader("3.1 Model Metrics")

    # Create a DataFrame for metrics
    metrics_data = {
        "Model": ["Linear Regression", "Random Forest", "XG Boost", "Cat Boost"],
        "MAE": [f"{mae_linear:.2f}", f"{mae_rf:.2f}", f"{mae_xgb:.2f}", f"{mae_catboost:.2f}"],
        "MSE": [f"{mse_linear:.2f}", f"{mse_rf:.2f}", f"{mse_xgb:.2f}", f"{mse_catboost:.2f}"],
        "R² Score": [f"{r2_linear:.2f}", f"{r2_rf:.2f}", f"{r2_xgb:.2f}", f"{r2_catboost:.2f}"]
    }
    metrics_df = pd.DataFrame(metrics_data)

    # Display the metrics table with custom CSS for better styling
    st.markdown("""
        <style>
        .metrics-table {
            width: 100%;
            border-collapse: collapse;
        }
        .metrics-table th, .metrics-table td {
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd;
        }
        .metrics-table th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .metrics-table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .metrics-table tr:hover {
            background-color: #ddd;
        }
        </style>
    """, unsafe_allow_html=True)

    # Convert the DataFrame to an HTML table
    metrics_table_html = metrics_df.to_html(index=False, classes="metrics-table")

    st.markdown(metrics_table_html, unsafe_allow_html=True)


    # Create a row with two columns
    st.subheader("3.2 Predictions vs Actual")
    col1, col2 = st.columns(2)

    # Linear Regression Plot in the first column
    with col1:
        fig1 = px.scatter(
            x=y_test, 
            y=y_pred_linear, 
            labels={'x': 'Actual Values', 'y': 'Predicted Values'}, 
            title="Linear Regression: Predictions vs Actual"
        )
        fig1.add_shape(
            type="line", 
            x0=y_test.min(), y0=y_test.min(), 
            x1=y_test.max(), y1=y_test.max(),
            line=dict(color="red", dash="dash")
        )
        fig1.update_traces(marker=dict(size=8, color="blue", line=dict(width=1, color="black")))
        st.plotly_chart(fig1)

    # Random Forest Plot in the second column
    with col2:
        fig2 = px.scatter(
            x=y_test, 
            y=y_pred_rf, 
            labels={'x': 'Actual Values', 'y': 'Predicted Values'}, 
            title="Random Forest: Predictions vs Actual"
        )
        fig2.add_shape(
            type="line", 
            x0=y_test.min(), y0=y_test.min(), 
            x1=y_test.max(), y1=y_test.max(),
            line=dict(color="red", dash="dash")
        )
        fig2.update_traces(marker=dict(size=8, color="orange", line=dict(width=1, color="black")))
        st.plotly_chart(fig2)

    st.markdown("---")

    # XGBoost and CatBoost Performance Plot
    col3, col4 = st.columns(2)

    # XGBoost Plot in the first column
    with col3:
        fig3 = px.scatter(
            x=y_test, 
            y=y_pred_xgb, 
            labels={'x': 'Actual Values', 'y': 'Predicted Values'}, 
            title="XG Boost: Predictions vs Actual"
        )
        fig3.add_shape(
            type="line", 
            x0=y_test.min(), y0=y_test.min(), 
            x1=y_test.max(), y1=y_test.max(),
            line=dict(color="red", dash="dash")
        )
        fig3.update_traces(marker=dict(size=8, color="green", line=dict(width=1, color="black")))
        st.plotly_chart(fig3)

    # CatBoost Plot in the second column
    with col4:
        fig4 = px.scatter(
            x=y_test, 
            y=y_pred_catboost, 
            labels={'x': 'Actual Values', 'y': 'Predicted Values'}, 
            title="Cat Boost: Predictions vs Actual"
        )
        fig4.add_shape(
            type="line", 
            x0=y_test.min(), y0=y_test.min(), 
            x1=y_test.max(), y1=y_test.max(),
            line=dict(color="red", dash="dash")
        )
        fig4.update_traces(marker=dict(size=8, color="red", line=dict(width=1, color="black")))
        st.plotly_chart(fig4)

    # 4. Title and introductory text with markdown
    st.markdown("### Model Selected: CatBoost")
    st.write(
        """
        **CatBoost** was selected in our study due to its strong predictive power and efficiency in handling complex data structures, 
        as well as its high evaluation metrics. CatBoost is specifically optimized to handle categorical features naturally, 
        making it a robust choice for this analysis.
        """
    )

    # Displaying the list of advantages with Streamlit's markdown and emojis for visual enhancement
    st.markdown("""
    - 🏆 **Performance**: CatBoost achieved the highest performance in terms of evaluation metrics, including the top R² score among the tested models.
    - 🔄 **Robustness**: Known for its robustness with default settings, CatBoost performs consistently well across diverse datasets.
    - 📈 **Evaluation Metrics Used**: We evaluated models using key metrics: **Mean Absolute Error (MAE)**, **Mean Squared Error (MSE)**, and **R²**, with CatBoost performing consistently well.
    """)

# Check if the script is being run directly
if __name__ == "__main__":
    main()