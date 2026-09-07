import React from 'react';
import { Compass, Clock, FolderGit2, Bookmark, PlusCircle } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, researchHistory = [], onSelectRun, currentRunId }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo-badge">R</div>
        <div>
          <h1 style={{ fontSize: '15px', fontWeight: '800', letterSpacing: '-0.02em' }}>ResearchOS</h1>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Deep Research Engine</p>
        </div>
      </div>

      <div className="sidebar-nav">
        <button
          className={`nav-item ${activeTab === 'workspace' ? 'active' : ''}`}
          onClick={() => setActiveTab('workspace')}
        >
          <Compass size={18} />
          <span>New Research</span>
        </button>

        <button
          className={`nav-item ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          <Clock size={18} />
          <span>Research History</span>
        </button>

        <div style={{ marginTop: '20px', padding: '0 8px', marginBottom: '8px' }}>
          <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Recent Inquiries
          </span>
        </div>

        {researchHistory.length === 0 ? (
          <div style={{ padding: '12px', fontSize: '12px', color: 'var(--text-dim)', textAlign: 'center' }}>
            No research runs yet
          </div>
        ) : (
          researchHistory.slice(0, 8).map((run) => (
            <div
              key={run.id}
              onClick={() => onSelectRun(run.id)}
              style={{
                padding: '8px 10px',
                borderRadius: 'var(--radius-md)',
                cursor: 'pointer',
                fontSize: '13px',
                color: currentRunId === run.id ? 'var(--text-primary)' : 'var(--text-secondary)',
                background: currentRunId === run.id ? 'var(--bg-subtle)' : 'transparent',
                border: currentRunId === run.id ? '1px solid var(--border-active)' : '1px solid transparent',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                transition: 'all 0.2s ease'
              }}
              title={run.question}
            >
              {run.question}
            </div>
          ))
        )}
      </div>

      <div style={{ padding: '16px', borderTop: '1px solid var(--border-subtle)', fontSize: '11px', color: 'var(--text-dim)' }}>
        ResearchOS v1.0 • Phase 1
      </div>
    </aside>
  );
}
