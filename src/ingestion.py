from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector

from config import Settings
from embeddings import create_embeddings
from pdf_reader import load_pdf


class PDFIngestionService:
    def __init__(self):
        self.model_config = Settings.model_config()
        self.embeddings = create_embeddings(self.model_config)

        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=Settings.PG_VECTOR_COLLECTION_NAME,
            connection=Settings.DATABASE_URL,
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
        )

    def ingest(self, pdf_path: str) -> None:
        documents = load_pdf(pdf_path)
        chunks = self.text_splitter.split_documents(documents)

        self.vector_store.add_documents(chunks)