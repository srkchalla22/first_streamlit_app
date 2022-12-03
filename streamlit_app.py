import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom''s New Healthy Diner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list= my_fruit_list.set_index('Fruit')

#Let's put a pick list here so they can pick fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the page
streamlit.dataframe(fruits_to_show)



#import requests
#fruityvice_response =  requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
##streamlit.text(fruityvice_response.json()) # just writes the data to the screen

#create a repeatable code block(called a function)
def get_fruityvice_data(this_fruit_choice):
    #streamlit.header('Line1 Function'+this_fruit_choice)
    fruityvice_responce = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    #if not fruityvice_responce:
    #    streamlit.header('Line2 Function Empty')    
    fruityvice_normalized = pandas.json_normalize(fruityvice_responce.json())
    #if not fruityvice_normalized:
    #    streamlit.header('Line3 Function')        
    return fruityvice_normalized

#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
    #Below code is choice based
    fruit_choice= streamlit.text_input('What fruit would you like the information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function=get_fruityvice_data(fruit_choice)
        #if not back_from_function:
        #    streamlit.error("Back from function is empty")
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
#import requests
#fruityvice_responce = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)

#take the json version of the response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_responce.json())
#output it the screen as a table
#streamlit.dataframe(fruityvice_normalized)

#don't run anything past here while we troubleshoot
#streamlit.stop()
#import snowflake.connector

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)

#my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
#Fecth all instead of one
#my_data_rows = my_cur.fetchall()
#streamlit.text("The fruit load list containse:")
#streamlit.text(my_data_row)

#To display in tabluar format
#streamlit.header("The fruit load list contains:")
streamlit.header("View Our Fruit List - Add Your Favorites!')
#Snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
#Allow the end user to add a fruit to th elist
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('"+ new_fruit +"')")
        return "Thanks for adding " + new_fruit

#Below code is choice based
add_my_fruit= streamlit.text_input('What fruit would you like add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

#This will not work correctly, but just go with it for now

#my_cur.execute("insert into fruit_load_list values('from streamlit')")
