import React, { useState, useRef } from 'react';
import { Send, Zap, Microscope, Paperclip, X, FileText, CheckCircle2 } from 'lucide-react';

export default function QuestionInput({ onSubmit, isLoading }) {
  const [question, setQuestion] = useState('');
  const [depth, setDepth] = useState('deep');
  const [uploadedFiles, setUploadedFiles] = useState([]);
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
      reader.readAsDataURL(file); // Encode as Base64 Data URL for lossless PDF / binary parsing
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
        provider: 'gemini',
      },
    });
  };

  return (
    <div className="glass-card prompt-composer">
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {/* Textarea */}
        <textarea
          className="prompt-textarea"
          placeholder="Ask a deep research inquiry, attach marksheets, or request custom code (e.g. 'Analyse these files and calculate my Anna University CGPA, subject strengths, and percentage conversion')..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
          disabled={isLoading}
        />

        {/* Attached Files Strip */}
        {uploadedFiles.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-dim)', fontWeight: '700' }}>
              <span>{uploadedFiles.length} ATTACHED DOCUMENTS (AI WILL SHARD & ANALYZE)</span>
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

        {/* Action Bar */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
          {/* Depth Modes */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <button
              type="button"
              className={`chip ${depth === 'quick' ? 'active' : ''}`}
              onClick={() => setDepth('quick')}
              disabled={isLoading}
              title="Fast direct answer with key references"
            >
              <Zap size={13} color={depth === 'quick' ? 'var(--accent-primary)' : 'var(--text-dim)'} />
              <span>Instant Answer</span>
            </button>

            <button
              type="button"
              className={`chip ${depth === 'deep' ? 'active' : ''}`}
              onClick={() => setDepth('deep')}
              disabled={isLoading}
              title="Full multi-AI parallel research with chapters, code & citations"
            >
              <Microscope size={13} color={depth === 'deep' ? 'var(--accent-primary)' : 'var(--text-dim)'} />
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
              style={{ background: 'rgba(255, 255, 255, 0.05)', color: '#fff' }}
              title="Attach up to 100+ PDFs, Transcripts, TXT, or Code files"
            >
              <Paperclip size={13} color="var(--accent-secondary)" />
              <span>Attach Docs ({uploadedFiles.length})</span>
            </button>

            <button
              type="submit"
              className="btn-primary"
              disabled={!question.trim() || isLoading}
            >
              <Send size={14} />
              <span>{isLoading ? 'Researching...' : 'Submit'}</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
