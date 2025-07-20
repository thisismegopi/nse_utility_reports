import streamlit as st
import NseUtility

nse = NseUtility.NseUtils()

st.write("### Corporate Announcements")
try:
    st.dataframe(nse.get_corporate_announcement(),height=600, column_config={
        "symbol": st.column_config.TextColumn("Symbol"),
        "sm_name": st.column_config.TextColumn("Company Name"),
        "desc": st.column_config.TextColumn("Subject"),
        "attchmntFile": st.column_config.LinkColumn("Attachment", display_text="Link"),
        "attchmntText": st.column_config.TextColumn("Details"),
        "exchdisstime": st.column_config.DatetimeColumn("Date and Time"),
    })
except Exception as e:
    st.warning("Failed to fetch Corporate Announcements. Please try again later.")