import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Corporate Actions")
try:
    st.dataframe(nse.get_corporate_action(),height=600)
except Exception as e:
    st.error(e)