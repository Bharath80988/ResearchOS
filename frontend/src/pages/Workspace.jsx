import React from 'react';
import QuestionInput from '../components/research/QuestionInput';
import ProgressStage from '../components/research/ProgressStage';
import ChapterViewer from '../components/research/ChapterViewer';
import Badge from '../components/common/Badge';
import { Sparkles, Microscope, Cpu, Layers } from 'lucide-react';

export default function Workspace({
  onSubmitResearch,
  isLoading,
  currentRun,
  tasks
}) {
  const hasReport = currentRun?.report && (currentRun?.report?.sections?.chapters?.length > 0 || currentRun?.summary);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Welcoming Hero Area (ChatGPT + Claude + Gemini inspired) */}
      {!currentRun && (
        <div className="hero-container">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(99, 102, 241, 0.1)', padding: '6px 14px', borderRadius: 'var(--radius-full)', border: '1px solid rgba(99, 102, 241, 0.25)' }}>
            <Sparkles size={14} color="var(--accent-primary)" />
            <span style={{ fontSize: '12px', fontWeight: '700', color: '#a5b4fc', letterSpacing: '0.05em' }}>
              AUTONOMOUS RESEARCH WORKSTATION
            </span>
          </div>
          <h1 className="hero-title">Where Deep Research Meets Autonomous AI</h1>
          <p className="hero-subtitle">
            Enter your natural-language question or attach up to 100+ documents. Multi-AI worker agents will plan, search open scholarly indexes, extract evidence, and synthesize comprehensive chapter reports with complete working code.
          </p>
        </div>
      )}

      {/* Prompt Composer & File Ingestion */}
      <QuestionInput onSubmit={onSubmitResearch} isLoading={isLoading} />

      {/* Active Run Status Bar */}
      {currentRun && (
        <div className="glass-card" style={{ padding: '16px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
              <Badge status={currentRun.status} />
              <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>
                ID: {currentRun.id?.slice(0, 8)}
              </span>
              <span style={{ fontSize: '11px', color: 'var(--accent-secondary)' }}>
                • Mode: {currentRun.depth?.toUpperCase()}
              </span>
            </div>
            <h2 style={{ fontSize: '16px', fontWeight: '800', color: '#fff', lineHeight: 1.4 }}>
              {currentRun.question}
            </h2>
          </div>
        </div>
      )}

      {/* Multi-AI Pipeline Step Tracker */}
      <ProgressStage
        currentStatus={currentRun?.status || 'queued'}
        currentStage={currentRun?.current_stage || (isLoading ? 'Multi-AI workers coordinating...' : 'Ready for inquiry')}
        progressPercentage={currentRun?.progress_percentage || 0}
      />

      {/* Synthesized Research Publication Chapter Viewer */}
      {hasReport && (
        <ChapterViewer report={currentRun.report} currentRun={currentRun} />
      )}
    </div>
  );
}
