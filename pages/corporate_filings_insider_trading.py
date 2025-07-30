import streamlit as st
import utils.NseUtility as NseUtility

nse = NseUtility.NseUtils()

st.write("### Corporate Filings - Insider Trading")

try:
    st.dataframe(nse.get_corporate_filings_insider_trading(),height=600)
except Exception as e:
    st.error(e)