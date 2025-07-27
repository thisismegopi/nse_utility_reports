import streamlit as st
import NseUtility

def color_negative_red(value):
    """
    Colors the text red if the value is negative based on theme.
    """
    return ['background-color: #00ff0020',]*len(value) if value['pChange'] > 0 else ['background-color: #ff000020']*len(value)

def main():
    nse = NseUtility.NseUtils()
    st.write('### Index Details!')
    index = st.selectbox("Select Index", nse.equity_market_list, index=0)
    try:
        index_details = nse.get_index_details(category=index)
        
        st.dataframe(index_details.style.apply(color_negative_red, axis=1), height=600, column_config={
            "symbol": st.column_config.TextColumn("Symbol"),
            "priority": st.column_config.NumberColumn("Priority"),
            "open": st.column_config.NumberColumn("Open", format="%0.2f"),
            "dayHigh": st.column_config.NumberColumn("High", format="%0.2f"),
            "dayLow": st.column_config.NumberColumn("Low", format="%0.2f"),
            "lastPrice": st.column_config.NumberColumn("LTP", format="%0.2f"),
            "previousClose": st.column_config.NumberColumn("Prev. Close", format="%0.2f"),
            "change": st.column_config.NumberColumn("Change", format="%0.2f"),
            "pChange": st.column_config.NumberColumn("% Change", format="%0.2f%%"),
            "ffmc": st.column_config.NumberColumn("Market Cap", format="%0.2f"),
            "yearHigh": st.column_config.NumberColumn("52W H", format="%0.2f"),
            "yearLow": st.column_config.NumberColumn("52W L", format="%0.2f"),
            "totalTradedVolume": st.column_config.NumberColumn("Volume (Shares)"),
            "totalTradedValue": st.column_config.NumberColumn("Value (₹ Lakhs)"),
            "perChange30d": st.column_config.NumberColumn("% Change 30d", format="%0.2f%%"),
            "perChange365d": st.column_config.NumberColumn("% Change 356d", format="%0.2f%%"),
        },hide_index=True)
    except:
        st.warning('Error fetching index details')

if __name__ == "__main__":
    main()