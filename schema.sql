-- To create the database:
--   CREATE DATABASE blog;
--   GRANT ALL PRIVILEGES ON blog.* TO 'blog'@'localhost' IDENTIFIED BY 'blog';
--
-- To reload the tables:
--   mysql --user=blog --password=blog --database=blog < schema.sql

SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";

DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    author_id INT NOT NULL REFERENCES authors(id),
    slug VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(512) NOT NULL,
    tags VARCHAR(100) NOT NULL,
    markdown MEDIUMTEXT NOT NULL,
    html MEDIUMTEXT NOT NULL,
    abstract TEXT NOT NULL,
    published DATETIME NOT NULL,
    updated TIMESTAMP NOT NULL,
	readtimes INT NOT NULL,
	comments INT NOT NULL,
    KEY (published)
);

DROP TABLE IF EXISTS authors;
CREATE TABLE authors (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE
);

DROP TABLE IF EXISTS statics;
CREATE TABLE statics (
	id INT NOT NULL PRIMARY KEY,
	cnt INT NOT NULL 
);

DROP TABLE IF EXISTS tags;
CREATE TABLE tags (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(20) NOT NULL UNIQUE,
	cnt INT NOT NULL
);

DROP TABLE IF EXISTS tagmaps;
CREATE TABLE tagmaps (
	tag_id INT NOT NULL,
	entry_id INT NOT NULL,
	PRIMARY KEY (tag_id, entry_id)
);

DROP TABLE IF EXISTS dates;
CREATE TABLE dates (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name CHAR(7) NOT NULL UNIQUE,
	cnt INT NOT NULL
);

DROP TABLE IF EXISTS datemaps;
CREATE TABLE datemaps (
	date_id INT NOT NULL,
	entry_id INT NOT NULL,
	PRIMARY KEY (date_id, entry_id)
);

DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	entry_id INT NOT NULL,
    reply_id INT NOT NULL,
	published DATETIME NOT NULL,
	author VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	url VARCHAR(100) NOT NULL,
	content TEXT NOT NULL,
	key (entry_id)
);
