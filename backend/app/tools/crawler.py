import re
import html
import httpx
from typing import Optional
from urllib.parse import urlparse
from ..config import get_settings
from ..utils import logger, generate_content_hash

settings = get_settings()


class WebCrawler:
    """
    Lightweight, noise-stripping web crawler that removes headers, footers,
    navigation scripts, and ads to minimize raw token size.
    """

    HEADERS = {
        "User-Agent": settings.CRAWL_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    @classmethod
    def clean_html(cls, html_content: str) -> str:
        """Strips scripts, styles, navigations, and collapses whitespace."""
        if not html_content:
            return ""

        # Remove script and style tags
        cleaned = re.sub(r"<(script|style|nav|footer|header|aside|noscript)[^>]*>.*?</\1>", " ", html_content, flags=re.DOTALL | re.IGNORECASE)
        # Remove remaining HTML tags
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)
        # Unescape HTML entities
        cleaned = html.unescape(cleaned)
        # Normalize whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    @classmethod
    def crawl_url(cls, url: str) -> Optional[str]:
        """Fetches and cleans page text."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return None

            # Prevent SSRF to local network
            if parsed.netloc.startswith("127.") or parsed.netloc.startswith("localhost") or parsed.netloc.startswith("192.168."):
                return None

            with httpx.Client(timeout=settings.CRAWL_TIMEOUT_SECONDS, follow_redirects=True, headers=cls.HEADERS) as client:
                res = client.get(url)
                if res.status_code == 200:
                    cleaned_text = cls.clean_html(res.text)
                    # Limit raw page content to reasonable maximum to protect context window
                    return cleaned_text[:8000]
        except Exception as e:
            logger.debug(f"Crawler failed to fetch {url}: {e}")
            return None
        return None
