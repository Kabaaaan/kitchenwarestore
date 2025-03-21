-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: kitchenware
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `brand`
--

DROP TABLE IF EXISTS `brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `brand` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brand`
--

LOCK TABLES `brand` WRITE;
/*!40000 ALTER TABLE `brand` DISABLE KEYS */;
INSERT INTO `brand` VALUES (1,'IKEA'),(2,'Tefal'),(3,'Luminarc');
/*!40000 ALTER TABLE `brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'╨з╨░╤И╨║╨╕'),(2,'╨С╨╛╨║╨░╨╗╤Л'),(3,'╨б╤В╨╛╨╗╨╛╨▓╤Л╨╡ ╨┐╤А╨╕╨▒╨╛╤А╤Л'),(4,'╨в╨░╤А╨╡╨╗╨║╨╕'),(5,'╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В╤Л');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`user_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (11,15,250.00,'default'),(12,23,100.00,'pending'),(13,23,200.00,'completed'),(14,23,150.00,'pending'),(15,15,520.00,'default'),(16,15,670.00,'default'),(17,15,570.00,'default'),(18,15,330.00,'default'),(19,15,460.00,'default'),(20,32,850.00,'default'),(21,15,3030.00,'default');
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderitem`
--

DROP TABLE IF EXISTS `orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderitem` (
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`order_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `orderitem_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `orderitem_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderitem`
--

LOCK TABLES `orderitem` WRITE;
/*!40000 ALTER TABLE `orderitem` DISABLE KEYS */;
INSERT INTO `orderitem` VALUES (11,8,2),(11,9,1),(11,10,3),(12,1,2),(12,3,1),(12,5,3),(13,2,1),(13,4,2),(13,6,1),(14,7,4),(14,8,2),(14,10,1);
/*!40000 ALTER TABLE `orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `price` decimal(10,2) NOT NULL,
  `category_id` int DEFAULT NULL,
  `brand_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `brand_id` (`brand_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `product_ibfk_2` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'╨з╨░╤И╨║╨░ ╨║╨╡╤А╨░╨╝╨╕╤З╨╡╤Б╨║╨░╤П','╨Ъ╨╡╤А╨░╨╝╨╕╤З╨╡╤Б╨║╨░╤П ╤З╨░╤И╨║╨░ ╤З╨╡╤А╨╜╨░╤П',160.00,1,1),(2,'╨з╨░╤И╨║╨░ ╤Б╤В╨╡╨║╨╗╤П╨╜╨╜╨░╤П','╨б╤В╨╡╨║╨╗╤П╨╜╨╜╨░╤П ╤З╨░╤И╨║╨░ ╨┤╨╗╤П ╤З╨░╤П',200.00,1,2),(3,'╨з╨░╤И╨║╨░ ╤Б ╤А╨╕╤Б╤Г╨╜╨║╨╛╨╝','╨з╨░╤И╨║╨░ ╤Б ╨║╤А╨░╤Б╨╕╨▓╤Л╨╝ ╤А╨╕╤Б╤Г╨╜╨║╨╛╨╝',180.00,1,3),(4,'╨з╨░╤И╨║╨░ ╤Б ╨║╤А╤Л╤И╨║╨╛╨╣','╨з╨░╤И╨║╨░ ╤Б ╨║╤А╤Л╤И╨║╨╛╨╣ ╨┤╨╗╤П ╤Б╨╛╤Е╤А╨░╨╜╨╡╨╜╨╕╤П ╤В╨╡╨┐╨╗╨░',220.00,1,1),(5,'╨з╨░╤И╨║╨░ ╤Б ╨▒╨╗╤О╨┤╤Ж╨╡╨╝','╨з╨░╤И╨║╨░ ╤Б ╨▒╨╗╤О╨┤╤Ж╨╡╨╝ ╨╕╨╖ ╤Д╨░╤А╤Д╨╛╤А╨░',250.00,1,2),(6,'╨з╨░╤И╨║╨░ ╨┤╨╗╤П ╨║╨╛╤Д╨╡','╨з╨░╤И╨║╨░ ╨┤╨╗╤П ╤Н╤Б╨┐╤А╨╡╤Б╤Б╨╛',130.00,1,3),(7,'╨з╨░╤И╨║╨░ ╤Б ╨┤╨▓╨╛╨╣╨╜╤Л╨╝╨╕ ╤Б╤В╨╡╨╜╨║╨░╨╝╨╕','╨з╨░╤И╨║╨░ ╤Б ╨┤╨▓╨╛╨╣╨╜╤Л╨╝╨╕ ╤Б╤В╨╡╨╜╨║╨░╨╝╨╕ ╨┤╨╗╤П ╨│╨╛╤А╤П╤З╨╕╤Е ╨╜╨░╨┐╨╕╤В╨║╨╛╨▓',300.00,1,1),(8,'╨С╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨▓╨╕╨╜╨░','╨б╤В╨╡╨║╨╗╤П╨╜╨╜╤Л╨╣ ╨▒╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨║╤А╨░╤Б╨╜╨╛╨│╨╛ ╨▓╨╕╨╜╨░',350.00,2,1),(9,'╨С╨╛╨║╨░╨╗ ╨┤╨╗╤П ╤И╨░╨╝╨┐╨░╨╜╤Б╨║╨╛╨│╨╛','╨н╨╗╨╡╨│╨░╨╜╤В╨╜╤Л╨╣ ╨▒╨╛╨║╨░╨╗ ╨┤╨╗╤П ╤И╨░╨╝╨┐╨░╨╜╤Б╨║╨╛╨│╨╛',400.00,2,2),(10,'╨С╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨┐╨╕╨▓╨░','╨С╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨┐╨╕╨▓╨░ ╤Б ╤А╤Г╤З╨║╨╛╨╣',250.00,2,3),(11,'╨С╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨║╨╛╨║╤В╨╡╨╣╨╗╤П','╨С╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨║╨╛╨║╤В╨╡╨╣╨╗╨╡╨╣ ╤Б ╤Г╨╖╨║╨╕╨╝ ╨│╨╛╤А╨╗╤Л╤И╨║╨╛╨╝',300.00,2,1),(12,'╨С╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨▓╨╕╤Б╨║╨╕','╨С╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨▓╨╕╤Б╨║╨╕ ╤Б ╤В╨╛╨╗╤Б╤В╤Л╨╝ ╨┤╨╜╨╛╨╝',450.00,2,2),(13,'╨С╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨▓╨╛╨┤╤Л','╨Я╤А╨╛╤Б╤В╨╛╨╣ ╨▒╨╛╨║╨░╨╗ ╨┤╨╗╤П ╨▓╨╛╨┤╤Л',150.00,2,3),(14,'╨С╨╛╨║╨░╨╗ ╤Б ╤Г╨╖╨╛╤А╨╛╨╝','╨С╨╛╨║╨░╨╗ ╤Б ╨║╤А╨░╤Б╨╕╨▓╤Л╨╝ ╤Г╨╖╨╛╤А╨╛╨╝',380.00,2,1),(15,'╨Э╨░╨▒╨╛╤А ╤Б╤В╨╛╨╗╨╛╨▓╤Л╤Е ╨╗╨╛╨╢╨╡╨║','╨Э╨░╨▒╨╛╤А ╨╕╨╖ 6 ╤Б╤В╨╛╨╗╨╛╨▓╤Л╤Е ╨╗╨╛╨╢╨╡╨║',500.00,3,1),(16,'╨Э╨░╨▒╨╛╤А ╨▓╨╕╨╗╨╛╨║','╨Э╨░╨▒╨╛╤А ╨╕╨╖ 6 ╨▓╨╕╨╗╨╛╨║',550.00,3,2),(17,'╨Э╨░╨▒╨╛╤А ╨╜╨╛╨╢╨╡╨╣','╨Э╨░╨▒╨╛╤А ╨╕╨╖ 6 ╨╜╨╛╨╢╨╡╨╣',600.00,3,3),(18,'╨Ы╨╛╨╢╨║╨░ ╨┤╨╗╤П ╤Б╤Г╨┐╨░','╨С╨╛╨╗╤М╤И╨░╤П ╨╗╨╛╨╢╨║╨░ ╨┤╨╗╤П ╤Б╤Г╨┐╨░',100.00,3,1),(19,'╨Т╨╕╨╗╨║╨░ ╨┤╨╗╤П ╨┤╨╡╤Б╨╡╤А╤В╨░','╨Т╨╕╨╗╨║╨░ ╨┤╨╗╤П ╨┤╨╡╤Б╨╡╤А╤В╨░',120.00,3,2),(23,'╨в╨░╤А╨╡╨╗╨║╨░ ╨╝╨╡╨╗╨║╨░╤П','╨Ь╨╡╨╗╨║╨░╤П ╤В╨░╤А╨╡╨╗╨║╨░ ╨┤╨╗╤П ╨╖╨░╨║╤Г╤Б╨╛╨║',250.00,4,2),(24,'╨в╨░╤А╨╡╨╗╨║╨░ ╨┤╨╗╤П ╨┐╨░╤Б╤В╤Л','╨в╨░╤А╨╡╨╗╨║╨░ ╨┤╨╗╤П ╨┐╨░╤Б╤В╤Л ╤Б ╤Г╨╖╨╛╤А╨╛╨╝',350.00,4,3),(25,'╨в╨░╤А╨╡╨╗╨║╨░ ╨┤╨╗╤П ╨┤╨╡╤Б╨╡╤А╤В╨░','╨в╨░╤А╨╡╨╗╨║╨░ ╨┤╨╗╤П ╨┤╨╡╤Б╨╡╤А╤В╨░',200.00,1,1),(26,'╨в╨░╤А╨╡╨╗╨║╨░ ╤Б ╨▒╨╛╤А╤В╨╕╨║╨░╨╝╨╕','╨в╨░╤А╨╡╨╗╨║╨░ ╤Б ╨▓╤Л╤Б╨╛╨║╨╕╨╝╨╕ ╨▒╨╛╤А╤В╨╕╨║╨░╨╝╨╕',400.00,4,2),(27,'╨в╨░╤А╨╡╨╗╨║╨░ ╨┤╨╗╤П ╤Б╨░╨╗╨░╤В╨░','╨в╨░╤А╨╡╨╗╨║╨░ ╨┤╨╗╤П ╤Б╨░╨╗╨░╤В╨░',300.00,4,3),(28,'╨Э╨░╨▒╨╛╤А ╤В╨░╤А╨╡╨╗╨╛╨║','╨Э╨░╨▒╨╛╤А ╨╕╨╖ 6 ╤В╨░╤А╨╡╨╗╨╛╨║',1200.00,4,1),(29,'╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╨┐╨╛╤Б╤Г╨┤╤Л','╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╨╕╨╖ 12 ╨┐╤А╨╡╨┤╨╝╨╡╤В╨╛╨▓',2500.00,5,1),(30,'╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╤Б╤В╨╛╨╗╨╛╨▓╤Л╤Е ╨┐╤А╨╕╨▒╨╛╤А╨╛╨▓','╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╨╕╨╖ 24 ╨┐╤А╨╡╨┤╨╝╨╡╤В╨╛╨▓',1500.00,5,2),(31,'╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╤З╨░╤И╨╡╨║','╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╨╕╨╖ 6 ╤З╨░╤И╨╡╨║ ╤Б ╨▒╨╗╤О╨┤╤Ж╨░╨╝╨╕',900.00,5,3),(32,'╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╨▒╨╛╨║╨░╨╗╨╛╨▓','╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╨╕╨╖ 4 ╨▒╨╛╨║╨░╨╗╨╛╨▓ ╨┤╨╗╤П ╨▓╨╕╨╜╨░',1200.00,5,1),(33,'╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╤В╨░╤А╨╡╨╗╨╛╨║','╨Ъ╨╛╨╝╨┐╨╗╨╡╨║╤В ╨╕╨╖ 6 ╤В╨░╤А╨╡╨╗╨╛╨║',1100.00,5,2);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productimages`
--

DROP TABLE IF EXISTS `productimages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productimages` (
  `product_id` int NOT NULL,
  `image_alt` varchar(255) NOT NULL,
  PRIMARY KEY (`product_id`),
  CONSTRAINT `productimages_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productimages`
--

LOCK TABLES `productimages` WRITE;
/*!40000 ALTER TABLE `productimages` DISABLE KEYS */;
INSERT INTO `productimages` VALUES (1,'None'),(2,'None'),(3,'None'),(5,'None'),(6,'None'),(7,'None');
/*!40000 ALTER TABLE `productimages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (15,'roma','kuksik','admin'),(23,'test','test','regular'),(32,'test_2','test_2','regular'),(37,'test_bro','bro','regular');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-07  0:05:47
