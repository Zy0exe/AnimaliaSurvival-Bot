-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 07-Nov-2023 às 21:20
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
-- Banco de dados: `kruger_park`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `players`
--

CREATE TABLE `players` (
  `steam_id` varchar(255) NOT NULL,
  `discord_id` varchar(255) DEFAULT NULL,
  `coins` int(11) DEFAULT NULL,
  `animals` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`animals`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Extraindo dados da tabela `players`
--

INSERT INTO `players` (`steam_id`, `discord_id`, `coins`, `animals`) VALUES
('76561198286908053', '550014074201833495', 133499533, NULL),
('76561199346987549', '690784176416489503', 79713, '{\"Lion\": {\"name\": \"Lion\", \"price\": 30000, \"quantity\": 1, \"genders\": [{\"gender\": \"M\", \"quantity\": 1}]}}');

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
-- Extraindo dados da tabela `warnings`
--

INSERT INTO `warnings` (`id`, `player_id`, `reason`, `warning_date`) VALUES
(12, '550014074201833495', 'why the fuck not right?', '2023-11-07');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de tabela `warnings`
--
ALTER TABLE `warnings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
