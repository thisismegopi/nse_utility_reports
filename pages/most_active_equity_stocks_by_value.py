import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Most Active Equity Stocks by Value")
try:
    st.dataframe(nse.most_active_equity_stocks_by_value(),height=600)
except Exception as e:
    st.error(e)