import React from 'react';
import Header from '../common/Header';
import Sidebar from '../common/Sidebar';

export default function ResearchLayout({
  activeTab,
  setActiveTab,
  systemHealth,
  researchHistory,
  onSelectRun,
  currentRunId,
  children,
  rightPanel
}) {
  return (
    <div className="app-container">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        researchHistory={researchHistory}
        onSelectRun={onSelectRun}
        currentRunId={currentRunId}
      />

      <div className="main-workspace">
        <Header systemHealth={systemHealth} />
        <div className="content-pane">
          <main className="center-pane">
            {children}
          </main>
          <aside className="right-pane">
            {rightPanel}
          </aside>
        </div>
      </div>
    </div>
  );
}
