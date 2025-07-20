import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Corporate Actions")
symbol = st.text_input("Search", key="symbol", placeholder="Enter a symbol to search")
try:
    st.dataframe(nse.get_corporate_action(symbol=symbol),height=600,column_config={
        "symbol": st.column_config.TextColumn("Symbol"),
        "series": st.column_config.TextColumn("Series"),
        "faceVal": st.column_config.TextColumn("Face Value"),
        "subject": st.column_config.TextColumn("Subject"),
        "exDate": st.column_config.DateColumn("Ex Date",format="localized"),
        "recDate": st.column_config.DateColumn("Record Date",format="localized"),
        "isin": st.column_config.TextColumn("ISIN"),
        "comp": st.column_config.TextColumn("Company"),
    })
except Exception as e:
    st.error(e)