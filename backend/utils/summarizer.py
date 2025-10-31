from transformers import pipeline

# Initialize summarization pipeline (loads once)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_text(text: str, max_length: int = 200) -> str:
    """
    Generate a concise summary of a transcript.
    Handles long text by chunking automatically.
    """
    if not text or len(text.split()) < 50:
        return "Transcript too short for summarization."

    # Break long transcripts into chunks
    chunks = []
    words = text.split()
    chunk_size = 700
    for i in range(0, len(words), chunk_size):
        part = " ".join(words[i:i + chunk_size])
        result = summarizer(part, max_length=max_length, min_length=60, do_sample=False)
        chunks.append(result[0]["summary_text"])

    return " ".join(chunks)
