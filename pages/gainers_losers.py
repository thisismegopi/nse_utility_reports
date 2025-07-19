import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Gainers & Losers")
try:
    gl = nse.get_gainers_losers()
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    with col1:
        st.dataframe({"Nifty Gainer":gl[0]['Nifty Gainer']})
    with col2:
        st.dataframe({"Nifty Loser":gl[1]['Nifty Loser']})
    with col3:
        st.dataframe({"Nifty Next 50 Gainer":gl[0]['Nifty Next 50 Gainer']})
    with col4:
        st.dataframe({"Nifty Next 50 Loser":gl[1]['Nifty Next 50 Loser']})
    with col5:
        st.dataframe({"Bank Nifty Gainer":gl[0]['Bank Nifty Gainer']})
    with col6:
        st.dataframe({"Bank Nifty Loser":gl[1]['Bank Nifty Loser']})
    with col7:
        st.dataframe({"All Securities Gainer":gl[0]['All Securities Gainer']})
    with col8:
        st.dataframe({"All Securities Loser":gl[1]['All Securities Loser']})
    with col9:
        st.dataframe({"FNO Gainer":gl[0]['FNO Gainer']})
    with col10:
        st.dataframe({"FNO Gainer":gl[1]['FNO Loser']})
except Exception as e:
    st.error(e)