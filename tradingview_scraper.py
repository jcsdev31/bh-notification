import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# Replace with the name of your JSON key file
JSON_KEY_FILE = 'ohlc-data-381211-b2ae96e8ab72.json'
SPREADSHEET_ID = '1nl3_3roDH5TK7LErXeWTqwELoXmd3I4s0sEmxQ6aiXM'

# Authenticate with your Google account
credentials = service_account.Credentials.from_service_account_file(JSON_KEY_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])

def write_data_to_google_sheet(sheet_id, sheet_range, data):
    try:
        sheets_instance = build('sheets', 'v4', credentials=credentials)
        body = {
            'range': sheet_range,
            'majorDimension': 'ROWS',
            'values': data
        }
        response = sheets_instance.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=sheet_range, body=body, valueInputOption='RAW').execute()
        print(f'{response.get("updatedCells")} cells updated.')
    except HttpError as error:
        print(f'An error occurred: {error}')
        response = None
    return response

# Replace the symbol and interval with your desired trading pair and time frame
symbol = 'BTCUSDT'
interval = '1h'

url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}'
response = requests.get(url)
ohlc_data = response.json()

# Save the JSON data to a file
with open('ohlc_data.json', 'w') as f:
    json.dump(ohlc_data, f)

# Convert the JSON data to a list of lists (rows and columns)
header = ['Timestamp', 'Open', 'High', 'Low', 'Close']
rows = [[datetime.fromtimestamp(entry[0] // 1000).strftime('%Y-%m-%d %H:%M:%S'), float(entry[1]), float(entry[2]), float(entry[3]), float(entry[4])] for entry in ohlc_data]

# Add the header to the data and write it to the Google Sheet
data_to_write = [header] + rows

SHEET_RANGE = 'Sheet1!A1:E'
write_data_to_google_sheet(SPREADSHEET_ID, SHEET_RANGE, data_to_write)
