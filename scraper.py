import pandas as pd
import random
from datetime import datetime, timezone, timedelta
import os

# Settings
MONITORING_LIST_FILE = 'monitoring_list.csv'
HISTORY_DATA_FILE = 'history_data.csv'

def get_taiwan_time():
    # Taiwan is UTC+8
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz)

def main():
    print(f"Reading {MONITORING_LIST_FILE}...")
    try:
        try:
            df_list = pd.read_csv(MONITORING_LIST_FILE, encoding='utf-8')
        except UnicodeDecodeError:
            print("UTF-8 decode failed, trying cp950...")
            df_list = pd.read_csv(MONITORING_LIST_FILE, encoding='cp950')
        
        print(f"Columns found: {df_list.columns.tolist()}")
        if 'ItemName' in df_list.columns:
            items = df_list['ItemName'].tolist()
        else:
            print("Warning: 'ItemName' column not found. Using the first column as item list.")
            items = df_list.iloc[:, 0].tolist()
    except FileNotFoundError:
        print(f"Error: {MONITORING_LIST_FILE} not found.")
        return

    # 2. Generate data
    current_time = get_taiwan_time()
    # Format timestamp as string for consistency
    timestamp_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    new_data = {
        'Timestamp': timestamp_str
    }
    
    print(f"Generating data for {timestamp_str}...")
    for item in items:
        # Generate varied simulated data based on item keywords
        value = get_simulated_value(item)
        new_data[item] = value

def get_simulated_value(item_name):
    item_lower = item_name.lower()
    
    # 1. Rates / Yields (Percentage-like low numbers)
    if any(k in item_lower for k in ['yield', 'rate', '殖利率', '利差', 'spread']):
        return round(random.uniform(1.5, 5.5), 2)
    
    # 2. Ratios / VIX (Mid-range numbers)
    if any(k in item_lower for k in ['pe', 'ratio', 'vix', '本益比']):
        return round(random.uniform(10, 40), 2)
        
    # 3. Oscillators / 0-100 Indicators
    if any(k in item_lower for k in ['rsi', 'fear', 'greed', '乖離', 'bias', 'sentiment', '情緒']):
        return round(random.uniform(20, 80), 2)
        
    # 4. Large Indices (Thousands) - optional, but user mentioned "Stock"
    # If the user didn't specificy indices, keeping it simple is safer, 
    # but let's assume default is 0-100 to be safe for unknown types, or keep the 10-500 from before but narrower.
    
    # Default fallback
    return round(random.uniform(10, 150), 2)

    # Convert to DataFrame (single row)
    df_new = pd.DataFrame([new_data])

    # 3. Append to history file
    if os.path.exists(HISTORY_DATA_FILE):
        print(f"Appending to {HISTORY_DATA_FILE}...")
        # Read existing to ensure columns match or append properly
        df_history = pd.read_csv(HISTORY_DATA_FILE)
        df_combined = pd.concat([df_history, df_new], ignore_index=True)
    else:
        print(f"Creating {HISTORY_DATA_FILE}...")
        df_combined = df_new

    # Save back to CSV
    df_combined.to_csv(HISTORY_DATA_FILE, index=False)
    print("Done!")

if __name__ == "__main__":
    main()
