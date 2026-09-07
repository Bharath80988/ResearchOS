import React, { useState, useRef } from 'react';
import { Send, Zap, Microscope, Paperclip, X, FileText, Cpu, Trash2 } from 'lucide-react';

export default function QuestionInput({ onSubmit, isLoading }) {
  const [question, setQuestion] = useState('');
  const [depth, setDepth] = useState('deep');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [provider, setProvider] = useState('multi-ai');
  const fileInputRef = useRef(null);

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    const parsedList = [];
    for (const file of files) {
      try {
        const base64Data = await readFileAsBase64(file);
        parsedList.push({
          name: file.name,
          content: base64Data,
          size: file.size,
          type: file.type || 'application/pdf'
        });
      } catch (err) {
        console.error(`Could not read ${file.name}:`, err);
      }
    }
    setUploadedFiles((prev) => [...prev, ...parsedList]);
  };

  const readFileAsBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
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
      intent: uploadedFiles.length > 0 ? 'document_analysis' : 'academic_research',
      depth,
      files: uploadedFiles,
      options: {
        provider,
      },
    });
  };

  return (
    <div className="glass-card prompt-composer">
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        {/* Textarea */}
        <textarea
          className="prompt-textarea"
          placeholder="Ask a deep research inquiry, attach academic marksheets (e.g. sem1.pdf ... sem8.pdf), or query scientific literature (e.g. 'Analyse these files and get Anna University CGPA conversion, subject strengths, and marks summary')..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
          disabled={isLoading}
        />

        {/* Attached Files Strip */}
        {uploadedFiles.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', background: '#050508', padding: '10px 14px', borderRadius: 'var(--radius-md)', border: '1px solid rgba(255,255,255,0.1)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '11.5px', color: '#94a3b8', fontWeight: '700' }}>
              <span>{uploadedFiles.length} ATTACHED DOCUMENTS (PARALLEL MULTI-AI SHARDING)</span>
              <button
                type="button"
                onClick={() => setUploadedFiles([])}
                style={{ background: 'transparent', border: 'none', color: '#ef4444', cursor: 'pointer', fontSize: '11.5px', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: '600' }}
              >
                <Trash2 size={12} /> Clear all
              </button>
            </div>
            <div className="files-preview-list">
              {uploadedFiles.map((file, idx) => (
                <div key={idx} className="file-chip">
                  <FileText size={13} color="var(--accent-secondary)" />
                  <span style={{ maxWidth: '180px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {file.name}
                  </span>
                  <X size={13} style={{ cursor: 'pointer', color: '#94a3b8' }} onClick={() => removeFile(idx)} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Controls & Action Bar */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          {/* Depth Modes & Provider Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <button
              type="button"
              className={`chip ${depth === 'quick' ? 'active' : ''}`}
              onClick={() => setDepth('quick')}
              disabled={isLoading}
              title="Fast direct answer with key references"
            >
              <Zap size={14} color={depth === 'quick' ? '#ffffff' : '#94a3b8'} />
              <span>Instant Answer</span>
            </button>

            <button
              type="button"
              className={`chip ${depth === 'deep' ? 'active' : ''}`}
              onClick={() => setDepth('deep')}
              disabled={isLoading}
              title="Full multi-AI parallel research with chapters, calculations & code"
            >
              <Microscope size={14} color={depth === 'deep' ? '#ffffff' : '#94a3b8'} />
              <span>Deep Research (Multi-AI)</span>
            </button>
          </div>

          {/* Attach & Submit */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
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
              style={{ background: '#14141e', color: '#ffffff', border: '1px solid rgba(255, 255, 255, 0.18)' }}
              title="Attach up to 100+ PDFs, Marksheets, TXT, or Code files"
            >
              <Paperclip size={14} color="var(--accent-secondary)" />
              <span>Attach Docs {uploadedFiles.length > 0 ? `(${uploadedFiles.length})` : ''}</span>
            </button>

            <button
              type="submit"
              className="btn-primary"
              disabled={!question.trim() || isLoading}
            >
              <Send size={15} />
              <span>{isLoading ? 'Synthesizing...' : 'Submit Inquiry'}</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
