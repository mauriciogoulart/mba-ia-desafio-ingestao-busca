# chat_mcp.py
import os
import time
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from src.mcp_client import MCPClient

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração do Cliente MCP e Ferramentas para LangChain ---

# Instanciar o cliente que se conecta ao nosso "servidor" local de ferramentas
mcp_client = MCPClient()

# Usar o decorador @tool do LangChain para expor os métodos do nosso cliente ao Agente
@tool
def consultar_partidas(time: str) -> str:
    """Retorna todas as partidas de um determinado time."""
    print(f"--> Chamando tool 'consultar_partidas' com o time: {time}")
    return mcp_client.call_tool("consultar_partidas", {"time": time})

@tool
def consultar_classificacao_time(time: str) -> str:
    """Retorna a classificação atual de um determinado time."""
    print(f"--> Chamando tool 'consultar_classificacao_time' com o time: {time}")
    return mcp_client.call_tool("consultar_classificacao_time", {"time": time})

@tool
def consultar_tabela_campeonato() -> str:
    """Retorna a classificação completa do campeonato."""
    print("--> Chamando tool 'consultar_tabela_campeonato'")
    return mcp_client.call_tool("consultar_tabela_campeonato", {})


# --- Configuração do Agente com LangChain ---

def create_agent():
    """Cria e configura o agente LangChain para interagir com o usuário e as ferramentas."""

    # 1. Lista de ferramentas que o agente poderá usar
    tools = [consultar_partidas, consultar_classificacao_time, consultar_tabela_campeonato]

    # 2. Modelo de linguagem (LLM)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # 3. Prompt do sistema
    # Define o comportamento do agente, as regras e o que fazer se a pergunta for inválida.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Você é um assistente especializado em informações do campeonato de futebol.
                Sua única função é responder às seguintes perguntas:
                - Todas as partidas de um determinado time.
                - A classificação atual de um determinado time.
                - A classificação completa do campeonato.

                Para isso, você DEVE usar as ferramentas disponíveis.
                
                Se o usuário fizer uma pergunta que não está listada acima ou que não pode ser respondida com as ferramentas,
                você DEVE responder exatamente com a seguinte mensagem, sem adicionar nada mais:
                'Desculpe, só posso fornecer informações sobre partidas e classificações do campeonato. Por favor, escolha uma das perguntas abaixo.'
                """,
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # 4. Criação do agente e do executor
    agent = create_tool_calling_agent(llm, tools, prompt)
    #agent = create_react_agent(llm=llm,tools=tools,prompt=prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor


def main():
    """Função principal para executar o chat."""
    print("Iniciando o Chat de Futebol...")
    agent_executor = create_agent()

    # Mensagem de boas-vindas e menu de perguntas
    welcome_message = """
Bem-vindo ao assistente de informações do campeonato!
Você pode me perguntar sobre:
    - Todas as partidas de um time (ex: 'quais as partidas do Flamengo?')
    - A classificação de um time (ex: 'qual a classificação do Palmeiras?')
    - A classificação geral do campeonato (ex: 'me mostre a tabela do campeonato')

Digite 'sair' a qualquer momento para terminar.
"""
    print(welcome_message)

    # Loop principal do chat
    while True:
        try:
            user_input = input("Você: ")
            if user_input.lower() == 'sair':
                print("Até logo!")
                break
            
            if not user_input.strip():
                continue

            print("\n[LOG] Iniciando chamada ao Agente...")
            start_time = time.time()

            # Invoca o agente com a entrada do usuário
            response = agent_executor.invoke({"input": user_input})
            
            end_time = time.time()
            print(f"[LOG] Chamada ao Agente concluída em {end_time - start_time:.2f} segundos.")
            
            print(f"Assistente: {response['output']}")

        except (KeyboardInterrupt, EOFError):
            print("\nSaindo do chat. Até logo!")
            break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Erro: A variável de ambiente GOOGLE_API_KEY não foi definida.")
        print("Por favor, crie um arquivo .env e adicione a linha: GOOGLE_API_KEY='sua_chave_api'")
    else:
        main()
