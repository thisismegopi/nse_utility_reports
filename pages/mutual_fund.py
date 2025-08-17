import streamlit as st
import json
from mftool import Mftool

st.write("# Mutual Funds")


mf = Mftool()

data = mf.get_scheme_codes(as_json=True)
selected_fund = st.selectbox("Select a Fund", options=json.loads(data).values())
selected_key = [k for k, v in json.loads(data).items() if v == selected_fund][0]


if selected_key != "Scheme Code":
    st.write("Selected Fund ID:", selected_key)
    st.write("#### Scheme Details")
    mf_details = mf.get_scheme_details(selected_key)
    st.write(mf_details)

    st.write("#### Scheme Quote")
    returns = mf.get_scheme_quote(selected_key)
    st.write(returns)
