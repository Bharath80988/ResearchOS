import React, { useEffect, useRef } from 'react';
import { Terminal } from 'lucide-react';

export default function EventStream({ events = [] }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  const formatTime = (dateStr) => {
    if (!dateStr) return '';
    const d = new Date(dateStr);
    return d.toTimeString().split(' ')[0];
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', padding: '16px', gap: '10px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
        <Terminal size={14} color="var(--accent-primary)" />
        <span style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Live Event Stream
        </span>
        <span style={{ marginLeft: 'auto', fontSize: '11px', color: 'var(--text-dim)' }}>
          {events.length} events
        </span>
      </div>

      <div className="terminal-container" ref={scrollRef}>
        {events.length === 0 ? (
          <div style={{ color: 'var(--text-dim)', fontStyle: 'italic', padding: '10px 0' }}>
            Waiting for research run execution...
          </div>
        ) : (
          events.map((evt, idx) => (
            <div key={evt.id || idx} className="terminal-line">
              <span className="terminal-time">[{formatTime(evt.created_at)}]</span>
              <span className={`terminal-badge ${evt.event_type}`}>
                {evt.event_type}
              </span>
              <span className="terminal-msg">{evt.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
