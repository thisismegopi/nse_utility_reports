import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Large Deals")

tab1, tab2, tab3 = st.tabs(["Bulk Deals", "Block Deals", "Short Selling"], width="stretch")

with tab1:
    try:
        st.dataframe(nse.large_deals('BULK_DEALS_DATA'),height=600,column_config={
        "date": st.column_config.DateColumn("Date"),
        "symbol": st.column_config.TextColumn("Symbol"),
        "name": st.column_config.TextColumn("Name"),
        "clientName": st.column_config.TextColumn("Client Name"),
        "buySell": st.column_config.TextColumn("BUY/SELL"),
        "qty": st.column_config.NumberColumn("Quantity Traded"),
        "watp": st.column_config.NumberColumn("Trade Price/ Weighted. AVG. Pprice"),
    })
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab2:
    try:
        st.dataframe(nse.large_deals('BLOCK_DEALS_DATA'),height=600,column_config={
        "date": st.column_config.DateColumn("Date"),
        "symbol": st.column_config.TextColumn("Symbol"),
        "name": st.column_config.TextColumn("Name"),
        "clientName": st.column_config.TextColumn("Client Name"),
        "buySell": st.column_config.TextColumn("BUY/SELL"),
        "qty": st.column_config.NumberColumn("Quantity Traded"),
        "watp": st.column_config.NumberColumn("Trade Price/ Weighted. AVG. Pprice"),
    })
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab3:
    try:
        st.dataframe(nse.large_deals('SHORT_DEALS_DATA'),height=600,column_config={
        "date": st.column_config.DateColumn("Date"),
        "symbol": st.column_config.TextColumn("Symbol"),
        "name": st.column_config.TextColumn("Name"),
        "clientName": st.column_config.TextColumn("Client Name"),
        "buySell": st.column_config.TextColumn("BUY/SELL"),
        "qty": st.column_config.NumberColumn("Quantity Traded"),
        "watp": st.column_config.NumberColumn("Trade Price/ Weighted. AVG. Pprice"),
    })
    except:
        st.warning("Unable to fetch data. Please try again later.")