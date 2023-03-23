import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.graph_objs as go

# Google Sheet credentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('ohlc-data-381211-b2ae96e8ab72.json', scope)
client = gspread.authorize(creds)

# Read data from Google Sheet
sheet = client.open('OHLC Scraper').sheet1  # Replace YOUR_SPREADSHEET_NAME with your sheet name
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Convert timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')

# Create candlestick chart
fig = go.Figure(data=[go.Candlestick(x=df['Timestamp'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

# Add chart title and axis labels
fig.update_layout(
    title='OHLC Chart',
    yaxis_title='Price',
    xaxis_title='Date'
)

# Display chart
fig.show()
