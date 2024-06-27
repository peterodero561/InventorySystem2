# INVENTORY SYSTEM 2.0H

## 1. Home Page

#### where all the records of the data stored will be displayed
![Home pic](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/home.png)

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

### b) Added Edit and Delete Functionality to the records  being stored
One can now edit the records stored in the database via prompt windows
![home page2](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/home2.png)


## 2. Login page
#### Allows users to login to view the contents of the Inventory
![Login page](https://github.com/peterodero561/InventorySystem2/blob/main/static/images/login.png)

### a) Database to handle the storage of user's credentials
sql code
```sql
-- create table
CREATE TABLE IF NOT EXISTS accounts (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(20) NOT NULL UNIQUE,
	password VARCHAR(20) NOT NULL,
	email VARCHAR(20) NOT NULL,
);
-- test cases
INSERT INTO accounts (username, password, email) VALUES
('testuser', 'testpassword', 'testuser@example.com'),
```
