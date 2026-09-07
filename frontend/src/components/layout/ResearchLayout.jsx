import React from 'react';
import Header from '../common/Header';
import Sidebar from '../common/Sidebar';

export default function ResearchLayout({
  activeTab,
  setActiveTab,
  systemHealth,
  researchHistory,
  onSelectRun,
  onDeleteRun,
  currentRunId,
  theme,
  setTheme,
  children,
  floatingProgress
}) {
  return (
    <div className="app-container">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        researchHistory={researchHistory}
        onSelectRun={onSelectRun}
        onDeleteRun={onDeleteRun}
        currentRunId={currentRunId}
        theme={theme}
        setTheme={setTheme}
      />

      <div className="main-workspace">
        <Header systemHealth={systemHealth} />
        <main style={{ flex: 1, overflowY: 'auto', padding: '24px 32px 140px 32px', maxWidth: '1120px', width: '100%', margin: '0 auto' }}>
          {children}
        </main>
        {floatingProgress}
      </div>
    </div>
  );
}
