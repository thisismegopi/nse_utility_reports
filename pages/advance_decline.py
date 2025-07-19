import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Advance/Decline")
try:
    st.dataframe(nse.get_advance_decline(),height=600)
except Exception as e:
    st.error(e)