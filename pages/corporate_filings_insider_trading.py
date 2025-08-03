import streamlit as st
import utils.NseUtility as NseUtility

nse = NseUtility.NseUtils()


def color_negative_red(value):
    """
    Colors the text red if the value is negative based on theme.
    """
    try:
        per_value = str(value["tdpTransactionType"])
    except (ValueError, TypeError, KeyError):
        # Handle cases where 'per' is missing or not a number
        return [""] * len(value)

    if per_value == "Buy":
        return ["background-color: #00ff0020"] * len(value)
    else:
        return ["background-color: #ff000020"] * len(value)


st.write("### Corporate Filings - Insider Trading")
symbol = st.text_input("Search", key="symbol", placeholder="Enter a symbol to search")
try:
    df = nse.get_corporate_filings_insider_trading(symbol=symbol)
    if df is None:
        raise ValueError("No data found for the given symbol.")
    st.dataframe(
        df.style.apply(color_negative_red, axis=1),
        height=600,
        hide_index=True,
        column_config={
            "symbol": st.column_config.TextColumn("Symbol"),
            "company": st.column_config.TextColumn("Company"),
            "acqName": st.column_config.TextColumn("Acquirer/Disposer"),
            "date": st.column_config.DatetimeColumn("Broadcast Date/Time"),
            "acqMode": st.column_config.TextColumn("Acquisition Mode"),
            "personCategory": st.column_config.TextColumn("Person Category"),
            "secType": st.column_config.TextColumn("Security Type"),
            "secAcq": st.column_config.NumberColumn("Security Acquired/Disposed"),
            "tdpTransactionType": st.column_config.TextColumn("Acquired/Disposed"),
            "befAcqSharesNo": st.column_config.NumberColumn(
                "Before Acquisition Shares No."
            ),
            "befAcqSharesPer": st.column_config.NumberColumn(
                "Before Acquisition Shares %", format="%0.2f%%"
            ),
            "secVal": st.column_config.NumberColumn(
                "Value of Securities Acquired/Disposed"
            ),
            "afterAcqSharesNo": st.column_config.NumberColumn(
                "After Acquisition Shares No."
            ),
            "afterAcqSharesPer": st.column_config.NumberColumn(
                "After Acquisition Shares %", format="%0.2f%%"
            ),
            "intimDt": st.column_config.DateColumn(
                "Intimation Date", format="YYYY-MM-DD"
            ),
        },
    )
except Exception as e:
    st.warning(e)
