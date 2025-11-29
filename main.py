import os
import argparse
from dotenv import load_dotenv
from core.pdf_loader import load_pdf
from core.text_chunker import chunk_text
from core.summarizer_agent import SummarizerAgent
from core.report_builder import ReportBuilder
from tools.metadata_fetcher import fetch_metadata

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY in .env file")
        return

    print("Loading PDF...")
    pdf_data = load_pdf(args.pdf_path)
    
    print("Fetching Metadata...")
    meta = fetch_metadata(pdf_data['metadata'].get('title', ''))
    if meta: pdf_data['metadata'].update(meta)

    print("Chunking...")
    chunks = chunk_text(pdf_data['pages'])

    print("Summarizing...")
    agent = SummarizerAgent()
    summaries = [agent.summarize_chunk(c['text']) for c in chunks]

    print("Building Report...")
    builder = ReportBuilder()
    path = builder.compile_report(pdf_data['filename'], pdf_data['metadata'], summaries)
    print(f"Done! Report at: {path}")

if __name__ == "__main__":
    main()
