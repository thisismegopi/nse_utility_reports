import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()


st.write('### Index Details!')
index = st.selectbox("Select Index", nse.equity_market_list, index=0)
st.dataframe(nse.get_index_details(category=index), height=600)