import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Pre Market Info")
list = st.selectbox("Select Index", nse.pre_market_list, index=0)
try:
    st.dataframe(nse.pre_market_info(category=list),height=600, column_config={
        "chartTodayPath": st.column_config.ImageColumn("Today Chart"),
    })
except Exception as e:
    st.error(e)