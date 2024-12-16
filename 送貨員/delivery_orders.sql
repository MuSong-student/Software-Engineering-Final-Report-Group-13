-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-16 03:13:17
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `delivery`
--

-- --------------------------------------------------------

--
-- 資料表結構 `delivery_orders`
--

CREATE TABLE `delivery_orders` (
  `D_I_id` int(11) NOT NULL,
  `I_id` int(11) NOT NULL,
  `D_id` int(11) DEFAULT NULL,
  `D_pickup_time` datetime DEFAULT NULL,
  `D_delivery_time` datetime DEFAULT NULL,
  `D_status` enum('待接單','配送中','已完成') NOT NULL DEFAULT '待接單'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `delivery_orders`
--

INSERT INTO `delivery_orders` (`D_I_id`, `I_id`, `D_id`, `D_pickup_time`, `D_delivery_time`, `D_status`) VALUES
(1, 1, 1, '2024-12-16 10:05:00', '2024-12-16 10:20:00', '已完成'),
(2, 2, 2, '2024-12-16 10:20:00', NULL, '配送中'),
(3, 3, NULL, NULL, NULL, '待接單'),
(4, 4, 1, '2024-12-16 11:05:00', '2024-12-16 11:20:00', '已完成');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
