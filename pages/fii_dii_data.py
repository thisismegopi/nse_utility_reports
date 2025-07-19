import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### FII and DII Activity")
try:
    st.dataframe(nse.fii_dii_activity())
except Exception as e:
    st.error(e)