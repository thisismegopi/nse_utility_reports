import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Index Dividend Yield")
try:
    st.dataframe(nse.get_index_div_yield(),height=600)
except Exception as e:
    st.error(e)