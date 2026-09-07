import React from 'react';
import { Cpu, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Header({ systemHealth }) {
  const isHealthy = systemHealth?.status === 'healthy';

  return (
    <header className="top-bar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <h2 style={{ fontSize: '15px', fontWeight: '800', color: '#ffffff', letterSpacing: '-0.02em' }}>
          Deep Research Workstation
        </h2>
        <span style={{ fontSize: '11px', color: '#94a3b8', background: '#121218', padding: '3px 8px', borderRadius: '4px', border: '1px solid rgba(255,255,255,0.08)' }}>
          Multi-AI v2.0
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        {/* Active AI Core */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          background: '#0d0d14',
          border: '1px solid rgba(255,255,255,0.12)',
          padding: '6px 14px',
          borderRadius: 'var(--radius-full)',
          fontSize: '12.5px',
          color: '#cbd5e1'
        }}>
          <Cpu size={14} color="var(--accent-primary)" />
          <span>Orchestrator: <strong style={{ color: '#ffffff' }}>Multi-AI Swarm</strong></span>
        </div>

        {/* Backend Status */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          fontSize: '12px',
          fontWeight: '600',
          color: isHealthy ? 'var(--accent-success)' : 'var(--accent-warning)',
          background: isHealthy ? 'rgba(16, 185, 129, 0.1)' : 'rgba(245, 158, 11, 0.1)',
          padding: '5px 12px',
          borderRadius: 'var(--radius-full)',
          border: `1px solid ${isHealthy ? 'rgba(16, 185, 129, 0.25)' : 'rgba(245, 158, 11, 0.25)'}`
        }}>
          {isHealthy ? <CheckCircle2 size={13} /> : <AlertCircle size={13} />}
          <span>{isHealthy ? 'Ready & Online' : 'Connecting...'}</span>
        </div>
      </div>
    </header>
  );
}
