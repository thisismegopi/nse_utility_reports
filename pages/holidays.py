import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Holidays for the calendar year 2025")

tab1, tab2 = st.tabs(["Trading Holidays", "Clearing Holidays"], width="stretch")

with tab1:
    try:
        st.dataframe(nse.trading_holidays(),height=600,column_config={
        "tradingDate": st.column_config.DateColumn("Date",format="localized"),
        "weekDay": st.column_config.TextColumn("Week day"),
        "description": st.column_config.TextColumn("Description"),
        "morning_session": st.column_config.TextColumn("Morning Session"),
        "evening_session": st.column_config.TextColumn("Evening Session"),
        "Sr_no": st.column_config.TextColumn("#"),
    })
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab2:
    try:
        st.dataframe(nse.clearing_holidays(),height=600,column_config={
        "tradingDate": st.column_config.DateColumn("Date",format="localized"),
        "weekDay": st.column_config.TextColumn("Week day"),
        "description": st.column_config.TextColumn("Description"),
        "morning_session": st.column_config.TextColumn("Morning Session"),
        "evening_session": st.column_config.TextColumn("Evening Session"),
        "Sr_no": st.column_config.TextColumn("#"),
    })
    except:
        st.warning("Unable to fetch data. Please try again later.")