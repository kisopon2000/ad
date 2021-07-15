CREATE DATABASE  IF NOT EXISTS `ad` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ad`;
-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ad
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ad_target_campany_sectors`
--

DROP TABLE IF EXISTS `ad_target_campany_sectors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ad_target_campany_sectors` (
  `ad_id` bigint NOT NULL COMMENT '広告ID',
  `campany_sector_id` varchar(100) NOT NULL COMMENT '業種ID',
  `campany_sector_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '業種名',
  `is_checked` bit(1) NOT NULL COMMENT '選択状態',
  PRIMARY KEY (`ad_id`),
  KEY `FK_ad_target_campany_sectors_campany_sector_id_idx` (`campany_sector_id`),
  CONSTRAINT `FK_ad_target_campany_sectors_ad_id` FOREIGN KEY (`ad_id`) REFERENCES `ads` (`ad_id`),
  CONSTRAINT `FK_ad_target_campany_sectors_campany_sector_id` FOREIGN KEY (`campany_sector_id`) REFERENCES `m_campany_sectors` (`campany_sector_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='広告ターゲット(業種)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ad_target_campany_sectors`
--

LOCK TABLES `ad_target_campany_sectors` WRITE;
/*!40000 ALTER TABLE `ad_target_campany_sectors` DISABLE KEYS */;
/*!40000 ALTER TABLE `ad_target_campany_sectors` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-02  0:02:44
