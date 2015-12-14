-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP TABLE IF EXISTS players, matches, resultsdisplay CASCADE;
CREATE TABLE players ( id SERIAL,
                       name TEXT );


CREATE TABLE matches ( matchid SERIAL,
                       player INTEGER,
                       name TEXT,
                       winner INTEGER,
                       loser INTEGER,
                       score INTEGER,
                       matches INTEGER);
