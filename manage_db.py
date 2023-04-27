"""Module allows to manage sqlite database - connects python to sqlite"""
import sqlite3
import os.path

db_structure = {  # defines a list of columns for each table in the database
    "Expense" : ["walletId","userId","amount","date","category","name"],
    "Income" : ["walletId","userId","amount","date","category","name"],
    "User" : ["name","password","userType"],
    "Wallet" : ["balance","type","name"],
    "WalletOwnership" : ["walletId","userId"],
    "WishlistItem" : ["userId","name","price"]
}

class Db:
    """Class enables initializing database as well as inserting,
    modifying and deleting data from specified column and row"""
    def __init__(self, file: str):
        if not os.path.exists('home_budget.db'):
            print("Database initialized!")
            os.system("python init_db.py")
        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()

    def insert_data(self, table: str, columns: list[str]):
        """Inserts row with specified columns to given table"""
        values = ""
        for column in columns:
            if column is None:  # if no value specified
                values += "NULL,"
                continue
            if isinstance(column, (int,float)):  # if a number
                values += f"{column},"
                continue
            values += f"\"{column}\","

        values = values[:-1]  # deletes last comma
        formated_columns = str(tuple(db_structure[table])).replace("'","").replace('"', '')
        self.cursor.execute('INSERT INTO '+table+' '+formated_columns+' '+'VALUES('+values+')')
        self.conn.commit()

    def modify_data(self, table: str, column: str, new_val):
        pass

    def delete_data(self, table: str, column: str):
        pass

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":

    baza_danych = Db('home_budget.db')
    baza_danych.insert_data("User", ["Fred", "admin", "Parent"])
    baza_danych.insert_data("Wallet", [10_000, "Savings", "For holidays"])
