from langchain_postgres import PGVector

from config import Settings
from embeddings import create_embeddings


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


class SemanticSearchService:
    def __init__(self, model_config):
        self._model_config = model_config
        self._embeddings = create_embeddings(self._model_config)
        self._vectorstore = PGVector(
            embeddings=self._embeddings,
            collection_name=Settings.PG_VECTOR_COLLECTION_NAME,
            connection=Settings.DATABASE_URL,
        )

    def get_retriever(self, search_kwargs={"k": 10}):
        return self._vectorstore.as_retriever(search_kwargs=search_kwargs)