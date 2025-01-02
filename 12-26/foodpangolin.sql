-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-29 14:45:24
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
(11, '222', '222', 2),
(12, '333', '333', 3),
(14, '666', '666', 4),
(27, 'user1229', 'user1229', 1),
(29, '2223', '2223', 2),
(30, '2222', '2222', 2);

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
(11, '1229', '1229', 932885461, 'user1229');

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
(72, 32, 1, 4, 11, 1, 4, '已完成', '2024-12-29 13:37:33', '2024-12-29 21:37:47', '2024-12-29 21:38:07', 480);

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
(32, 1, 480, 'ready', '2024-12-29 13:37:58', 11);

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
(2, 26, 10, 3, '還不錯'),
(3, 32, 11, 1, '外送速度太慢，外送員態度不佳');

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
  MODIFY `A_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `C_id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `delivery`
--
ALTER TABLE `delivery`
  MODIFY `D_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `item`
--
ALTER TABLE `item`
  MODIFY `I_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `M_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orders`
--
ALTER TABLE `orders`
  MODIFY `O_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `R_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `stars`
--
ALTER TABLE `stars`
  MODIFY `S_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
