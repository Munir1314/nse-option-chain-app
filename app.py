import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Live Option Chain", layout="wide")
st.title("📈 Live NSE Option Chain Viewer")

# Dropdown to select index
symbol = st.selectbox("Select Index", ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"])

# Fetch function with correct headers
def fetch_option_chain(symbol):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json",
        "Referer": f"https://www.nseindia.com/get-quotes/derivatives?symbol={symbol}",
    }

    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    time.sleep(1)  # Pause for 1 sec (important)
    response = session.get(url, headers=headers)
    
    data = response.json()
    all_data = data['records']['data']
    ce_list = []
    pe_list = []

    for record in all_data:
        ce = record.get('CE')
        pe = record.get('PE')

        if ce:
            ce_list.append({
                "Strike": ce['strikePrice'],
                "Expiry": ce['expiryDate'],
                "OI": ce['openInterest'],
                "COI": ce['changeinOpenInterest'],
                "Vol": ce['totalTradedVolume'],
                "IV": ce['impliedVolatility'],
                "LTP": ce['lastPrice'],
                "Type": "CE"
            })

        if pe:
            pe_list.append({
                "Strike": pe['strikePrice'],
                "Expiry": pe['expiryDate'],
                "OI": pe['openInterest'],
                "COI": pe['changeinOpenInterest'],
                "Vol": pe['totalTradedVolume'],
                "IV": pe['impliedVolatility'],
                "LTP": pe['lastPrice'],
                "Type": "PE"
            })

    df = pd.DataFrame(ce_list + pe_list)
    return df

# Load and display
st.write("Fetching live data...")
try:
    df = fetch_option_chain(symbol)
    df_sorted = df.sort_values(by=["Strike", "Type"])
    st.dataframe(df_sorted)
except:
    st.error("⚠️ Unable to load data. Please refresh the app.")
