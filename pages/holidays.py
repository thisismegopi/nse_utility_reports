import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Holidays for the calendar year 2025")

tab1, tab2 = st.tabs(["Trading Holidays", "Clearing Holidays"], width="stretch")

with tab1:
    try:
        st.dataframe(nse.trading_holidays(),height=600,column_config={
        "tradingDate": st.column_config.DateColumn("Date",format="localized"),
        "weekDay": st.column_config.TextColumn("Week day"),
        "description": st.column_config.TextColumn("Description"),
        "morning_session": st.column_config.TextColumn("Morning Session"),
        "evening_session": st.column_config.TextColumn("Evening Session"),
        "Sr_no": st.column_config.TextColumn("#"),
        })
        st.warning("⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.")
        st.write("Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).")
    except:
        st.warning("Unable to fetch data. Please try again later.")
with tab2:
    try:
        st.dataframe(nse.clearing_holidays(),height=600,column_config={
        "tradingDate": st.column_config.DateColumn("Date",format="localized"),
        "weekDay": st.column_config.TextColumn("Week day"),
        "description": st.column_config.TextColumn("Description"),
        "morning_session": st.column_config.TextColumn("Morning Session"),
        "evening_session": st.column_config.TextColumn("Evening Session"),
        "Sr_no": st.column_config.TextColumn("#"),
        })
        st.warning("⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals.")
        st.write("Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi).")
    except:
        st.warning("Unable to fetch data. Please try again later.")