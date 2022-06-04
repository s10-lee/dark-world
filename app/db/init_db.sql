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

/***

  "uid" UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,

***/


INSERT INTO "grabber" (name, icon, type, patterns, search_xpath, element_index) VALUES ('Youtube', '/static/icons/web/youtube-144.png', 'youtube', '["youtu\\.be", "youtube\\.com"]', '', null);
INSERT INTO "grabber" (name, icon, type, patterns, search_xpath, element_index) VALUES ('Dribbble', '/static/icons/web/dribbble-192.png', 'html', '["dribbble\\.com"]', '//img[@data-animated-url]/@data-animated-url', null);
INSERT INTO "grabber" (name, icon, type, patterns, search_xpath, element_index) VALUES ('Pinterest', '/static/icons/web/pinterest.png', 'html', '["pinterest\\.", "wwww\\.pinterest", "pin\\.it"]', '//head/link[@as="image"]/@href', null);