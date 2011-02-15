BEGIN;
DROP TABLE "chat_chat_users";
DROP TABLE "chat_line";
DROP TABLE "chat_chat";
DROP TABLE "chat_useractivity";
CREATE TABLE "chat_useractivity" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "chat_id" integer NOT NULL,
    "ping" datetime NOT NULL
)
;
CREATE TABLE "chat_chat" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(30),
    "created" datetime NOT NULL,
    "content_type_id" integer REFERENCES "django_content_type" ("id"),
    "object_id" integer unsigned
)
;
CREATE TABLE "chat_line" (
    "id" integer NOT NULL PRIMARY KEY,
    "text" varchar(1000) NOT NULL,
    "is_emote" bool NOT NULL,
    "is_action" bool NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "chat_id" integer REFERENCES "chat_chat" ("id"),
    "timestamp" datetime NOT NULL
)
;
CREATE TABLE "chat_chat_users" (
    "id" integer NOT NULL PRIMARY KEY,
    "chat_id" integer NOT NULL REFERENCES "chat_chat" ("id"),
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    UNIQUE ("chat_id", "user_id")
)
;
CREATE INDEX "chat_useractivity_user_id" ON "chat_useractivity" ("user_id");
CREATE INDEX "chat_useractivity_chat_id" ON "chat_useractivity" ("chat_id");
CREATE INDEX "chat_chat_content_type_id" ON "chat_chat" ("content_type_id");
CREATE INDEX "chat_line_user_id" ON "chat_line" ("user_id");
CREATE INDEX "chat_line_chat_id" ON "chat_line" ("chat_id");
COMMIT;
