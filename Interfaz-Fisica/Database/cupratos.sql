-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: cupratos
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
-- Table structure for table `abovetco`
--

DROP TABLE IF EXISTS `abovetco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `abovetco` (
  `id_aboveTco` int NOT NULL AUTO_INCREMENT,
  `muestra` varchar(15) NOT NULL,
  `tc` double(6,4) NOT NULL,
  `tirr` double(6,4) NOT NULL,
  `tco` double(6,4) NOT NULL,
  `dimensionalidad` double(6,4) NOT NULL,
  `asl` double NOT NULL,
  `bld` double NOT NULL,
  `longitudab` double NOT NULL,
  `longitudc` double NOT NULL,
  `gamma` double NOT NULL,
  `fecha` date DEFAULT NULL,
  PRIMARY KEY (`id_aboveTco`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `abovetco`
--

LOCK TABLES `abovetco` WRITE;
/*!40000 ALTER TABLE `abovetco` DISABLE KEYS */;
INSERT INTO `abovetco` VALUES (1,'Sample',72.0700,70.1000,84.6600,0.0000,593000000000,7.35e22,20.5,7440000,0.00000276,'2020-08-30');
/*!40000 ALTER TABLE `abovetco` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `belowtco`
--

DROP TABLE IF EXISTS `belowtco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `belowtco` (
  `id_belowtco` int NOT NULL AUTO_INCREMENT,
  `muestra` varchar(15) NOT NULL,
  `t` double(5,2) NOT NULL,
  `emu` double(5,2) NOT NULL,
  `m` double(5,2) NOT NULL,
  `fecha` date DEFAULT NULL,
  PRIMARY KEY (`id_belowtco`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `belowtco`
--

LOCK TABLES `belowtco` WRITE;
/*!40000 ALTER TABLE `belowtco` DISABLE KEYS */;
INSERT INTO `belowtco` VALUES (1,'sm358',34.60,23.60,34.50,'0000-00-00'),(2,'sm358',34.60,23.60,34.50,'2020-09-13'),(3,'sm358',34.60,23.60,34.50,'2020-09-13'),(4,'sm358',34.60,23.60,34.50,'2020-09-13'),(6,'sm358',34.60,23.60,34.50,'2020-09-13'),(7,'sm358',34.60,23.60,34.50,'2020-09-13'),(8,'sm358',34.60,23.60,34.50,'2020-09-13'),(9,'sm358',34.60,23.60,34.50,'2020-09-13'),(10,'sm358',34.60,23.60,34.50,'2020-09-13'),(11,'sm358',34.60,23.60,34.50,'2020-09-13'),(12,'sm358',34.60,23.60,34.50,'2020-09-13'),(13,'sm358',34.60,23.60,34.50,'2020-09-13');
/*!40000 ALTER TABLE `belowtco` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'cupratos'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-31 18:00:37
