import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Corporate Announcements")
try:
    st.dataframe(nse.get_corporate_announcement(),height=600)
except Exception as e:
    st.error(e)