import time
from mcp.server.fastmcp import FastMCP
try:
    from .db_manager import DatabaseManager
except ImportError:
    from db_manager import DatabaseManager

# Inicializa o servidor MCP
mcp = FastMCP("FutebolStats")

def get_db():
    db = DatabaseManager()
    db.connect()
    return db

@mcp.tool()
def consultar_partidas(time: str):
    """Retorna todas as partidas de um determinado time."""
    db = get_db()
    try:
        print(f"\n[LOG] Servidor MCP: Consultando DB para partidas do time '{time}'...")
        start_time = time.time()
        partidas = db.listar_partidas_time(time)
        end_time = time.time()
        print(f"[LOG] Servidor MCP: Consulta ao DB (partidas) finalizada em {end_time - start_time:.2f} segundos.")
        return str(partidas)
    finally:
        db.close()

@mcp.tool()
def consultar_classificacao_time(time: str):
    """Retorna a classificação atual de um determinado time."""
    db = get_db()
    try:
        print(f"\n[LOG] Servidor MCP: Consultando DB para classificação do time '{time}'...")
        start_time = time.time()
        classificacao = db.obter_classificacao_time(time)
        end_time = time.time()
        print(f"[LOG] Servidor MCP: Consulta ao DB (classificação) finalizada em {end_time - start_time:.2f} segundos.")
        if not classificacao:
            return f"Time {time} não encontrado na classificação."
        return classificacao
    finally:
        db.close()

@mcp.tool()
def consultar_tabela_campeonato():
    """Retorna a classificação completa do campeonato."""
    db = get_db()
    try:
        print(f"\n[LOG] Servidor MCP: Consultando DB para tabela completa...")
        start_time = time.time()
        tabela = db.obter_classificacao_geral()
        end_time = time.time()
        print(f"[LOG] Servidor MCP: Consulta ao DB (tabela) finalizada em {end_time - start_time:.2f} segundos.")
        return tabela
    finally:
        db.close()

if __name__ == "__main__":
    # Permite rodar o servidor diretamente
    mcp.run()
