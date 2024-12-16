-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-16 03:13:08
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

-- --------------------------------------------------------

--
-- 資料表結構 `delivery_person`
--

CREATE TABLE `delivery_person` (
  `D_id` int(11) NOT NULL,
  `D_name` varchar(100) NOT NULL,
  `D_phone` varchar(15) NOT NULL,
  `D_available` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `delivery_person`
--

INSERT INTO `delivery_person` (`D_id`, `D_name`, `D_phone`, `D_available`) VALUES
(1, '張三', '0912345678', 1),
(2, '李四', '0923456789', 1),
(3, '王五', '0934567890', 0);

-- --------------------------------------------------------

--
-- 資料表結構 `orders`
--

CREATE TABLE `orders` (
  `I_id` int(11) NOT NULL,
  `R_id` int(11) NOT NULL,
  `C_id` int(11) NOT NULL,
  `I_time` datetime NOT NULL,
  `I_price` decimal(10,2) NOT NULL,
  `status` enum('已下單','準備中','配送中','完成') NOT NULL DEFAULT '已下單'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `orders`
--

INSERT INTO `orders` (`I_id`, `R_id`, `C_id`, `I_time`, `I_price`, `status`) VALUES
(1, 1, 1, '2024-12-16 10:00:00', 150.00, '已下單'),
(2, 2, 2, '2024-12-16 10:15:00', 200.00, '準備中'),
(3, 3, 3, '2024-12-16 10:30:00', 120.00, '配送中'),
(4, 1, 2, '2024-12-16 11:00:00', 100.00, '完成');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
