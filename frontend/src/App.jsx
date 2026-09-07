import React, { useState, useEffect } from 'react';
import ResearchLayout from './components/layout/ResearchLayout';
import Workspace from './pages/Workspace';
import History from './pages/History';
import FloatingProgressBar from './components/research/FloatingProgressBar';
import {
  checkHealth,
  createResearchRun,
  fetchResearchRuns,
  fetchResearchRun,
  deleteResearchRun,
  fetchResearchEvents,
  subscribeToResearchEvents
} from './api/research';

export default function App() {
  const [activeTab, setActiveTab] = useState('workspace');
  const [theme, setTheme] = useState('default');
  const [systemHealth, setSystemHealth] = useState(null);
  const [researchHistory, setResearchHistory] = useState([]);
  const [currentRun, setCurrentRun] = useState(null);
  const [events, setEvents] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
  }, [theme]);

  useEffect(() => {
    checkHealth()
      .then(setSystemHealth)
      .catch((err) => console.error('Health check failed:', err));
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await fetchResearchRuns(40);
      setResearchHistory(data.items || []);
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  const handleSelectRun = async (runId) => {
    if (!runId) {
      setCurrentRun(null);
      setEvents([]);
      setTasks([]);
      return;
    }
    try {
      const runData = await fetchResearchRun(runId);
      setCurrentRun(runData);
      setTasks(runData.tasks || []);

      const eventsData = await fetchResearchEvents(runId);
      setEvents(eventsData.events || []);

      setActiveTab('workspace');
    } catch (err) {
      console.error('Failed to select run:', err);
    }
  };

  const handleDeleteRun = async (runId) => {
    try {
      await deleteResearchRun(runId);
      if (currentRun?.id === runId) {
        setCurrentRun(null);
        setTasks([]);
        setEvents([]);
      }
      loadHistory();
    } catch (err) {
      console.error('Failed to delete run:', err);
    }
  };

  const handleSubmitResearch = async (formData) => {
    setIsLoading(true);
    setEvents([]);
    setTasks([]);

    try {
      const response = await createResearchRun(formData);
      const researchId = response.research_id;

      setCurrentRun({
        id: researchId,
        question: formData.question,
        intent: formData.intent,
        depth: formData.depth,
        status: 'queued',
        current_stage: formData.files?.length ? `Parsing ${formData.files.length} attached documents...` : 'Research queued',
        progress_percentage: 0,
      });

      const unsubscribe = subscribeToResearchEvents(
        researchId,
        (sseEvent) => {
          const { type, data } = sseEvent;
          
          if (data.message) {
            setEvents((prev) => [...prev, data]);
          }

          if (data.status) {
            setCurrentRun((prev) => ({
              ...prev,
              status: data.status,
              progress_percentage: data.progress_percentage ?? prev?.progress_percentage,
              current_stage: data.current_stage ?? prev?.current_stage,
              summary: data.summary ?? prev?.summary,
            }));
          }

          if (type === 'plan_created' || type === 'done' || type === 'research_completed') {
            fetchResearchRun(researchId)
              .then((updated) => {
                setCurrentRun(updated);
                setTasks(updated.tasks || []);
              })
              .catch(console.error);
            loadHistory();
          }

          if (type === 'done' || type === 'error') {
            setIsLoading(false);
          }
        },
        (err) => {
          console.error('SSE Stream error:', err);
          setIsLoading(false);
        }
      );
    } catch (err) {
      alert(`Failed to start research: ${err.message}`);
      setIsLoading(false);
    }
  };

  return (
    <ResearchLayout
      activeTab={activeTab}
      setActiveTab={setActiveTab}
      systemHealth={systemHealth}
      researchHistory={researchHistory}
      onSelectRun={handleSelectRun}
      onDeleteRun={handleDeleteRun}
      currentRunId={currentRun?.id}
      theme={theme}
      setTheme={setTheme}
      floatingProgress={
        currentRun && (
          <FloatingProgressBar
            currentRun={currentRun}
            events={events}
            tasks={tasks}
          />
        )
      }
    >
      {activeTab === 'workspace' && (
        <Workspace
          onSubmitResearch={handleSubmitResearch}
          isLoading={isLoading}
          currentRun={currentRun}
          tasks={tasks}
        />
      )}
      {activeTab === 'history' && (
        <History
          researchHistory={researchHistory}
          onSelectRun={handleSelectRun}
          onDeleteRun={handleDeleteRun}
        />
      )}
    </ResearchLayout>
  );
}
