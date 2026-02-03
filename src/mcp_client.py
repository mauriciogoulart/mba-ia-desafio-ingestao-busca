# src/mcp_client.py
import time
from typing import List, Dict, Any
import mcp_server

class MCPClient:
    """
    Um cliente para interagir com as ferramentas definidas no MCP Server.
    Este cliente importa diretamente as funções do servidor para simplificar a comunicação local.
    """

    def __init__(self):
        self._tools = {
            "consultar_partidas": mcp_server.consultar_partidas,
            "consultar_classificacao_time": mcp_server.consultar_classificacao_time,
            "consultar_tabela_campeonato": mcp_server.consultar_tabela_campeonato,
        }
        self._tool_definitions = [
            {
                "name": "consultar_partidas",
                "description": "Retorna todas as partidas de um determinado time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "time": {
                            "type": "string",
                            "description": "O nome do time para consultar as partidas.",
                        }
                    },
                    "required": ["time"],
                },
            },
            {
                "name": "consultar_classificacao_time",
                "description": "Retorna a classificação atual de um determinado time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "time": {
                            "type": "string",
                            "description": "O nome do time para consultar a classificação.",
                        }
                    },
                    "required": ["time"],
                },
            },
            {
                "name": "consultar_tabela_campeonato",
                "description": "Retorna a classificação completa do campeonato.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        ]

    def list_tools(self) -> List[Dict[str, Any]]:
        """Retorna a definição das ferramentas disponíveis."""
        return self._tool_definitions

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Chama uma ferramenta pelo nome com os argumentos fornecidos.

        Args:
            tool_name: O nome da ferramenta a ser chamada.
            arguments: Um dicionário com os argumentos para a ferramenta.

        Returns:
            O resultado da execução da ferramenta.
        """
        if tool_name not in self._tools:
            raise ValueError(f"Ferramenta '{tool_name}' não encontrada.")
        
        tool_function = self._tools[tool_name]
        
        print(f"\n[LOG] Cliente MCP: Chamando ferramenta '{tool_name}' com args: {arguments}")
        start_time = time.time()
        
        result = tool_function(**arguments)

        end_time = time.time()
        print(f"[LOG] Cliente MCP: Ferramenta '{tool_name}' executada em {end_time - start_time:.2f} segundos.")

        return result

if __name__ == '__main__':
    # Exemplo de uso do cliente
    client = MCPClient()
    
    print("Ferramentas disponíveis:")
    print(client.list_tools())
    
    print("\n--- Testando consultar_partidas ---")
    partidas_flamengo = client.call_tool("consultar_partidas", {"time": "Flamengo"})
    print(partidas_flamengo)

    print("\n--- Testando consultar_classificacao_time ---")
    classificacao_palmeiras = client.call_tool("consultar_classificacao_time", {"time": "Palmeiras"})
    print(classificacao_palmeiras)

    print("\n--- Testando consultar_tabela_campeonato ---")
    tabela = client.call_tool("consultar_tabela_campeonato", {{}})
    print(tabela)
