import os
from dotenv import load_dotenv

# 1. LOAD ENV VARS FIRST
load_dotenv()

import argparse
from core.pdf_loader import load_pdf
from core.text_chunker import chunk_text
from core.summarizer_agent import SummarizerAgent
from core.report_builder import ReportBuilder
from core.memory_manager import MemoryManager
from tools.metadata_fetcher import fetch_metadata

def main():
    parser = argparse.ArgumentParser(description="AI Research Summarizer Agent")
    parser.add_argument("pdf_path", help="Path to the research paper PDF")
    # Change default model to Gemini
    parser.add_argument("--model", default="gemini-1.5-flash", help="LLM model to use")
    parser.add_argument("--chunk_size", type=int, default=2000, help="Token limit per chunk")
    args = parser.parse_args()

    # --- CHANGED: Check for GOOGLE Key instead of OpenAI ---
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in .env file.")
        print("   Please ensure your .env file has GOOGLE_API_KEY=AIzaSy...")
        return
    # -----------------------------------------------------

    print(f"📄 Processing: {args.pdf_path}")

    # Load PDF
    try:
        pdf_data = load_pdf(args.pdf_path)
        if not pdf_data:
            print("❌ Failed to read PDF text.")
            return
        print(f"✅ Loaded PDF: {pdf_data['total_pages']} pages.")
    except Exception as e:
        print(f"❌ Failed to load PDF: {e}")
        return

    # Fetch Metadata
    print("🌍 Fetching external metadata...")
    meta = fetch_metadata(pdf_data['metadata'].get('title', ''))
    if meta:
        print(f"   Found: {meta.get('title')} ({meta.get('year')})")
        pdf_data['metadata'].update(meta)
    else:
        print("   No external metadata found.")

    # Memory Check
    memory = MemoryManager()
    paper_title = pdf_data['metadata'].get('title', pdf_data['filename'])
    existing_memory = memory.get_similar_papers(paper_title)
    if existing_memory:
        print("\n🧠 MEMORY ACTIVATED: I have read this paper before!")
        print(f"   Stored Summary: {existing_memory.get('summary', 'No summary stored')}")
        return

    # Chunk Text
    print("✂️  Chunking text...")
    chunks = chunk_text(pdf_data['pages'], chunk_size=args.chunk_size)
    print(f"   Created {len(chunks)} chunks.")

    # Summarize
    agent = SummarizerAgent(model=args.model)
    chunk_summaries = []
    
    print("🤖 Summarizing chunks with Google Gemini...")
    for i, chunk in enumerate(chunks):
        print(f"   Processing chunk {i+1}/{len(chunks)}...", end="\r")
        summary = agent.summarize_chunk(chunk['text'])
        chunk_summaries.append(summary)
    print("\n✅ Summarization complete.")

    # Build Report
    print("📝 Building final report...")
    builder = ReportBuilder()
    report_path = builder.compile_report(pdf_data['filename'], pdf_data['metadata'], chunk_summaries)
    
    # Save to Memory
    full_text_summary = f"Processed on {os.environ.get('OS', 'System')}. Sections: {len(chunk_summaries)}."
    if chunk_summaries and 'summary_points' in chunk_summaries[0]:
        first_points = " ".join(chunk_summaries[0]['summary_points'][:2])
        full_text_summary = f"{full_text_summary} Preview: {first_points}..."

    memory.add_paper(
        title=paper_title,
        summary=full_text_summary,
        filename=args.pdf_path
    )

    print(f"\n🎉 Success! Report saved to: {report_path}")

if __name__ == "__main__":
    main()