import os
import psycopg
from psycopg.rows import dict_row
try:
    from .models import Partida
except ImportError:
    from models import Partida

class DatabaseManager:
    def __init__(self):
        # Tenta pegar a string de conexão do ambiente, padrão comum em projetos RAG/LangChain
        # Exemplo: postgresql://user:pass@host:port/dbname
        self.conn_str = os.getenv("DATABASE_URL")
        
        # Ajuste: psycopg espera 'postgresql://', mas SQLAlchemy pode usar 'postgresql+psycopg://'
        if self.conn_str and self.conn_str.startswith("postgresql+psycopg://"):
            self.conn_str = self.conn_str.replace("postgresql+psycopg://", "postgresql://")

        if not self.conn_str:
            # Fallback para construção manual se variáveis separadas existirem
            user = os.getenv("POSTGRES_USER", "postgres")
            password = os.getenv("POSTGRES_PASSWORD", "postgres")
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = os.getenv("POSTGRES_PORT", "5432")
            db = os.getenv("POSTGRES_DB", "postgres")
            self.conn_str = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg.connect(self.conn_str, row_factory=dict_row)
            print("Conexão com o banco de dados estabelecida.")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")

    def salvar_partida(self, partida: Partida):
        query = """
            INSERT INTO partidas (campeonato, mandante, visitante, gols_mandante, gols_visitante)
            VALUES (%s, %s, %s, %s, %s)
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (
                partida.campeonato,
                partida.mandante,
                partida.visitante,
                partida.gols_mandante,
                partida.gols_visitante
            ))
            # O commit é feito no final do processo da partida em atualizar_classificacao para atomicidade

    def atualizar_classificacao(self, partida: Partida):
        # Processar Mandante
        self._processar_time(partida.campeonato, partida.mandante, 
                             partida.gols_mandante, partida.gols_visitante)
        # Processar Visitante
        self._processar_time(partida.campeonato, partida.visitante, 
                             partida.gols_visitante, partida.gols_mandante)
        
        self.conn.commit()

    def _processar_time(self, campeonato, time, gols_pro, gols_cedidos):
        vitoria = 1 if gols_pro > gols_cedidos else 0
        empate = 1 if gols_pro == gols_cedidos else 0
        derrota = 1 if gols_pro < gols_cedidos else 0

        with self.conn.cursor() as cur:
            # Verifica se o time já existe na classificação deste campeonato
            cur.execute("SELECT id FROM classificacao WHERE campeonato = %s AND time = %s", (campeonato, time))
            res = cur.fetchone()

            if res:
                # Atualiza
                query = "UPDATE classificacao SET vitorias = vitorias + %s, empates = empates + %s, derrotas = derrotas + %s, gols_pro = gols_pro + %s, gols_cedidos = gols_cedidos + %s WHERE id = %s"
                cur.execute(query, (vitoria, empate, derrota, gols_pro, gols_cedidos, res['id']))
            else:
                # Insere novo
                query = "INSERT INTO classificacao (campeonato, time, vitorias, empates, derrotas, gols_pro, gols_cedidos) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cur.execute(query, (campeonato, time, vitoria, empate, derrota, gols_pro, gols_cedidos))

    def listar_partidas_time(self, time: str):
        query = """
            SELECT * FROM partidas 
            WHERE mandante = %s OR visitante = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (time, time))
            return cur.fetchall()

    def obter_classificacao_time(self, time: str):
        query = "SELECT * FROM classificacao WHERE time = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (time,))
            return cur.fetchone()

    def obter_classificacao_geral(self):
        # Ordenar por pontos (vitorias * 3 + empates) e depois saldo de gols (gols_pro - gols_cedidos)
        query = """
            SELECT *, (vitorias * 3 + empates) as pontos, (gols_pro - gols_cedidos) as saldo_gols 
            FROM classificacao 
            ORDER BY pontos DESC, saldo_gols DESC, gols_pro DESC
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()