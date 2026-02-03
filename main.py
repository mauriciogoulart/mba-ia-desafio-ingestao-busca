import os
from dotenv import load_dotenv
try:
    from .file_reader import JsonFileReader
    from .db_manager import DatabaseManager
    from .models import Partida
except ImportError:
    from file_reader import JsonFileReader
    from db_manager import DatabaseManager
    from models import Partida

# Carrega variáveis de ambiente (do .env na raiz do projeto)
load_dotenv()

def main():
    # Define o caminho do arquivo JSON (assumindo que está na mesma pasta deste script)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'partidas.json')

    print(f"Iniciando processamento. Lendo arquivo: {json_path}")

    reader = JsonFileReader()
    try:
        dados = reader.read(json_path)
    except FileNotFoundError:
        print("Arquivo de dados não encontrado.")
        return

    db = DatabaseManager()
    try:
        db.connect()

        for item in dados:
            partida = Partida(
                campeonato=item.get('campeonato'),
                mandante=item.get('mandante'),
                visitante=item.get('visitante'),
                gols_mandante=item.get('gols_mandante'),
                gols_visitante=item.get('gols_visitante')
            )
            
            print(f"Processando partida: {partida.mandante} {partida.gols_mandante} x {partida.gols_visitante} {partida.visitante}")
            
            db.salvar_partida(partida)
            db.atualizar_classificacao(partida)
            
        print("Processamento concluído com sucesso!")

    finally:
        db.close()

if __name__ == "__main__":
    main()