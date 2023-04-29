"""Module initializes database using sqlite instructions from home_budget.sql"""
import sqlite3

def create_db(name: str):
    """ Creates database from """
    conn = sqlite3.connect(name+".db")
    c = conn.cursor()

    with open(name+".sql", 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()

    c.executescript(sql_script)
    conn.commit()

    conn.close()
