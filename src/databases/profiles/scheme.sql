BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "nicknames" (
    "user_id" INTEGER PRIMARY KEY,
    "user_username" TEXT DEFAULT "None",
    "minecraft_nickname" TEXT,
    "registration_date" INTEGER,
    "nickname_changes_count" INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "roleplays" (
    "user_id" INTEGER PRIMARY KEY,
    "is_prisoner" INTEGER DEFAULT 0,
    "is_rebel" INTEGER DEFAULT 0,
    "is_military" INTEGER DEFAULT 0,
    "party_membership" TEXT DEFAULT "None"
);
CREATE TABLE IF NOT EXISTS "donates" (
    "user_id" INTEGER PRIMARY KEY,
    "balance" INTEGER DEFAULT 0,
    "inventory" TEXT DEFAULT "None",
    "is_tradeban" INTEGER DEFAULT 0,
    "donate_count" INTEGER DEFAULT 0
);
COMMIT;