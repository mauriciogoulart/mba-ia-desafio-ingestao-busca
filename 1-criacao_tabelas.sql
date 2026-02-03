-- Tabela para armazenar o resultado das partidas
CREATE TABLE IF NOT EXISTS partidas (
    id SERIAL PRIMARY KEY,
    campeonato VARCHAR(255) NOT NULL,
    mandante VARCHAR(255) NOT NULL,
    visitante VARCHAR(255) NOT NULL,
    gols_mandante INTEGER NOT NULL,
    gols_visitante INTEGER NOT NULL
);

-- Tabela para armazenar a classificação dos times no campeonato
CREATE TABLE IF NOT EXISTS classificacao (
    id SERIAL PRIMARY KEY,
    campeonato VARCHAR(255) NOT NULL,
    time VARCHAR(255) NOT NULL,
    vitorias INTEGER DEFAULT 0,
    empates INTEGER DEFAULT 0,
    derrotas INTEGER DEFAULT 0,
    gols_pro INTEGER DEFAULT 0,
    gols_cedidos INTEGER DEFAULT 0
);
