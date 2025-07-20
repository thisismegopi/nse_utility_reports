import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### NSE Trading Holidays")
try:
    st.dataframe(nse.trading_holidays(),height=600,column_config={
        "tradingDate": st.column_config.DateColumn("Date",format="localized"),
        "weekDay": st.column_config.TextColumn("Week day"),
        "description": st.column_config.TextColumn("Description"),
        "morning_session": st.column_config.TextColumn("Morning Session"),
        "evening_session": st.column_config.TextColumn("Evening Session"),
        "Sr_no": st.column_config.TextColumn("#"),
    })
except Exception as e:
    st.error(e)