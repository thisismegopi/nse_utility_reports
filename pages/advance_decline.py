import streamlit as st
import utils.NseUtility as NseUtility

nse = NseUtility.NseUtils()

st.write("### Advance/Decline")
try:
    st.dataframe(nse.get_advance_decline(),height=600)
    st.warning("⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.")
    st.write("Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).")
except Exception as e:
    st.error(e)