import React, { useState } from 'react';
import { Activity, CheckCircle, ChevronUp, ChevronDown, Terminal, ListChecks, Database, X, Loader2 } from 'lucide-react';
import EventStream from './EventStream';
import PlanViewer from './PlanViewer';
import EvidenceViewer from './EvidenceViewer';
import Tabs from '../common/Tabs';

export default function FloatingProgressBar({ currentRun, events = [], tasks = [] }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('plan');

  if (!currentRun) return null;

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
        bottom: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        width: 'min(90vw, 860px)',
        background: 'rgba(15, 23, 42, 0.92)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.12)',
        borderRadius: 'var(--radius-lg)',
        padding: '12px 20px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '16px',
        boxShadow: '0 12px 40px rgba(0, 0, 0, 0.7), 0 0 20px rgba(99, 102, 241, 0.2)',
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
              <CheckCircle size={18} color="var(--accent-success)" />
            ) : isFailed ? (
              <span style={{ color: '#ef4444', fontWeight: '800' }}>!</span>
            ) : (
              <Loader2 size={18} color="var(--accent-primary)" className="animate-spin" />
            )}
          </div>

          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
              <span style={{ fontSize: '12px', fontWeight: '700', color: '#fff', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {currentRun.current_stage || (isCompleted ? 'Research Completed' : 'Processing...')}
              </span>
              <span style={{ fontSize: '12px', fontWeight: '800', color: 'var(--accent-primary)' }}>
                {progress}%
              </span>
            </div>

            {/* Micro Progress Bar */}
            <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.08)', borderRadius: '9999px', overflow: 'hidden' }}>
              <div style={{
                width: `${progress}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #6366f1 0%, #06b6d4 100%)',
                transition: 'width 0.4s ease'
              }} />
            </div>
          </div>
        </div>

        {/* Expand / Touch Subtasks Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="chip"
          style={{
            background: isOpen ? 'var(--accent-primary)' : 'rgba(255, 255, 255, 0.08)',
            color: isOpen ? '#fff' : 'var(--text-secondary)',
            padding: '6px 14px',
            fontSize: '12px',
            flexShrink: 0
          }}
        >
          <span>{isOpen ? 'Hide Details' : 'Inspect Subtasks & Evidence'}</span>
          {isOpen ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
        </button>
      </div>

      {/* Expanded Subtasks & Details Modal Overlay */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: '88px',
          left: '50%',
          transform: 'translateX(-50%)',
          width: 'min(92vw, 900px)',
          height: '60vh',
          background: 'rgba(11, 15, 26, 0.97)',
          backdropFilter: 'blur(25px)',
          border: '1px solid rgba(255, 255, 255, 0.15)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: '0 25px 60px rgba(0,0,0,0.8), 0 0 30px rgba(99, 102, 241, 0.25)',
          display: 'flex',
          flexDirection: 'column',
          zIndex: 99,
          overflow: 'hidden',
          animation: 'slideUp 0.25s ease-out'
        }}>
          {/* Header */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 16px', background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border-subtle)' }}>
            <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />
            <button
              onClick={() => setIsOpen(false)}
              style={{ background: 'transparent', border: 'none', color: 'var(--text-dim)', cursor: 'pointer', padding: '4px' }}
            >
              <X size={18} />
            </button>
          </div>

          {/* Body Content */}
          <div style={{ flex: 1, overflow: 'hidden' }}>
            {activeTab === 'plan' && <PlanViewer tasks={tasks} />}
            {activeTab === 'events' && <EventStream events={events} />}
            {activeTab === 'evidence' && <EvidenceViewer summary={currentRun.summary} currentRun={currentRun} />}
          </div>
        </div>
      )}
    </>
  );
}
