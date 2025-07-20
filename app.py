import streamlit as st

st.set_page_config(layout="wide")
pg = st.navigation([
    st.Page("./pages/index_details.py", title="Index Details", icon="📈"),
    st.Page("./pages/pre_market_info.py", title="Pre Market Info", icon="📈"),
    st.Page("./pages/fii_dii_data.py", title="FII & DII Data", icon="📈"),
    st.Page("./pages/advance_decline.py", title="Advance/Decline", icon="📈"),
    st.Page("./pages/gainers_losers.py", title="Gainers & Losers", icon="📈"),
    st.Page("./pages/most_active_equity.py", title="Most Active Equities", icon="📈"),
    st.Page("./pages/index_div_yield.py", title="Index Dividend Yield", icon="📈"),
    st.Page("./pages/index_pe_pb_ratio.py", title="Index PE & PB Ratio", icon="📈"),
    st.Page("./pages/corporate_action.py", title="Corporate Actions", icon="📈"),
    st.Page("./pages/corporate_announcement.py", title="Corporate Announcements", icon="📈"),
    st.Page("./pages/upcoming_results_calendar.py", title="Upcoming Results", icon="📈"),
    st.Page("./pages/holidays.py", title="Holidays", icon="📈"),
    st.Page("./pages/etf.py", title="ETF's", icon="📈"),
    st.Page("./pages/mutual_funds.py", title="Mutual Funds", icon="💵"),
])
pg.run()