-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 27-Dez-2023 às 02:06
-- Versão do servidor: 10.4.25-MariaDB
-- versão do PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `animalia_bot`
--
CREATE DATABASE IF NOT EXISTS `animalia_bot` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `animalia_bot`;

-- --------------------------------------------------------

--
-- Estrutura da tabela `players`
--

CREATE TABLE `players` (
  `steam_id` varchar(255) NOT NULL,
  `discord_id` varchar(255) DEFAULT NULL,
  `coins` int(11) DEFAULT NULL,
  `animals` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`animals`)),
  `last_work_time` datetime DEFAULT NULL,
  `coins_received` tinyint(4) NOT NULL DEFAULT 0,
  `last_voice_time` datetime DEFAULT NULL,
  `voice_start_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Acionadores `players`
--
DELIMITER $$
CREATE TRIGGER `award_coins_after_link` AFTER UPDATE ON `players` FOR EACH ROW BEGIN
    IF NEW.coins_received = 1 AND OLD.coins_received = 0 THEN
        -- Award 75k coins to the user's balance
        UPDATE players
        SET coins = coins + 75000
        WHERE discord_id = NEW.discord_id;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estrutura da tabela `strikes`
--

CREATE TABLE `strikes` (
  `id` int(11) NOT NULL,
  `date_issued` timestamp NOT NULL DEFAULT current_timestamp(),
  `admin_id` varchar(255) DEFAULT NULL,
  `player_steam_id` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estrutura da tabela `warnings`
--

CREATE TABLE `warnings` (
  `id` int(11) NOT NULL,
  `player_id` varchar(255) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `warning_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `players`
--
ALTER TABLE `players`
  ADD PRIMARY KEY (`steam_id`);

--
-- Índices para tabela `strikes`
--
ALTER TABLE `strikes`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `warnings`
--
ALTER TABLE `warnings`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `strikes`
--
ALTER TABLE `strikes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de tabela `warnings`
--
ALTER TABLE `warnings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
