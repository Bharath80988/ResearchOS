import React from 'react';
import { Database, FileText, CheckCircle, Download, FileSpreadsheet, Presentation, Printer } from 'lucide-react';

export default function EvidenceViewer({ summary, currentRun }) {
  const researchId = currentRun?.id;

  const handleDownload = (format) => {
    if (!researchId) return;
    const url = `/api/research/${researchId}/export/${format}`;
    if (format === 'pdf') {
      window.open(url, '_blank');
    } else {
      window.location.href = url;
    }
  };

  return (
    <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '14px', height: '100%', overflowY: 'auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
          <Database size={15} color="var(--accent-primary)" />
          <span style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Evidence & Exports
          </span>
        </div>
      </div>

      {/* Export Deliverables Toolbar */}
      {currentRun?.status === 'completed' && (
        <div style={{
          background: 'var(--bg-subtle)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          padding: '12px',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px'
        }}>
          <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-dim)', textTransform: 'uppercase' }}>
            Download Deliverables
          </span>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
            <button
              className="chip"
              onClick={() => handleDownload('pdf')}
              style={{ justifyContent: 'center', padding: '8px 10px' }}
            >
              <Printer size={13} color="var(--accent-primary)" />
              <span>Print / PDF</span>
            </button>
            <button
              className="chip"
              onClick={() => handleDownload('markdown')}
              style={{ justifyContent: 'center', padding: '8px 10px' }}
            >
              <FileText size={13} color="var(--accent-secondary)" />
              <span>Markdown (.md)</span>
            </button>
            <button
              className="chip"
              onClick={() => handleDownload('csv')}
              style={{ justifyContent: 'center', padding: '8px 10px' }}
            >
              <FileSpreadsheet size={13} color="var(--accent-success)" />
              <span>Excel / CSV</span>
            </button>
            <button
              className="chip"
              onClick={() => handleDownload('presentation')}
              style={{ justifyContent: 'center', padding: '8px 10px' }}
            >
              <Presentation size={13} color="var(--accent-warning)" />
              <span>PPT Deck Outline</span>
            </button>
          </div>
        </div>
      )}

      {summary ? (
        <div style={{
          background: 'var(--bg-subtle)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          padding: '14px',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-success)', fontSize: '12px', fontWeight: '600' }}>
            <CheckCircle size={14} />
            <span>Research Synthesis Ready</span>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-primary)', lineHeight: 1.6 }}>
            {summary}
          </p>
        </div>
      ) : (
        <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-dim)', fontSize: '13px' }}>
          Evidence extraction will appear here as multi-AI workers complete their batches.
        </div>
      )}

      {/* Model & Source Attribution Card */}
      <div style={{
        background: 'rgba(99, 102, 241, 0.05)',
        border: '1px solid rgba(99, 102, 241, 0.15)',
        borderRadius: 'var(--radius-md)',
        padding: '12px',
        fontSize: '12px',
        color: 'var(--text-secondary)',
        lineHeight: 1.5
      }}>
        <div style={{ fontWeight: '600', color: 'var(--accent-primary)', marginBottom: '4px' }}>
          Multi-AI Provenance Architecture
        </div>
        Head AI (Gemini / DeepSeek) plans and synthesizes, while parallel workers (Groq, DeepSeek, HF) extract evidence concurrently, saving over 85% in tokens.
      </div>
    </div>
  );
}
