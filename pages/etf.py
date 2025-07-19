import streamlit as st
import NseUtility
nse = NseUtility.NseUtils()

st.write("### ETF's")
st.dataframe(nse.get_etf_list(), height=600)