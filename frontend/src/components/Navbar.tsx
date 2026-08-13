import React from 'react';
import { Sparkles, Layers } from 'lucide-react';

interface NavbarProps {
  apiStatus: 'checking' | 'online' | 'offline';
}

export const Navbar: React.FC<NavbarProps> = ({ apiStatus }) => {
  return (
    <nav className="glass-panel" style={{ margin: '16px 24px', padding: '16px 24px', borderRadius: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 14px rgba(99, 102, 241, 0.4)'
          }}>
            <Layers size={24} color="#ffffff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '1.4rem', fontWeight: 800, background: 'linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                DealLens AI
              </span>
              <span className="shimmer-badge" style={{ fontSize: '0.7rem', padding: '2px 8px', borderRadius: '6px', color: '#f59e0b', fontWeight: 700, border: '1px solid rgba(245, 158, 11, 0.3)' }}>
                DEMO DATA
              </span>
            </div>
            <p style={{ fontSize: '0.82rem', color: '#94a3b8', margin: 0 }}>
              Find the best deal, not just the lowest price.
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div className="glass-pill" style={{ cursor: 'default' }}>
            <Sparkles size={14} color="#6366f1" />
            <span>Hybrid Match & Scorer</span>
          </div>

          <div className="glass-pill" style={{ cursor: 'default' }}>
            <span style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: apiStatus === 'online' ? '#10b981' : apiStatus === 'offline' ? '#f43f5e' : '#f59e0b'
            }} />
            <span style={{ fontSize: '0.8rem' }}>
              Backend: {apiStatus === 'online' ? 'Connected' : apiStatus === 'offline' ? 'Offline' : 'Connecting...'}
            </span>
          </div>
        </div>
      </div>
    </nav>
  );
};
