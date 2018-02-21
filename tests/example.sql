CREATE TABLE employees (

    id            INTEGER      PRIMARY KEY,
    first_name    VARCHAR(50)  NULL,
    last_name     VARCHAR(75)  NOT NULL,
    dateofbirth   DATE         NULL
);

-- SQL comment

DROP TABLE employees;

-- More comments

CREATE TABLE former employees (

    id            INTEGER      PRIMARY KEY,
    first_name    VARCHAR(50)  NULL,
    last_name     VARCHAR(75)  NOT NULL,
    dateofbirth   DATE         NULL
);

-- SQL comment

DROP TABLE former employees;

-- More comments

CREATE TABLE YET to BE employees (

    id            INTEGER      PRIMARY KEY,
    first_name    VARCHAR(50)  NULL,
    last_name     VARCHAR(75)  NOT NULL,
    dateofbirth   DATE         NULL
);

-- SQL comment

DROP TABLE YET to BE employEeS;

-- More comments

DROP TABLE "all employees";

-- More comments

CREATE TABLE "all employees" (

    id            INTEGER      PRIMARY KEY,
    first_name    VARCHAR(50)  NULL,
    last_name     VARCHAR(75)  NOT NULL,
    dateofbirth   DATE         NULL
);

-- SQL comment

INSERT INTO "all employees("id", "first_name", "last_name", "dateofbirth")
    VALUES(1, "tom", "brady", 1/1/1900),
    (2, "lisa", "grady", 2/2/1901);

DROP TABLE "all employees";

-- More comments

CREATE TABLE "all employees" (

    id            INTEGER      PRIMARY KEY,
    first_name    VARCHAR(50)  NULL,
    last_name     VARCHAR(75)  NOT NULL,
    dateofbirth   DATE         NULL
);

-- SQL comment