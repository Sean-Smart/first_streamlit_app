#Main body
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Snowflake Diner')

streamlit.header('Food made by Sean, For Sean (out of Sean)')
streamlit.header('Menu')

streamlit.text('🐔 Beans on toast (egg optional)')
streamlit.text('🥣Boring healthy cereal (ask for alternative milks)')
streamlit.text('🥗Nothing (fasting day)')
streamlit.text('🥑🍞Avacado on toast')
 
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


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


#make fruit search function
def get_fruityvice_data(this_fruit_choice):
    #Retreieve data from api
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
    #create a dataframe from the fruityvice api 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    #disaply df
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    #Inital prompt
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
         back_from_function = get_fruityvice_data(fruit_choice)
         streamlit.dataframe(back_from_function)
        
except URLError as e:
    streamlit.error(e)


  
#Exctract data from the SQL database
streamlit.text("The fruit load list contains:")
#snowflake related functions:
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
         my_cur.execute("SELECT * FROM fruit_load_list")
         return my_cur.fetchall()
    
#Add a button to load the fruit load list
if streamlit.button('Get fruit load list'):
    #Establish connection to snowflake
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    #Close connection
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
     


#User input of fruit function
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO fruit_load_list values ('"+new_fruit+"')")
        return "Thanks for adding " + new_fruit
   
#Allow user to input fruit 
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)


    
#New feature
#my_cur.execute("INSERT INTO fruit_load_list values ('from streamlit')")

