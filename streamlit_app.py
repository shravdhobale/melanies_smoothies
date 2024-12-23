import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Snowflake connection parameters
connection_parameters = {
    "account": "your_account",
    "user": "your_username",
    "password": "your_password",
    "role": "your_role",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema"
}

# Create a Snowflake session
session = Session.builder.configs(connection_parameters).create()

# Streamlit UI
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Add your favourite fruits for a custom smoothie")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Fetch data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe['FRUIT_NAME'], max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    st.write(my_insert_stmt)

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
