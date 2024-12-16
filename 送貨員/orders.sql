-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-16 03:13:26
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
