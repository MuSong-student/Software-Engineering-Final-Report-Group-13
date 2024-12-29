-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-26 05:55:23
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `foodpangolin`
--

-- --------------------------------------------------------

--
-- 資料表結構 `account`
--

CREATE TABLE `account` (
  `A_id` int(20) NOT NULL,
  `A_account` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `A_password` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `A_role` int(5) NOT NULL COMMENT '用代號(數字)判斷哪個腳色'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `account`
--

INSERT INTO `account` (`A_id`, `A_account`, `A_password`, `A_role`) VALUES
(1, 'admin', 'admin123', 3),
(2, 'merchant1', 'merchant123', 2),
(3, 'merchant2', 'merchant456', 2),
(4, 'customer1', 'customer123', 1),
(5, 'customer2', 'customer456', 1),
(10, '111', '111', 1),
(11, '222', '222', 2),
(12, '333', '333', 3),
(13, '2222', '2222', 2),
(14, '666', '666', 4),
(15, 'test123', 'test123', 1),
(16, 'user123', 'user123', 1),
(17, 'user222', 'user222', 1),
(18, 'test1223', 'test1223', 2),
(19, '9999', '9999', 1),
(20, 'user1223', 'user1223', 1),
(21, '王大明', '888', 1),
(22, 'pa1223', '1223', 1),
(23, 'papa123', '123', 1),
(24, 'papa345', '345', 1),
(25, 'Lala1223', '1223', 1),
(26, 'user1226', '1226', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `C_id` int(30) NOT NULL,
  `C_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `C_address` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `C_phone` int(20) NOT NULL,
  `A_account` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `customer`
--

INSERT INTO `customer` (`C_id`, `C_name`, `C_address`, `C_phone`, `A_account`) VALUES
(1, '小明', '台北市中山區', 977888999, ''),
(2, '小華', '台中市北屯區', 966777888, ''),
(3, '小美', '高雄市左營區', 955666777, ''),
(4, '小王', '南投市OO', 912345678, 'user123'),
(5, '貪吃鬼', '南投市埔里鎮', 987654321, 'user1223'),
(6, '王大明', '南投縣埔里鎮', 909123456, '王大明'),
(7, '小潘', '南投縣埔里鎮', 923132123, 'pa1223'),
(8, 'papa測試', '哈哈哈', 9123, 'papa345'),
(9, 'lala', 'haha', 912, 'Lala1223'),
(10, 'user1226', '台灣南投縣', 912345678, 'user1226');

-- --------------------------------------------------------

--
-- 資料表結構 `delivery`
--

CREATE TABLE `delivery` (
  `D_id` int(20) NOT NULL,
  `D_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `D_phone` int(20) NOT NULL,
  `A_account` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `delivery`
--

INSERT INTO `delivery` (`D_id`, `D_name`, `D_phone`, `A_account`) VALUES
(1, '張4', 911122233, '444'),
(2, '李四', 922333444, ''),
(3, '王五', 933444555, ''),
(4, '阿瓜', 727272, '666');

-- --------------------------------------------------------

--
-- 資料表結構 `item`
--

CREATE TABLE `item` (
  `I_id` int(20) NOT NULL,
  `O_id` int(20) NOT NULL,
  `R_id` int(20) NOT NULL COMMENT 'FK-連結餐廳ID',
  `D_id` int(11) DEFAULT NULL,
  `C_id` int(20) NOT NULL COMMENT 'FK-連結顧客ID',
  `M_id` int(20) NOT NULL COMMENT 'FK-連結至Menu(菜品)ID',
  `I_quantity` int(20) NOT NULL,
  `status` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '訂單狀態',
  `time` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '會儲存現在當下的時間',
  `D_pickup_time` datetime DEFAULT NULL,
  `D_delivery_time` datetime DEFAULT NULL,
  `price` float DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `item`
--

INSERT INTO `item` (`I_id`, `O_id`, `R_id`, `D_id`, `C_id`, `M_id`, `I_quantity`, `status`, `time`, `D_pickup_time`, `D_delivery_time`, `price`) VALUES
(1, 0, 1, 1, 1, 1, 2, '已完成', '2024-12-18 07:49:16', '2024-12-18 13:18:24', '2024-12-17 13:18:40', 0),
(2, 0, 2, 2, 2, 2, 1, '已完成', '2024-12-18 07:49:16', '2024-12-17 13:18:28', '2024-12-19 13:18:42', 0),
(3, 0, 3, 3, 3, 3, 3, '已完成', '2024-12-18 07:49:16', '2024-12-17 13:18:32', '2024-12-18 13:18:44', 0),
(4, 0, 2, 1, 1, 4, 5, '已完成', '2024-12-18 07:49:16', '2024-12-11 13:18:34', '2024-12-16 13:18:46', 0),
(5, 0, 3, 2, 2, 5, 2, '已完成', '2024-12-18 07:49:16', '2024-12-16 13:18:36', '2024-12-17 13:18:49', 0),
(8, 0, 3, 1, 3, 2, 1, '已完成', '2024-12-18 05:42:21', '2024-12-18 13:44:55', '2024-12-18 13:44:57', 0),
(9, 0, 1, 1, 2, 3, 2, '已完成', '2024-12-18 05:49:21', '2024-12-18 13:49:33', '2024-12-18 14:13:51', 0),
(10, 0, 2, 4, 1, 4, 1, '已完成', '2024-12-18 05:49:21', '2024-12-18 14:22:50', '2024-12-18 17:36:52', 0),
(11, 0, 3, 1, 3, 2, 1, '已完成', '2024-12-18 05:49:21', '2024-12-18 17:29:39', '2024-12-18 17:29:44', 90),
(12, 1, 1, 4, 1, 1, 2, '已完成', '2024-12-18 09:35:01', '2024-12-20 16:29:21', '2024-12-20 16:30:46', 240),
(13, 2, 1, 1, 2, 1, 2, '已拒單', '2024-12-20 08:49:37', NULL, NULL, 240),
(14, 0, 2, NULL, 3, 3, 3, '待接單', '2024-12-18 09:35:01', NULL, NULL, 450),
(15, 0, 3, NULL, 2, 4, 4, '待接單', '2024-12-18 09:35:01', NULL, NULL, 200),
(16, 0, 3, NULL, 1, 5, 2, '待接單', '2024-12-18 09:35:01', NULL, NULL, 160),
(17, 2, 1, 1, 2, 6, 1, '已拒單', '2024-12-20 08:49:37', NULL, NULL, 100),
(18, 3, 1, NULL, 2, 6, 2, '商家已拒單', '2024-12-20 09:08:02', NULL, NULL, 200),
(19, 4, 1, NULL, 2, 1, 2, '待接單', '2024-12-20 09:13:26', NULL, NULL, 240),
(43, 19, 1, NULL, 16, 1, 1, '待接單', '2024-12-22 15:51:15', NULL, NULL, 120),
(44, 19, 1, NULL, 16, 6, 1, '待接單', '2024-12-22 15:51:17', NULL, NULL, 100),
(45, 12, 3, NULL, 17, 3, 1, '待接單', '2024-12-22 15:52:07', NULL, NULL, 150),
(46, 12, 3, 4, 17, 5, 1, '已完成', '2024-12-22 15:52:08', '2024-12-23 00:11:24', '2024-12-23 00:11:36', 80),
(47, 12, 3, NULL, 17, 3, 1, '待接單', '2024-12-22 15:57:09', NULL, NULL, 150),
(48, 12, 3, NULL, 17, 5, 1, '待接單', '2024-12-22 15:57:10', NULL, NULL, 80),
(49, 16, 1, 4, 16, 1, 2, '已完成', '2024-12-22 17:03:11', '2024-12-23 01:06:30', '2024-12-23 01:06:37', 240),
(50, 19, 1, NULL, 16, 6, 5, '待接單', '2024-12-22 17:03:16', NULL, NULL, 500),
(51, 19, 1, NULL, 16, 1, 1, '待接單', '2024-12-23 07:50:40', NULL, NULL, 120),
(52, 18, 2, NULL, 20, 2, 1, '待接單', '2024-12-23 07:52:45', NULL, NULL, 90),
(53, 18, 2, NULL, 20, 4, 1, '待接單', '2024-12-23 07:52:46', NULL, NULL, 50),
(54, 0, 1, NULL, 16, 1, 1, '待接單', '2024-12-23 14:32:53', NULL, NULL, 120),
(55, 0, 1, NULL, 16, 1, 1, '待接單', '2024-12-23 14:33:35', NULL, NULL, 120),
(56, 0, 1, NULL, 16, 1, 1, '待接單', '2024-12-23 14:33:43', NULL, NULL, 120),
(57, 25, 1, NULL, 4, 1, 1, '待接單', '2024-12-26 04:09:04', NULL, NULL, 120),
(58, 20, 1, NULL, 6, 1, 1, '待接單', '2024-12-23 15:12:40', NULL, NULL, 120),
(59, 21, 2, 4, 8, 2, 1, '已完成', '2024-12-23 15:24:12', '2024-12-23 23:26:04', '2024-12-23 23:26:08', 90),
(60, 22, 3, NULL, 9, 3, 1, '待接單', '2024-12-23 15:28:31', NULL, NULL, 150),
(61, 22, 3, NULL, 9, 5, 1, '待接單', '2024-12-23 15:28:33', NULL, NULL, 80),
(62, 23, 1, 4, 4, 6, 1, '已完成', '2024-12-26 04:09:04', '2024-12-26 12:10:17', '2024-12-26 12:10:22', 100),
(63, 25, 1, NULL, 4, 6, 1, '待接單', '2024-12-26 04:20:25', NULL, NULL, 100),
(64, 26, 3, NULL, 10, 5, 1, '待接單', '2024-12-26 04:50:48', NULL, NULL, 80),
(65, 26, 3, NULL, 10, 3, 1, '待接單', '2024-12-26 04:50:49', NULL, NULL, 150);

-- --------------------------------------------------------

--
-- 資料表結構 `menu`
--

CREATE TABLE `menu` (
  `M_id` int(20) NOT NULL,
  `M_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `M_price` int(20) NOT NULL,
  `M_description` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `R_id` int(20) NOT NULL COMMENT 'FK-連結餐廳ID'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `menu`
--

INSERT INTO `menu` (`M_id`, `M_name`, `M_price`, `M_description`, `R_id`) VALUES
(1, '牛肉麵', 120, '經典紅燒牛肉麵', 1),
(2, '雞排飯', 90, '香脆雞排搭配白飯', 2),
(3, '義大利麵', 150, '特製茄汁義大利麵', 3),
(4, '水餃', 50, '手工豬肉水餃', 2),
(5, '沙拉', 80, '健康蔬菜沙拉', 3),
(6, '雞肉飯', 100, '好吃雞肉飯', 1),
(7, '炒飯', 100, '好吃', 2);

-- --------------------------------------------------------

--
-- 資料表結構 `orders`
--

CREATE TABLE `orders` (
  `O_id` int(20) NOT NULL,
  `R_id` int(20) NOT NULL,
  `total_price` int(20) NOT NULL,
  `status` enum('pending','accepted','rejected','ready','completed') CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `C_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `orders`
--

INSERT INTO `orders` (`O_id`, `R_id`, `total_price`, `status`, `time`, `C_id`) VALUES
(1, 1, 240, 'rejected', '2024-12-22 16:00:57', NULL),
(2, 1, 340, 'rejected', '2024-12-22 16:01:04', NULL),
(3, 1, 200, 'rejected', '2024-12-22 16:01:11', NULL),
(4, 1, 340, 'ready', '2024-12-22 16:01:16', NULL),
(7, 1, 600, 'ready', '2024-12-22 16:09:55', 16),
(8, 1, 600, 'ready', '2024-12-22 16:09:50', 16),
(9, 1, 720, 'ready', '2024-12-22 16:09:53', 16),
(10, 1, 220, 'ready', '2024-12-22 16:27:21', NULL),
(11, 3, 230, 'accepted', '2024-12-22 15:52:11', 17),
(12, 3, 460, 'accepted', '2024-12-22 15:57:15', 17),
(13, 1, 220, 'accepted', '2024-12-22 16:21:29', 16),
(14, 1, 220, 'accepted', '2024-12-22 16:22:53', 16),
(15, 1, 220, 'ready', '2024-12-23 05:12:49', 16),
(16, 1, 960, 'ready', '2024-12-22 17:04:51', 16),
(17, 1, 720, 'accepted', '2024-12-23 05:13:54', 16),
(18, 2, 140, 'ready', '2024-12-23 15:31:12', 20),
(19, 1, 840, 'accepted', '2024-12-23 14:28:00', 16),
(20, 1, 120, 'accepted', '2024-12-23 15:12:52', 6),
(21, 2, 90, 'ready', '2024-12-23 15:25:19', 8),
(22, 3, 230, 'accepted', '2024-12-23 15:28:39', 9),
(23, 1, 220, 'ready', '2024-12-26 04:09:07', 4),
(24, 1, 220, 'pending', '2024-12-26 04:20:27', 4),
(25, 1, 220, 'pending', '2024-12-26 04:20:52', 4),
(26, 3, 230, 'pending', '2024-12-26 04:50:52', 10);

-- --------------------------------------------------------

--
-- 資料表結構 `restaurant`
--

CREATE TABLE `restaurant` (
  `R_id` int(20) NOT NULL,
  `R_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `R_address` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `R_phone` int(20) NOT NULL,
  `A_account` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `restaurant`
--

INSERT INTO `restaurant` (`R_id`, `R_name`, `R_address`, `R_phone`, `A_account`) VALUES
(1, '美味餐廳', '台北市信義區', 912345678, 222),
(2, '家鄉味小吃', '台中市西屯區', 987654321, 2222),
(3, '異國料理館', '高雄市鼓山區', 922333444, 2223);

-- --------------------------------------------------------

--
-- 資料表結構 `stars`
--

CREATE TABLE `stars` (
  `S_id` int(20) NOT NULL,
  `O_id` int(20) NOT NULL COMMENT 'FK-連結訂單orderID',
  `C_id` int(20) NOT NULL COMMENT 'FK-連結顧客ID',
  `S_stars` int(2) NOT NULL,
  `S_comment` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `stars`
--

INSERT INTO `stars` (`S_id`, `O_id`, `C_id`, `S_stars`, `S_comment`) VALUES
(1, 23, 4, 2, '好吃'),
(2, 26, 10, 3, '還不錯');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`A_id`);

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`C_id`);

--
-- 資料表索引 `delivery`
--
ALTER TABLE `delivery`
  ADD PRIMARY KEY (`D_id`);

--
-- 資料表索引 `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`I_id`);

--
-- 資料表索引 `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`M_id`);

--
-- 資料表索引 `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`O_id`);

--
-- 資料表索引 `restaurant`
--
ALTER TABLE `restaurant`
  ADD PRIMARY KEY (`R_id`);

--
-- 資料表索引 `stars`
--
ALTER TABLE `stars`
  ADD PRIMARY KEY (`S_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `account`
--
ALTER TABLE `account`
  MODIFY `A_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `C_id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `delivery`
--
ALTER TABLE `delivery`
  MODIFY `D_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `item`
--
ALTER TABLE `item`
  MODIFY `I_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `M_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orders`
--
ALTER TABLE `orders`
  MODIFY `O_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `R_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `stars`
--
ALTER TABLE `stars`
  MODIFY `S_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;