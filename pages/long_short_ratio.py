import streamlit as st
import pandas as pd

st.write("# Participants Long/Short Ratio")
st.write(
    "Download the CSV file from [F&O - Participant wise Open Interest(csv)](https://www.nseindia.com/all-reports-derivatives) and upload it here."
)
csv = st.file_uploader("Upload a CSV file", type=["csv"])


def calculate_ratio(long, short):
    total = long + short
    long_ratio = (long / total) * 100 if total != 0 else 0
    short_ratio = (short / total) * 100 if total != 0 else 0
    return long_ratio, short_ratio


if csv is not None:
    df = pd.read_csv(csv, header=1)
    # st.dataframe(df, use_container_width=True)
    data = df.to_json()

    fii_future_index_long_ratio, fii_future_index_short_ratio = calculate_ratio(
        df["Future Index Long"][2], df["Future Index Short"][2]
    )
    dii_future_index_long_ratio, dii_future_index_short_ratio = calculate_ratio(
        df["Future Index Long"][1], df["Future Index Short"][1]
    )
    client_future_index_long_ratio, client_future_index_short_ratio = calculate_ratio(
        df["Future Index Long"][0], df["Future Index Short"][0]
    )
    pro_future_index_long_ratio, pro_future_index_short_ratio = calculate_ratio(
        df["Future Index Long"][3], df["Future Index Short"][3]
    )

    fii_future_stock_long_ratio, fii_future_stock_short_ratio = calculate_ratio(
        df["Future Stock Long"][2], df["Future Stock Short       "][2]
    )
    dii_future_stock_long_ratio, dii_future_stock_short_ratio = calculate_ratio(
        df["Future Stock Long"][1], df["Future Stock Short       "][1]
    )
    client_future_stock_long_ratio, client_future_stock_short_ratio = calculate_ratio(
        df["Future Stock Long"][0], df["Future Stock Short       "][0]
    )
    pro_future_stock_long_ratio, pro_future_stock_short_ratio = calculate_ratio(
        df["Future Stock Long"][3], df["Future Stock Short       "][3]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("### FII")
        fiiCol1, fiiCol2 = st.columns(2)
        with fiiCol1:
            st.metric(
                "Future Index Long",
                f"{fii_future_index_long_ratio:.2f}%",
                border=True,
            )
            st.metric(
                "Future Stock Long",
                f"{fii_future_stock_long_ratio:.2f}%",
                border=True,
            )
        with fiiCol2:
            st.metric(
                "Future Index Short",
                f"{fii_future_index_short_ratio:.2f}%",
                border=True,
            )
            st.metric(
                "Future Stock Short",
                f"{fii_future_stock_short_ratio:.2f}%",
                border=True,
            )
    with col2:
        st.write("### DII")
        diiCol1, diiCol2 = st.columns(2)
        with diiCol1:
            st.metric(
                "Future Index Long",
                f"{dii_future_index_long_ratio:.2f}%",
                border=True,
            )
            st.metric(
                "Future Stock Long",
                f"{dii_future_stock_long_ratio:.2f}%",
                border=True,
            )
        with diiCol2:
            st.metric(
                "Future Index Short",
                f"{dii_future_index_short_ratio:.2f}%",
                border=True,
            )
            st.metric(
                "Future Stock Short",
                f"{dii_future_stock_short_ratio:.2f}%",
                border=True,
            )
    with col3:
        st.write("### Client")
        clientCol1, clientCol2 = st.columns(2)
        with clientCol1:
            st.metric(
                "Future Index Long",
                f"{client_future_index_long_ratio:.2f}%",
                border=True,
            )
            st.metric(
                "Future Stock Long",
                f"{client_future_stock_long_ratio:.2f}%",
                border=True,
            )
        with clientCol2:
            st.metric(
                "Future Index Short",
                f"{client_future_index_short_ratio:.2f}%",
                border=True,
            )
            st.metric(
                "Future Stock Short",
                f"{client_future_stock_short_ratio:.2f}%",
                border=True,
            )
    with col4:
        st.write("### Pro")
        proCol1, proCol2 = st.columns(2)
        with proCol1:
            st.metric(
                "Future Index Long",
                f"{pro_future_index_long_ratio:.2f}%",
                border=True,
            )
            st.metric(
                "Future Stock Long",
                f"{pro_future_stock_long_ratio:.2f}%",
                border=True,
            )
        with proCol2:
            st.metric(
                "Future Index Short",
                f"{pro_future_index_short_ratio:.2f}%",
                border=True,
            )
            st.metric(
                "Future Stock Short",
                f"{pro_future_stock_short_ratio:.2f}%",
                border=True,
            )
