import React, { useState } from 'react';
import { Send, Sparkles, BookOpen, Layers, Globe, Github, Cpu, Zap, Search, Microscope } from 'lucide-react';

export default function QuestionInput({ onSubmit, isLoading }) {
  const [question, setQuestion] = useState('');
  const [intent, setIntent] = useState('academic_research');
  const [depth, setDepth] = useState('deep');
  const [provider, setProvider] = useState('gemini');
  const [options, setOptions] = useState({
    include_academic: true,
    include_web: true,
    include_github: false,
    include_reddit: false,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;
    onSubmit({
      question: question.trim(),
      intent,
      depth,
      options: {
        ...options,
        provider,
      },
    });
  };

  const intents = [
    { id: 'academic_research', label: 'Academic & Papers', icon: BookOpen },
    { id: 'technical_research', label: 'Technical & Code', icon: Github },
    { id: 'general_research', label: 'General & Web', icon: Globe },
    { id: 'literature_review', label: 'Lit Review', icon: Layers },
  ];

  const depthModes = [
    { id: 'quick', label: 'Instant Answer', desc: 'Fast direct answer with key references', icon: Zap },
    { id: 'standard', label: 'Mid (Analysis & Debugging)', desc: 'Comparative study, benchmarks & trade-offs', icon: Search },
    { id: 'deep', label: 'Deep Research (Multi-AI)', desc: 'Multi-AI parallel workers, 30+ sources, contradictions & gaps', icon: Microscope },
  ];

  const orchestratorTeams = [
    { id: 'gemini', label: 'Gemini Head + Groq & DeepSeek Workers', desc: 'Gemini plans, Groq & DeepSeek extract in parallel' },
    { id: 'openrouter', label: 'DeepSeek-R1 Head + Multi-Workers', desc: 'DeepSeek R1 reasoning + fast worker pool' },
    { id: 'groq', label: 'Groq High-Speed Team', desc: '300+ tokens/sec fast response' },
  ];

  return (
    <div className="glass-card prompt-composer">
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <textarea
          className="prompt-textarea"
          placeholder="Ask a deep research question (e.g. 'Can multimodal RAG improve clinical diagnosis workflows, what benchmarks exist, and what research gaps remain?')..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
          disabled={isLoading}
        />

        <div className="composer-toolbar">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', width: '100%' }}>
            {/* Research Depth Selection */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: '700', textTransform: 'uppercase' }}>
                RESEARCH DEPTH:
              </span>
              {depthModes.map((dm) => {
                const Icon = dm.icon;
                return (
                  <button
                    key={dm.id}
                    type="button"
                    className={`chip ${depth === dm.id ? 'active' : ''}`}
                    onClick={() => setDepth(dm.id)}
                    disabled={isLoading}
                    title={dm.desc}
                    style={{ fontWeight: '600' }}
                  >
                    <Icon size={13} color={depth === dm.id ? 'var(--accent-primary)' : 'var(--text-dim)'} />
                    <span>{dm.label}</span>
                  </button>
                );
              })}
            </div>

            {/* Orchestrator AI Team Selection */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
              <div className="chips-group">
                <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: '700', textTransform: 'uppercase' }}>
                  AI TEAM:
                </span>
                {orchestratorTeams.map((t) => (
                  <button
                    key={t.id}
                    type="button"
                    className={`chip ${provider === t.id ? 'active' : ''}`}
                    onClick={() => setProvider(t.id)}
                    disabled={isLoading}
                    title={t.desc}
                  >
                    <Cpu size={12} />
                    <span>{t.label}</span>
                  </button>
                ))}
              </div>

              <button
                type="submit"
                className="btn-primary"
                disabled={!question.trim() || isLoading}
                style={{ padding: '10px 24px', fontSize: '14px' }}
              >
                <Send size={15} />
                <span>{isLoading ? 'Researching...' : 'Start Research'}</span>
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}
