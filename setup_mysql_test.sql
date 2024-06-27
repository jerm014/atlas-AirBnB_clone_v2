-- make a new database make sure you USE THE UPPERCASE SQL it's dumb.
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- make a new user with all privileges on the database.
CREATE USER IF NOT EXISTS 'localhost'@'hbnb_test' IDENTIFIED BY 'hbnb_test_pwd';
-- grant all privileges to the new user on the database.
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'localhost'@'hbnb_test';
-- hbnb_test should have SELECT privilege on the database performance_schema
GRANT SELECT ON performance_schema.* TO 'localhost'@'hbnb_test';
