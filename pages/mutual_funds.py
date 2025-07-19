import streamlit as st

st.write('# Mutual fund! 💵')

def connecto_to_db():
    try:
        return st.connection("postgresql", type="sql")
    except KeyError:
        return st.error("Could not connect to database")

conn = connecto_to_db()
df = conn.query("SELECT mft.symbol AS Fund, " \
    "AVG(mft.price) AS average_price, " \
    "mfn.nav AS current_price, "
    "SUM(mft.quantity) AS units, " \
    "SUM(mft.price * mft.quantity) AS invested, " \
    "SUM(mft.price * mft.quantity + (mfn.nav - mft.price) * mft.quantity) AS current_value, " \
    "SUM((mfn.nav - mft.price) * mft.quantity) AS profit_or_loss " \
    "FROM mutual_fund_transaction AS mft " \
    "LEFT JOIN mutual_fund_nav AS mfn ON mft.isin = mfn.isin " \
    "WHERE mft.trade_type = 'buy' AND mft.isin NOT IN ('INF247L01445', 'INF204K01ZH0') " \
    "GROUP BY mft.symbol, mft.isin, mfn.nav " \
    "ORDER BY invested DESC;")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Invested", df["invested"].sum().round(), border=True   )

with col2:
    st.metric("Current value", df["current_value"].sum().round(), border=True)

with col3:
    st.metric("Profit & Loss", df["profit_or_loss"].sum().round(), border=True)

st.write("### Holdings")
st.dataframe(df, use_container_width=True, hide_index=True)

st.write("### Last 10 transactions")
transaction = conn.query("SELECT * FROM mutual_fund_transaction ORDER BY trade_date DESC LIMIT 10")
st.dataframe(transaction, use_container_width=True, hide_index=True)