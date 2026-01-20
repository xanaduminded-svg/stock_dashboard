import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Stock & Data Monitor", layout="wide")

st.title("📊 Stock & Data Monitoring Dashboard")

DATA_FILE = 'history_data.csv'

def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        return df.sort_index()
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.warning("No data found yet. The scraper hasn't run or history_data.csv is missing.")
else:
    # 1. Calculate Latest Data & Changes
    if len(df) >= 1:
        latest_row = df.iloc[-1]
        latest_time = df.index[-1]
    
    if len(df) >= 2:
        prev_row = df.iloc[-2]
    else:
        # If only one record exists, there is no previous data to compare
        prev_row = latest_row 

    # Prepare Summary Data
    summary_data = []
    for col in df.columns:
        current_val = latest_row[col]
        prev_val = prev_row[col]
        diff = current_val - prev_val
        
        # Calculate percentage change if possible
        if prev_val != 0:
            pct_change = (diff / prev_val) * 100
        else:
            pct_change = 0.0

        summary_data.append({
            "Item Name": col,
            "Latest Value": current_val,
            "Change": diff,
            "Change %": f"{pct_change:.2f}%"
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    st.info(f"Last updated: {latest_time}")

    # 2. Display Summary Table
    st.subheader("📋 Market Summary")
    st.caption("Select a row to view detailed trends.")

    # Configure columns for better visualization
    column_config = {
        "Latest Value": st.column_config.NumberColumn(format="%.2f"),
        "Change": st.column_config.NumberColumn(format="%.2f"),
    }

    event = st.dataframe(
        summary_df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )

    # 3. Handle Selection & Plot Chart
    st.subheader("📈 Trend Analysis")
    
    selected_rows = event.selection.rows
    if selected_rows:
        # Get the item name from the selected row index
        selected_index = selected_rows[0]
        selected_item = summary_df.iloc[selected_index]["Item Name"]
        
        st.markdown(f"### Historical Trend: **{selected_item}**")
        
        # Plot only the selected column
        # Highlight: Create a dedicated chart for this item
        # Rename the column to a safe name for plotting to avoid Altair encoding errors with special chars
        chart_data = df[[selected_item]].rename(columns={selected_item: "Value"})
        st.line_chart(chart_data)
        
        # Optional: Show stats for this specific item
        with st.expander(f"Raw Data for {selected_item}"):
            st.dataframe(chart_data.sort_index(ascending=False))
            
    else:
        # Default view: summary of all or instructions
        st.markdown("👈 **Please select an item from the table above to see its chart.**")
        
        with st.expander("Or view all trends at once (messy for many items)"):
            st.line_chart(df)

    # 4. Footer with Dashboard URL
    st.divider()
    st.markdown(f"**Dashboard URL:** [http://localhost:8501](http://localhost:8501)")
