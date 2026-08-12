import React, { useEffect, useState } from 'react';
import { Search, FileText, CheckCircle2, Sliders, Award, Bot } from 'lucide-react';

interface PipelineProgressProps {
  isLoading: boolean;
}

const STEPS = [
  { id: 1, label: 'Search Listings', icon: Search, desc: 'Querying demo marketplace adapters' },
  { id: 2, label: 'Extract Specs', icon: FileText, desc: 'Parsing raw attributes & pricing' },
  { id: 3, label: 'Normalize Data', icon: CheckCircle2, desc: '128 GB → 128GB, 1 Yr → 12 mos, Free → ₹0' },
  { id: 4, label: 'Product Matching', icon: Sliders, desc: 'Evaluating hard constraints & similarity' },
  { id: 5, label: 'Deterministic Scoring', icon: Award, desc: 'Calculating effective price & component scores' },
  { id: 6, label: 'AI Explanation', icon: Bot, desc: 'Generating natural language deal summary' }
];

export const PipelineProgress: React.FC<PipelineProgressProps> = ({ isLoading }) => {
  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    if (!isLoading) {
      setCurrentStep(6);
      return;
    }
    setCurrentStep(1);
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < 5 ? prev + 1 : prev));
    }, 400);
    return () => clearInterval(interval);
  }, [isLoading]);

  if (!isLoading) return null;

  return (
    <div className="glass-panel" style={{ margin: '24px auto', maxWidth: '800px', padding: '24px' }}>
      <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px', color: '#6366f1', textAlign: 'center' }}>
        DealLens Orchestration Pipeline in Progress...
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
        {STEPS.map((step) => {
          const Icon = step.icon;
          const isActive = currentStep === step.id;
          const isDone = currentStep > step.id;

          return (
            <div
              key={step.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px',
                borderRadius: '12px',
                background: isActive ? 'rgba(99, 102, 241, 0.15)' : 'rgba(255, 255, 255, 0.02)',
                border: isActive ? '1px solid #6366f1' : '1px solid rgba(255, 255, 255, 0.05)',
                transition: 'all 0.3s ease'
              }}
            >
              <div style={{
                width: '34px',
                height: '34px',
                borderRadius: '8px',
                backgroundColor: isDone ? '#10b981' : isActive ? '#6366f1' : '#1e293b',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0
              }}>
                <Icon size={18} color="#ffffff" />
              </div>
              <div>
                <div style={{ fontSize: '0.88rem', fontWeight: 600, color: isActive ? '#ffffff' : '#cbd5e1' }}>
                  {step.label}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                  {step.desc}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
