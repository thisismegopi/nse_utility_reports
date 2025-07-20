import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Upcoming Results Calendar")
# symbol = st.text_input("Search", key="symbol", placeholder="Enter a symbol to search")
try:
    df = nse.get_upcoming_results_calendar()
    if df is None or df.empty:
        st.warning("No upcoming results found.")
    else:
        st.dataframe(df, height=600,column_config={
        "symbol": st.column_config.TextColumn("Symbol"),
        "company": st.column_config.TextColumn("Company"),
        "purpose": st.column_config.TextColumn("Purpose"),
        "bm_desc": st.column_config.TextColumn("Description"),
        "date": st.column_config.DateColumn("Date", format="localized"),
    })
except Exception as e:
    st.error(e)