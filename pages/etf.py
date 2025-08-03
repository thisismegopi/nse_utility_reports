import streamlit as st
import utils.NseUtility as NseUtility


def color_negative_red(value):
    """
    Colors the text red if the value is negative based on theme.
    """
    try:
        per_value = float(value["per"])
    except (ValueError, TypeError, KeyError):
        # Handle cases where 'per' is missing or not a number
        return [""] * len(value)

    if per_value > 0:
        return ["background-color: #00ff0020"] * len(value)
    else:
        return ["background-color: #ff000020"] * len(value)


def main():
    nse = NseUtility.NseUtils()
    st.write("### ETF's")

    search_text = st.text_input("Search", placeholder="Search ETF's.")
    show_row_color = st.toggle(
        "Show Row Color", label_visibility="visible", value=False
    )
    try:
        df = nse.get_etf_list(search_text=search_text)
        if df is None or df.empty:
            raise ValueError("ETF's not found for the given criteria.")
        if show_row_color is True:
            df = df.style.apply(color_negative_red, axis=1)
        st.dataframe(
            df,
            height=600,
            column_config={
                "symbol": st.column_config.TextColumn("Symbol"),
                "assets": st.column_config.TextColumn("Underlying Asset"),
                "open": st.column_config.NumberColumn("Open", format="%0.2f"),
                "high": st.column_config.NumberColumn("High", format="%0.2f"),
                "low": st.column_config.NumberColumn("Low", format="%0.2f"),
                "ltP": st.column_config.NumberColumn("LTP", format="%0.2f"),
                "chn": st.column_config.NumberColumn("Change", format="%0.2f"),
                "per": st.column_config.NumberColumn("% Change", format="%0.2f%%"),
                "qty": st.column_config.NumberColumn("Volume"),
                "trdVal": st.column_config.NumberColumn(
                    "Value (₹ Crores)", format="%0.2f"
                ),
                "nav": st.column_config.NumberColumn("NAV", format="%0.2f"),
                "wkhi": st.column_config.NumberColumn("52W H", format="%0.2f"),
                "wklo": st.column_config.NumberColumn("52W L", format="%0.2f"),
                "perChange30d": st.column_config.NumberColumn(
                    "30d % Change", format="%0.2f%%"
                ),
                "perChange365d": st.column_config.NumberColumn(
                    "365d % Change", format="%0.2f%%"
                ),
            },
            hide_index=True,
        )
    except Exception as e:
        st.error(f"Failed : {e}")


if __name__ == "__main__":
    main()
    st.warning(
        "⚠️Disclaimer : This Tool is meant for educational purposes only. Downloading data from NSE website requires explicit approval from the exchange. Hence, the usage of this utility is for limited purposes only under proper/explicit approvals."
    )
    st.write(
        "Please give a ⭐️ on [GitHub](https://github.com/thisismegopi/nse_utility_reports). Made with ❤️ by [Gopi](https://github.com/thisismegopi)."
    )
