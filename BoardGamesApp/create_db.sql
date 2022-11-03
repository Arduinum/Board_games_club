PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS gamer;
CREATE TABLE gamer (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));

DROP TABLE IF EXISTS dungeon_master;
CREATE TABLE dungeon_master (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));

DROP TABLE IF EXISTS category;
CREATE TABLE category (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));

DROP TABLE IF EXISTS game;
CREATE TABLE game (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, type_game VARCHAR (32), name VARCHAR (32), category VARCHAR (32));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;