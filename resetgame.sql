BEGIN;
DROP TABLE "game_game_players";
DROP TABLE "game_team_players";
DROP TABLE "game_game";
DROP TABLE "game_team";
CREATE TABLE "game_team" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(300) NOT NULL
)
;
CREATE TABLE "game_game" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "opened_date" datetime NOT NULL,
    "team1_id" integer UNIQUE REFERENCES "game_team" ("id"),
    "team2_id" integer UNIQUE REFERENCES "game_team" ("id"),
    "max_players" integer NOT NULL,
    "status" varchar(10) NOT NULL
)
;
CREATE TABLE "game_team_players" (
    "id" integer NOT NULL PRIMARY KEY,
    "team_id" integer NOT NULL REFERENCES "game_team" ("id"),
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    UNIQUE ("team_id", "user_id")
)
;
CREATE TABLE "game_game_players" (
    "id" integer NOT NULL PRIMARY KEY,
    "game_id" integer NOT NULL REFERENCES "game_game" ("id"),
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    UNIQUE ("game_id", "user_id")
)
;
COMMIT;
