DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `customers` WRITE;
UNLOCK TABLES;


DROP TABLE IF EXISTS `drivers`;
CREATE TABLE `drivers` (
  `driver_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `license_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`driver_id`),
  UNIQUE KEY `license_number` (`license_number`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `drivers` WRITE;
INSERT INTO `drivers` VALUES (9,'Іванка','AA2322324');
UNLOCK TABLES;

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `vehicle_id` int DEFAULT NULL,
  `route_id` int DEFAULT NULL,
  `status` enum('нове','в дорозі','доставлено') DEFAULT 'нове',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `vehicle_id` (`vehicle_id`),
  KEY `route_id` (`route_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`vehicle_id`),
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`route_id`) REFERENCES `routes` (`route_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



LOCK TABLES `orders` WRITE;
UNLOCK TABLES;


DROP TABLE IF EXISTS `routes`;
CREATE TABLE `routes` (
  `route_id` int NOT NULL AUTO_INCREMENT,
  `start_location` varchar(100) DEFAULT NULL,
  `end_location` varchar(100) DEFAULT NULL,
  `distance_km` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`route_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `routes` WRITE;

INSERT INTO `routes` VALUES (2,'Київ','Одеса',475.00),(3,'Львів','Одеса',780.00),(4,'Київ','Харків',480.00),(5,'Львів','Харків',1020.00),(6,'Київ','Дніпро',480.00),(7,'Одеса','Дніпро',540.00),(8,'Харків','Дніпро',215.00),(9,'Львів','Івано-Франківськ',135.00),(10,'Київ','Житомир',140.00),(11,'Львів','Тернопіль',120.00),(13,'Одеса','Миколаїв',135.00),(14,'Харків','Полтава',142.00),(15,'Львів','Луцьк',150.00);

UNLOCK TABLES;


DROP TABLE IF EXISTS `vehicles`;
CREATE TABLE `vehicles` (
  `vehicle_id` int NOT NULL AUTO_INCREMENT,
  `plate_number` varchar(20) DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  `driver_id` int DEFAULT NULL,
  PRIMARY KEY (`vehicle_id`),
  UNIQUE KEY `plate_number` (`plate_number`),
  KEY `driver_id` (`driver_id`),
  CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`driver_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `vehicles` WRITE;
INSERT INTO `vehicles` VALUES (11,'8658608',1000,9);
UNLOCK TABLES;