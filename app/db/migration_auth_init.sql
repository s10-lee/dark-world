-- upgrade --
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
-- downgrade --
DROP TABLE IF EXISTS "key_pair";
DROP TABLE IF EXISTS "signup";