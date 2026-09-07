import React from 'react';
import { ListChecks, CheckCircle2, Clock, Globe } from 'lucide-react';

export default function PlanViewer({ tasks = [] }) {
  return (
    <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '14px', height: '100%', overflowY: 'auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
        <ListChecks size={15} color="var(--accent-primary)" />
        <span style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Decomposed Subtasks ({tasks.length})
        </span>
      </div>

      {tasks.length === 0 ? (
        <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-dim)', fontSize: '13px' }}>
          No decomposed subtasks generated yet.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {tasks.map((task, idx) => {
            const isDone = task.status === 'completed';
            return (
              <div
                key={task.id || idx}
                style={{
                  background: 'var(--bg-subtle)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '12px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '11px', fontWeight: '700', color: 'var(--accent-primary)' }}>
                    PRIORITY {task.priority || idx + 1}
                  </span>
                  <span style={{
                    fontSize: '11px',
                    padding: '2px 6px',
                    borderRadius: 'var(--radius-sm)',
                    background: isDone ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                    color: isDone ? 'var(--accent-success)' : 'var(--accent-warning)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}>
                    {isDone ? <CheckCircle2 size={11} /> : <Clock size={11} />}
                    {task.status}
                  </span>
                </div>

                <h5 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--text-primary)' }}>
                  {task.title}
                </h5>

                {task.purpose && (
                  <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                    {task.purpose}
                  </p>
                )}

                {task.source_types && task.source_types.length > 0 && (
                  <div style={{ display: 'flex', gap: '4px', marginTop: '4px', flexWrap: 'wrap' }}>
                    {task.source_types.map((st) => (
                      <span
                        key={st}
                        style={{
                          fontSize: '10px',
                          background: 'rgba(255, 255, 255, 0.05)',
                          padding: '2px 6px',
                          borderRadius: 'var(--radius-full)',
                          color: 'var(--text-dim)'
                        }}
                      >
                        {st}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
