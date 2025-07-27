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
    st.warning("⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.")
    st.write("Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).")
except Exception as e:
    st.warning("Failed to fetch FII and DII data. Please try again later.")