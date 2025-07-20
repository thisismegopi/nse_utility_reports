import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### FII and DII Activity")
try:
    st.dataframe(nse.fii_dii_activity(), column_config={
        "category": st.column_config.TextColumn("Category"),
        "date": st.column_config.DateColumn("Date", format="localized"),
        "buyValue": st.column_config.NumberColumn("Buy Value", format="₹%.2f"),
        "sellValue": st.column_config.NumberColumn("Sell Value", format="₹%.2f"),
        "netValue": st.column_config.NumberColumn("Net Value", format="₹%.2f"),
    })
except Exception as e:
    st.warning("Failed to fetch FII and DII data. Please try again later.")