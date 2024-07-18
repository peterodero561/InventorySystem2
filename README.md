# INVENTORY SYSTEM 2.0H

## 1. Home Page

#### where all the records of the data stored will be displayed
![Home pic](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/home5.png)

### a) Database to handle the storage of the records
The sql code
```sql
CREATE DATABASE IF NOT EXISTS inventory;
USE inventory;

CREATE TABLE general(
	item_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	item_name VARCHAR(100),
	item_quantity VARCHAR(100),
	item_category VARCHAR(100),
	brand VARCHAR(100),
	notes VARCHAR(100)
	);
```

### b) Edit and Delete Functionality to the records  being stored
One can now edit the records stored in the database via prompt windows
![home page3](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/home3.png)


## 2. Login pages

### a) Admin Login Page
#### Allows Admin to login to view the contents of the Inventory
![Login page](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/login.png)

#### Admin homepage
![Login page](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/home3.png)

### b) User Login page
#### Allows users to login to view the records
![Sign In page](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/signin.png)

#### Users home page
![user home page](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/home6.png)

#### Allows users to Sign up
![Sign UP page](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/signup.png)

### c) Database to handle the storage of users credentials
sql code
```sql
-- create table
CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
);
-- test cases
INSERT INTO accounts (username, password, email) VALUES
('testuser', 'testpassword', 'testuser@example.com'),
```
