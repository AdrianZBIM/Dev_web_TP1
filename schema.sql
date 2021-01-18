PRAGMA foreign_keys = ON;
--
-- Gender
--
CREATE TABLE IF NOT EXISTS gender (
	id INTEGER PRIMARY KEY,
	name VARCHAR(1)
);
INSERT INTO gender VALUES (null, 'f');
INSERT INTO gender VALUES (null, 'm');

--
-- Fields
--
CREATE TABLE IF NOT EXISTS fieldname (
id INTEGER PRIMARY KEY,
name TEXT
);
INSERT INTO fieldname VALUES (NULL, 'mathematics'); --1
INSERT INTO fieldname VALUES (NULL, 'logic'); -- 2
INSERT INTO fieldname VALUES (NULL, 'physics'); -- 3
INSERT INTO fieldname VALUES (NULL, 'biology'); -- 4
INSERT INTO fieldname VALUES (NULL, 'computer'); -- 5
CREATE TABLE IF NOT EXISTS field (
     id INTEGER PRIMARY KEY,
     user_id INTEGER,
     field_id INTEGER,
     FOREIGN KEY(field_id) REFERENCES fieldname(id),
     FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS users (
     id INTEGER PRIMARY KEY,
     name TEXT UNIQUE,
     wikiid INTEGER,
     birth DATE,
     gender_id INTEGER,
     FOREIGN KEY(gender_id) REFERENCES gender(id)
);
INSERT INTO users VALUES (NULL, 'Alan Turing', 1208, '1912-06-23', 2);
INSERT INTO field VALUES (NULL, 1, 1); -- math
INSERT INTO field VALUES (NULL, 1, 2); -- logic
INSERT INTO field VALUES (NULL, 1, 5); -- computer

INSERT INTO users VALUES (NULL, 'Katherine Johnson', 25568315, '1918-8-26', 1);
INSERT INTO field VALUES (NULL, 2, 4); -- computer
INSERT INTO field VALUES (NULL, 2, 2); -- logic

INSERT INTO users VALUES (NULL, 'John Neumann', 15942, '1903-12-28', 2);
INSERT INTO field VALUES (NULL, 3, 5); -- computer
INSERT INTO field VALUES (NULL, 3, 2); -- logic

INSERT INTO users VALUES (NULL, 'Kurt Gödel', 16636, '1906-4-28', 2);
INSERT INTO field VALUES (NULL, 4, 1); -- math
INSERT INTO field VALUES (NULL, 4, 2); -- logic

INSERT INTO users VALUES (NULL, 'Richard Dawkins', 25867, '1941-3-26', 2);
INSERT INTO field VALUES (NULL, 5, 4); -- biology
