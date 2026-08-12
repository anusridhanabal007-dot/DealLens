import React from 'react';
import { Sliders } from 'lucide-react';
import type { Listing } from '../types';

interface SpecComparisonProps {
  listings: Listing[];
  normalizedSpecs: Record<string, Record<string, string>>;
}

export const SpecComparison: React.FC<SpecComparisonProps> = ({ listings, normalizedSpecs }) => {
  const specKeys = ['storage', 'ram', 'color', 'condition', 'warranty', 'delivery'];

  return (
    <div className="glass-panel" style={{ padding: '24px', margin: '24px 0' }}>
      <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#ffffff', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Sliders size={20} color="#a855f7" /> Normalized Specification Matrix
      </h3>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', color: '#94a3b8' }}>
              <th style={{ padding: '10px 14px' }}>Specification</th>
              {listings.map((l) => (
                <th key={l.id} style={{ padding: '10px 14px' }}>
                  {l.platform} <span style={{ fontSize: '0.75rem', color: '#a855f7' }}>({l.id})</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {specKeys.map((key) => (
              <tr key={key} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                <td style={{ padding: '12px 14px', textTransform: 'capitalize', fontWeight: 600, color: '#94a3b8' }}>
                  {key}
                </td>
                {listings.map((l) => {
                  const val = normalizedSpecs[l.id]?.[key] || l[key as keyof Listing] || 'N/A';
                  return (
                    <td key={l.id} style={{ padding: '12px 14px', color: '#ffffff', fontWeight: 500 }}>
                      {String(val)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
