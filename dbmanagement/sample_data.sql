INSERT INTO User (name,password,userType)
VALUES
   ('Joshua','qwerty','parent'),
   ('Stella','123456','parent'),
   ('Miranda','abc123','child'),
   ('Gibson','1234','child');

INSERT INTO Wallet (balance,type,name)
VALUES
   (53643.34,'joint','Main budget'),
   (147074.84,'savings','Savings'),
   (5295.25,'personal',"Joshua's wallet"),
   (897.11,'personal',"Stella's wallet"),
   (12.45,"children's","Miranda's wallet"),
   (25.01,"children's","Gibson's wallet");

INSERT INTO WalletOwnership (walletId,userId)
VALUES
   (1,1),
   (1,2),
   (1,3),
   (2,1),
   (2,2),
   (2,4),
   (3,5),
   (4,6);

INSERT INTO Category (name)
VALUES
   ("Housing"),
   ("Entertainment"),
   ("Car"),
   ("Groceries"),
   ("Utilities"),
   ("Clothing"),
   ("Healthcare"),
   ("Household supplies"),
   ("Personal"),
   ("Education"),
   ("Savings"),
   ("Salary"),
   ("Investing");

INSERT INTO WishlistItem (userId,name,price)
VALUES
   (1,'Motorcycle',45000),
   (1,'Piano',20000),
   (2,'Purse',1500),
   (2,'Phone',4000),
   (3,'Bike',2000),
   (3,'Headphones',500),
   (4,'Polaroid',500),
   (4,'Trip',800);

INSERT INTO Income (walletId,userId,amount,date,category,name)
VALUES
   (1,1,15000,"03.01.2023","Salary","NULL"),
   (1,1,2000,"11.03.2023","Investing","Interest"),
   (1,2,5000,"01.02.2023","Salary","NULL"),
   (5,3,200,"23.02.2023","Personal","Gift"),
   (6,4,100,"13.03.2023","Personal","Lottery");

INSERT INTO Expense (walletId,userId,amount,date,category,name)
VALUES
   (1,1,1500,"01.02.2023","Housing","Mortgage"),
   (1,1,100,"10.02.2023","Utilities","Water"),
   (1,2,80,"10.02.2023","Utilities","Internet"),
   (1,2,500,"14.02.2023","Housing","Property tax"),
   (3,1,200,"28.02.2023","Car","NULL"),
   (3,1,300,"04.03.2023","Clothing","Sneakers"),
   (4,2,50,"05.03.2023","Personal","Hairdresser"),
   (4,2,45,"29.03.2023","Personal","Cosmetics"),
   (5,3,150,"03.04.2023","Entertainment ","Concerts"),
   (5,3,25,"27.02.2023","Education","NULL"),
   (6,4,30,"15.01.2023","Entertainment ","Games"),
   (6,4,50,"16.03.2023","Personal","Gym memberships");
