--- Initial Table Creation Queries ---
CREATE TABLE IF NOT EXISTS "User" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"userType"	TEXT NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "Category" (
	"name"	TEXT NOT NULL,
	PRIMARY KEY("name")
);

CREATE TABLE IF NOT EXISTS "Expense" (
	"id"	INTEGER NOT NULL,
	"walletId"	INTEGER NOT NULL,
	"userId"	INTEGER NOT NULL,
	"amount"	REAL NOT NULL,
	"date"	TEXT NOT NULL,
	"category"	TEXT NOT NULL,
	"name"	TEXT,
	FOREIGN KEY("category") REFERENCES "Category"("name"),
	FOREIGN KEY("walletId") REFERENCES "Wallet"("id"),
	FOREIGN KEY("userId") REFERENCES "User"("id"),
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "Income" (
	"id"	INTEGER NOT NULL,
	"walletId"	INTEGER NOT NULL,
	"userId"	INTEGER NOT NULL,
	"amount"	REAL NOT NULL,
	"date"	TEXT NOT NULL,
	"category"	TEXT NOT NULL,
	"name"	TEXT,
	FOREIGN KEY("category") REFERENCES "Category"("name"),
	FOREIGN KEY("walletId") REFERENCES "Wallet"("id"),
	FOREIGN KEY("userId") REFERENCES "User"("id"),
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "Wallet" (
	"id"	INTEGER NOT NULL,
	"balance"	REAL NOT NULL,
	"type"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "WalletOwnership" (
	"walletId"	INTEGER NOT NULL,
	"userId"	INTEGER NOT NULL,
	FOREIGN KEY("userId") REFERENCES "User"("id"),
	FOREIGN KEY("walletId") REFERENCES "Wallet"("id")
);

CREATE TABLE IF NOT EXISTS "WishlistItem" (
	"id"	INTEGER NOT NULL,
	"userId"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"price"	REAL NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("userId") REFERENCES "User"("id")
);

--- Index Creation Queries ---

CREATE INDEX IF NOT EXISTS "ix_expense_amount" ON "Expense" (
	"amount"	DESC
);

CREATE INDEX IF NOT EXISTS "ix_expense_category" ON "Expense" (
	"category"
);

CREATE INDEX IF NOT EXISTS "ix_expense_date" ON "Expense" (
	"date"
);

CREATE INDEX IF NOT EXISTS "ix_income_amount" ON "Income" (
	"amount"	DESC
);

CREATE INDEX IF NOT EXISTS "ix_income_category" ON "Income" (
	"category"
);

CREATE INDEX IF NOT EXISTS "ix_income_date" ON "Income" (
	"date"
);

CREATE INDEX IF NOT EXISTS "ix_wishlistitem_price" ON "WishlistItem" (
	"price"
);

--- View Creation Queries ---

CREATE VIEW IF NOT EXISTS v_login AS
	SELECT
		id, name, password
	FROM
		User;

CREATE VIEW IF NOT EXISTS v_user_type AS
	SELECT
		id, name, type
	FROM
		User;

--- Trigger Creation Queries ---

CREATE TRIGGER IF NOT EXISTS TR_update_wallet
    AFTER INSERT ON Income 
  BEGIN
    UPDATE Wallet SET balance = (balance + new.amount) WHERE id = new.walletId;
  END;

CREATE TRIGGER IF NOT EXISTS TR_modify_income
    AFTER UPDATE ON Income 
  BEGIN
    UPDATE Wallet SET balance = (balance - old.amount + new.amount) WHERE id = new.walletId;
  END;

 CREATE TRIGGER IF NOT EXISTS TR_delete_income
    AFTER DELETE ON Income 
  BEGIN
    UPDATE Wallet SET balance = (balance - old.amount) WHERE id = new.walletId;
  END;
 
 CREATE TRIGGER IF NOT EXISTS TR_add_expense
    AFTER INSERT ON Expense 
  BEGIN
    UPDATE Wallet SET balance = (balance - new.amount) WHERE id = new.walletId;
  END;

CREATE TRIGGER IF NOT EXISTS TR_modify_expense
    AFTER UPDATE ON Expense 
  BEGIN
    UPDATE Wallet SET balance = (balance + old.amount - new.amount) WHERE id = new.walletId;
  END;

 CREATE TRIGGER IF NOT EXISTS TR_delete_expense
    AFTER DELETE ON Expense 
  BEGIN
    UPDATE Wallet SET balance = (balance + old.amount) WHERE id = new.walletId;
  END;