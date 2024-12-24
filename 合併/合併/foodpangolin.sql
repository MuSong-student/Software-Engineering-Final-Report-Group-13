-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-18 07:49:10
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.2.4

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
(13, '444', '444', 4),
(14, '666', '666', 4);

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `C_id` int(30) NOT NULL,
  `C_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `C_address` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `C_phone` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `customer`
--

INSERT INTO `customer` (`C_id`, `C_name`, `C_address`, `C_phone`) VALUES
(1, '小明', '台北市中山區', 977888999),
(2, '小華', '台中市北屯區', 966777888),
(3, '小美', '高雄市左營區', 955666777);

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
(1, '張456', 911122233, '444'),
(2, '李四', 922333444, ''),
(3, '王五', 933444555, ''),
(4, '阿瓜', 727272, '666');

-- --------------------------------------------------------

--
-- 資料表結構 `item`
--

CREATE TABLE `item` (
  `I_id` int(20) NOT NULL,
  `R_id` int(20) NOT NULL COMMENT 'FK-連結餐廳ID',
  `D_id` int(11) DEFAULT NULL,
  `C_id` int(20) NOT NULL COMMENT 'FK-連結顧客ID',
  `M_id` int(20) NOT NULL COMMENT 'FK-連結至Menu(菜品)ID',
  `I_quantity` int(20) NOT NULL,
  `status` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '訂單狀態',
  `time` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '會儲存現在當下的時間',
  `D_pickup_time` datetime DEFAULT NULL,
  `D_delivery_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `item`
--

INSERT INTO `item` (`I_id`, `R_id`, `D_id`, `C_id`, `M_id`, `I_quantity`, `status`, `time`, `D_pickup_time`, `D_delivery_time`) VALUES
(1, 1, 1, 1, 1, 2, '已完成', '2024-12-18 07:49:16', '2024-12-18 13:18:24', '2024-12-17 13:18:40'),
(2, 2, 2, 2, 2, 1, '已完成', '2024-12-18 07:49:16', '2024-12-17 13:18:28', '2024-12-19 13:18:42'),
(3, 3, 3, 3, 3, 3, '已完成', '2024-12-18 07:49:16', '2024-12-17 13:18:32', '2024-12-18 13:18:44'),
(4, 2, 1, 1, 4, 5, '已完成', '2024-12-18 07:49:16', '2024-12-11 13:18:34', '2024-12-16 13:18:46'),
(5, 3, 2, 2, 5, 2, '已完成', '2024-12-18 07:49:16', '2024-12-16 13:18:36', '2024-12-17 13:18:49'),
(8, 3, 1, 3, 2, 1, '已完成', '2024-12-18 05:42:21', '2024-12-18 13:44:55', '2024-12-18 13:44:57'),
(9, 1, 1, 2, 3, 2, '已完成', '2024-12-18 05:49:21', '2024-12-18 13:49:33', '2024-12-18 14:13:51'),
(10, 2, 4, 1, 4, 1, '配送中', '2024-12-18 05:49:21', '2024-12-18 14:22:50', NULL),
(11, 3, NULL, 3, 2, 1, '待接單', '2024-12-18 05:49:21', NULL, NULL);

-- --------------------------------------------------------

--
-- 資料表結構 `menu`
--

CREATE TABLE `menu` (
  `M_id` int(20) NOT NULL,
  `M_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `M_pirce` int(20) NOT NULL,
  `M_description` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `R_id` int(20) NOT NULL COMMENT 'FK-連結餐廳ID'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `menu`
--

INSERT INTO `menu` (`M_id`, `M_name`, `M_pirce`, `M_description`, `R_id`) VALUES
(1, '牛肉麵', 120, '經典紅燒牛肉麵', 1),
(2, '雞排飯', 90, '香脆雞排搭配白飯', 2),
(3, '義大利麵', 150, '特製茄汁義大利麵', 3),
(4, '水餃', 50, '手工豬肉水餃', 2),
(5, '沙拉', 80, '健康蔬菜沙拉', 3);

-- --------------------------------------------------------

--
-- 資料表結構 `restaurant`
--

CREATE TABLE `restaurant` (
  `R_id` int(20) NOT NULL,
  `R_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `R_address` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `R_phone` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- 傾印資料表的資料 `restaurant`
--

INSERT INTO `restaurant` (`R_id`, `R_name`, `R_address`, `R_phone`) VALUES
(1, '美味餐廳', '台北市信義區', 912345678),
(2, '家鄉味小吃', '台中市西屯區', 987654321),
(3, '異國料理館', '高雄市鼓山區', 922333444);

-- --------------------------------------------------------

--
-- 資料表結構 `stars`
--

CREATE TABLE `stars` (
  `S_id` int(20) NOT NULL,
  `I_id` int(20) NOT NULL COMMENT 'FK-連結訂單ID',
  `C_id` int(20) NOT NULL COMMENT 'FK-連結顧客ID',
  `S_stars` int(2) NOT NULL,
  `S_comment` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
  MODIFY `A_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `C_id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `delivery`
--
ALTER TABLE `delivery`
  MODIFY `D_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `item`
--
ALTER TABLE `item`
  MODIFY `I_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `M_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `R_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `stars`
--
ALTER TABLE `stars`
  MODIFY `S_id` int(20) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
