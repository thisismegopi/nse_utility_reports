import streamlit as st
import utils.NseUtility as NseUtility


def color_negative_red(value):
    """
    Colors the text red if the value is negative based on theme.
    """
    try:
        per_value = float(value["change"])
    except (ValueError, TypeError, KeyError):
        # Handle cases where 'per' is missing or not a number
        return [""] * len(value)

    if per_value > 0:
        return ["background-color: #00ff0020"] * len(value)
    else:
        return ["background-color: #ff000020"] * len(value)


def main():
    nse = NseUtility.NseUtils()

    st.write("### Pre Market Info")
    list = st.selectbox("Select Index", nse.pre_market_list, index=0)
    try:
        data = nse.pre_market_info(category=list)

        col1, col2, col3 = st.columns(3)
        with col1:
            col1.metric(
                "Advance",
                data["advance_decline"]["advance"],
                border=True,
            )
        with col2:
            col2.metric(
                "Decline",
                data["advance_decline"]["decline"],
                border=True,
            )
        with col3:
            col3.metric(
                "Unchanged",
                data["advance_decline"]["unchanged"],
                border=True,
            )
        st.dataframe(
            data["data_frame"].style.apply(color_negative_red, axis=1),
            height=600,
            column_config={
                "symbol": st.column_config.TextColumn("Symbol"),
                "previousClose": st.column_config.NumberColumn(
                    "Prev. Close", format="%0.2f"
                ),
                "iep": st.column_config.NumberColumn("IEP", format="%0.2f"),
                "change": st.column_config.NumberColumn("Change", format="%0.2f"),
                "pChange": st.column_config.NumberColumn("% Change", format="%0.2f%%"),
                "lastPrice": st.column_config.NumberColumn("LTP", format="%0.2f"),
                "finalQuantity": st.column_config.NumberColumn("Final Qty"),
                "totalTurnover": st.column_config.NumberColumn(
                    "Value (₹ Crores)", format="%0.2f"
                ),
                "marketCap": st.column_config.NumberColumn(
                    "FFMC (₹ Crores)", format="%0.2f"
                ),
                "yearHigh": st.column_config.NumberColumn("52W H", format="%0.2f"),
                "yearLow": st.column_config.NumberColumn("52W L", format="%0.2f"),
                "chartTodayPath": st.column_config.ImageColumn("Today"),
            },
            hide_index=True,
        )
    except Exception:
        st.error("Failed to fetch pre-market data. Please try again later.")


if __name__ == "__main__":
    main()
