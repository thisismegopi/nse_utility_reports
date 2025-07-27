import streamlit as st
import NseUtility
from datetime import datetime, timedelta

nse = NseUtility.NseUtils()

st.write("### Corporate Announcements")
col1, col2, col3 = st.columns(3)
with col1:
    symbol = st.text_input("Search", key="symbol", placeholder="Enter a symbol to search")
with col2:
    from_date = st.date_input("From Date", value=datetime.now() - timedelta(days=30), key="from_date",)
with col3:
    to_date = st.date_input("To Date", value=datetime.now(), key="to_date")
try:
    df = nse.get_corporate_announcement(symbol=symbol, from_date_str=from_date.strftime("%d-%m-%Y"), to_date_str=to_date.strftime("%d-%m-%Y"))
    if df is None or df.empty:
        raise ValueError("No corporate announcements found for the given criteria.")
    st.dataframe(df,height=600, column_config={
        "symbol": st.column_config.TextColumn("Symbol"),
        "sm_name": st.column_config.TextColumn("Company Name"),
        "desc": st.column_config.TextColumn("Subject"),
        "attchmntFile": st.column_config.LinkColumn("Attachment", display_text="Link"),
        "attchmntText": st.column_config.TextColumn("Details"),
        "exchdisstime": st.column_config.DatetimeColumn("Date and Time"),
    })
except Exception as e:
    st.warning("Failed: " + str(e))