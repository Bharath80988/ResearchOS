import React, { useState, useRef } from 'react';
import { Send, BookOpen, Layers, Globe, Github, Cpu, Zap, Search, Microscope, Upload, FileText, X, Paperclip } from 'lucide-react';

export default function QuestionInput({ onSubmit, isLoading }) {
  const [question, setQuestion] = useState('');
  const [intent, setIntent] = useState('academic_research');
  const [depth, setDepth] = useState('deep');
  const [provider, setProvider] = useState('gemini');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const fileInputRef = useRef(null);

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    const parsedList = [];
    for (const file of files) {
      try {
        const text = await readFileAsText(file);
        parsedList.push({
          name: file.name,
          content: text,
          size: file.size,
          type: file.type || 'text/plain'
        });
      } catch (err) {
        console.error(`Could not read ${file.name}:`, err);
      }
    }
    setUploadedFiles((prev) => [...prev, ...parsedList]);
  };

  const readFileAsText = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsText(file);
    });
  };

  const removeFile = (idx) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== idx));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;
    onSubmit({
      question: question.trim(),
      intent,
      depth,
      files: uploadedFiles,
      options: {
        provider,
      },
    });
  };

  const depthModes = [
    { id: 'quick', label: 'Instant Answer', desc: 'Instant direct answer with key references', icon: Zap },
    { id: 'standard', label: 'Mid (Analysis & Debugging)', desc: 'Comparative study, benchmarks & trade-offs', icon: Search },
    { id: 'deep', label: 'Deep Research (Multi-AI)', desc: 'Multi-AI workers, 30+ sources, chapters & code', icon: Microscope },
  ];

  const orchestratorTeams = [
    { id: 'gemini', label: 'Gemini Head + Groq & DeepSeek Workers', desc: 'Gemini plans, Groq & DeepSeek extract concurrently' },
    { id: 'openrouter', label: 'DeepSeek-R1 Head + Multi-Workers', desc: 'DeepSeek R1 reasoning + fast worker pool' },
    { id: 'groq', label: 'Groq High-Speed Team', desc: '300+ tokens/sec fast response' },
  ];

  return (
    <div className="glass-card prompt-composer">
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <textarea
          className="prompt-textarea"
          placeholder="Ask a deep research question or request code implementation (e.g. 'Can multimodal RAG improve clinical diagnosis workflows? Provide introduction, chapters, working code, and export to PPT')..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
          disabled={isLoading}
        />

        {/* Attached Files Strip */}
        {uploadedFiles.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-dim)', fontWeight: '700' }}>
              <span>SUPPORTING DOCUMENTS ({uploadedFiles.length} files attached - AI will shard & process)</span>
              <button
                type="button"
                onClick={() => setUploadedFiles([])}
                style={{ background: 'transparent', border: 'none', color: '#ef4444', cursor: 'pointer', fontSize: '11px' }}
              >
                Clear all
              </button>
            </div>
            <div className="files-preview-list">
              {uploadedFiles.map((file, idx) => (
                <div key={idx} className="file-chip">
                  <FileText size={12} color="var(--accent-secondary)" />
                  <span style={{ maxWidth: '160px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {file.name}
                  </span>
                  <X size={12} style={{ cursor: 'pointer' }} onClick={() => removeFile(idx)} />
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="composer-toolbar">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', width: '100%' }}>
            {/* Research Depth Selection */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: '700', textTransform: 'uppercase' }}>
                DEPTH MODE:
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
                  >
                    <Icon size={13} color={depth === dm.id ? 'var(--accent-primary)' : 'var(--text-dim)'} />
                    <span>{dm.label}</span>
                  </button>
                );
              })}
            </div>

            {/* AI Team & File Upload Button */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
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

                {/* File Upload Trigger */}
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  multiple
                  style={{ display: 'none' }}
                />
                <button
                  type="button"
                  className="chip"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isLoading}
                  style={{ background: 'rgba(255, 255, 255, 0.05)', color: '#fff' }}
                  title="Attach up to 100+ PDFs, TXT, Code, or CSV files"
                >
                  <Paperclip size={13} color="var(--accent-secondary)" />
                  <span>Attach Files ({uploadedFiles.length})</span>
                </button>
              </div>

              <button
                type="submit"
                className="btn-primary"
                disabled={!question.trim() || isLoading}
                style={{ padding: '10px 26px', fontSize: '14px' }}
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
