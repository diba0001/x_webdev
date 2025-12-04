-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Vært: mariadb
-- Genereringstid: 04. 12 2025 kl. 15:30:48
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
-- Struktur-dump for tabellen `follows`
--

CREATE TABLE `follows` (
  `follow_follower_fk` char(32) NOT NULL,
  `follow_followed_fk` char(32) NOT NULL,
  `follow_timestamp` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `follows`
--

INSERT INTO `follows` (`follow_follower_fk`, `follow_followed_fk`, `follow_timestamp`) VALUES
('', '88a93bb5267e443eb0047f421a7a2f34', 1764581121),
('', '9860c6174a3141c5b1e7c8b3638b2f2b', 1764855078);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `likes`
--

CREATE TABLE `likes` (
  `like_user_fk` char(32) NOT NULL,
  `like_post_fk` char(32) NOT NULL,
  `like_timestamp` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `likes`
--
DELIMITER $$
CREATE TRIGGER `after_like_delete` AFTER DELETE ON `likes` FOR EACH ROW BEGIN
    UPDATE `posts` 
    SET `post_total_likes` = GREATEST(0, CAST(`post_total_likes` AS SIGNED) - 1)
    WHERE `post_pk` = OLD.like_post_fk;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_like_insert` AFTER INSERT ON `likes` FOR EACH ROW BEGIN
    UPDATE `posts` 
    SET `post_total_likes` = `post_total_likes` + 1 
    WHERE `post_pk` = NEW.like_post_fk;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `posts`
--

CREATE TABLE `posts` (
  `post_pk` char(32) NOT NULL,
  `post_user_fk` char(32) NOT NULL,
  `post_message` varchar(280) NOT NULL,
  `post_total_likes` int(11) NOT NULL DEFAULT 0,
  `post_media_path` varchar(255) NOT NULL,
  `post_blocked_at` bigint(20) DEFAULT NULL,
  `post_created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `post_deleted_at` bigint(20) NOT NULL,
  `post_updated_at` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `posts`
--

INSERT INTO `posts` (`post_pk`, `post_user_fk`, `post_message`, `post_total_likes`, `post_media_path`, `post_blocked_at`, `post_created_at`, `post_deleted_at`, `post_updated_at`) VALUES
('070678cb348846839b79d2ed6834f743', '88a93bb5267e443eb0047f421a7a2f34', 'a post with a pic', 0, 'images/aa147d759fcb4ceeb7dc8d1e45939aa4_twitter_erd_crowsfoot.png', 0, '2025-12-04 15:22:31', 0, 1764861780),
('28dd4c1671634d73acd29a0ab109bef1', '805a39cd8c854ee8a83555a308645bf5', 'My first super life !', 1, 'images/post_3.jpg', 0, '2025-12-03 11:41:46', 0, 0),
('299323cf81924589b0de265e715a1f9e', '225a9fc15b8f409aa5c8ee7eafee516b', 'test3', 1, 'images/post_1.jpg', 0, '2025-12-03 11:41:46', 0, 0),
('2c47ae1bc8f249109157eeda70504ac5', '88a93bb5267e443eb0047f421a7a2f34', 'A picture', 0, 'images/0026ecf80e9341c1b534c155f8eb6c8e_IMG_6962.jpeg', 0, '2025-12-04 15:19:06', 0, 0),
('2e6532f3d6084a54afd4f49a32cc24cf', '5388749', 'hi', 0, '', 0, '2025-12-04 13:27:16', 0, 0),
('3ccd07dc9eb64fe4a9e7059ada79d61d', '', 'malthe og emil dater', 0, '', 0, '2025-12-04 14:47:49', 0, 0),
('4634e7714feb42aea9cb055b85f352fc', '237485250205824500245', 'hi', 0, '', 0, '2025-12-04 13:31:28', 0, 0),
('508f6200791446d49165c0cccd7d7268', '240927592750274', 'hi', 0, 'images/3d76bdd0a6414c0b89a9dc7dc1c7c3f5_twitter_erd_crowsfoot.png', 0, '2025-12-04 13:16:43', 0, 0),
('5ed0a8395020449ba2c5abe294689d3b', '88a93bb5267e443eb0047f421a7a2f34', 'emil elzker kanelgifflz', 0, 'images/7e73abc8fda8474595a145387d1abbc7_favicon-16x16.png', 0, '2025-12-04 14:51:07', 0, 1764860941),
('663f6045b08c49aeae88ae10eb1d2625', '', 'claus', 0, '', 0, '2025-12-04 14:50:13', 0, 0),
('7d6f40e626c54efaa32494bce5f739d7', '88a93bb5267e443eb0047f421a7a2f34', 'test2', 1, 'images/post_2.jpg', 0, '2025-12-03 11:41:46', 0, 1764860711),
('9605bb608a324ff185fc5033744d62ad', '', 'emil elsker majskiks', 0, '', NULL, '2025-12-04 14:40:34', 0, 0),
('99fefea24ea5419da19ed1f8cf8e9499', '225a9fc15b8f409aa5c8ee7eafee516b', 'wow', 0, 'images/post_1.jpg', 1764838458, '2025-12-03 11:41:46', 0, 0),
('ab2f3c649a444eb588cd8307c6f8ae56', '2342304205092', 'hi', 0, '', 0, '2025-12-04 13:29:53', 0, 0),
('bcaa6df8880e411a9c25deaafae2314a', '225a9fc15b8f409aa5c8ee7eafee516b', 'test4', 2, '', 0, '2025-12-03 11:41:46', 0, 0),
('c0e92aad8b6c46c6899d59ecc5e8105a', '', 'hej', 0, '', NULL, '2025-12-04 14:32:49', 0, 0),
('c156b4470e084e529cc5189c44b9d030', '', 'emil', 0, '', NULL, '2025-12-04 14:33:27', 0, 0),
('c4dca608ab1c4e788d34a818658313ed', '235702945879450', 'hi', 0, 'images/66b1f63a3bdd45e28805007e28eb02cd_twitter_erd_crowsfoot.png', 0, '2025-12-04 13:13:32', 0, 0),
('c4ddb3c171a34cb2903bc98d03883d24', '', 'hi', 0, '', 0, '2025-12-04 13:29:35', 0, 0),
('d60b8eedfcb6420587b2f528566386df', '', 'hi', 0, 'images/666c6234a4254807b73e134781ec282a_android-chrome-512x512.png', 0, '2025-12-04 13:22:29', 0, 1764857447),
('e428fa103e6c41c5948c553b0a64b7b9', '', 'emil er zuper zød', 0, '', 0, '2025-12-04 14:42:01', 0, 0),
('e4652c7659fa456babd12e27c33155d4', '', 'hi 2', 0, '', 0, '2025-12-04 13:39:27', 0, 1764855574),
('fca0b7f700de4682909ec8372744b8fd', '', 'jeg laver et post', 0, '', 0, '2025-12-04 14:16:15', 0, 0);

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
('6543c995d1af4ebcbd5280a4afaa1e2c', 'Politics are rotten', 'Everyone talks and only a few try to do something'),
('8343c995d1af4ebcbd5280a6afaa1e2d', 'New rocket to the moon', 'A new rocket has been sent towards the moon, but id didn\'t make it');

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
  `user_avatar_path` varchar(255) NOT NULL,
  `user_verification_key` char(32) NOT NULL,
  `user_verified_at` bigint(20) UNSIGNED NOT NULL,
  `user_deleted_at` bigint(20) UNSIGNED NOT NULL,
  `user_is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `user_blocked_at` bigint(20) UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `users`
--

INSERT INTO `users` (`user_pk`, `user_email`, `user_password`, `user_username`, `user_first_name`, `user_last_name`, `user_avatar_path`, `user_verification_key`, `user_verified_at`, `user_deleted_at`, `user_is_admin`, `user_blocked_at`) VALUES
('', 'r@r.dk', 'scrypt:32768:8:1$wnse70hQwhCvR9tC$724c32a91b5f277201afbb141f9293a93168327df5c9124f482d3c32b8dff991c41629f477dfaee021965f9b15318a4257aad2e933101a4c998ef3c346fc84e4', 'RasmusOlsen', 'Rasmus', '', 'static/images/avatars/avatar_1.jpg', '', 12321321, 0, 1, 0),
('225a9fc15b8f409aa5c8ee7eafee516b', 'ralle147@hotmail.com', 'scrypt:32768:8:1$wnse70hQwhCvR9tC$724c32a91b5f277201afbb141f9293a93168327df5c9124f482d3c32b8dff991c41629f477dfaee021965f9b15318a4257aad2e933101a4c998ef3c346fc84e4', 'aTest', 'Tester', '', 'static/images/avatars/avatar_2.jpg', '', 455656, 0, 0, 0),
('6b48c6095913402eb4841529830e5415', 'a@a1.com', 'scrypt:32768:8:1$rRjuDGIwaA31YlPi$f73f9a059fb3757ba6724d9c94e2a192d8b8d59fcd18d7b11c57e508f1b9cfb94bb7c6fd4f8d632b777e31cd47aef9c95adcad2451786cbb7e7c073fe8cbaf3a', 'santiago1', 'Santiago', '', 'static/images/avatars/avatar_3.jpg', 'ee92b2c86a6c48569138a43ce8bc1d48', 0, 0, 0, 0),
('805a39cd8c854ee8a83555a308645bf5', 'fullflaskdemomail@gmail.com', 'scrypt:32768:8:1$VlBgiW1xFsZuKRML$a5f61d62ac3f45d42c58cf8362637e717793b8760f026b1b47b7bfec47037abbe13e1c20e8bdc66fc03cc153d0bcf6185e15cf25ad58eb9d344267882dd7e78c', 'santiago', 'Santiago', '', 'static/images/avatars/avatar_4.jpg', '', 565656, 0, 0, 0),
('88a93bb5267e443eb0047f421a7a2f34', 'santi@gmail.com', 'scrypt:32768:8:1$PEIO0eliDPqnCCbw$acb791128831bc90030ac363e4b76db196689bd99c1ccde5c2c20a7d4fe909e07129f3f4fd4f086e347375edbb8229e9ba5dc126cc14f6107fb1fc2abf6498f8', 'gustav', 'Gustav', '', 'static/images/avatars/f6262d530c0d46a48710087334157593.png', '', 54654564, 0, 0, 0),
('9860c6174a3141c5b1e7c8b3638b2f2b', 'maltheaaen@gmail.com', 'scrypt:32768:8:1$5NSH8Gsqi83lQV24$b61989755f5e00e7632463dee7b806b93acab7d4de36b6e32caf47a2fcef8bf23db0624a3767d5bae3ba40c77673171dad51a4b472e44a9463fc141a0b7f37bb', 'Malt', 'Malthe', '', 'static/images/avatars/avatar_5.jpg', '', 54654564, 0, 0, 0);

--
-- Begrænsninger for dumpede tabeller
--

--
-- Indeks for tabel `follows`
--
ALTER TABLE `follows`
  ADD PRIMARY KEY (`follow_follower_fk`,`follow_followed_fk`),
  ADD KEY `follow_followed_fk` (`follow_followed_fk`);

--
-- Indeks for tabel `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`like_user_fk`,`like_post_fk`),
  ADD KEY `like_post_fk` (`like_post_fk`);

--
-- Indeks for tabel `posts`
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
-- Begrænsninger for dumpede tabeller
--

--
-- Begrænsninger for tabel `follows`
--
ALTER TABLE `follows`
  ADD CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follow_follower_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`follow_followed_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`like_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`like_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
