import sys
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Settings
from llm import create_llm
from search import PROMPT_TEMPLATE, SemanticSearchService


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


class ChatService:
    def __init__(self):
        self._model_config = Settings.model_config()
        self._llm = create_llm(self._model_config)
        self._search_service = SemanticSearchService(self._model_config)
        self._rag_chain = self._create_rag_chain()

    def _create_rag_chain(self):
        retriever = self._search_service.get_retriever()
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        return (
            {"contexto": retriever | format_docs, "pergunta": RunnablePassthrough()}
            | prompt
            | self._llm
            | StrOutputParser()
        )

    def run(self):
        print("Bem-vindo ao chat! Digite 'sair' para terminar.")
        while True:
            try:
                question = input("Sua pergunta: ")
                if question.lower() == "sair":
                    print("Até logo!")
                    break

                if not question.strip():
                    continue

                print("\nResposta:")
                for chunk in self._rag_chain.stream(question):
                    print(chunk, end="", flush=True)
                print("\n")

            except (KeyboardInterrupt, EOFError):
                print("\n\nAté logo!")
                break


def main():
    chat_service = ChatService()
    chat_service.run()


if __name__ == "__main__":
    main()
