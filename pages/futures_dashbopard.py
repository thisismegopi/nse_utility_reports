import streamlit as st
import utils.NseUtility as NseUtility
from datetime import datetime
import pandas as pd
import duckdb

nse = NseUtility.NseUtils()

st.write("### Future Market Movers")

try:
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Enter Date", datetime.now().date())
        
    fo_main = pd.DataFrame(nse.fno_bhav_copy(trade_date=date.strftime('%d-%m-%Y')))
    sec_main = pd.DataFrame(nse.bhav_copy_with_delivery(trade_date=date.strftime('%d-%m-%Y')))
    con = duckdb.connect(database=':memory:', read_only=False)

    with col2:
        xpry_dt = st.selectbox("Select Expiry Date", con.execute("SELECT DISTINCT XpryDt FROM fo_main WHERE FinInstrmTp ='STF' ORDER BY XpryDt").df())
    fo = con.execute(f'''SELECT * FROM fo_main WHERE XpryDt = '{xpry_dt}' AND FinInstrmTp ='STF' ''').df()
    sec = con.execute(f'''SELECT * FROM sec_main WHERE SERIES = 'EQ' ''').df()

    consolidated = con.execute(f'''
        SELECT 
            fo."TckrSymb",
            fo."OpnIntrst", 
            fo."ChngInOpnIntrst", 
            sec."PREV_CLOSE" AS "Prev Close",
            sec."CLOSE_PRICE" AS "Close Price",
            sec."CLOSE_PRICE" - sec."PREV_CLOSE" AS "Price Change",
            CASE 
                WHEN (sec."CLOSE_PRICE" - sec."PREV_CLOSE") > 0 AND fo."ChngInOpnIntrst" > 0 THEN 'Long Buildup'
                WHEN (sec."CLOSE_PRICE" - sec."PREV_CLOSE") > 0 AND fo."ChngInOpnIntrst" < 0 THEN 'Short Covering'
                WHEN (sec."CLOSE_PRICE" - sec."PREV_CLOSE") < 0 AND fo."ChngInOpnIntrst" < 0 THEN 'Long Unwinding'
                WHEN (sec."CLOSE_PRICE" - sec."PREV_CLOSE") < 0 AND fo."ChngInOpnIntrst" > 0 THEN 'Short Buildup'
            END AS "Participant Action",
            sec."DELIV_PER" as "Delivery Percentage"
        FROM fo AS fo 
        INNER JOIN sec AS sec ON fo."TckrSymb" = sec."SYMBOL" 
    ''').df()
    def style_participant_action(row):
        action = row['Participant Action']
        if action in ['Long Buildup', 'Short Covering']:
            return ['background-color: #d4edda; color: #155724'] * len(row)
        elif action in ['Long Unwinding', 'Short Buildup']:
            return ['background-color: #f8d7da; color: #721c24'] * len(row)
        return [''] * len(row)

    st.dataframe(consolidated.style.apply(style_participant_action, axis=1), height=600)
    st.warning(
    "⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals."
    )
    st.write(
    "Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi)."
    )
except Exception as e:
    st.error(e)