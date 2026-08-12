import React from 'react';
import { Bot, ThumbsUp, AlertTriangle, Sparkles } from 'lucide-react';
import type { RecommendationDetail } from '../types';

interface RecommendationExplanationProps {
  recommendation: RecommendationDetail;
}

export const RecommendationExplanation: React.FC<RecommendationExplanationProps> = ({ recommendation }) => {
  return (
    <div className="glass-panel" style={{ padding: '24px', margin: '24px 0' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Bot size={20} color="#ffffff" />
          </div>
          <div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#ffffff', margin: 0 }}>
              AI Recommendation & Explanation
            </h3>
            <span style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
              Fact-checked synthesis based on structured listing parameters
            </span>
          </div>
        </div>

        <div className="glass-pill" style={{ cursor: 'default', border: '1px solid rgba(99, 102, 241, 0.4)' }}>
          <Sparkles size={14} color="#a855f7" />
          <span>AI mode: <strong>{recommendation.ai_mode}</strong></span>
        </div>
      </div>

      <div style={{
        backgroundColor: 'rgba(255, 255, 255, 0.02)',
        borderRadius: '12px',
        padding: '16px 20px',
        borderLeft: '4px solid #6366f1',
        marginBottom: '20px',
        lineHeight: 1.6,
        color: '#e2e8f0',
        whiteSpace: 'pre-line',
        fontSize: '0.95rem'
      }}>
        {recommendation.ai_explanation}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
        {/* Pros / Reasons */}
        <div style={{ background: 'rgba(16, 185, 129, 0.05)', padding: '16px', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#10b981', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '10px' }}>
            <ThumbsUp size={16} /> Key Advantages
          </h4>
          <ul style={{ paddingLeft: '20px', margin: 0, color: '#cbd5e1', fontSize: '0.88rem' }}>
            {recommendation.reasons.map((r, idx) => (
              <li key={idx} style={{ marginBottom: '6px' }}>{r}</li>
            ))}
          </ul>
        </div>

        {/* Trade-offs */}
        {recommendation.trade_offs.length > 0 && (
          <div style={{ background: 'rgba(245, 158, 11, 0.05)', padding: '16px', borderRadius: '12px', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f59e0b', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '10px' }}>
              <AlertTriangle size={16} /> Trade-offs to Consider
            </h4>
            <ul style={{ paddingLeft: '20px', margin: 0, color: '#cbd5e1', fontSize: '0.88rem' }}>
              {recommendation.trade_offs.map((t, idx) => (
                <li key={idx} style={{ marginBottom: '6px' }}>{t}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};
