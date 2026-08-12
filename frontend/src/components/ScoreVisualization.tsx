import React from 'react';
import { BarChart2 } from 'lucide-react';
import type { Listing, ListingScores } from '../types';

interface ScoreVisualizationProps {
  listings: Listing[];
  scoresMap: Record<string, ListingScores>;
  winnerId: string;
}

export const ScoreVisualization: React.FC<ScoreVisualizationProps> = ({ listings, scoresMap, winnerId }) => {
  return (
    <div className="glass-panel" style={{ padding: '24px', margin: '24px 0' }}>
      <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#ffffff', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <BarChart2 size={20} color="#6366f1" /> Score Breakdown Comparison
      </h3>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px' }}>
        {listings.map((l) => {
          const s = scoresMap[l.id] || { price_score: 0, seller_score: 0, warranty_score: 0, delivery_score: 0, overall_score: 0 };
          const isWinner = l.id === winnerId;

          return (
            <div
              key={l.id}
              style={{
                background: isWinner ? 'rgba(16, 185, 129, 0.06)' : 'rgba(255, 255, 255, 0.02)',
                padding: '16px',
                borderRadius: '14px',
                border: isWinner ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid rgba(255, 255, 255, 0.06)'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <div>
                  <span style={{ fontSize: '0.8rem', color: '#a855f7', fontWeight: 600 }}>{l.platform}</span>
                  <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff' }}>Listing {l.id}</div>
                </div>
                <div style={{
                  background: isWinner ? '#10b981' : '#6366f1',
                  color: '#ffffff',
                  padding: '4px 10px',
                  borderRadius: '8px',
                  fontSize: '0.85rem',
                  fontWeight: 800
                }}>
                  {s.overall_score.toFixed(1)}
                </div>
              </div>

              {/* Price Score */}
              <div style={{ marginBottom: '8px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', marginBottom: '2px' }}>
                  <span>Price Score</span>
                  <span>{s.price_score.toFixed(1)}</span>
                </div>
                <div style={{ height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ width: `${s.price_score}%`, height: '100%', backgroundColor: '#38bdf8' }} />
                </div>
              </div>

              {/* Seller Score */}
              <div style={{ marginBottom: '8px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', marginBottom: '2px' }}>
                  <span>Seller Rating Score</span>
                  <span>{s.seller_score.toFixed(1)}</span>
                </div>
                <div style={{ height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ width: `${s.seller_score}%`, height: '100%', backgroundColor: '#f59e0b' }} />
                </div>
              </div>

              {/* Warranty Score */}
              <div style={{ marginBottom: '8px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', marginBottom: '2px' }}>
                  <span>Warranty Score</span>
                  <span>{s.warranty_score.toFixed(1)}</span>
                </div>
                <div style={{ height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ width: `${s.warranty_score}%`, height: '100%', backgroundColor: '#a855f7' }} />
                </div>
              </div>

              {/* Delivery Score */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', marginBottom: '2px' }}>
                  <span>Delivery Score</span>
                  <span>{s.delivery_score.toFixed(1)}</span>
                </div>
                <div style={{ height: '6px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ width: `${s.delivery_score}%`, height: '100%', backgroundColor: '#10b981' }} />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
