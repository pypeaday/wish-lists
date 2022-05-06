import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

import time

SQLALCHEMY_DATABASE_URL = "sqlite:///wishes.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# # @st.cache()
# def get_data(engine):

#     df = pd.read_sql_table('Wishes', engine)
#     return df


# if __name__ == "__main__":
#     df = get_data(engine)
#     st.dataframe(df)

df = pd.read_sql_table("Wishes", engine)

with st.form("add item", clear_on_submit=True):
    st.write("Make an addition")

    person = st.text_input("Whose wish?")
    item = st.text_input("What item?")
    link = st.text_input("Gimmie a link")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")

    # s = pd.DataFrame.from_dict({
    #     'person': person,
    #     'item': item,
    #     'link': link,
    #     'purchased': False,
    #     'purchased_by': None,
    #     'date_added': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # }, orient="index")
    s = pd.DataFrame.from_dict(
        {
            "row": [
                person,
                item,
                link,
                False,
                None,
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            ]
        },
        orient="index",
        columns=["person", "item", "link", "purchased", "purchased_by", "date_added"],
    )

    if submitted:
        s.to_sql("Wishes", engine, if_exists="append", index=False)
        df = pd.read_sql_table("Wishes", engine)

st.write("Outside the form")

st.markdown(df.to_markdown())
