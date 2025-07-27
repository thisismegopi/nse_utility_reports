import streamlit as st
import NseUtility
from datetime import datetime, timedelta

nse = NseUtility.NseUtils()

st.write("### Upcoming Results")
col1, col2, col3 = st.columns(3)
with col1:
    symbol = st.text_input("Search", key="symbol", placeholder="Enter a symbol to search")
with col2:
    from_date = st.date_input("From Date", value=datetime.now(), key="from_date",)
with col3:
    to_date = st.date_input("To Date", value=datetime.now() + timedelta(days=30), key="to_date")

try:
    df = nse.get_upcoming_results_calendar(symbol=symbol, from_date_str=from_date.strftime("%d-%m-%Y"), to_date_str=to_date.strftime("%d-%m-%Y"))
    if df is None or df.empty:
        st.warning("No upcoming results found.")
    else:
        st.dataframe(df, height=600,column_config={
        "symbol": st.column_config.TextColumn("Symbol"),
        "company": st.column_config.TextColumn("Company"),
        "purpose": st.column_config.TextColumn("Purpose"),
        "bm_desc": st.column_config.TextColumn("Description"),
        "date": st.column_config.DateColumn("Date", format="localized"),
        })
        st.warning("⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.")
        st.write("Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).")
except Exception as e:
    st.error(e)