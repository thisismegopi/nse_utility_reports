import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Upcoming Results Calendar")
try:
    st.dataframe(nse.get_upcoming_results_calendar(), height=600, selection_mode="multi-row")
except Exception as e:
    st.error(e)