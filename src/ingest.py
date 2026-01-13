import sys
import os
from ingestion import PDFIngestionService
from dotenv import load_dotenv

load_dotenv()


def main():
    pdf_path = os.getenv("PDF_PATH")

    ingestion_service = PDFIngestionService()
    ingestion_service.ingest(pdf_path)

    print("PDF ingestion completed successfully.")


if __name__ == "__main__":
    main()