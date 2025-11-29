import os
import argparse
from dotenv import load_dotenv

# Import our core modules
from core.pdf_loader import load_pdf
from core.text_chunker import chunk_text
from core.summarizer_agent import SummarizerAgent
from core.report_builder import ReportBuilder
from core.memory_manager import MemoryManager  # <--- NEW IMPORT
from tools.metadata_fetcher import fetch_metadata

# Load environment variables (API keys)
load_dotenv()

def main():
    # 1. Setup Arguments
    parser = argparse.ArgumentParser(description="AI Research Summarizer Agent")
    parser.add_argument("pdf_path", help="Path to the research paper PDF")
    parser.add_argument("--model", default="gpt-4o", help="LLM model to use")
    parser.add_argument("--chunk_size", type=int, default=2000, help="Token limit per chunk")
    args = parser.parse_args()

    # 2. Check API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in .env file.")
        return

    print(f"📄 Processing: {args.pdf_path}")

    # 3. Load PDF
    try:
        pdf_data = load_pdf(args.pdf_path)
        print(f"✅ Loaded PDF: {pdf_data['total_pages']} pages.")
    except Exception as e:
        print(f"❌ Failed to load PDF: {e}")
        return

    # 4. Fetch Metadata (Tool Call)
    print("🌍 Fetching external metadata...")
    meta = fetch_metadata(pdf_data['metadata'].get('title', ''))
    if meta:
        print(f"   Found: {meta.get('title')} ({meta.get('year')})")
        pdf_data['metadata'].update(meta)
    else:
        print("   No external metadata found. Using PDF internal data.")

    # ---------------------------------------------------------
    # 5. MEMORY CHECK (Agentic Behavior)
    # ---------------------------------------------------------
    memory = MemoryManager()
    paper_title = pdf_data['metadata'].get('title', pdf_data['filename'])
    
    existing_memory = memory.get_similar_papers(paper_title)
    if existing_memory:
        print("\n🧠 MEMORY ACTIVATED: I have read this paper before!")
        print(f"   Stored Summary: {existing_memory.get('summary', 'No summary stored')}")
        print("   Skipping AI processing to save costs.")
        return
    # ---------------------------------------------------------

    # 6. Chunk Text
    print("✂️  Chunking text...")
    chunks = chunk_text(pdf_data['pages'], chunk_size=args.chunk_size)
    print(f"   Created {len(chunks)} chunks.")

    # 7. Summarize (The "Agent" Part)
    agent = SummarizerAgent(model=args.model)
    chunk_summaries = []
    
    print("🤖 Summarizing chunks (this may take a moment)...")
    for i, chunk in enumerate(chunks):
        print(f"   Processing chunk {i+1}/{len(chunks)}...", end="\r")
        summary = agent.summarize_chunk(chunk['text'])
        chunk_summaries.append(summary)
    print("\n✅ Summarization complete.")

    # 8. Build Report
    print("📝 Building final report...")
    builder = ReportBuilder()
    report_path = builder.compile_report(pdf_data['filename'], pdf_data['metadata'], chunk_summaries)
    
    # ---------------------------------------------------------
    # 9. SAVE TO MEMORY
    # ---------------------------------------------------------
    # Construct a lightweight summary for the DB
    full_text_summary = f"Processed on {os.environ.get('OS', 'System')}. Sections found: {len(chunk_summaries)}."
    
    # Try to grab the first chunk's points as a preview
    if chunk_summaries and 'summary_points' in chunk_summaries[0]:
        first_points = " ".join(chunk_summaries[0]['summary_points'][:2])
        full_text_summary = f"{full_text_summary} Preview: {first_points}..."

    memory.add_paper(
        title=paper_title,
        summary=full_text_summary,
        filename=args.pdf_path
    )
    # ---------------------------------------------------------

    print(f"\n🎉 Success! Report saved to: {report_path}")

if __name__ == "__main__":
    main()
