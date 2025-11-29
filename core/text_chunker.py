import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

def chunk_text(pages: list, chunk_size: int = 2000) -> list:
    chunks = []
    accumulated_text = ""
    current_tokens = 0
    start_page = pages[0]['page_num'] if pages else 1
    chunk_id = 0

    for page in pages:
        text = page['text']
        tokens = count_tokens(text)
        
        if current_tokens + tokens > chunk_size:
            chunks.append({
                "chunk_id": chunk_id,
                "text": accumulated_text.strip(),
                "page_start": start_page,
                "page_end": page['page_num'] - 1
            })
            chunk_id += 1
            accumulated_text = text
            current_tokens = tokens
            start_page = page['page_num']
        else:
            accumulated_text += "\n\n" + text
            current_tokens += tokens

    if accumulated_text:
        chunks.append({
            "chunk_id": chunk_id,
            "text": accumulated_text.strip(),
            "page_start": start_page,
            "page_end": pages[-1]['page_num']
        })

    return chunks
