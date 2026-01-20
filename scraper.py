import pandas as pd
import random
from datetime import datetime, timezone, timedelta
import os
import traceback

# Settings
MONITORING_LIST_FILE = 'monitoring_list.csv'
HISTORY_DATA_FILE = 'history_data.csv'

def get_taiwan_time():
    # Taiwan is UTC+8
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz)

def get_simulated_value(item_name):
    # Ensure string
    if not isinstance(item_name, str):
        item_name = str(item_name)
        
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
        
    # Default fallback
    return round(random.uniform(10, 150), 2)

def main():
    print(f"Reading {MONITORING_LIST_FILE}...")
    try:
        try:
            df_list = pd.read_csv(MONITORING_LIST_FILE, encoding='utf-8')
        except UnicodeDecodeError:
            print("UTF-8 decode failed, trying cp950...")
            df_list = pd.read_csv(MONITORING_LIST_FILE, encoding='cp950')
        
        print(f"Columns found: {df_list.columns.tolist()}")
        
        # Data Cleaning: If the dataframe thinks everything is one column due to messy CSV
        if len(df_list.columns) == 1:
            print("Warning: Only 1 column found. Trying to parse...")
            # If the column name itself looks like a CSV header "A,B,C"
            # We might want to just proceed using the values in this column as the identifiers
            items = df_list.iloc[:, 0].tolist()
        elif 'ItemName' in df_list.columns:
            items = df_list['ItemName'].tolist()
        else:
            print("Warning: 'ItemName' column not found. Using the first column as item list.")
            items = df_list.iloc[:, 0].tolist()
            
    except FileNotFoundError:
        print(f"Error: {MONITORING_LIST_FILE} not found.")
        return
    except Exception as e:
        print(f"Error reading CSV: {e}")
        traceback.print_exc()
        return

    # 2. Generate data
    try:
        current_time = get_taiwan_time()
        timestamp_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        new_data = {
            'Timestamp': timestamp_str
        }
        
        print(f"Generating data for {timestamp_str}...")
        if items:
            print(f"Sample item: {items[0]}")
            
        for item in items:
            value = get_simulated_value(item)
            new_data[item] = value

        # Convert to DataFrame (single row)
        df_new = pd.DataFrame([new_data])

        # 3. Append to history file
        if os.path.exists(HISTORY_DATA_FILE):
            print(f"Appending to {HISTORY_DATA_FILE}...")
            # Reload history to check structure
            try:
                df_history = pd.read_csv(HISTORY_DATA_FILE)
                # Concatenate
                df_combined = pd.concat([df_history, df_new], ignore_index=True)
            except pd.errors.EmptyDataError:
                print("History file empty, overwriting...")
                df_combined = df_new
            except Exception as e:
                print(f"Error reading history file: {e}")
                # Backup and overwrite
                os.rename(HISTORY_DATA_FILE, HISTORY_DATA_FILE + ".bak")
                df_combined = df_new
        else:
            print(f"Creating {HISTORY_DATA_FILE}...")
            df_combined = df_new

        # Save back to CSV
        df_combined.to_csv(HISTORY_DATA_FILE, index=False)
        print("Done!")
        
    except Exception as e:
        print("CRITICAL ERROR during processing:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
