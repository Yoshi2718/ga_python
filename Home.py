# import libraries
import streamlit as st

# Set layout
st.set_page_config(page_title="Interactive Report for Bike Sharing Service", layout="wide")

# Display the image
st.markdown(
    """
    <style>
        .cover-container {
            position: relative;
            width: 100%;
            height: 80vh;
            background-image: url('https://www.fcnp.com/wp-content/uploads/2019/05/913bikeshareWEB.jpg');
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            font-family: Arial, sans-serif;
        }
        .cover-title {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            color: white;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
        }
    </style>
    <div class="cover-container">
        <div class="cover-title">Interactive Bike-Sharing Report - Group 1</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Display presenters' names in a horizontal layout using columns
st.write("")  # Blank space to align below the title
cols = st.columns(5)  # Create five equal-width columns
presenters = ["Bernardo Santos", "Hernan Fermin", "Juliana Haddad", "Philippa Quadt", "Yoshiki Kitagawa"]

# Display each name in a separate column
for col, name in zip(cols, presenters):
    col.markdown(
        f"<div style='font-size:1.2em; font-weight:bold; color:white; text-align:center; background:rgba(0,0,0,0.5); padding:10px; border-radius:8px;'>{name}</div>",
        unsafe_allow_html=True
    )