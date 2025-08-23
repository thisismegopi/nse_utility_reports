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

    col1, col2 = st.columns(2)
    with col1:
        st.write("#### Scheme Details")
        scheme_details = mf.get_scheme_details(selected_key)
        scheme_details_df = {
            "Fund House": scheme_details["fund_house"],
            "Scheme Type": scheme_details["scheme_type"],
            "Scheme Category": scheme_details["scheme_category"],
            "Scheme Code": scheme_details["scheme_code"],
            "Scheme Name": scheme_details["scheme_name"],
            "Scheme Start Date": scheme_details["scheme_start_date"]["date"],
            "NAV at Start Date": scheme_details["scheme_start_date"]["nav"],
        }
        st.dataframe(scheme_details_df, use_container_width=True)

    with col2:
        st.write("#### Scheme Quote")
        scheme_quote = mf.get_scheme_quote(selected_key)
        scheme_quote_df = {
            "Scheme Code": scheme_quote["scheme_code"],
            "Scheme Name": scheme_quote["scheme_name"],
            "Last Updated": scheme_quote["last_updated"],
            "NAV": scheme_quote["nav"],
        }
        st.dataframe(scheme_quote_df, use_container_width=True)

    st.write("#### Calculate Market value of Units")
    balance_units = st.number_input(
        "Enter Balance Units", min_value=0.0, value=0.0, step=0.01
    )
    if balance_units > 0:
        balance_units_value = mf.calculate_balance_units_value(
            selected_key, balance_units
        )
        balance_units_value_df = {
            "Scheme Code": balance_units_value["scheme_code"],
            "Scheme Name": balance_units_value["scheme_name"],
            "Last Updated": balance_units_value["last_updated"],
            "NAV": balance_units_value["nav"],
            "Balance Units": balance_units,
            "Market Value of Units": balance_units_value["balance_units_value"],
        }
        st.dataframe(balance_units_value_df, use_container_width=True)
