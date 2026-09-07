import React, { useState } from 'react';
import { Send, Sparkles, BookOpen, Layers, Globe, Github } from 'lucide-react';

export default function QuestionInput({ onSubmit, isLoading }) {
  const [question, setQuestion] = useState('');
  const [intent, setIntent] = useState('academic_research');
  const [depth, setDepth] = useState('standard');
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
      options,
    });
  };

  const intents = [
    { id: 'academic_research', label: 'Academic & Papers', icon: BookOpen },
    { id: 'technical_research', label: 'Technical & Code', icon: Github },
    { id: 'general_research', label: 'General & Web', icon: Globe },
    { id: 'literature_review', label: 'Lit Review', icon: Layers },
  ];

  return (
    <div className="glass-card prompt-composer">
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <textarea
          className="prompt-textarea"
          placeholder="Ask a deep research question (e.g. 'Can multimodal RAG improve clinical decision workflows, what benchmarks exist and what research gaps remain?')..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
          disabled={isLoading}
        />

        <div className="composer-toolbar">
          <div className="chips-group">
            <span style={{ fontSize: '12px', color: 'var(--text-dim)', fontWeight: '600' }}>MODE:</span>
            {intents.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  type="button"
                  className={`chip ${intent === item.id ? 'active' : ''}`}
                  onClick={() => setIntent(item.id)}
                  disabled={isLoading}
                >
                  <Icon size={13} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div className="chips-group">
              <span style={{ fontSize: '12px', color: 'var(--text-dim)', fontWeight: '600' }}>DEPTH:</span>
              {['quick', 'standard', 'deep'].map((d) => (
                <button
                  key={d}
                  type="button"
                  className={`chip ${depth === d ? 'active' : ''}`}
                  onClick={() => setDepth(d)}
                  disabled={isLoading}
                >
                  {d.toUpperCase()}
                </button>
              ))}
            </div>

            <button
              type="submit"
              className="btn-primary"
              disabled={!question.trim() || isLoading}
            >
              <Send size={15} />
              <span>{isLoading ? 'Researching...' : 'Start Research'}</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
