import streamlit as st
import utils.NseUtility as NseUtility

nse = NseUtility.NseUtils()

def color_negative_red(value):
    """
    Colors the text red if the value is negative based on theme.
    """
    try:
        per_value = float(value['change'])
    except (ValueError, TypeError, KeyError):
        # Handle cases where 'per' is missing or not a number
        return [''] * len(value)

    if per_value > 0:
        return ['background-color: #00ff0020'] * len(value)
    else:
        return ['background-color: #ff000020'] * len(value)

st.write("### Most Active Equities")

tab1, tab2, tab3, tab4 = st.tabs(["Stocks by Volume", "Stocks by Value", "ETF's by Volume", "ETF's by Value"], width="stretch")

with tab1:
    try:
        df = nse.most_active_equity_stocks('volume')
        if df is None or df.empty:
            raise ValueError("No data available for the selected criteria.")
        st.dataframe(df.style.apply(color_negative_red, axis=1),height=600, column_config={
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
        }, hide_index=True)
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab2:
    try:
        df = nse.most_active_equity_stocks('value')
        if df is None or df.empty:
            raise ValueError("No data available for the selected criteria.")
        st.dataframe(df.style.apply(color_negative_red, axis=1),height=600, column_config={
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
        },hide_index=True)
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab3:
    try:
        df = nse.most_active_equity_etf('volume')
        if df is None or df.empty:
            raise ValueError("No data available for the selected criteria.")
        st.dataframe(df.style.apply(color_negative_red, axis=1),height=600, column_config={
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
        },hide_index=True)
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab4:
    try:
        df = nse.most_active_equity_etf('value')
        if df is None or df.empty:
            raise ValueError("No data available for the selected criteria.")
        st.dataframe(df.style.apply(color_negative_red, axis=1),height=600, column_config={
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
        },hide_index=True)
    except:
        st.warning("Unable to fetch data. Please try again later.")