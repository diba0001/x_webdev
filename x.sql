-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Vært: mariadb
-- Genereringstid: 24. 11 2025 kl. 10:43:52
-- Serverversion: 10.6.20-MariaDB-ubu2004
-- PHP-version: 8.2.27

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
-- Struktur-dump for tabellen `posts`
--

CREATE TABLE `posts` (
  `post_pk` char(32) NOT NULL,
  `post_user_fk` char(32) NOT NULL,
  `post_message` varchar(280) NOT NULL,
  `post_total_likes` bigint(20) UNSIGNED NOT NULL,
  `post_image_path` varchar(255) NOT NULL,
  `post_created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `posts`
--

INSERT INTO `posts` (`post_pk`, `post_user_fk`, `post_message`, `post_total_likes`, `post_image_path`, `post_created_at`) VALUES
('00aedfa5929745498ea613c43954e866', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'Can I delete this picture?', 0, '', '2025-11-19 15:37:06'),
('1030d251278040a7a06c2e25218f1bf2', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'A browsing test', 0, '', '2025-11-19 15:37:06'),
('1e5ecc804e1f46bc8e723437bf4bfc4b', '225a9fc15b8f409aa5c8ee7eafee516b', 'And this just works!', 0, 'post_3.jpg', '2025-11-19 15:37:06'),
('258aeac7242348058c8c36f025b10fd5', '225a9fc15b8f409aa5c8ee7eafee516b', 'tes5', 0, '', '2025-11-19 15:37:06'),
('28dd4c1671634d73acd29a0ab109bef1', '805a39cd8c854ee8a83555a308645bf5', 'My first super life !', 0, 'post_3.jpg', '2025-11-19 15:37:06'),
('299323cf81924589b0de265e715a1f9e', '225a9fc15b8f409aa5c8ee7eafee516b', 'test3', 0, 'post_1.jpg', '2025-11-19 15:37:06'),
('32cae9be7eb443648be045dc8d0627f0', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'I am at class', 0, '', '2025-11-19 15:37:06'),
('39e97f6c17354b59888518ea56501e29', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'This is a picture of Arturos task for us', 0, 'ac59dc424bbe4a41a0c43c02a88b332d_GetImage.ashx-2.png', '2025-11-19 15:37:06'),
('3cb78d73518c4c01a29ad33d196ce962', '225a9fc15b8f409aa5c8ee7eafee516b', 'This is new', 0, '', '2025-11-19 15:37:06'),
('3e4f0c3ab65344d8b79c849400418758', '225a9fc15b8f409aa5c8ee7eafee516b', 'test1', 0, '', '2025-11-19 15:37:06'),
('50293af4d1f64798af9b7dfcbf5ed3e7', '225a9fc15b8f409aa5c8ee7eafee516b', 'new', 0, '', '2025-11-19 15:37:06'),
('56b89bdf56a64f95b82b76aebbb062b8', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'hi world', 0, '74bed71a30624b4b8ac96d88bb58008a_wdc_black.png', '2025-11-19 15:37:06'),
('5b147eb4f0064bd9be7f18e6be2b3347', '225a9fc15b8f409aa5c8ee7eafee516b', 'First great test', 0, '', '2025-11-19 15:37:06'),
('616c38c6e9e14406a92439e2d81490fc', '225a9fc15b8f409aa5c8ee7eafee516b', 'A browser', 0, '', '2025-11-19 15:37:06'),
('63ed90b8cafc47fa9a3253fa1ecfeb04', '225a9fc15b8f409aa5c8ee7eafee516b', 'this', 0, '', '2025-11-19 15:37:06'),
('7c2e073e08154a84b4d0fdd2659221fc', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'Now, is this picture visible?', 0, 'b4e0588617fc4ba2ac183211d0882e02_HK-ad.webp', '2025-11-19 15:37:06'),
('7c49e2bf4ad74fb3a2b7f85708470a1f', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'Can you see this post?', 0, '', '2025-11-19 15:37:06'),
('7d6f40e626c54efaa32494bce5f739d7', '88a93bb5267e443eb0047f421a7a2f34', 'test', 0, 'post_2.jpg', '2025-11-19 15:37:06'),
('99fefea24ea5419da19ed1f8cf8e9499', '225a9fc15b8f409aa5c8ee7eafee516b', 'wow', 0, 'post_1.jpg', '2025-11-19 15:37:06'),
('ad95e1d3f62f4d07b7bf9e3e6d4dd527', '225a9fc15b8f409aa5c8ee7eafee516b', 'And this just works!', 0, '', '2025-11-19 15:37:06'),
('b4b23963a6a4479e918e66f47baef200', '225a9fc15b8f409aa5c8ee7eafee516b', 'test1', 0, '', '2025-11-19 15:37:06'),
('b8f59662ce5b4b58bf19a5fe0eda3122', '225a9fc15b8f409aa5c8ee7eafee516b', 'test2', 0, '', '2025-11-19 15:37:06'),
('bcaa6df8880e411a9c25deaafae2314a', '225a9fc15b8f409aa5c8ee7eafee516b', 'test4', 0, '', '2025-11-19 15:37:06'),
('c0ca62e423b347119061b54aac82998e', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'hej verden', 0, '0ba7d30b6aae4faca258fe312373c8d2_wdc_black.png', '2025-11-19 15:37:06'),
('c7ecd2a9b3cb4c09924c578b6cf0c995', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'Okay, can we make 2 posts in a row?', 0, '6c4779307fba45bba819cae679ff4477_therese-samvirke-beskaret.jpg', '2025-11-19 15:37:06'),
('d0ab2ed244824cffb3474727d5091fd8', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'What date and time did I upload this?', 0, 'db96c78162be4251a4eca17652f96e71_r-whiskey-ad-samvirke.jpg', '2025-11-24 10:36:22'),
('ddf42242f8484141956a59641805321e', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'hej', 0, '', '2025-11-19 15:37:06'),
('e40967338e8c466985dbde4e3f9c712a', '225a9fc15b8f409aa5c8ee7eafee516b', 'Testing', 0, '', '2025-11-19 15:37:06'),
('e5287e15b19d4e87b192f08642cfa659', '4d2fcca97ea24b3d9f91e986d0c7f42a', 'hi', 0, '', '2025-11-19 15:37:06');


-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `trends`
--

CREATE TABLE `trends` (
  `trend_pk` char(32) NOT NULL,
  `trend_title` varchar(100) NOT NULL,
  `trend_message` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `trends`
--

INSERT INTO `trends` (`trend_pk`, `trend_title`, `trend_message`) VALUES
('', 'War in Sudan', 'Ongoing war in South Sudan'),
('6543c995d1af4ebcbd5280a4afaa1e2c', 'Politics are rotten', 'Politicians talk, but do nothing'),
('8343c995d1af4ebcbd5280a6afaa1e2d', 'New rocket to the moon', 'A new rocket has been sent to the moon'),
('89', 'UEFA World Cup', 'Greece did not qualify for the cup');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `users`
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
-- Data dump for tabellen `users`
--

INSERT INTO `users` (`user_pk`, `user_email`, `user_password`, `user_username`, `user_first_name`, `user_last_name`, `user_avatar_path`, `user_verification_key`, `user_verified_at`) VALUES
('225a9fc15b8f409aa5c8ee7eafee516b', 'a@a.com', 'scrypt:32768:8:1$wnse70hQwhCvR9tC$724c32a91b5f277201afbb141f9293a93168327df5c9124f482d3c32b8dff991c41629f477dfaee021965f9b15318a4257aad2e933101a4c998ef3c346fc84e4', 'aTest', 'Tester', '', 'avatar_1.jpg', '', 455656),
('4d2fcca97ea24b3d9f91e986d0c7f42a', 'dim@dim.com', 'scrypt:32768:8:1$iccyjxosFx2ZWWch$c56df1a873341f331a399e51999de28ba84b6fab11fe2476a46824b626491115f6bb13145aa418415f95d2525008c6c87753ccc38e02d3df943a36959a891160', 'dimdim', 'dddjdjd', '', 'avatar_3.jpg', '', 0),
('6b48c6095913402eb4841529830e5415', 'a@a1.com', 'scrypt:32768:8:1$rRjuDGIwaA31YlPi$f73f9a059fb3757ba6724d9c94e2a192d8b8d59fcd18d7b11c57e508f1b9cfb94bb7c6fd4f8d632b777e31cd47aef9c95adcad2451786cbb7e7c073fe8cbaf3a', 'santiago1', 'Santiago', '', 'avatar_4.jpg', 'ee92b2c86a6c48569138a43ce8bc1d48', 0),
('805a39cd8c854ee8a83555a308645bf5', 'fullflaskdemomail@gmail.com', 'scrypt:32768:8:1$VlBgiW1xFsZuKRML$a5f61d62ac3f45d42c58cf8362637e717793b8760f026b1b47b7bfec47037abbe13e1c20e8bdc66fc03cc153d0bcf6185e15cf25ad58eb9d344267882dd7e78c', 'santiago', 'Santiago', '', 'avatar_1.jpg', '', 565656),
('88a93bb5267e443eb0047f421a7a2f34', 'santi@gmail.com', 'scrypt:32768:8:1$PEIO0eliDPqnCCbw$acb791128831bc90030ac363e4b76db196689bd99c1ccde5c2c20a7d4fe909e07129f3f4fd4f086e347375edbb8229e9ba5dc126cc14f6107fb1fc2abf6498f8', 'gustav', 'Gustav', '', 'avatar_2.jpg', '', 54654564);

--
-- Begrænsninger for dumpede tabeller
--

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_pk`),
  ADD UNIQUE KEY `post_pk` (`post_pk`);

--
-- Indeks for tabel `trends`
--
ALTER TABLE `trends`
  ADD UNIQUE KEY `trend_pk` (`trend_pk`);

--
-- Indeks for tabel `users`
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

--
-- Constraints for dumped tables
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
