use adsinfo_crawler;

drop table if exists `appannie_app_ranking`;

CREATE TABLE `appannie_app_ranking` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `query_category` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `category` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ranking` int(11) DEFAULT NULL,
  `ranking_change` int(11) DEFAULT NULL,
  `appannie_app_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `app_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `appannie_crawl_date` char(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `has_iap` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `query_date` char(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `feed_type` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `icon_id` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(8) COLLATE utf8_unicode_ci DEFAULT 'US',
  `os` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_key` (`query_date`,`country`,`os`,`query_category`,`feed_type`,`ranking`) USING BTREE,
  KEY `idx_app_id` (`appannie_app_id`),
  KEY `idx_q_date` (`query_date`),
  KEY `idx_country` (`country`),
  KEY `idx_feed` (`feed_type`),
  KEY `idx_os` (`os`),
  KEY `idx_cate` (`query_category`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
