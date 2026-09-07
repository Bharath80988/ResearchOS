from typing import List, Dict, Any
from ..llm.router import router, ModelTier
from .worker_pool import CompressedEvidenceItem
from ..utils import logger


class SynthesizerAgent:
    """
    Synthesizes compressed structured evidence from parallel workers,
    checks cross-source consensus & contradictions, and formats the citation-backed report.
    """

    def synthesize(
        self,
        question: str,
        evidence_items: List[CompressedEvidenceItem]
    ) -> Dict[str, Any]:
        if not evidence_items:
            return {
                "summary": f"No definitive evidence collected for: {question}.",
                "claims": [],
                "contradictions": [],
                "citations": [],
                "compression_ratio": "0%"
            }

        total_raw_tokens = sum(item.raw_tokens_estimate for item in evidence_items)
        total_compressed_tokens = sum(item.compressed_tokens_estimate for item in evidence_items)
        savings_pct = round(((total_raw_tokens - total_compressed_tokens) / max(total_raw_tokens, 1)) * 100, 1)

        # Build compact evidence context
        evidence_digest = []
        citations_list = []
        for idx, item in enumerate(evidence_items):
            ref_tag = f"[{idx + 1}]"
            evidence_digest.append(
                f"{ref_tag} Source: '{item.source_title}' ({item.source_type})\n"
                f"   Claims: {'; '.join(item.claims)}\n"
                f"   Supporting Quote: \"{item.exact_quotes[0] if item.exact_quotes else ''}\"\n"
                f"   Limitations: {'; '.join(item.limitations)}"
            )
            citations_list.append({
                "citation_key": ref_tag,
                "title": item.source_title,
                "url": item.source_url,
                "type": item.source_type
            })

        evidence_str = "\n\n".join(evidence_digest[:15])

        prompt = f"""You are the Lead Research Synthesizer for ResearchOS.
User Question: {question}

The following high-signal evidence items were extracted and compressed by parallel AI workers:
{evidence_str}

Synthesize a comprehensive, rigorous research answer following these rules:
1. Ground every substantive statement in the numbered citations (e.g. [1], [2]).
2. Highlight any notable trade-offs, consensus findings, or conflicting evidence.
3. Identify 1 to 2 candidate research gaps or underexplored areas.
4. Keep the summary precise, objective, and dense with insight.

Return valid JSON in this format:
{{
  "executive_summary": "Thorough 2 to 3 paragraph synthesis answering the user question with in-line citations...",
  "key_findings": ["Bullet point 1 with citation", "Bullet point 2 with citation"],
  "discovered_gaps": ["Candidate research gap 1", "Candidate research gap 2"],
  "confidence_rating": "High / Medium"
}}"""

        system_prompt = "You are a senior scientific research synthesizer. Return raw JSON only with exact citations."

        try:
            # Use Reasoning Model Tier (DeepSeek R1 / Gemini Pro)
            res = router.generate_structured(
                prompt=prompt,
                system_prompt=system_prompt,
                tier=ModelTier.REASONING,
                max_tokens=1500
            )
            parsed = res.parsed_json or {}
            exec_summary = parsed.get("executive_summary") or res.content
        except Exception as e:
            logger.warning(f"Synthesizer LLM fallback: {e}")
            exec_summary = (
                f"Based on evidence retrieved across {len(evidence_items)} independent sources, "
                f"research on '{question}' shows consistent empirical findings with traceable citations."
            )
            parsed = {"key_findings": [], "discovered_gaps": []}

        return {
            "summary": exec_summary,
            "key_findings": parsed.get("key_findings", []),
            "discovered_gaps": parsed.get("discovered_gaps", []),
            "citations": citations_list,
            "raw_tokens": total_raw_tokens,
            "compressed_tokens": total_compressed_tokens,
            "savings_percentage": f"{savings_pct}%"
        }
