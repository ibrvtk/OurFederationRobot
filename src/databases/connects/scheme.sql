CREATE TABLE IF NOT EXISTS `connects` (
    `user_id` BIGINT NOT NULL PRIMARY KEY,
    `minecraft_nickname` VARCHAR(255),
    `keyword` VARCHAR(255)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;