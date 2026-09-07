import React from 'react';
import { Check, Loader2, Circle, Users, Sparkles } from 'lucide-react';

const STAGES = [
  { id: 'planning', label: '1. Intent & Planning', desc: 'Reasoning model structures subtasks' },
  { id: 'searching', label: '2. Multi-Source Search', desc: 'Querying OpenAlex, arXiv & Web' },
  { id: 'analyzing', label: '3. Sharded AI Workers', desc: 'Parallel AI workers (10 sites/worker)' },
  { id: 'synthesizing', label: '4. Synthesis & Citations', desc: 'Merging evidence & research gaps' },
];

export default function ProgressStage({ currentStatus, currentStage, progressPercentage }) {
  const getStageState = (stageId, index) => {
    const statusMap = {
      queued: 0,
      planning: 1,
      searching: 2,
      analyzing: 3,
      synthesizing: 4,
      completed: 5,
      failed: -1,
    };

    const currentLevel = statusMap[currentStatus] ?? 0;
    const stageLevel = index + 1;

    if (currentStatus === 'failed') return 'failed';
    if (currentLevel > stageLevel) return 'completed';
    if (currentLevel === stageLevel) return 'active';
    return 'pending';
  };

  return (
    <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h3 style={{ fontSize: '15px', fontWeight: '700' }}>Multi-AI Orchestration Pipeline</h3>
            <span style={{
              fontSize: '10px',
              padding: '2px 8px',
              borderRadius: 'var(--radius-full)',
              background: 'rgba(99, 102, 241, 0.15)',
              color: 'var(--accent-primary)',
              fontWeight: '700',
              textTransform: 'uppercase'
            }}>
              1 Orchestrator + N Workers
            </span>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>{currentStage || 'Ready for research'}</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '13px', fontWeight: '700', color: 'var(--accent-primary)' }}>
            {progressPercentage}%
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div style={{
        width: '100%',
        height: '6px',
        background: 'var(--bg-subtle)',
        borderRadius: 'var(--radius-full)',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${progressPercentage}%`,
          height: '100%',
          background: 'linear-gradient(90deg, #6366f1 0%, #06b6d4 100%)',
          transition: 'width 0.4s ease'
        }} />
      </div>

      {/* Pipeline Step Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px' }}>
        {STAGES.map((stg, idx) => {
          const state = getStageState(stg.id, idx);
          return (
            <div key={stg.id} className={`stage-step ${state}`} style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '8px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
                <span className="stage-step-icon">
                  {state === 'completed' && <Check size={14} />}
                  {state === 'active' && <Loader2 size={14} className="animate-spin" />}
                  {state === 'pending' && <Circle size={10} />}
                  {state === 'failed' && '!'}
                </span>
                <span style={{ fontSize: '10px', textTransform: 'uppercase', fontWeight: '700', color: state === 'active' ? 'var(--accent-primary)' : 'var(--text-dim)' }}>
                  {state}
                </span>
              </div>
              <div>
                <h4 style={{ fontSize: '13px', fontWeight: '600' }}>{stg.label}</h4>
                <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>{stg.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
