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
                       winner INTEGER,
                       loser INTEGER);

CREATE TABLE resultsdisplay (player INTEGER,
                          name TEXT,
                          score INTEGER,
                          matches INTEGER);
