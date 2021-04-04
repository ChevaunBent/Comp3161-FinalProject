CREATE TABLE IF NOT EXISTS users(
    userid INTEGER NOT Null,
    firstname varchar(20),
    lastname varchar(20),
    age int,
    email varchar(50),
    telephone varchar(20),
    preference varchar(20),
    username varchar (20),
    password varchar(100),
    PRIMARY KEY(userid)
);
CREATE TABLE IF NOT EXISTS recipes(
    recipeid INTEGER NOT NULL,
    title VARCHAR(20),
    instructions VARCHAR(250),
    filename VARCHAR(100),
    PRIMARY KEY(recipeid)
);
CREATE TABLE IF NOT EXISTS adds(
    userid INTEGER NOT NULL,
    recipeid INTEGER NOT NULL,
    datecreated Date NOT NULL,
    PRIMARY KEY(userid,recipeid),
    FOREIGN KEY (userid) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(recipeid) REFERENCES recipes(recipeid) ON UPDATE CASCADE ON DELETE CASCADE
);