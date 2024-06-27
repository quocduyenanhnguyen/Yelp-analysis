import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="username",
  password="password",
  database="database_name"
)

mycursor = mydb.cursor()


data = pd.read_csv("path/csv_file_name")
df = pd.DataFrame(data)


engine = create_engine("mysql+mysqlconnector://username:password@localhost/database_name")

df.to_sql('table_name', con=engine, if_exists='replace', index=False)


