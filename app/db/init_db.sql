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


-- INSERT INTO "grabber" (name, icon, type, patterns, search_xpath, element_index) VALUES ('Youtube', '/static/icons/web/youtube-144.png', 'youtube', '["youtu\\.be", "youtube\\.com"]', '', null);
-- INSERT INTO "grabber" (name, icon, type, patterns, search_xpath, element_index) VALUES ('Dribbble', '/static/icons/web/dribbble-192.png', 'html', '["dribbble\\.com"]', '//img[@data-animated-url]/@data-animated-url', null);
-- INSERT INTO "grabber" (name, icon, type, patterns, search_xpath, element_index) VALUES ('Pinterest', '/static/icons/web/pinterest.png', 'html', '["pinterest\\.", "wwww\\.pinterest", "pin\\.it"]', '//head/link[@as="image"]/@href', null);


-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (1, 'A-IM', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (2, 'Accept', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (3, 'Accept-Charset', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (4, 'Accept-Encoding', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (5, 'Accept-Language', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (6, 'Accept-Datetime', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (7, 'Access-Control-Request-Method', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (8, 'Access-Control-Request-Headers', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (9, 'Authorization', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (10, 'Cache-Control', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (11, 'Connection', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (12, 'Content-Length', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (13, 'Content-Type', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (14, 'Cookie', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (15, 'Date', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (16, 'Expect', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (17, 'Forwarded', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (18, 'From', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (19, 'Host', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (20, 'If-Match', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (21, 'If-Modified-Since', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (22, 'If-None-Match', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (23, 'If-Range', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (24, 'If-Unmodified-Since', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (25, 'Max-Forwards', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (26, 'Origin', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (27, 'Pragma', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (28, 'Proxy-Authorization', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (29, 'Range', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (30, 'Referer', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (31, 'TE', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (32, 'User-Agent', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (33, 'Upgrade', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (34, 'Via', true, false);
-- INSERT INTO public.http_header (id, name, in_request, in_response) VALUES (35, 'Warning', true, false);