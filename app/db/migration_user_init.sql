-- upgrade --
CREATE TABLE IF NOT EXISTS "permission" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "slug" VARCHAR(60) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "email" VARCHAR(100)  UNIQUE,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_staff" BOOL NOT NULL  DEFAULT False,
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
-- downgrade --
DROP TABLE IF EXISTS "user_permission";
DROP TABLE IF EXISTS "user_refresh_token";
DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS "permission";
