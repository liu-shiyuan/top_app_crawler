use adsinfo_crawler;
DROP TABLE IF EXISTS `appannie_app_icon`;
CREATE TABLE `appannie_app_icon` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `icon_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `icon_url_idx` (`icon_url`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
