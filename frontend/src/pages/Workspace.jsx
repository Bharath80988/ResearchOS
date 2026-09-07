import React from 'react';
import QuestionInput from '../components/research/QuestionInput';
import ProgressStage from '../components/research/ProgressStage';
import Badge from '../components/common/Badge';
import { Layers, HelpCircle, FileText, CheckCircle2 } from 'lucide-react';

export default function Workspace({
  onSubmitResearch,
  isLoading,
  currentRun,
  tasks
}) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Question / Prompt Composer */}
      <QuestionInput onSubmit={onSubmitResearch} isLoading={isLoading} />

      {/* Active Research Card if a run exists */}
      {currentRun && (
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '16px' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <Badge status={currentRun.status} />
                <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>
                  ID: {currentRun.id}
                </span>
              </div>
              <h2 style={{ fontSize: '17px', fontWeight: '700', color: 'var(--text-primary)', lineHeight: 1.4 }}>
                {currentRun.question}
              </h2>
            </div>
            <div style={{
              background: 'rgba(255, 255, 255, 0.04)',
              padding: '6px 12px',
              borderRadius: 'var(--radius-sm)',
              fontSize: '12px',
              color: 'var(--text-secondary)',
              flexShrink: 0
            }}>
              Depth: <strong style={{ color: '#fff' }}>{currentRun.depth?.toUpperCase()}</strong>
            </div>
          </div>
        </div>
      )}

      {/* Multi-Stage Visual Pipeline Progress */}
      <ProgressStage
        currentStatus={currentRun?.status || 'queued'}
        currentStage={currentRun?.current_stage || (isLoading ? 'Initializing research run...' : 'Awaiting prompt...')}
        progressPercentage={currentRun?.progress_percentage || 0}
      />

      {/* Synthesis / Findings Section */}
      {currentRun?.summary && (
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileText size={16} color="var(--accent-primary)" />
            <h3 style={{ fontSize: '15px', fontWeight: '700' }}>Executive Findings & Evidence Synthesis</h3>
          </div>
          <p style={{ fontSize: '14px', color: 'var(--text-primary)', lineHeight: 1.7 }}>
            {currentRun.summary}
          </p>
        </div>
      )}
    </div>
  );
}
