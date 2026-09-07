import base64
import io
import re
from typing import Optional, List, Dict
from pypdf import PdfReader
from ..utils import logger


class PDFParser:
    """
    Robust PDF parser for marksheets, transcripts, research papers, and technical reports.
    Extracts structured page-by-page text and tabular data.
    """

    @classmethod
    def extract_text_from_base64_or_raw(cls, content_str: str, filename: str = "") -> str:
        """
        Handles base64 encoded PDF data (data:application/pdf;base64,...) or raw string content.
        """
        if not content_str:
            return ""

        # Check if content is base64 encoded
        if "base64," in content_str:
            try:
                base64_data = content_str.split("base64,")[1]
                pdf_bytes = base64.b64decode(base64_data)
                return cls.extract_from_bytes(pdf_bytes, filename)
            except Exception as e:
                logger.warning(f"Failed to parse base64 PDF {filename}: {e}")

        # If it looks like base64 without prefix
        if len(content_str) > 100 and not content_str.startswith("%PDF") and re.match(r'^[A-Za-z0-9+/=\r\n]+$', content_str[:200]):
            try:
                pdf_bytes = base64.b64decode(content_str)
                if pdf_bytes.startswith(b"%PDF"):
                    return cls.extract_from_bytes(pdf_bytes, filename)
            except Exception:
                pass

        # If it's already plain text
        return content_str

    @classmethod
    def extract_from_bytes(cls, pdf_bytes: bytes, filename: str = "") -> str:
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            pages_text = []
            for page_num, page in enumerate(reader.pages):
                txt = page.extract_text() or ""
                if txt.strip():
                    pages_text.append(f"--- [Page {page_num + 1} of {filename}] ---\n{txt}")
            extracted = "\n\n".join(pages_text)
            logger.info(f"Successfully extracted {len(reader.pages)} pages ({len(extracted)} chars) from {filename}")
            return extracted
        except Exception as e:
            logger.error(f"Error reading PDF bytes for {filename}: {e}")
            return ""
