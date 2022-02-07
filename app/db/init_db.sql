CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS "key_pair" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "public_key" TEXT NOT NULL,
    "private_key" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "signup" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "expires_at" TIMESTAMPTZ,
    "activated_at" TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS "permission" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "slug" VARCHAR(60) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "email" VARCHAR(100) UNIQUE,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_staff" BOOL NOT NULL DEFAULT False,
    "last_login" TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS "user_refresh_token" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(64) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "expires_at" TIMESTAMPTZ,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_permission" (
    "permission_id" INT NOT NULL REFERENCES "permission" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);

-- "uid" UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,

CREATE TABLE IF NOT EXISTS "pin_board"
(
    "id"         SERIAL       NOT NULL PRIMARY KEY,
    "uid"        UUID         NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    "name"       VARCHAR(255) NOT NULL,
    "user_id"    UUID         NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "created_at" TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "pin_item"
(
    "id"         SERIAL       NOT NULL PRIMARY KEY,
    "uid"        UUID         NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    "name"       VARCHAR(255) NOT NULL,
    "extension"  VARCHAR(10)  NOT NULL,
    "type"       VARCHAR(5)   NOT NULL DEFAULT 'image',
    "board_id"   INT          REFERENCES "pin_board" ("id") ON DELETE SET NULL,
    "user_id"    UUID         NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "created_at" TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "pin_item"."type" IS 'IMAGE: image\nVIDEO: video\nAUDIO: audio';