use adsinfo_crawler;
DROP TABLE IF EXISTS `top_app`;

CREATE TABLE `top_app` (
  `appannie_app_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `app_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `app_store_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `os` int(11) DEFAULT NULL,
  `release_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_update_date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `appannie_company_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `appannie_publisher_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `owner_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `appannie_detail_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `unified_app_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`appannie_app_id`),
  UNIQUE KEY `idx_storeurl` (`app_store_url`),
  KEY `idx_detail_id` (`appannie_detail_id`),
  KEY `idx_unified_id` (`unified_app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
