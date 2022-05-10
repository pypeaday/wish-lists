import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

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

# options = {"Show me the lists": "lists", "I need to mark a wish as purchased": "mark"}

# _page = st.sidebar.selectbox("Where do you want to go?", options.keys())

# page = options[_page]


# if page == "lists":
#     with st.form("add item", clear_on_submit=True):
#         st.write("Make an addition")

#         person = st.text_input("Whose wish?")
#         item = st.text_input("What item?")
#         link = st.text_input("Gimmie a link")

#         # Every form must have a submit button.
#         submitted = st.form_submit_button("Submit")

#         s = pd.DataFrame.from_dict(
#             {
#                 "row": [
#                     person,
#                     item,
#                     link,
#                     False,
#                     None,
#                     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
#                 ]
#             },
#             orient="index",
#             columns=[
#                 "person",
#                 "item",
#                 "link",
#                 "purchased",
#                 "purchased_by",
#                 "date_added",
#             ],
#         )

#         if submitted:
#             s.to_sql("Wishes", engine, if_exists="append", index=False)
#             df = pd.read_sql_table("Wishes", engine)

#     st.markdown(df.to_markdown())

# elif page == "mark":
#     with st.form ("Which item did you purchase?"):
#         item = st.selectbox("Pick which wish",
#         [(id, p, i) for id, p,i in zip(df.id, df.person, df.item)])

#         # Every form must have a submit button.
#         submitted = st.form_submit_button("Submit")
#         if submitted:
#             requests.patch(f"http://localhost:8000/wishes/{id}", data={"purchased": True})
#     df = pd.read_sql_table("Wishes", engine)

st.markdown(df.to_markdown())

st.text(df.to_markdown())
