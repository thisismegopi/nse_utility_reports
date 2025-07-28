import streamlit as st
import pandas as pd
import utils.NseUtility as NseUtility

nse = NseUtility.NseUtils()

st.write("### Gainers & Losers")

selectBox = st.selectbox('Select Index', options={
    'NIFTY 50':'NIFTY',
    'BANK NIFTY':'BANKNIFTY',
    'NIFTY NEXT 50':'NIFTYNEXT50',
    'F&O Securities':'FOSec',
    'All Securities':'allSec',
})

index = {
    'NIFTY 50':'NIFTY',
    'BANK NIFTY':'BANKNIFTY',
    'NIFTY NEXT 50':'NIFTYNEXT50',
    'F&O Securities':'FOSec',
    'All Securities':'allSec',
}

tab1, tab2 = st.tabs(["Gainers", "Losers"])

with tab1:
    try:
        gainers = nse.get_gainers_losers_v2('gainers')
        if gainers is None:
            raise Exception("No data available for gainers.")
        else:
            # ✅ Only extract specific keys from each dictionary
            keys_to_extract = ['symbol', 'open_price','high_price', 'low_price', 'ltp', 'prev_price', 'perChange', 'trade_quantity', 'turnover']
            filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in gainers[index[selectBox]]['data']]
            df = pd.DataFrame(filtered_data)
            if df.empty:
                raise Exception("No data available for gainers.")
            else:
                st.dataframe(df, height=600, column_config={
                    "symbol": st.column_config.TextColumn("Symbol"),
                    "open_price": st.column_config.NumberColumn("Open Price", format="%0.2f"),
                    "high_price": st.column_config.NumberColumn("High Price", format="%0.2f"),
                    "low_price": st.column_config.NumberColumn("Low Price", format="%0.2f"),
                    "ltp": st.column_config.NumberColumn("LTP", format="%0.2f"),
                    "prev_price": st.column_config.NumberColumn("Previous Price", format="%0.2f"),
                    "perChange": st.column_config.NumberColumn("% Change", format="%0.2f%%"),
                    "trade_quantity": st.column_config.NumberColumn("Volume"),
                    "turnover": st.column_config.NumberColumn("Value"),
                })
                st.warning("⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.")
                st.write("Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).")
    except Exception as e:
        st.error(e)
with tab2:
    try:
        loosers = nse.get_gainers_losers_v2('loosers')
        if loosers is None:
            raise Exception("No data available for loosers.")
        else:
            # ✅ Only extract specific keys from each dictionary
            keys_to_extract = ['symbol', 'open_price','high_price', 'low_price', 'ltp', 'prev_price', 'perChange', 'trade_quantity', 'turnover']
            filtered_data = [{k: d.get(k) for k in keys_to_extract} for d in loosers[index[selectBox]]['data']]
            df = pd.DataFrame(filtered_data)
            if df.empty:
                raise Exception("No data available for loosers.")
            else:
                st.dataframe(df, height=600, column_config={
                    "symbol": st.column_config.TextColumn("Symbol"),
                    "open_price": st.column_config.NumberColumn("Open Price", format="%0.2f"),
                    "high_price": st.column_config.NumberColumn("High Price", format="%0.2f"),
                    "low_price": st.column_config.NumberColumn("Low Price", format="%0.2f"),
                    "ltp": st.column_config.NumberColumn("LTP", format="%0.2f"),
                    "prev_price": st.column_config.NumberColumn("Previous Price", format="%0.2f"),
                    "perChange": st.column_config.NumberColumn("% Change", format="%0.2f%%"),
                    "trade_quantity": st.column_config.NumberColumn("Volume"),
                    "turnover": st.column_config.NumberColumn("Value"),
                })
                st.warning("⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.")
                st.write("Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).")
    except Exception as e:
        st.error(f"Error fetching loosers: {e}")
