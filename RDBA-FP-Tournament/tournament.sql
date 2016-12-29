-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS match_records CASCADE;
DROP TABLE IF EXISTS players CASCADE;

-- CREATE DATABASE tournament;

CREATE TABLE players (id SERIAL primary key, name TEXT);

CREATE TABLE match_records (winner INTEGER references players(id), loser INTEGER references players(id));

