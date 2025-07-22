import streamlit as st
import NseUtility
nse = NseUtility.NseUtils()

st.write("### ETF's")

search_text = st.text_input("Search", placeholder="Search ETF's.")
st.dataframe(nse.get_etf_list(search_text=search_text), height=600)