import streamlit
streamlit.title('Snowflake Diner')

streamlit.header('Food made by Sean, For Sean (out of Sean)')
streamlit.header('Menu')

streamlit.text('🐔 Beans on toast (egg optional)')
streamlit.text('🥣Boring healthy cereal (ask for alternative milks)')
streamlit.text('🥗Nothing (fasting day)')
streamlit.text('🥑🍞Avacado on toast')
 
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


import pandas
#Load table
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#Set index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick your poison:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
#Chosen fruits assigned to variable
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display table
streamlit.dataframe(my_fruit_list)

import requests
streamlit.header("Fruityvice Fruit Advice!")
#Retreieve data from api
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#display it
streamlit.text(fruityvice_response.json())
