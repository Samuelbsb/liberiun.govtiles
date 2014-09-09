--
-- Table structure for table `liberiun_govtiles_DB`.`lib_govtiles_accesspage`
--

DROP TABLE IF EXISTS `liberiun_govtiles_DB`.`lib_govtiles_accesspage`;
CREATE TABLE `liberiun_govtiles_DB`.`lib_govtiles_accesspage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deleted` tinyint(1) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `date_excluded` datetime DEFAULT NULL,
  `content_type` varchar(100) DEFAULT NULL,
  `uid` varchar(200) DEFAULT NULL,
  `amount_of_access` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;

--
-- Table structure for table `liberiun_govtiles_DB`.`lib_govtiles_searchterms`
--

DROP TABLE IF EXISTS `liberiun_govtiles_DB`.`lib_govtiles_searchterms`;
CREATE TABLE `liberiun_govtiles_DB`.`lib_govtiles_searchterms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deleted` tinyint(1) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `date_excluded` datetime DEFAULT NULL,
  `value` varchar(500) DEFAULT NULL,
  `uid_object` varchar(100) DEFAULT NULL,
  `type_object` varchar(100) DEFAULT NULL,
  `amount_of_search` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

--
-- Table structure for table `liberiun_govtiles_DB`.`lib_govtiles_ratecontent`
--

DROP TABLE IF EXISTS `liberiun_govtiles_DB`.`lib_govtiles_ratecontent`;
CREATE TABLE `liberiun_govtiles_DB`.`lib_govtiles_ratecontent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deleted` tinyint(1) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `date_excluded` datetime DEFAULT NULL,
  `uid` varchar(100) DEFAULT NULL,
  `username` varchar(200) DEFAULT NULL,
  `rate` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `liberiun_govtiles_DB`.`lib_govtiles_commentcontent`
--

DROP TABLE IF EXISTS `liberiun_govtiles_DB`.`lib_govtiles_commentcontent`;
CREATE TABLE IF NOT EXISTS `liberiun_govtiles_DB`.`lib_govtiles_commentcontent` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `deleted` TINYINT(1) NULL,
  `date_created` DATETIME NULL,
  `date_modified` DATETIME NULL,
  `date_excluded` DATETIME NULL,
  `uid` VARCHAR(100) NULL,
  `username` VARCHAR(100) NULL,
  `name` VARCHAR(100) NULL,
  `email` VARCHAR(100) NULL,
  `text` TEXT NULL,
  `status` INT NULL,
  `date_status` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB