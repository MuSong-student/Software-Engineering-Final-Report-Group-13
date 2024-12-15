-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-15 12:08:19
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `food`
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

-- --------------------------------------------------------

--
-- 資料表結構 `delivery`
--

CREATE TABLE `delivery` (
  `D_id` int(20) NOT NULL,
  `D_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `D_phone` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `item`
--

CREATE TABLE `item` (
  `I_id` int(20) NOT NULL,
  `R_id` int(20) NOT NULL COMMENT 'FK-連結餐廳ID',
  `D_id` int(20) NOT NULL COMMENT 'FK-連結送貨員ID',
  `C_id` int(20) NOT NULL COMMENT 'FK-連結顧客ID',
  `M_id` int(20) NOT NULL COMMENT 'FK-連結至Menu(菜品)ID',
  `I_quantity` int(20) NOT NULL,
  `status` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '訂單狀態',
  `time` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '會儲存現在當下的時間'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
  MODIFY `A_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `C_id` int(30) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `delivery`
--
ALTER TABLE `delivery`
  MODIFY `D_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `item`
--
ALTER TABLE `item`
  MODIFY `I_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `M_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `R_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `stars`
--
ALTER TABLE `stars`
  MODIFY `S_id` int(20) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
