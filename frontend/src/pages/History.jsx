import React from 'react';
import Badge from '../components/common/Badge';
import { Clock, ArrowRight, FolderSearch } from 'lucide-react';

export default function History({ researchHistory = [], onSelectRun }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: '800' }}>Research Workspace History</h2>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            All past deep research investigations, queries, and generated reports.
          </p>
        </div>
        <span style={{ fontSize: '12px', color: 'var(--text-dim)' }}>
          Total runs: {researchHistory.length}
        </span>
      </div>

      {researchHistory.length === 0 ? (
        <div className="glass-card" style={{ padding: '40px', textAlign: 'center' }}>
          <FolderSearch size={36} color="var(--text-dim)" style={{ margin: '0 auto 12px auto' }} />
          <h4 style={{ fontSize: '15px', fontWeight: '600' }}>No Research History Found</h4>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Start a new research investigation in the workstation to view execution logs and evidence here.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {researchHistory.map((run) => (
            <div
              key={run.id}
              className="glass-card"
              style={{
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '16px 20px',
                gap: '16px'
              }}
              onClick={() => onSelectRun(run.id)}
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Badge status={run.status} />
                  <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>
                    {run.created_at ? new Date(run.created_at).toLocaleString() : ''}
                  </span>
                  <span style={{ fontSize: '11px', color: 'var(--accent-primary)' }}>
                    [{run.intent}]
                  </span>
                </div>
                <h4 style={{ fontSize: '14px', fontWeight: '600', color: 'var(--text-primary)' }}>
                  {run.question}
                </h4>
                {run.summary && (
                  <p style={{ fontSize: '12px', color: 'var(--text-muted)', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {run.summary}
                  </p>
                )}
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: 'var(--text-dim)' }}>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)' }}>
                    {run.depth?.toUpperCase()}
                  </div>
                  <div style={{ fontSize: '11px' }}>{run.progress_percentage}% done</div>
                </div>
                <ArrowRight size={16} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
