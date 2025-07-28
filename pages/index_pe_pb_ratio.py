import streamlit as st
import utils.NseUtility as NseUtility

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

st.warning("⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.")
st.write("Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).")