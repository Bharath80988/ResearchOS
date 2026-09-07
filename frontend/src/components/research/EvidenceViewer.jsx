import React from 'react';
import { Database, FileText, CheckCircle, ExternalLink } from 'lucide-react';

export default function EvidenceViewer({ summary, currentRun }) {
  return (
    <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '14px', height: '100%', overflowY: 'auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
        <Database size={15} color="var(--accent-primary)" />
        <span style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Evidence Ledger & Traceability
        </span>
      </div>

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
          Evidence extraction will appear here as research progresses.
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
          Provenance & Verification Note
        </div>
        Every factual claim in ResearchOS is mapped directly to underlying document chunks and DOI/URL references with calculated confidence scores.
      </div>
    </div>
  );
}
