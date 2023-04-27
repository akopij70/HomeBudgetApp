"""Module initializes database using sqlite instructions from home_budget.sql"""
import sqlite3

conn = sqlite3.connect('home_budget.db')
c = conn.cursor()

with open('home_budget.sql', 'r', encoding='utf-8') as sql_file:
    sql_script = sql_file.read()

c.executescript(sql_script)
conn.commit()

conn.close()
