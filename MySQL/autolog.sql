-- Notes: use "mysql -p -u root -t < autolog.sql"
--        to create the database and the table in 
--        the mysql database


DROP DATABASE IF EXISTS autolog;
CREATE DATABASE IF NOT EXISTS autolog;
USE autolog;

SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';

DROP TABLE IF EXISTS sf_grids;

CREATE TABLE sf_grids (
    grid_id         INT               NOT NULL,
    average_speed   DECIMAL(5,2)      NOT NULL,
    unique_cars     INT               NOT NULL,
    PRIMARY KEY (grid_id)
);
