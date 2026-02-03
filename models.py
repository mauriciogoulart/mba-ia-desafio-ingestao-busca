from dataclasses import dataclass

@dataclass
class Partida:
    campeonato: str
    mandante: str
    visitante: str
    gols_mandante: int
    gols_visitante: int

@dataclass
class Classificacao:
    campeonato: str
    time: str
    vitorias: int = 0
    empates: int = 0
    derrotas: int = 0
    gols_pro: int = 0
    gols_cedidos: int = 0