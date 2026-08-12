import React, { useState } from 'react';
import { Search, ArrowRight, Sparkles } from 'lucide-react';

interface HeroSearchProps {
  onSearch: (query: string) => void;
  isLoading: boolean;
  demoQueries: string[];
}

export const HeroSearch: React.FC<HeroSearchProps> = ({ onSearch, isLoading, demoQueries }) => {
  const [inputQuery, setInputQuery] = useState('iPhone 15 128GB');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputQuery.trim()) {
      onSearch(inputQuery.trim());
    }
  };

  const handlePillClick = (q: string) => {
    setInputQuery(q);
    onSearch(q);
  };

  return (
    <div style={{ textAlign: 'center', padding: '32px 20px 24px 20px', maxWidth: '840px', margin: '0 auto' }}>
      <h1 style={{
        fontSize: '2.5rem',
        fontWeight: 800,
        marginBottom: '12px',
        background: 'linear-gradient(135deg, #ffffff 30%, #94a3b8 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent'
      }}>
        Compare Listings Across Marketplaces
      </h1>
      <p style={{ color: '#94a3b8', fontSize: '1.05rem', marginBottom: '28px', lineHeight: 1.6 }}>
        DealLens AI normalizes specs, matches exact products, calculates effective prices (Price + Delivery), and deterministically scores total value.
      </p>

      <form onSubmit={handleSubmit} style={{ position: 'relative', marginBottom: '20px' }}>
        <div className="glass-panel" style={{
          display: 'flex',
          alignItems: 'center',
          padding: '8px 12px 8px 20px',
          borderRadius: '9999px',
          border: '1px solid rgba(99, 102, 241, 0.3)',
          boxShadow: '0 12px 36px rgba(0,0,0,0.4)'
        }}>
          <Search size={22} color="#94a3b8" style={{ marginRight: '12px', flexShrink: 0 }} />
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder="e.g., iPhone 15 128GB, Samsung Galaxy S24..."
            style={{
              width: '100%',
              background: 'transparent',
              border: 'none',
              outline: 'none',
              color: '#ffffff',
              fontSize: '1.05rem',
              fontWeight: 500
            }}
          />
          <button
            type="submit"
            disabled={isLoading}
            style={{
              background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
              color: '#ffffff',
              border: 'none',
              borderRadius: '9999px',
              padding: '12px 28px',
              fontSize: '0.95rem',
              fontWeight: 700,
              cursor: isLoading ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              boxShadow: '0 4px 16px rgba(99, 102, 241, 0.4)',
              transition: 'transform 0.15s ease'
            }}
          >
            <span>{isLoading ? 'Analyzing...' : 'Compare'}</span>
            <ArrowRight size={18} />
          </button>
        </div>
      </form>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.85rem', color: '#64748b', display: 'flex', alignItems: 'center', gap: '4px' }}>
          <Sparkles size={14} color="#6366f1" /> Try Benchmark Products:
        </span>
        {demoQueries.map((q) => (
          <button
            key={q}
            onClick={() => handlePillClick(q)}
            className="glass-pill"
            style={{ border: inputQuery.toLowerCase() === q.toLowerCase() ? '1px solid #6366f1' : undefined }}
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
};
