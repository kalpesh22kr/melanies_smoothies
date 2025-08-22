# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for customer name
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be", name_on_order)

# Connect to Snowflake and get fruit options
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table('smoothies.public.fruit_options').select(col('Fruit_name'))

# Multiselect for ingredients (up to 5)
ingredients_list = st.multiselect(
    'Choose up to five ingredients:',
    my_dataframe,
    max_selections=5
)

# Only proceed if user selects ingredients
if ingredients_list:
    # Build ingredients string
    ingredients_string = ' '.join(ingredients_list)

    # For now, the API call is hardcoded to watermelon - could be dynamic later
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

    # Show API response in a dataframe
    st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
