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
        
        items = df_list['ItemName'].tolist()
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
        # Generate a random value between 10 and 500
        # In a real scenario, this would be a scraped value
        value = round(random.uniform(10, 500), 2)
        new_data[item] = value

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
