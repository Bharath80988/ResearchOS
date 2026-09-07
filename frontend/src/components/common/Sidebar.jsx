import React, { useState } from 'react';
import { Compass, BookOpen, Clock, Plus, Trash2, Search, Palette } from 'lucide-react';

export default function Sidebar({
  activeTab,
  setActiveTab,
  researchHistory = [],
  onSelectRun,
  onDeleteRun,
  currentRunId,
  theme,
  setTheme
}) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredHistory = researchHistory.filter((r) =>
    (r.question || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo-badge">R</div>
        <div>
          <h1 style={{ fontSize: '15px', fontWeight: '800', letterSpacing: '-0.02em' }}>ResearchOS</h1>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Multi-AI Workstation</p>
        </div>
      </div>

      {/* New Research Button */}
      <button
        className="new-chat-btn"
        onClick={() => {
          setActiveTab('workspace');
          onSelectRun(null);
        }}
      >
        <Plus size={16} />
        <span>New Research</span>
      </button>

      <div className="sidebar-nav">
        <button
          className={`nav-item ${activeTab === 'workspace' && !currentRunId ? 'active' : ''}`}
          onClick={() => setActiveTab('workspace')}
        >
          <Compass size={16} />
          <span>Research Canvas</span>
        </button>

        <button
          className={`nav-item ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          <BookOpen size={16} />
          <span>Library & Publications</span>
        </button>

        {/* History Section Header with Search */}
        <div style={{ marginTop: '16px', marginBottom: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '11px', fontWeight: '800', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Past Inquiries ({researchHistory.length})
            </span>
          </div>

          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'rgba(255, 255, 255, 0.03)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            padding: '4px 8px'
          }}>
            <Search size={12} color="var(--text-dim)" />
            <input
              type="text"
              placeholder="Filter inquiries..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                background: 'transparent',
                border: 'none',
                outline: 'none',
                color: '#fff',
                fontSize: '12px',
                width: '100%'
              }}
            />
          </div>
        </div>

        {/* History List */}
        {filteredHistory.length === 0 ? (
          <div style={{ padding: '12px', fontSize: '12px', color: 'var(--text-dim)', textAlign: 'center' }}>
            {searchTerm ? 'No matching inquiries' : 'No past research'}
          </div>
        ) : (
          filteredHistory.slice(0, 15).map((run) => (
            <div
              key={run.id}
              className={`history-item ${currentRunId === run.id ? 'active' : ''}`}
              onClick={() => onSelectRun(run.id)}
            >
              <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1, paddingRight: '8px' }} title={run.question}>
                {run.question}
              </div>

              {onDeleteRun && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    if (confirm('Delete this research run?')) onDeleteRun(run.id);
                  }}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: 'var(--text-dim)',
                    cursor: 'pointer',
                    padding: '2px',
                    display: 'flex',
                    alignItems: 'center'
                  }}
                  title="Delete run"
                >
                  <Trash2 size={12} />
                </button>
              )}
            </div>
          ))
        )}
      </div>

      {/* Theme Switcher Footer */}
      <div style={{
        padding: '14px 16px',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '11px',
        color: 'var(--text-dim)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Palette size={13} color="var(--accent-primary)" />
          <span>Theme</span>
        </div>

        <div style={{ display: 'flex', gap: '4px' }}>
          <button
            onClick={() => setTheme('default')}
            style={{
              width: '18px',
              height: '18px',
              borderRadius: '50%',
              background: '#6366f1',
              border: theme === 'default' ? '2px solid #fff' : 'none',
              cursor: 'pointer'
            }}
            title="Obsidian Midnight"
          />
          <button
            onClick={() => setTheme('aurora')}
            style={{
              width: '18px',
              height: '18px',
              borderRadius: '50%',
              background: '#ec4899',
              border: theme === 'aurora' ? '2px solid #fff' : 'none',
              cursor: 'pointer'
            }}
            title="Nebula Aurora"
          />
          <button
            onClick={() => setTheme('cyber')}
            style={{
              width: '18px',
              height: '18px',
              borderRadius: '50%',
              background: '#06b6d4',
              border: theme === 'cyber' ? '2px solid #fff' : 'none',
              cursor: 'pointer'
            }}
            title="Cyber Slate"
          />
        </div>
      </div>
    </aside>
  );
}
