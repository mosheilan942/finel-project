-- Active: 1687858621452@@127.0.0.1@3306@task_manager
CREATE DATABASE Task_manager;

USE Task_manager;

CREATE TABLE Users(
    User_id INT(8) PRIMARY KEY NOT NULL,
    First_name VARCHAR(50),
    Last_name  VARCHAR(50),
    email VARCHAR(50),
    job_title VARCHAR(50),
    password INT(50)
);


CREATE TABLE Categories(
    Category_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Category_name VARCHAR(50)
);


CREATE TABLE Tasks(
    Task_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Task_title VARCHAR(50),
    Description VARCHAR(100),
    Status BOOLEAN,
    Due_date DATE,
    priority_level VARCHAR(50),
    Category_id INT,
    FOREIGN KEY (Category_id) REFERENCES Categories(Category_id)
);


CREATE TABLE Collaborators(
    Task_id INT,
    FOREIGN KEY (Task_id) REFERENCES Tasks(Task_id),
    User_id INT(8),
    FOREIGN KEY (User_id) REFERENCES Users(User_id)
);


SELECT * from Tasks;
WHERE Status;
 

SELECT * from users;

SELECT * FROM categories;

SELECT * FROM Collaborators;

DELETE FROM users;
DELETE FROM Collaborators;

DELETE FROM tasks;

DROP TABLE Collaborators;
DROP TABLE categories;


DROP TABLE tasks;


SELECT * from collaborators 

