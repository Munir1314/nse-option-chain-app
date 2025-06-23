import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Live NSE Option Chain", layout="wide")
st.title("📈 Live NSE Option Chain Viewer")

symbol = st.selectbox("Select Index", ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"])

def fetch_option_chain(symbol):
    try:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/json",
            "Referer": f"https://www.nseindia.com/get-quotes/derivatives?symbol={symbol}"
        }

        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers, timeout=5)
        time.sleep(1)
        response = session.get(url, headers=headers, timeout=5)
        data = response.json()

        ce_list = []
        pe_list = []

        for record in data["records"]["data"]:
            ce = record.get("CE")
            pe = record.get("PE")

            if ce:
                ce_list.append({
                    "Strike": ce["strikePrice"],
                    "Expiry": ce["expiryDate"],
                    "OI": ce["openInterest"],
                    "COI": ce["changeinOpenInterest"],
                    "Vol": ce["totalTradedVolume"],
                    "IV": ce["impliedVolatility"],
                    "LTP": ce["lastPrice"],
                    "Type": "CE"
                })

            if pe:
                pe_list.append({
                    "Strike": pe["strikePrice"],
                    "Expiry": pe["expiryDate"],
                    "OI": pe["openInterest"],
                    "COI": pe["changeinOpenInterest"],
                    "Vol": pe["totalTradedVolume"],
                    "IV": pe["impliedVolatility"],
                    "LTP": pe["lastPrice"],
                    "Type": "PE"
                })

        df = pd.DataFrame(ce_list + pe_list)
        return df

    except Exception as e:
        st.error("❌ Could not load live data from NSE.")
        st.stop()

# Show Data
st.write("Fetching live data...")

df = fetch_option_chain(symbol)
df = df.sort_values(by=["Strike", "Type"])
st.dataframe(df, use_container_width=True)
