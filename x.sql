-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: Nov 24, 2025 at 09:02 AM
-- Server version: 10.6.20-MariaDB-ubu2004
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `x`
--

-- --------------------------------------------------------

--
-- Table structure for table `likes`
--

CREATE TABLE `likes` (
  `like_user_fk` char(32) NOT NULL,
  `like_post_fk` char(32) NOT NULL,
  `like_timestamp` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `likes`
--

INSERT INTO `likes` (`like_user_fk`, `like_post_fk`, `like_timestamp`) VALUES
('9860c6174a3141c5b1e7c8b3638b2f2b', '299323cf81924589b0de265e715a1f9e', 1763551080);

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `post_pk` char(32) NOT NULL,
  `post_user_fk` char(32) NOT NULL,
  `post_message` varchar(280) NOT NULL,
  `post_total_likes` bigint(20) UNSIGNED NOT NULL,
  `post_image_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_pk`, `post_user_fk`, `post_message`, `post_total_likes`, `post_image_path`) VALUES
('1e5ecc804e1f46bc8e723437bf4bfc4b', '225a9fc15b8f409aa5c8ee7eafee516b', 'And this just works!', 1, 'post_3.jpg'),
('28dd4c1671634d73acd29a0ab109bef1', '805a39cd8c854ee8a83555a308645bf5', 'My first super life !', 1, 'post_3.jpg'),
('299323cf81924589b0de265e715a1f9e', '225a9fc15b8f409aa5c8ee7eafee516b', 'test3', 1, 'post_1.jpg'),
('7d6f40e626c54efaa32494bce5f739d7', '88a93bb5267e443eb0047f421a7a2f34', 'test', 1, 'post_2.jpg'),
('99fefea24ea5419da19ed1f8cf8e9499', '225a9fc15b8f409aa5c8ee7eafee516b', 'wow', 0, 'post_1.jpg'),
('bcaa6df8880e411a9c25deaafae2314a', '225a9fc15b8f409aa5c8ee7eafee516b', 'test4', 2, '');

-- --------------------------------------------------------

--
-- Table structure for table `trends`
--

CREATE TABLE `trends` (
  `trend_pk` char(32) NOT NULL,
  `trend_title` varchar(100) NOT NULL,
  `trend_message` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `trends`
--

INSERT INTO `trends` (`trend_pk`, `trend_title`, `trend_message`) VALUES
('6543c995d1af4ebcbd5280a4afaa1e2c', 'Politics are rotten', 'Everyone talks and only a few try to do something'),
('8343c995d1af4ebcbd5280a6afaa1e2d', 'New rocket to the moon', 'A new rocket has been sent towards the moon, but id didn\'t make it');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` char(32) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `user_username` varchar(20) NOT NULL,
  `user_first_name` varchar(20) NOT NULL,
  `user_last_name` varchar(20) NOT NULL DEFAULT '',
  `user_avatar_path` varchar(50) NOT NULL,
  `user_verification_key` char(32) NOT NULL,
  `user_verified_at` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_email`, `user_password`, `user_username`, `user_first_name`, `user_last_name`, `user_avatar_path`, `user_verification_key`, `user_verified_at`) VALUES
('225a9fc15b8f409aa5c8ee7eafee516b', 'a@a.com', 'scrypt:32768:8:1$wnse70hQwhCvR9tC$724c32a91b5f277201afbb141f9293a93168327df5c9124f482d3c32b8dff991c41629f477dfaee021965f9b15318a4257aad2e933101a4c998ef3c346fc84e4', 'aTest', 'Tester', '', 'avatar_1.jpg', '', 455656),
('6b48c6095913402eb4841529830e5415', 'a@a1.com', 'scrypt:32768:8:1$rRjuDGIwaA31YlPi$f73f9a059fb3757ba6724d9c94e2a192d8b8d59fcd18d7b11c57e508f1b9cfb94bb7c6fd4f8d632b777e31cd47aef9c95adcad2451786cbb7e7c073fe8cbaf3a', 'santiago1', 'Santiago', '', 'https://avatar.iran.liara.run/public/40', 'ee92b2c86a6c48569138a43ce8bc1d48', 0),
('805a39cd8c854ee8a83555a308645bf5', 'fullflaskdemomail@gmail.com', 'scrypt:32768:8:1$VlBgiW1xFsZuKRML$a5f61d62ac3f45d42c58cf8362637e717793b8760f026b1b47b7bfec47037abbe13e1c20e8bdc66fc03cc153d0bcf6185e15cf25ad58eb9d344267882dd7e78c', 'santiago', 'Santiago', '', 'avatar_1.jpg', '', 565656),
('88a93bb5267e443eb0047f421a7a2f34', 'santi@gmail.com', 'scrypt:32768:8:1$PEIO0eliDPqnCCbw$acb791128831bc90030ac363e4b76db196689bd99c1ccde5c2c20a7d4fe909e07129f3f4fd4f086e347375edbb8229e9ba5dc126cc14f6107fb1fc2abf6498f8', 'gustav', 'Gustav', '', 'avatar_2.jpg', '', 54654564),
('9860c6174a3141c5b1e7c8b3638b2f2b', 'maltheaaen@gmail.com', 'scrypt:32768:8:1$5NSH8Gsqi83lQV24$b61989755f5e00e7632463dee7b806b93acab7d4de36b6e32caf47a2fcef8bf23db0624a3767d5bae3ba40c77673171dad51a4b472e44a9463fc141a0b7f37bb', 'Malt', 'Malthe', '', 'https://avatar.iran.liara.run/public/40', '', 54654564);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`like_user_fk`,`like_post_fk`),
  ADD KEY `like_post_fk` (`like_post_fk`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_pk`),
  ADD UNIQUE KEY `post_pk` (`post_pk`);

--
-- Indexes for table `trends`
--
ALTER TABLE `trends`
  ADD UNIQUE KEY `trend_pk` (`trend_pk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_pk` (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_name` (`user_username`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`like_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`like_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
