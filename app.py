import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Stock & Data Monitor", layout="wide")

st.title("📊 Stock & Data Monitoring Dashboard")

DATA_FILE = 'history_data.csv'

try:
    # Read the data
    df = pd.read_csv(DATA_FILE)
    
    # Convert Timestamp to datetime for better plotting
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Set Timestamp as index for the chart
    df.set_index('Timestamp', inplace=True)
    
    # Show the latest update time
    latest_time = df.index.max()
    st.info(f"Last updated: {latest_time}")

    # Interactive Chart
    st.subheader("Historical Trends")
    st.line_chart(df)

    # Show raw data (optional, expandable)
    with st.expander("View Raw Data"):
        st.dataframe(df.sort_index(ascending=False))

except FileNotFoundError:
    st.warning("No data found yet. The scraper hasn't run or history_data.csv is missing.")
except Exception as e:
    st.error(f"An error occurred: {e}")
