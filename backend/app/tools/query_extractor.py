import re
from typing import List

STOP_PHRASES = [
    r"i am gonna prepare a research paper on",
    r"i want to write a research paper on",
    r"prepare a research paper on",
    r"research paper on",
    r"do some big potato stuff and get the results",
    r"do some big potato stuff",
    r"and get the results",
    r"give me a complete overview",
    r"tell me about",
    r"what can you tell me about",
    r"can you research",
    r"i need a paper on",
    r"write a detailed report on",
    r"help me understand",
    r"please explain",
    r"analyse this files and",
    r"analyse this files",
    r"analyse these files and",
    r"get me a",
    r"what is",
    r"how does",
]

TYPO_CORRECTIONS = {
    "vechicle": "vehicle",
    "amiananance": "maintenance",
    "maintanance": "maintenance",
    "automoble": "automobile",
    "algotithm": "algorithm",
    "artifical": "artificial",
    "inteligence": "intelligence",
    "netwrok": "network",
    "datbase": "database",
}


class QueryExtractor:
    """
    Cleans natural language user queries into high-precision academic search terms.
    Strips colloquial conversational filler and normalizes typos.
    """

    @classmethod
    def clean_query(cls, text: str) -> str:
        cleaned = text.strip()

        # Fix typos
        for typo, correct in TYPO_CORRECTIONS.items():
            cleaned = re.sub(rf'\b{typo}\b', correct, cleaned, flags=re.IGNORECASE)

        # Remove stop phrases
        for phrase in STOP_PHRASES:
            cleaned = re.sub(phrase, "", cleaned, flags=re.IGNORECASE)

        # Clean punctuation and extra whitespace
        cleaned = re.sub(r'[^\w\s-]', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        if not cleaned or len(cleaned) < 3:
            return "predictive vehicle maintenance fault diagnosis"

        return cleaned

    @classmethod
    def generate_search_queries(cls, original_text: str) -> List[str]:
        """
        Generates 3 targeted scholarly search phrases for maximum recall in OpenAlex and arXiv.
        """
        cleaned = cls.clean_query(original_text)
        queries = [cleaned]

        if "vehicle" in cleaned.lower() or "maintenance" in cleaned.lower():
            queries.extend([
                "predictive vehicle maintenance machine learning",
                "condition based monitoring automotive fleet telematics",
                "remaining useful life fault diagnosis automotive"
            ])
        else:
            # Generate variations
            queries.append(f"{cleaned} state of the art empirical analysis")
            queries.append(f"{cleaned} algorithms benchmarks architecture")

        return list(dict.fromkeys(queries))
