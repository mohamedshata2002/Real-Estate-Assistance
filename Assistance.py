import sqlite3 as db
import pandas as pd
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema ,StructuredOutputParser
import os 
from apis import google


os.environ["google_api_key"] =google
conn = db.connect("real_state.db")
cursor = conn.cursor()
model = GoogleGenerativeAI(model="models/gemini-1.5-flash")
disc = ResponseSchema(name="sql",description="extract the sql code that can run on sqlite")
sql_output = StructuredOutputParser(response_schemas=[disc])
template =template ="you are sql writer who write the top 5 rows  for these a table called real_state it and has columns: that is brokered by (categorically encoded agency/broker)\
status (Housing status - for_sale or  to_build)\
price (Housing price, it is either the current listing price or recently sold price if the house is sold recently)\
bed (# of beds)\
bath (# of bathrooms)\
acre_lot (Property / Land size in acres)\
street (categorically encoded street address)\
city (city name)\
state (state name)\
zip_code (postal code of the area)\
house_size (house area/size/living space in square feet)\
prev_sold_date (Previously sold date) \
    you have question and transfer it into sql the get the result \
        I want the output to be just no big spaces or labels sql query  and dont write any thing after ; or / \
        question:{question}\
             table called real_state \
            from that query extract the sql and the output  and the format instruction :its a json formate that have name sql and the discription is extract the sql code that can run on sqlite "
prompt = ChatPromptTemplate.from_template(template=template)
sql_transfromer = ({'question':RunnablePassthrough()}|
         prompt|model|sql_output)



template_2 ="You are a real state agent you get a dataframe result I want you to rephrase it for  a real state customer and return it as he is talking to you  but view all the dataframe options \
    if the dataframe is empty tell him that you dont have it \
        I want you to talk arabic about the result and the number is arabic and I just want all arabic no head lines bec it will be readed by voice ai  and make the number has , bettween them so it can be readed good\
    dataframe:{dataframe}"
prompt_2 = ChatPromptTemplate.from_template(template_2)
real_state_assistance = ({'dataframe':RunnablePassthrough()}|
         prompt_2|model|StrOutputParser())




template_3 = "from the context The user will select a one  from it make a markdown dataframe  from his instraction if there no instruction dont write any thing  \
    context :{context} \
        instraction:{inst}"
prompt_3 = ChatPromptTemplate.from_template(template_3)
choser = ({"context":RunnablePassthrough(),'inst':RunnablePassthrough()}|
         prompt_3|model|StrOutputParser())

def sql_excuter(sql):
    dataset =pd.read_sql_query(sql,conn)
    return dataset





prompt_ar = ChatPromptTemplate.from_template("these word is coming from automited voice regonation so try to make sence of it just give me the answer dont explain it to me words :{words}")
arabic_transformer = ({'words':RunnablePassthrough()}|
         prompt_ar|model|StrOutputParser())
