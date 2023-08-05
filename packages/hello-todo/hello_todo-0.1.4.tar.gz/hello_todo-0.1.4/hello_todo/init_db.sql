DROP TABLE IF EXISTS todolist ;
DROP TABLE IF EXISTS todo ;

CREATE TABLE todolist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(150)
);

CREATE TABLE todo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(150),
    deadline VARCHAR(23),
    status INTEGER,
    todolist_id INTEGER NOT NULL,
    FOREIGN KEY (todolist_id) REFERENCES todolist (id)
);
