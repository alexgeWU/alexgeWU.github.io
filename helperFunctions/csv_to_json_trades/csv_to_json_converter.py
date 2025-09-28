import csv
import json
from datetime import datetime

# Define the file paths
CSV_FILE_PATH = 'trades.csv'
JSON_FILE_PATH = '../../src/data.json'

def convert_date_to_iso(date_string):
    """Converts 'MM/DD/YYYY HH:MM' string to ISO 8601 format."""
    dt_object = datetime.strptime(date_string, '%m/%d/%Y %H:%M')
    return dt_object.isoformat() + '.000Z'

def process_trades():
    """Reads trades from CSV, converts them to JSON format, and updates data.json."""
    try:
        with open(JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: '{JSON_FILE_PATH}' not found. A new file will be created.")
        data = {"games": [], "trades": [], "blogPosts": []}

    new_trades = []
    try:
        with open(CSV_FILE_PATH, 'r', newline='') as f:


            reader = csv.DictReader(f)
            for row in reader:
                trade_entry = {
                    "status": "CLOSED",
                    "ticker": row['Symbol'],
                    "purchaseDateTime": convert_date_to_iso(row['Opened Data']),
                    "purchasePrice": float(row['Cost Per Share'].strip().replace('$', '').replace(',', '')),
                    "quantity": int(row['Quantity']),
                    "closeDateTime": convert_date_to_iso(row['Closed Data']),
                    "closePrice": float(row['Proceeds Per Share'].strip().replace('$', '').replace(',', '')),
                    "costBasis": float(row['Cost Basis (CB)'].strip().replace('$', '').replace(',', '')),
                    "proceeds": float(row['Proceeds'].strip().replace('$', '').replace(',', '')),
                    "notes": ""
                }
                new_trades.append(trade_entry)
    except FileNotFoundError:
        print(f"Error: '{CSV_FILE_PATH}' not found. Please make sure it exists in the root directory.")
        return

    data['trades'] = new_trades

    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Success! Updated '{JSON_FILE_PATH}' with {len(new_trades)} trades from '{CSV_FILE_PATH}'.")

if __name__ == '__main__':
    process_trades()