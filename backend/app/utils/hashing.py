import hashlib

def generate_content_hash(text: str) -> str:
    """Computes SHA-256 hash of raw textual content for deduplication."""
    if not text:
        return ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def generate_query_hash(query: str) -> str:
    """Computes normalized query hash to avoid repeated duplicate searches."""
    normalized = query.strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
