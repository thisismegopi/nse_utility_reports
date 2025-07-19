import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Index PE Ratio")
try:
    st.dataframe(nse.get_index_pe_ratio(),height=600)
except Exception as e:
    st.error(e)

st.write("### Index PB Ratio")
try:
    st.dataframe(nse.get_index_pb_ratio(),height=600)
except Exception as e:
    st.error(e)