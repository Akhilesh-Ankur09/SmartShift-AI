from pydub import AudioSegment
import math, tempfile
from typing import List, Tuple


def split_audio_to_chunks(file_path: str, chunk_minutes: int = 5) -> List[Tuple[str, int, int]]:
    """
    Split audio into fixed-length chunks.
    Returns: list of (chunk_file_path, start_ms, end_ms)
    """
    audio = AudioSegment.from_file(file_path)
    chunk_ms = chunk_minutes * 60 * 1000
    duration_ms = len(audio)

    chunks = []
    total = math.ceil(duration_ms / chunk_ms)
    for i in range(total):
        start_ms = i * chunk_ms
        end_ms = min((i + 1) * chunk_ms, duration_ms)
        seg = audio[start_ms:end_ms]
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        seg.export(tmp.name, format="wav")
        chunks.append((tmp.name, start_ms, end_ms))
    return chunks
