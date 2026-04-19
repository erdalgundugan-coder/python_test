import pandas as pd
import sqlite3

#df = pd.read_csv("C:\\Users\\exper\\Documents\\python_test\\nba.csv")
#df = pd.read_csv()
#df = pd.read_json("C:\\Users\\exper\\Documents\\python_test\\sample.json",encoding="UTF-8")
#df = pd.read_excel("C:\\Users\\exper\\Documents\\python_test\\sample.xlsx")
connection = sqlite3.connect("C:\\Users\\exper\\Documents\\python_test\\sample.db")
df = pd.read_sql_query("SELECT * FROM students", connection)
print(df)