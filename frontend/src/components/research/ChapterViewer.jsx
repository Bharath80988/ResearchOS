import React, { useState } from 'react';
import { BookOpen, Code, Copy, Check, Printer, Presentation, FileSpreadsheet, FileText, ChevronDown, ChevronUp } from 'lucide-react';

export default function ChapterViewer({ report, currentRun }) {
  const [copiedCodeIdx, setCopiedCodeIdx] = useState(null);
  const [collapsedChapters, setCollapsedChapters] = useState({});

  const sections = report?.sections || {};
  const chapters = sections.chapters || [];
  const researchId = currentRun?.id;

  const handleCopy = (codeText, idx) => {
    navigator.clipboard.writeText(codeText);
    setCopiedCodeIdx(idx);
    setTimeout(() => setCopiedCodeIdx(null), 2000);
  };

  const toggleCollapse = (idx) => {
    setCollapsedChapters((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const handleDownload = (format) => {
    if (!researchId) return;
    const url = `/api/research/${researchId}/export/${format}`;
    if (format === 'pdf' || format === 'presentation') {
      window.open(url, '_blank');
    } else {
      window.location.href = url;
    }
  };

  return (
    <div className="chapter-container">
      {/* Deliverable Action Bar */}
      <div className="glass-card" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <span style={{ fontSize: '11px', fontWeight: '800', color: 'var(--accent-primary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            EXPORT PUBLICATION
          </span>
          <h4 style={{ fontSize: '14px', fontWeight: '700', marginTop: '2px' }}>
            Download Research Deliverables
          </h4>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <button className="chip" onClick={() => handleDownload('pdf')} title="Print or Save as Publication PDF">
            <Printer size={14} color="var(--accent-primary)" />
            <span>Print / PDF (Default)</span>
          </button>
          <button className="chip" onClick={() => handleDownload('presentation')} title="Open Animated Slide Presentation">
            <Presentation size={14} color="var(--accent-warning)" />
            <span>PPT Slide Deck</span>
          </button>
          <button className="chip" onClick={() => handleDownload('csv')} title="Download Excel-compatible Evidence CSV">
            <FileSpreadsheet size={14} color="var(--accent-success)" />
            <span>Excel / CSV</span>
          </button>
          <button className="chip" onClick={() => handleDownload('markdown')} title="Download Markdown Document">
            <FileText size={14} color="var(--accent-secondary)" />
            <span>Markdown (.md)</span>
          </button>
        </div>
      </div>

      {/* Chapters Breakdown */}
      {chapters.map((ch, idx) => {
        const isCollapsed = collapsedChapters[idx];
        return (
          <div key={idx} className="chapter-card">
            <div className="chapter-header" onClick={() => toggleCollapse(idx)} style={{ cursor: 'pointer' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{
                  background: 'rgba(99, 102, 241, 0.15)',
                  color: 'var(--accent-primary)',
                  fontWeight: '800',
                  fontSize: '12px',
                  padding: '4px 10px',
                  borderRadius: 'var(--radius-full)'
                }}>
                  CHAPTER {ch.chapter_number || idx + 1}
                </span>
                <h3 style={{ fontSize: '16px', fontWeight: '800', color: '#fff' }}>
                  {ch.title}
                </h3>
              </div>

              <div style={{ color: 'var(--text-dim)' }}>
                {isCollapsed ? <ChevronDown size={18} /> : <ChevronUp size={18} />}
              </div>
            </div>

            {!isCollapsed && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: 1.8, whiteSpace: 'pre-line' }}>
                  {ch.content}
                </p>

                {ch.code_snippet && (
                  <div className="code-block">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', color: 'var(--text-dim)', fontSize: '11px', fontWeight: '700' }}>
                      <span>PYTHON / SYSTEM IMPLEMENTATION</span>
                      <button className="copy-btn" onClick={() => handleCopy(ch.code_snippet, idx)}>
                        {copiedCodeIdx === idx ? (
                          <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#34d399' }}>
                            <Check size={12} /> Copied
                          </span>
                        ) : (
                          <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <Copy size={12} /> Copy Code
                          </span>
                        )}
                      </button>
                    </div>
                    <pre style={{ margin: 0, overflowX: 'auto', lineHeight: 1.5 }}>
                      <code>{ch.code_snippet}</code>
                    </pre>
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
