--Estrutura de tabelas para o Gov Tiles


--
-- Table structure for table `my_db_name`.`lib_govtiles_accesspage`
--

DROP TABLE IF EXISTS `my_db_name`.`lib_govtiles_accesspage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lib_govtiles_accesspage` (
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `my_db_name`.`lib_govtiles_searchterms`
--

DROP TABLE IF EXISTS `my_db_name`.`lib_govtiles_searchterms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lib_govtiles_searchterms` (
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `my_db_name`.`lib_govtiles_ratecontent`
--

DROP TABLE IF EXISTS `my_db_name`.`lib_govtiles_ratecontent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lib_govtiles_ratecontent` (
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
/*!40101 SET character_set_client = @saved_cs_client */;