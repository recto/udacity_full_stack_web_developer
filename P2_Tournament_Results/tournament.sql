-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop table tournaments cascade;
drop table players cascade;
drop table participants cascade;
drop table matches cascade;

-- tournaments table stores tournament ID and its name.
-- id : serial ID for the tournament, name : name of tournament.
create table tournaments (
    id serial primary key,
    name text unique
);

-- players table stores player ID and their full name.
-- These players are registered at the system level, not tournament level.
-- id : player ID. it's text, not integer unlike the original implementation.
create table players (
    id text primary key,
    name text
);

-- participants table stores players, who participate the tournament.
-- t_id : tournament ID, p_id : player ID.
create table participants (
    t_id integer references tournaments (id),
    p_id text references players (id),
    primary key (t_id, p_id)
);

-- matches table stores game results. Each match will have a integer ID.
-- id : match ID, t_id : tournament ID, p_id : player ID,
-- points : point the player earned.
create table matches (
    id integer,
    t_id integer references tournaments (id),
    p_id text references players (id),
    points integer,
    primary key (id, t_id, p_id)
);

