import React from 'react';
import Badge from '../components/common/Badge';
import { BookOpen, ArrowRight, FolderSearch, Trash2, Printer, Presentation, FileSpreadsheet, FileText } from 'lucide-react';

export default function History({ researchHistory = [], onSelectRun, onDeleteRun }) {
  const handleDownload = (e, runId, format) => {
    e.stopPropagation();
    const url = `/api/research/${runId}/export/${format}`;
    if (format === 'pdf' || format === 'presentation') {
      window.open(url, '_blank');
    } else {
      window.location.href = url;
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: '800' }}>Research Library & Publications</h2>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            All past deep research inquiries, chapter reports, and downloadable deliverables.
          </p>
        </div>
        <span style={{ fontSize: '12px', color: 'var(--text-dim)', fontWeight: '700' }}>
          {researchHistory.length} Publications
        </span>
      </div>

      {researchHistory.length === 0 ? (
        <div className="glass-card" style={{ padding: '50px 20px', textAlign: 'center' }}>
          <FolderSearch size={40} color="var(--text-dim)" style={{ margin: '0 auto 12px auto' }} />
          <h4 style={{ fontSize: '16px', fontWeight: '700' }}>Library is Empty</h4>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Start a new research inquiry in the canvas to generate chapter reports and export deliverables here.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {researchHistory.map((run) => (
            <div
              key={run.id}
              className="glass-card"
              style={{
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
                padding: '18px 22px',
                transition: 'all 0.2s ease'
              }}
              onClick={() => onSelectRun(run.id)}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Badge status={run.status} />
                  <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>
                    {run.created_at ? new Date(run.created_at).toLocaleString() : ''}
                  </span>
                  <span style={{ fontSize: '11px', color: 'var(--accent-primary)', fontWeight: '700' }}>
                    [{run.depth?.toUpperCase()}]
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  {run.status === 'completed' && (
                    <>
                      <button
                        className="chip"
                        onClick={(e) => handleDownload(e, run.id, 'pdf')}
                        title="Print / Save PDF"
                        style={{ padding: '3px 8px', fontSize: '11px' }}
                      >
                        <Printer size={12} color="var(--accent-primary)" />
                        <span>PDF</span>
                      </button>
                      <button
                        className="chip"
                        onClick={(e) => handleDownload(e, run.id, 'presentation')}
                        title="PPT Deck"
                        style={{ padding: '3px 8px', fontSize: '11px' }}
                      >
                        <Presentation size={12} color="var(--accent-warning)" />
                        <span>PPT</span>
                      </button>
                      <button
                        className="chip"
                        onClick={(e) => handleDownload(e, run.id, 'csv')}
                        title="CSV Evidence Ledger"
                        style={{ padding: '3px 8px', fontSize: '11px' }}
                      >
                        <FileSpreadsheet size={12} color="var(--accent-success)" />
                        <span>CSV</span>
                      </button>
                    </>
                  )}

                  {onDeleteRun && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        if (confirm('Delete this publication?')) onDeleteRun(run.id);
                      }}
                      style={{
                        background: 'transparent',
                        border: 'none',
                        color: 'var(--text-dim)',
                        cursor: 'pointer',
                        padding: '4px'
                      }}
                      title="Delete publication"
                    >
                      <Trash2 size={14} />
                    </button>
                  )}
                </div>
              </div>

              <h3 style={{ fontSize: '15px', fontWeight: '800', color: '#fff' }}>
                {run.question}
              </h3>

              {run.summary && (
                <p style={{
                  fontSize: '13px',
                  color: 'var(--text-secondary)',
                  lineHeight: 1.6,
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden'
                }}>
                  {run.summary}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
