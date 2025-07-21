import streamlit as st
import NseUtility
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
        st.warning("No corporate actions found for the given symbol.")
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
except Exception as e:
    st.error(e)