DROP DATABASE IF EXISTS sensors;
CREATE DATABASE sensors;
\c sensors
DROP TABLE IF EXISTS ADDRESS;
CREATE TABLE ADDRESS(ID SERIAL PRIMARY KEY, URL CHAR(100) UNIQUE NOT NULL);
