"""Module initializes database using sqlite instructions from home_budget.sql"""
import sqlite3


def create_db(name: str, load_sample: bool):
    """Creates database from"""
    conn = sqlite3.connect(name + ".db")
    c = conn.cursor()

    with open(name + ".sql", "r", encoding="utf-8") as sql_file:
        sql_script = sql_file.read()

    c.executescript(sql_script)

    if load_sample:
        with open("sample_data.sql", "r", encoding="utf-8") as sample_file:
            c.executescript(sample_file.read())

    conn.commit()
    conn.close()
