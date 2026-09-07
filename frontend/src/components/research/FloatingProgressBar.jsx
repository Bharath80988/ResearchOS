import React, { useState } from 'react';
import { Activity, CheckCircle2, ChevronUp, ChevronDown, Terminal, ListChecks, Database, X, Loader2 } from 'lucide-react';
import EventStream from './EventStream';
import PlanViewer from './PlanViewer';
import EvidenceViewer from './EvidenceViewer';
import Tabs from '../common/Tabs';

export default function FloatingProgressBar({ currentRun, events = [], tasks = [] }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('plan');
  const [dismissed, setDismissed] = useState(false);

  if (!currentRun || dismissed) return null;

  const isCompleted = currentRun.status === 'completed';
  const isFailed = currentRun.status === 'failed';
  const progress = currentRun.progress_percentage || 0;

  const tabs = [
    { id: 'plan', label: `Subtasks (${tasks.length})` },
    { id: 'events', label: `Live Stream (${events.length})` },
    { id: 'evidence', label: 'Evidence & Ledger' },
  ];

  return (
    <>
      {/* Floating Bottom Bar */}
      <div style={{
        position: 'fixed',
        bottom: '16px',
        left: '50%',
        transform: 'translateX(-50%)',
        width: 'min(92vw, 840px)',
        background: 'rgba(8, 8, 12, 0.96)',
        backdropFilter: 'blur(25px)',
        border: '1px solid rgba(255, 255, 255, 0.16)',
        borderRadius: 'var(--radius-lg)',
        padding: '12px 20px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '16px',
        boxShadow: '0 15px 45px rgba(0, 0, 0, 0.95), 0 0 25px rgba(99, 102, 241, 0.25)',
        zIndex: 100,
        transition: 'all 0.3s ease'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flex: 1, minWidth: 0 }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            background: isCompleted ? 'rgba(16, 185, 129, 0.2)' : 'rgba(99, 102, 241, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0
          }}>
            {isCompleted ? (
              <CheckCircle2 size={18} color="var(--accent-success)" />
            ) : isFailed ? (
              <span style={{ color: '#ef4444', fontWeight: '800' }}>!</span>
            ) : (
              <Loader2 size={18} color="var(--accent-primary)" className="animate-spin" />
            )}
          </div>

          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
              <span style={{ fontSize: '12.5px', fontWeight: '700', color: '#ffffff', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {currentRun.current_stage || (isCompleted ? 'Research Completed & Verified' : 'Processing...')}
              </span>
              <span style={{ fontSize: '12.5px', fontWeight: '800', color: '#818cf8' }}>
                {progress}%
              </span>
            </div>

            {/* Micro Progress Bar */}
            <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '9999px', overflow: 'hidden' }}>
              <div style={{
                width: `${progress}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #06b6d4 100%)',
                transition: 'width 0.4s ease'
              }} />
            </div>
          </div>
        </div>

        {/* Expand / Details Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
          <button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            className="chip"
            style={{
              background: isOpen ? '#1e1e2f' : 'rgba(255, 255, 255, 0.08)',
              color: '#ffffff',
              padding: '6px 14px',
              fontSize: '12px'
            }}
          >
            <span>{isOpen ? 'Hide Stream' : 'Live Agent Stream'}</span>
            {isOpen ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
          </button>

          {isCompleted && (
            <button
              type="button"
              onClick={() => setDismissed(true)}
              style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}
              title="Dismiss floating bar"
            >
              <X size={16} />
            </button>
          )}
        </div>
      </div>

      {/* Expanded Subtasks & Details Modal Overlay */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: '80px',
          left: '50%',
          transform: 'translateX(-50%)',
          width: 'min(92vw, 860px)',
          height: '55vh',
          background: '#07070a',
          border: '1px solid rgba(255, 255, 255, 0.18)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: '0 25px 60px rgba(0,0,0,0.95), 0 0 30px rgba(99, 102, 241, 0.3)',
          display: 'flex',
          flexDirection: 'column',
          zIndex: 99,
          overflow: 'hidden'
        }}>
          {/* Header */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 16px', background: '#0a0a0f', borderBottom: '1px solid var(--border-subtle)' }}>
            <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '6px' }}
            >
              <X size={18} />
            </button>
          </div>

          {/* Body Content */}
          <div style={{ flex: 1, overflow: 'hidden', background: '#030305' }}>
            {activeTab === 'plan' && <PlanViewer tasks={tasks} />}
            {activeTab === 'events' && <EventStream events={events} />}
            {activeTab === 'evidence' && <EvidenceViewer summary={currentRun.summary} currentRun={currentRun} />}
          </div>
        </div>
      )}
    </>
  );
}
