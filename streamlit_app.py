#Main body
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
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#Retreieve data from api
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#display it
#streamlit.text(fruityvice_response.json())

#create a dataframe from the fruityvice api 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#disaply df
streamlit.dataframe(fruityvice_normalized)




#Adding snowflake connector functionality
import snowflake.connector

#This allows you to execute SQL queries I think
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("SELECT * FROM fruit_load_list")
my_cur.execute("INSERT INTO fruit_load_list values ('from streamlit)")
my_data_row = my_cur.fetchone()
#streamlit.text("Greetings Earthling, you have made connection with the following:")
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)

#User input of fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

