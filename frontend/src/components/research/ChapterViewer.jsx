import React, { useState } from 'react';
import { BookOpen, Code, Copy, Check, Printer, Presentation, FileSpreadsheet, FileText, ChevronDown, ChevronUp, Award, CheckCircle2 } from 'lucide-react';

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
      <div className="glass-card" style={{ padding: '18px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '2px' }}>
            <Award size={14} color="var(--accent-primary)" />
            <span style={{ fontSize: '11px', fontWeight: '800', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              RESEARCH DELIVERABLES & EXPORTS
            </span>
          </div>
          <h3 style={{ fontSize: '15px', fontWeight: '800', color: '#ffffff' }}>
            Download Multi-Format Deliverables
          </h3>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <button type="button" className="chip active" onClick={() => handleDownload('pdf')} title="Print or Save as Publication PDF">
            <Printer size={15} color="#ffffff" />
            <span>Print / PDF</span>
          </button>
          <button type="button" className="chip" onClick={() => handleDownload('presentation')} title="Open Animated Slide Presentation">
            <Presentation size={15} color="var(--accent-warning)" />
            <span>PPT Slides</span>
          </button>
          <button type="button" className="chip" onClick={() => handleDownload('csv')} title="Download Excel Evidence Ledger">
            <FileSpreadsheet size={15} color="var(--accent-success)" />
            <span>Excel / CSV</span>
          </button>
          <button type="button" className="chip" onClick={() => handleDownload('markdown')} title="Download Full Markdown">
            <FileText size={15} color="var(--accent-secondary)" />
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
                  background: 'rgba(99, 102, 241, 0.2)',
                  color: '#a5b4fc',
                  fontWeight: '800',
                  fontSize: '12px',
                  padding: '5px 12px',
                  borderRadius: 'var(--radius-full)',
                  border: '1px solid rgba(99, 102, 241, 0.4)'
                }}>
                  CHAPTER {ch.chapter_number || idx + 1}
                </span>
                <h3 style={{ fontSize: '16.5px', fontWeight: '800', color: '#ffffff' }}>
                  {ch.title}
                </h3>
              </div>

              <div style={{ color: '#94a3b8' }}>
                {isCollapsed ? <ChevronDown size={20} /> : <ChevronUp size={20} />}
              </div>
            </div>

            {!isCollapsed && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div style={{ fontSize: '14.5px', color: '#f1f5f9', lineHeight: 1.8, whiteSpace: 'pre-line' }}>
                  {ch.content}
                </div>

                {ch.code_snippet && (
                  <div className="code-block">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px', color: '#94a3b8', fontSize: '11.5px', fontWeight: '700' }}>
                      <span style={{ color: '#38bdf8' }}>PYTHON / EXECUTION SCRIPT</span>
                      <button type="button" className="copy-btn" onClick={() => handleCopy(ch.code_snippet, idx)}>
                        {copiedCodeIdx === idx ? (
                          <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#34d399' }}>
                            <Check size={13} /> Copied
                          </span>
                        ) : (
                          <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <Copy size={13} /> Copy Code
                          </span>
                        )}
                      </button>
                    </div>
                    <pre style={{ margin: 0, overflowX: 'auto', lineHeight: 1.6, color: '#67e8f9' }}>
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
