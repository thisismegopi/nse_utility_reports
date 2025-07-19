import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Most Active Equity Stocks by Volume")
try:
    st.dataframe(nse.most_active_equity_stocks_by_volume(),height=600)
except Exception as e:
    st.error(e)