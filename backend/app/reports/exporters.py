import csv
import io
import json
from typing import Dict, Any, List


class ReportExporter:
    """
    Generates structured export deliverables for ResearchOS:
    - Markdown Research Document
    - Printable PDF / HTML
    - Standalone Animated Presentation Deck (HTML Presentation Player with fullscreen & slide transitions)
    - Excel / CSV Evidence Ledger
    """

    @classmethod
    def to_markdown(cls, question: str, summary: str, citations: List[Dict[str, Any]], chapters: List[Dict[str, Any]] = None, findings: List[str] = None, gaps: List[str] = None) -> str:
        md = []
        md.append(f"# {question}\n\n")
        md.append(f"**ResearchOS Multi-Agent Deep Research Publication**\n\n---\n\n")
        md.append("## Executive Summary\n\n")
        md.append(f"{summary}\n\n---\n\n")

        if chapters:
            for ch in chapters:
                c_num = ch.get("chapter_number", "")
                c_title = ch.get("title", "")
                c_content = ch.get("content", "")
                c_code = ch.get("code_snippet")
                c_lang = ch.get("code_language", "python")
                md.append(f"## Chapter {c_num}: {c_title}\n\n{c_content}\n\n")
                if c_code:
                    md.append(f"```{c_lang}\n{c_code}\n```\n\n")

        if findings:
            md.append("## Key Verified Findings\n\n")
            for f in findings:
                md.append(f"- {f}\n")
            md.append("\n")

        if gaps:
            md.append("## Candidate Research Gaps & Future Directions\n\n")
            for g in gaps:
                md.append(f"- **[Candidate Gap]** {g}\n")
            md.append("\n")

        if citations:
            md.append("## Traceable Citations & Evidence Ledger\n\n")
            for c in citations:
                tag = c.get("citation_key", "[1]")
                title = c.get("title", "Untitled Source")
                url = c.get("url", "")
                stype = c.get("type", "academic")
                md.append(f"{tag} **{title}** ({stype.upper()})  \n  URL: [{url}]({url})\n\n")

        return "".join(md)

    @classmethod
    def to_csv_evidence_ledger(cls, question: str, citations: List[Dict[str, Any]], findings: List[str] = None) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Citation Tag", "Source Title", "Source URL", "Domain / Type", "Status", "Verification Scope"])

        for c in (citations or []):
            writer.writerow([
                c.get("citation_key", "[1]"),
                c.get("title", ""),
                c.get("url", ""),
                c.get("type", "web"),
                "Verified",
                f"Grounding for inquiry: {question[:50]}"
            ])
        return output.getvalue()

    @classmethod
    def to_animated_presentation_html(cls, question: str, summary: str, chapters: List[Dict[str, Any]] = None, findings: List[str] = None, gaps: List[str] = None) -> str:
        """Generates a standalone, beautiful HTML presentation deck with keyboard slide navigation and animations."""
        slides_data = [
            {
                "title": question,
                "subtitle": "ResearchOS Autonomous Multi-Agent Synthesis",
                "badge": "TITLE SLIDE",
                "body": f"<p style='font-size: 1.2rem; color: #cbd5e1; line-height: 1.6;'>Comprehensive Deep Research Publication</p>"
            },
            {
                "title": "Executive Summary",
                "badge": "OVERVIEW",
                "body": f"<p style='font-size: 1.1rem; line-height: 1.7; color: #f1f5f9;'>{summary[:450]}...</p>"
            }
        ]

        if chapters:
            for ch in chapters:
                c_title = ch.get("title", "")
                c_content = ch.get("content", "")[:320]
                c_code = ch.get("code_snippet")
                code_html = f"<pre style='background:#0f172a; padding:12px; border-radius:8px; font-size:0.85rem; color:#38bdf8; overflow-x:auto;'><code>{c_code[:250]}...</code></pre>" if c_code else ""
                slides_data.append({
                    "title": f"Chapter {ch.get('chapter_number')}: {c_title}",
                    "badge": "CHAPTER",
                    "body": f"<p style='font-size: 1.05rem; line-height: 1.6; margin-bottom: 12px;'>{c_content}...</p>{code_html}"
                })

        if findings:
            findings_bullets = "".join([f"<li style='margin-bottom: 10px;'>{f}</li>" for f in findings[:4]])
            slides_data.append({
                "title": "Empirical Findings & Evidence",
                "badge": "KEY FINDINGS",
                "body": f"<ul style='font-size: 1.1rem; line-height: 1.6;'>{findings_bullets}</ul>"
            })

        if gaps:
            gaps_bullets = "".join([f"<li style='margin-bottom: 10px;'>{g}</li>" for g in gaps[:3]])
            slides_data.append({
                "title": "Candidate Research Gaps & Novel Directions",
                "badge": "FUTURE WORK",
                "body": f"<ul style='font-size: 1.1rem; line-height: 1.6; color:#a5b4fc;'>{gaps_bullets}</ul>"
            })

        slides_json = json.dumps(slides_data)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Presentation: {question}</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: #090d16;
            color: #f8fafc;
            font-family: 'Plus Jakarta Sans', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
        }}
        .deck-container {{
            width: 90vw;
            max-width: 1000px;
            height: 75vh;
            background: rgba(18, 24, 38, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 30px rgba(99, 102, 241, 0.2);
            display: flex;
            flex-direction: column;
            padding: 40px;
            position: relative;
            backdrop-filter: blur(20px);
        }}
        .slide-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }}
        .badge {{ background: rgba(99, 102, 241, 0.2); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.4); padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 800; }}
        .slide-title {{ font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }}
        .slide-content {{ flex: 1; overflow-y: auto; line-height: 1.7; }}
        .slide-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 16px; font-size: 0.85rem; color: #64748b; }}
        .nav-btn {{ background: #6366f1; color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; margin-left: 8px; }}
        .nav-btn:hover {{ background: #4f46e5; }}
    </style>
</head>
<body>
    <div class="deck-container">
        <div class="slide-header">
            <span class="badge" id="slideBadge">SLIDE 1</span>
            <span id="slideCounter" style="color: #64748b; font-weight: 600;">1 / {len(slides_data)}</span>
        </div>
        <h2 class="slide-title" id="slideTitle">Loading...</h2>
        <div class="slide-content" id="slideBody"></div>
        <div class="slide-footer">
            <span>ResearchOS Presentation Player • Use Left / Right arrows</span>
            <div>
                <button class="nav-btn" onclick="prevSlide()">Previous</button>
                <button class="nav-btn" onclick="nextSlide()">Next</button>
            </div>
        </div>
    </div>

    <script>
        const slides = {slides_json};
        let currentIdx = 0;

        function renderSlide() {{
            const s = slides[currentIdx];
            document.getElementById('slideBadge').innerText = s.badge || `SLIDE ${{currentIdx + 1}}`;
            document.getElementById('slideCounter').innerText = `${{currentIdx + 1}} / ${{slides.length}}`;
            document.getElementById('slideTitle').innerText = s.title;
            document.getElementById('slideBody').innerHTML = s.body;
        }}

        function nextSlide() {{
            if (currentIdx < slides.length - 1) {{
                currentIdx++;
                renderSlide();
            }}
        }}

        function prevSlide() {{
            if (currentIdx > 0) {{
                currentIdx--;
                renderSlide();
            }}
        }}

        window.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === 'Space') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
        }});

        renderSlide();
    </script>
</body>
</html>"""

    @classmethod
    def to_printable_html(cls, question: str, summary: str, citations: List[Dict[str, Any]], chapters: List[Dict[str, Any]] = None, findings: List[str] = None) -> str:
        """Generates an elegant, publication-grade printable research paper / PDF."""
        chapters_html = ""
        if chapters:
            for ch in chapters:
                c_num = ch.get("chapter_number", "")
                c_title = ch.get("title", "")
                c_content = ch.get("content", "")
                c_code = ch.get("code_snippet")
                code_block = f"<pre style='background:#f1f5f9; padding:12px; border-radius:6px; font-family:monospace; font-size:12px; overflow-x:auto;'><code>{c_code}</code></pre>" if c_code else ""
                chapters_html += f"<h2>Chapter {c_num}: {c_title}</h2><p>{c_content}</p>{code_block}"

        findings_html = "".join([f"<li>{f}</li>" for f in (findings or [])])
        citations_html = "".join([
            f"<tr><td><strong>{c.get('citation_key')}</strong></td><td>{c.get('title')}</td><td><a href='{c.get('url')}' target='_blank'>{c.get('url')}</a></td><td>{c.get('type')}</td></tr>"
            for c in (citations or [])
        ])

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ResearchOS Publication - {question}</title>
    <style>
        body {{ font-family: 'Georgia', 'Times New Roman', serif; padding: 50px; color: #0f172a; line-height: 1.8; max-width: 850px; margin: 0 auto; }}
        h1 {{ font-family: 'Helvetica Neue', Arial, sans-serif; color: #0f172a; border-bottom: 3px solid #6366f1; padding-bottom: 12px; font-size: 26px; }}
        h2 {{ font-family: 'Helvetica Neue', Arial, sans-serif; color: #1e293b; margin-top: 30px; font-size: 19px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }}
        p {{ margin-bottom: 16px; text-align: justify; }}
        .badge {{ font-family: sans-serif; background: #e0e7ff; color: #4338ca; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
        .summary-box {{ background: #f8fafc; border-left: 4px solid #6366f1; padding: 20px; margin: 24px 0; border-radius: 6px; font-family: sans-serif; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; font-family: sans-serif; font-size: 13px; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 10px 14px; text-align: left; }}
        th {{ background: #f1f5f9; }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="no-print" style="margin-bottom: 24px; display: flex; justify-content: flex-end;">
        <button onclick="window.print()" style="background: #6366f1; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-family: sans-serif; font-weight: bold;">
            Print / Save as PDF
        </button>
    </div>
    <h1>{question}</h1>
    <div style="margin: 12px 0;"><span class="badge">ResearchOS Multi-AI Publication</span></div>
    <div class="summary-box">
        <h3 style="margin-top:0; color:#4338ca;">Executive Summary</h3>
        <p>{summary}</p>
    </div>
    {chapters_html}
    <h2>Key Verified Findings</h2>
    <ul style="font-family:sans-serif; margin-left:20px;">{findings_html}</ul>
    <h2>Traceable Evidence Sources & Citations</h2>
    <table>
        <thead>
            <tr><th>Tag</th><th>Source Title</th><th>Link</th><th>Type</th></tr>
        </thead>
        <tbody>
            {citations_html}
        </tbody>
    </table>
</body>
</html>"""
