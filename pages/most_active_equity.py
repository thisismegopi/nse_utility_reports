import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Most Active Equities")

tab1, tab2, tab3, tab4 = st.tabs(["Stocks by Volume", "Stocks by Value", "ETF's by Volume", "ETF's by Value"], width="stretch")

with tab1:
    try:
        st.dataframe(nse.most_active_equity_stocks('volume'),height=600, column_config={
            "symbol": st.column_config.TextColumn("Symbol"),
            "open": st.column_config.NumberColumn("Open", format="%0.2f"),
            "dayHigh": st.column_config.NumberColumn("High", format="%0.2f"),
            "dayLow": st.column_config.NumberColumn("Low", format="%0.2f"),
            "lastPrice": st.column_config.NumberColumn("LTP", format="%0.2f"),
            "previousClose": st.column_config.NumberColumn("Previous Close", format="%0.2f"),
            "change": st.column_config.NumberColumn("Change", format="%0.2f"),
            "pChange": st.column_config.NumberColumn("%", format="%0.2f%%"),
            "totalTradedVolume": st.column_config.NumberColumn("Volume (Shares)"),
            "totalTradedValue": st.column_config.NumberColumn("Value (₹ Lakhs)"),
            "yearHigh": st.column_config.NumberColumn("52WH"),
            "yearLow": st.column_config.NumberColumn("52WL"),
            "lastUpdateTime": st.column_config.DatetimeColumn("Last Updated Time"),
        })
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab2:
    try:
        st.dataframe(nse.most_active_equity_stocks('value'),height=600, column_config={
            "symbol": st.column_config.TextColumn("Symbol"),
            "open": st.column_config.NumberColumn("Open", format="%0.2f"),
            "dayHigh": st.column_config.NumberColumn("High", format="%0.2f"),
            "dayLow": st.column_config.NumberColumn("Low", format="%0.2f"),
            "lastPrice": st.column_config.NumberColumn("LTP", format="%0.2f"),
            "previousClose": st.column_config.NumberColumn("Previous Close", format="%0.2f"),
            "change": st.column_config.NumberColumn("Change", format="%0.2f"),
            "pChange": st.column_config.NumberColumn("%", format="%0.2f%%"),
            "totalTradedVolume": st.column_config.NumberColumn("Volume (Shares)"),
            "totalTradedValue": st.column_config.NumberColumn("Value (₹ Lakhs)"),
            "yearHigh": st.column_config.NumberColumn("52WH"),
            "yearLow": st.column_config.NumberColumn("52WL"),
            "lastUpdateTime": st.column_config.DatetimeColumn("Last Updated Time"),
        })
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab3:
    try:
        st.dataframe(nse.most_active_equity_etf('volume'),height=600, column_config={
            "symbol": st.column_config.TextColumn("Symbol"),
            "open": st.column_config.NumberColumn("Open", format="%0.2f"),
            "dayHigh": st.column_config.NumberColumn("High", format="%0.2f"),
            "dayLow": st.column_config.NumberColumn("Low", format="%0.2f"),
            "lastPrice": st.column_config.NumberColumn("LTP", format="%0.2f"),
            "nav": st.column_config.NumberColumn("NAV", format="%0.2f"),
            "previousClose": st.column_config.NumberColumn("Previous Close", format="%0.2f"),
            "change": st.column_config.NumberColumn("Change", format="%0.2f"),
            "pChange": st.column_config.NumberColumn("%", format="%0.2f%%"),
            "totalTradedVolume": st.column_config.NumberColumn("Volume (Shares)"),
            "totalTradedValue": st.column_config.NumberColumn("Value (₹ Lakhs)"),
        })
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab4:
    try:
        st.dataframe(nse.most_active_equity_etf('value'),height=600, column_config={
            "symbol": st.column_config.TextColumn("Symbol"),
            "open": st.column_config.NumberColumn("Open", format="%0.2f"),
            "dayHigh": st.column_config.NumberColumn("High", format="%0.2f"),
            "dayLow": st.column_config.NumberColumn("Low", format="%0.2f"),
            "lastPrice": st.column_config.NumberColumn("LTP", format="%0.2f"),
            "nav": st.column_config.NumberColumn("NAV", format="%0.2f"),
            "previousClose": st.column_config.NumberColumn("Previous Close", format="%0.2f"),
            "change": st.column_config.NumberColumn("Change", format="%0.2f"),
            "pChange": st.column_config.NumberColumn("%", format="%0.2f%%"),
            "totalTradedVolume": st.column_config.NumberColumn("Volume (Shares)"),
            "totalTradedValue": st.column_config.NumberColumn("Value (₹ Lakhs)"),
        })
    except:
        st.warning("Unable to fetch data. Please try again later.")