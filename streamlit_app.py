# Import python packages
import streamlit as st
from snowflake.snowpark.session import session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(" :cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """
    Add your favourite fruits for custom smoothie
    """
)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:"
    , my_dataframe
    , max_Selections=5
)



if ingredients_list:
    ingredients_string = ''

    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
    #st.write(ingredients_list)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """' , '"""+name_on_order+"""')"""
    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

cnx = st.connected("snowflake")
session = cnx.session()
