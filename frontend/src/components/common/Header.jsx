import React from 'react';
import { Activity, ShieldCheck, Cpu } from 'lucide-react';

export default function Header({ systemHealth }) {
  const isHealthy = systemHealth?.status === 'healthy';

  return (
    <header className="top-bar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <h2 style={{ fontSize: '16px', fontWeight: '700', letterSpacing: '-0.02em' }}>
          Deep Research Workstation
        </h2>
        <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
          Phase 1 Foundation
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          background: 'rgba(255,255,255,0.04)',
          padding: '6px 12px',
          borderRadius: 'var(--radius-full)',
          fontSize: '12px'
        }}>
          <Cpu size={14} color="var(--accent-primary)" />
          <span>Provider: <strong style={{ color: '#fff' }}>Gemini (Configurable)</strong></span>
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          fontSize: '12px',
          color: isHealthy ? 'var(--accent-success)' : 'var(--accent-warning)'
        }}>
          <span style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: isHealthy ? 'var(--accent-success)' : 'var(--accent-warning)'
          }} />
          <span>{isHealthy ? 'Backend Connected' : 'Checking Connection...'}</span>
        </div>
      </div>
    </header>
  );
}
