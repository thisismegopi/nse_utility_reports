import streamlit as st
import utils.NseUtility as NseUtility
from datetime import datetime, timedelta

nse = NseUtility.NseUtils()

st.write("### Corporate Actions")
col1, col2, col3 = st.columns(3)
with col1:
    symbol = st.text_input("Search", key="symbol", placeholder="Enter a symbol to search")
with col2:
    from_date = st.date_input("From Date", value=datetime.now(), key="from_date",)
with col3:
    to_date = st.date_input("To Date", value=datetime.now(), key="to_date")

try:
    data = nse.get_corporate_action(symbol=symbol, from_date_str=from_date.strftime("%d-%m-%Y"), to_date_str=to_date.strftime("%d-%m-%Y"))
    if data is None:
        st.warning("No corporate actions found for the given criteria.")
        st.stop()
    st.dataframe(data,height=600,column_config={
        "symbol": st.column_config.TextColumn("Symbol"),
        "series": st.column_config.TextColumn("Series"),
        "faceVal": st.column_config.TextColumn("Face Value"),
        "subject": st.column_config.TextColumn("Subject"),
        "exDate": st.column_config.DateColumn("Ex Date",format="localized"),
        "recDate": st.column_config.DateColumn("Record Date",format="localized"),
        "isin": st.column_config.TextColumn("ISIN"),
        "comp": st.column_config.TextColumn("Company"),
    })
    st.warning("⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.")
    st.write("Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).")
except Exception as e:
    st.error(e)