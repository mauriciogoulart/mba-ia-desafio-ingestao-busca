import sys
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_postgres import PGVector

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Settings
from embeddings import create_embeddings
from llm import create_llm
from search import PROMPT_TEMPLATE


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def main():
    model_config = Settings.model_config()
    embeddings = create_embeddings(model_config)
    llm = create_llm(model_config)

    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=Settings.PG_VECTOR_COLLECTION_NAME,
        connection=Settings.DATABASE_URL,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    rag_chain = (
        {"contexto": retriever | format_docs, "pergunta": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

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
            for chunk in rag_chain.stream(question):
                print(chunk, end="", flush=True)
            print("\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\nAté logo!")
            break


if __name__ == "__main__":
    main()
