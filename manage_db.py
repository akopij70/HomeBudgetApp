"""Module allows to manage sqlite database - connects python to sqlite"""
import sqlite3
import os.path
import init_db

db_structure = {  # defines a list of columns for each table in the database
    "Expense": ["walletId", "userId", "amount", "date", "category", "name"],
    "Income": ["walletId", "userId", "amount", "date", "category", "name"],
    "User": ["name", "password", "userType"],
    "Wallet": ["balance", "type", "name"],
    "WalletOwnership": ["walletId", "userId"],
    "WishlistItem": ["userId", "name", "price"],
    "Category": ["name"],

    "v_login": ["name", "password"],
    "v_user_type": ["userType"],
    "v_wallet_incomes": ["name", "userId", "amount", "date", "category", "name"],
    "v_wallet_expenses": ["name", "userId", "amount", "date", "category", "name"]
}


class Db:
    """Class enables initializing database as well as inserting,
    modifying and deleting data from specified column and row"""
    def __init__(self, name: str, sample_data: bool = False):
        if not os.path.exists(name+".db"):
            print("Database initialized!")
            init_db.create_db(name,sample_data)
        self.conn = sqlite3.connect(name+".db")
        self.cursor = self.conn.cursor()

    def insert(self, table: str, columns: list[str]) -> None:
        """Inserts a row with specified columns to the given table"""
        values = ""
        for column in columns:
            if column is None:  # if no value specified
                values += "NULL,"
                continue
            if isinstance(column, (int,float)):  # if a number
                values += f"{column},"
                continue
            values += f"\"{column}\","
        if table in ["Expense", "Income", "v_wallet_incomes", "v_wallet_expenses"]:  # category validation
            if not self.is_category(columns[4]):
                self.cursor.execute(f'INSERT INTO Category (name) VALUES(\'{columns[4]}\')')
                print(f'A new category "{columns[4]}" has been created implicitly.')
        values = values[:-1]  # deletes last comma
        formated_columns = str(db_structure[table]).replace("'","").replace('"',''
                                                  ).replace("[","(").replace("]",")")
        self.cursor.execute('INSERT INTO '+table+' '+formated_columns+' '+'VALUES('+values+')')
        self.conn.commit()

    def delete(self, table: str, row_specifier=None) -> bool:
        """Deletes row from the specified table using row_specifier expressed as follows:
           \n For "Expense" and "Income": id: int
           \n For "WalletOwnership": [walletId,userId]: list
           \n For the other columns: name: str
           \n Returns 'True' if the row was deleted and 'False' if the row wasn't found."""

        if row_specifier is None:
            self.cursor.execute(f'DELETE FROM {table}')  # deletes all rows
            self.conn.commit()
            return True

        if table in ["Expense", "Income", "Wallet"]:
            is_elem = self.cursor.execute(f'SELECT id FROM {table} WHERE id = {row_specifier}').fetchone()
            self.cursor.execute(f'DELETE FROM {table} WHERE id = {row_specifier}')

        elif table in ["User", "WishlistItem", "Category"]:
            is_elem = self.cursor.execute(f'SELECT name FROM {table} WHERE name = \'{row_specifier}\'').fetchone()
            self.cursor.execute(f'DELETE FROM {table} WHERE name = \'{row_specifier}\'')

        elif table in ["WalletOwnership"]:
            is_elem = self.cursor.execute(f'SELECT walletId,userId FROM {table} WHERE walletId = {row_specifier[0]} AND userId = {row_specifier[1]}').fetchone()
            self.cursor.execute(f'DELETE FROM {table} WHERE walletId = {row_specifier[0]} AND userId = {row_specifier[1]}')

        if not is_elem:
            return False
        self.conn.commit()
        return True

    def set(self, table: str, column: str, row_specifier, new_val) -> None:
        """Modifies row of the given column with new_val using row_specifier expressed as follows:
           \n For "Expense" and "Income": id: int
           \n For "WalletOwnership": [walletId,userId]: list
           \n For the other columns: name: str"""

        if table in ["Expense", "Income", "Wallet"]:
            self.cursor.execute(f'UPDATE {table} SET {column}=\'{new_val}\' WHERE id = {row_specifier}')
        elif table in ["User", "WishlistItem", "Category"]:
            self.cursor.execute(f'UPDATE {table} SET {column}=\'{new_val}\' WHERE name = \'{row_specifier}\'')
        elif table in ["WalletOwnership"]:
            self.cursor.execute(f'UPDATE {table} SET {column}=\'{new_val}\' WHERE walletId = {row_specifier[0]} AND userId = {row_specifier[1]}')
        self.conn.commit()

    def get(self, table: str, row_specifier=None) -> list:
        """Returns row represented as list from a given column. row_specifier is expressed as follows:
           \n For "Expense" and "Income": id: int
           \n For "WalletOwnership": [walletId,userId]: list
           \n For the other columns: name: str"""

        if row_specifier is None:
            return self.cursor.execute(f'SELECT * FROM {table}').fetchall()
        elif table in ["Expense", "Income", "Wallet"]:
            return self.cursor.execute(f'SELECT * FROM {table} WHERE id = {row_specifier}').fetchall()
        elif table in ["User", "WishlistItem", "Category"]:
            return self.cursor.execute(f'SELECT * FROM {table} WHERE name = \'{row_specifier}\'').fetchall()
        elif table in ["WalletOwnership"]:
            return self.cursor.execute(f'SELECT * FROM {table} WHERE walletId = {row_specifier[0]} AND userId = {row_specifier[1]}').fetchall()
        return []

    def is_category(self, name: str) -> bool:
        """Checks if the given category is in the Category table"""
        self.cursor.execute("SELECT name FROM Category")
        categories = [elem[0] for elem in self.cursor.fetchall()]  # tuple unpacking
        for category in categories:
            if category == name:
                return True
        return False

    def get_view(self, view_name: str) -> list:
        """Returns a list of data from the given view specified by view_name."""
        views = [table for table in db_structure.keys() if table.startswith("v_")]
        if view_name not in views:
            raise ValueError(f'There is no {view_name} in the database!')

        return self.cursor.execute(f'SELECT * FROM {view_name}').fetchall()

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass


if __name__ == "__main__":  # debug and testing purpose only

    baza_danych = Db('home_budget', True)

    # baza_danych.insert("User", ["Fred", "admin", "Parent"])
    # baza_danych.insert("Wallet", [10_000, "Savings", "For holidays"])
    # baza_danych.insert("WalletOwnership", [1,1])
    # baza_danych.insert("WishlistItem", [1,"Car",20_000])
    # baza_danych.insert("Category", ["Bills"])
    # baza_danych.insert("Income", [1,1,100,"29.04.2023","Gift", None])
    # baza_danych.insert("Expense", [1,1,200,"26.04.2023","Gift", "Bob's birthday"])

    # baza_danych.delete("Category", "Gift")
    # baza_danych.delete("Expense", 1)
    # baza_danych.delete("User", "Fred")
    # baza_danych.delete("Wallet", "1")
    # baza_danych.delete("User")

    # baza_danych.set("Wallet", "balance", 1, 34_567)
    # baza_danych.set("Wallet", "type", 1, "deposit")
    # baza_danych.set("Wallet", "name", 1, "For future")
    # baza_danych.set("User", "name", "Fred", "Fredo")
    # baza_danych.set("WishlistItem", "price", "Car", 25_000)

    # print(baza_danych.get("Wallet", 1))
    # print(baza_danych.get("WishlistItem", "Car"))
    # print(baza_danych.get("Category"))

    # print(baza_danych.get_view("v_login"))

