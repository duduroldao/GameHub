-- =====================================================================
-- GameHub - Catalogo Digital de Jogos
-- Banco: MySQL | Importar com:  mysql -u root -p < database/gamehub.sql
-- Observacao: este script NAO apaga nada. Se o banco ja tiver os dados,
-- rodar de novo causa erro de chave duplicada (e protege os registros).
-- =====================================================================

CREATE DATABASE IF NOT EXISTS gamehub DEFAULT CHARACTER SET utf8mb4;
USE gamehub;

-- ---------------------------------------------------------------------
-- TABELAS
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS generos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS jogos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100) NOT NULL,
    desenvolvedora VARCHAR(100) NOT NULL,
    ano_lancamento INT NOT NULL CHECK (ano_lancamento >= 1970 AND ano_lancamento <= 2100),
    descricao TEXT NOT NULL,
    imagem VARCHAR(255) NOT NULL DEFAULT 'padrao.png'
);

-- Tabela associativa que resolve o relacionamento N:N entre jogos e generos
CREATE TABLE IF NOT EXISTS jogo_genero (
    jogo_id INT NOT NULL,
    genero_id INT NOT NULL,
    PRIMARY KEY (jogo_id, genero_id),
    FOREIGN KEY (jogo_id) REFERENCES jogos(id),
    FOREIGN KEY (genero_id) REFERENCES generos(id)
);

-- ---------------------------------------------------------------------
-- DADOS INICIAIS: GENEROS
-- ---------------------------------------------------------------------
INSERT INTO generos (id, nome) VALUES
(1, 'Aventura'),
(2, 'Ação'),
(3, 'Plataforma'),
(4, 'RPG'),
(5, 'Simulação'),
(6, 'Quebra-cabeça'),
(7, 'Corrida'),
(8, 'Esporte'),
(9, 'Sandbox'),
(10, 'Roguelike'),
(11, 'Metroidvania'),
(12, 'Indie'),
(13, 'Multiplayer');

-- ---------------------------------------------------------------------
-- DADOS INICIAIS: 12 JOGOS
-- ---------------------------------------------------------------------
INSERT INTO jogos (id, titulo, desenvolvedora, ano_lancamento, descricao, imagem) VALUES
(1, 'Minecraft', 'Mojang Studios', 2011,
 'Jogo de construção em mundo de blocos. O jogador coleta recursos, constrói estruturas e explora cenários gerados de forma aleatória, sozinho ou com amigos.',
 'minecraft.png'),
(2, 'The Legend of Zelda: Breath of the Wild', 'Nintendo EPD', 2017,
 'Aventura em mundo aberto em que Link desperta em Hyrule e pode explorar o reino com grande liberdade, resolvendo desafios e enfrentando a Calamidade Ganon.',
 'zelda-botw.png'),
(3, 'Hollow Knight', 'Team Cherry', 2017,
 'Ação e exploração em 2D no reino subterrâneo de Hallownest, com combate preciso, mapas interligados e chefes desafiadores.',
 'hollow-knight.png'),
(4, 'Celeste', 'Maddy Makes Games', 2018,
 'Jogo de plataforma de precisão em que Madeline escala a montanha Celeste, enfrentando fases difíceis e uma história sobre superação.',
 'celeste.png'),
(5, 'Stardew Valley', 'ConcernedApe', 2016,
 'Simulador de vida no campo: o jogador cuida de uma fazenda, cultiva plantações, cria animais, pesca e constrói amizades com os moradores da cidade.',
 'stardew-valley.png'),
(6, 'Hades', 'Supergiant Games', 2020,
 'Ação roguelike em que Zagreu tenta fugir do Submundo grego. A cada tentativa, o jogador ganha novas armas e poderes e avança na história.',
 'hades.png'),
(7, 'Portal 2', 'Valve', 2011,
 'Jogo de quebra-cabeças em primeira pessoa baseado em portais, que permitem atravessar o cenário e resolver testes cheios de física e humor.',
 'portal-2.png'),
(8, 'Super Mario Odyssey', 'Nintendo EPD', 2017,
 'Aventura de plataforma 3D em que Mario viaja por diversos reinos com a ajuda do chapéu Cappy para recolher Luas de Energia.',
 'mario-odyssey.png'),
(9, 'Undertale', 'Toby Fox', 2015,
 'RPG em que o jogador pode resolver os combates de forma pacífica. As escolhas feitas durante a jornada mudam a história e o final.',
 'undertale.png'),
(10, 'Rocket League', 'Psyonix', 2015,
 'Futebol com carros: partidas rápidas e competitivas em que equipes usam veículos acrobáticos para marcar gols.',
 'rocket-league.png'),
(11, 'Terraria', 'Re-Logic', 2011,
 'Aventura 2D de exploração, construção e combate, em que o jogador cava, fabrica itens e enfrenta chefes em mundos gerados aleatoriamente.',
 'terraria.png'),
(12, 'Mario Kart 8 Deluxe', 'Nintendo EPD', 2017,
 'Jogo de corrida com itens e pistas criativas, que reúne personagens da série Mario em disputas para até vários jogadores.',
 'mario-kart-8-deluxe.png');

-- ---------------------------------------------------------------------
-- DADOS INICIAIS: JOGO x GENERO
-- ---------------------------------------------------------------------
INSERT INTO jogo_genero (jogo_id, genero_id) VALUES
(1, 9), (1, 1),
(2, 1), (2, 2),
(3, 11), (3, 2), (3, 3), (3, 12),
(4, 3), (4, 12),
(5, 5), (5, 4), (5, 12),
(6, 2), (6, 10), (6, 4),
(7, 6), (7, 1),
(8, 3), (8, 1),
(9, 4), (9, 12),
(10, 8), (10, 13),
(11, 9), (11, 1), (11, 2), (11, 12),
(12, 7), (12, 13);

-- ---------------------------------------------------------------------
-- CONSULTAS DE VERIFICACAO
-- ---------------------------------------------------------------------
-- 1) Quantidade de registros (esperado: 12 jogos, 13 generos, 30 ligacoes)
SELECT COUNT(*) AS total_jogos FROM jogos;
SELECT COUNT(*) AS total_generos FROM generos;
SELECT COUNT(*) AS total_ligacoes FROM jogo_genero;

-- 2) Jogos com seus generos (uma linha por ligacao)
SELECT j.id, j.titulo, g.nome AS genero
FROM jogos j
INNER JOIN jogo_genero jg ON jg.jogo_id = j.id
INNER JOIN generos g ON g.id = jg.genero_id
ORDER BY j.id, g.nome;

-- 3) Quantos jogos existem em cada genero
SELECT g.nome AS genero, COUNT(jg.jogo_id) AS total_jogos
FROM generos g
LEFT JOIN jogo_genero jg ON jg.genero_id = g.id
GROUP BY g.nome
ORDER BY total_jogos DESC, g.nome;

-- 4) Jogos sem nenhum genero (esperado: nenhum resultado)
SELECT j.id, j.titulo
FROM jogos j
LEFT JOIN jogo_genero jg ON jg.jogo_id = j.id
WHERE jg.jogo_id IS NULL;
