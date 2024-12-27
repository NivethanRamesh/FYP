-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 14, 2024 at 04:06 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `car_parts_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `feedback_text` text NOT NULL,
  `submission_date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `name`, `email`, `phone_number`, `feedback_text`, `submission_date`) VALUES
(1, 'Asad', 'Asad@gmail.com', '03419827549', 'Good', '2024-07-11 20:58:00'),
(2, 'Faiq', 'Faiq@gmail.com', '123456789', 'Nice Website', '2024-07-11 22:39:02'),
(4, 'Hammad', 'Hammad@gmail.com', '123456789', 'Good Website', '2024-07-11 22:41:19'),
(5, 'Kamran', 'Kamran@gmail.com', '11223344', 'Very Nice Application', '2024-07-11 22:45:51'),
(6, 'Areeb', 'Areeb@gmail.com', '987654321', 'Nice Concept', '2024-07-11 23:35:07');

-- --------------------------------------------------------

--
-- Table structure for table `prediction`
--

CREATE TABLE `prediction` (
  `id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `component` varchar(50) NOT NULL,
  `condition` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prediction`
--

INSERT INTO `prediction` (`id`, `timestamp`, `component`, `condition`) VALUES
(1, '2024-07-11 20:38:20', 'spark-plug', 'Damaged'),
(2, '2024-07-11 20:39:51', 'spark-plug', 'Damaged'),
(3, '2024-07-11 22:49:25', 'BRAKE PAD', 'Damaged'),
(4, '2024-07-11 22:52:01', 'BRAKE PAD', 'Damaged'),
(5, '2024-07-11 22:52:15', 'spark-plug', 'Damaged'),
(6, '2024-07-11 22:54:33', 'spark-plug', 'Undamaged'),
(7, '2024-07-11 22:54:47', 'spark-plug', 'Damaged'),
(8, '2024-07-11 22:56:41', 'spark-plug', 'Damaged'),
(9, '2024-07-11 22:56:56', 'BRAKE PAD', 'Damaged'),
(10, '2024-07-11 23:01:31', 'BRAKE PAD', 'Damaged'),
(11, '2024-07-11 23:01:44', 'BRAKE PAD', 'Damaged'),
(12, '2024-07-11 23:02:31', 'BRAKE PAD', 'Damaged'),
(13, '2024-07-11 23:02:45', 'BRAKE PAD', 'Damaged'),
(14, '2024-07-11 23:03:53', 'BRAKE PAD', 'Damaged'),
(15, '2024-07-11 23:05:20', 'BRAKE PAD', 'Damaged'),
(16, '2024-07-11 23:05:40', 'BRAKE PAD', 'Damaged'),
(17, '2024-07-11 23:07:25', 'BRAKE PAD', 'Damaged'),
(18, '2024-07-11 23:07:38', 'spark-plug', 'Damaged'),
(19, '2024-07-11 23:18:42', 'spark-plug', 'Damaged'),
(20, '2024-07-11 23:23:57', 'spark-plug', 'Damaged'),
(21, '2024-07-11 23:25:31', 'BRAKE PAD', 'Damaged'),
(22, '2024-07-11 23:25:51', 'BRAKE PAD', 'Damaged'),
(23, '2024-07-11 23:35:33', 'BRAKE PAD', 'Damaged'),
(24, '2024-07-11 23:35:58', 'spark-plug', 'Damaged'),
(25, '2024-07-13 23:36:44', 'spark-plug', 'Damaged'),
(26, '2024-07-13 23:38:16', 'spark-plug', 'Damaged');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `prediction`
--
ALTER TABLE `prediction`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `prediction`
--
ALTER TABLE `prediction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
