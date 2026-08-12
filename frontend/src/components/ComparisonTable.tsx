import React from 'react';
import { Award, ExternalLink, Star } from 'lucide-react';
import type { Listing, ListingScores } from '../types';

interface ComparisonTableProps {
  listings: Listing[];
  scoresMap: Record<string, ListingScores>;
  winnerId: string;
}

export const ComparisonTable: React.FC<ComparisonTableProps> = ({ listings, scoresMap, winnerId }) => {
  return (
    <div className="glass-panel" style={{ padding: '24px', margin: '24px 0', overflowX: 'auto' }}>
      <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#ffffff', marginBottom: '16px' }}>
        Detailed Marketplace Comparison Matrix
      </h3>

      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', minWidth: '700px' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', color: '#94a3b8', fontSize: '0.85rem' }}>
            <th style={{ padding: '12px 16px' }}>Platform / Seller</th>
            <th style={{ padding: '12px 16px' }}>Listing Title</th>
            <th style={{ padding: '12px 16px' }}>Raw Price</th>
            <th style={{ padding: '12px 16px' }}>Delivery</th>
            <th style={{ padding: '12px 16px' }}>Effective Price</th>
            <th style={{ padding: '12px 16px' }}>Rating</th>
            <th style={{ padding: '12px 16px' }}>Warranty</th>
            <th style={{ padding: '12px 16px' }}>Condition</th>
            <th style={{ padding: '12px 16px' }}>Overall Score</th>
          </tr>
        </thead>
        <tbody>
          {listings.map((l) => {
            const isWinner = l.id === winnerId;
            const score = scoresMap[l.id]?.overall_score || 0;

            return (
              <tr
                key={l.id}
                style={{
                  borderBottom: '1px solid rgba(255, 255, 255, 0.04)',
                  backgroundColor: isWinner ? 'rgba(16, 185, 129, 0.08)' : 'transparent',
                  transition: 'background-color 0.2s ease'
                }}
              >
                <td style={{ padding: '16px', verticalAlign: 'top' }}>
                  <div style={{ fontWeight: 700, color: '#ffffff' }}>{l.platform}</div>
                  <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>{l.seller_name || 'Verified Seller'}</div>
                  {isWinner && (
                    <span style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '4px',
                      fontSize: '0.7rem',
                      fontWeight: 800,
                      color: '#10b981',
                      marginTop: '4px'
                    }}>
                      <Award size={12} /> WINNER
                    </span>
                  )}
                </td>

                <td style={{ padding: '16px', verticalAlign: 'top', maxWidth: '240px' }}>
                  <div style={{ fontSize: '0.9rem', color: '#e2e8f0', fontWeight: 500 }}>{l.product_name}</div>
                  <a
                    href={l.product_url || '#'}
                    target="_blank"
                    rel="noreferrer"
                    style={{ fontSize: '0.75rem', color: '#6366f1', display: 'inline-flex', alignItems: 'center', gap: '2px', marginTop: '4px', textDecoration: 'none' }}
                  >
                    View Listing <ExternalLink size={10} />
                  </a>
                </td>

                <td style={{ padding: '16px', verticalAlign: 'top', color: '#cbd5e1', fontWeight: 600 }}>
                  ₹{l.price.toLocaleString()}
                </td>

                <td style={{ padding: '16px', verticalAlign: 'top', color: l.delivery_fee === 0 ? '#10b981' : '#f59e0b' }}>
                  {l.delivery_fee === 0 ? 'Free' : `+ ₹${l.delivery_fee.toLocaleString()}`}
                </td>

                <td style={{ padding: '16px', verticalAlign: 'top', fontWeight: 800, fontSize: '1.05rem', color: isWinner ? '#10b981' : '#ffffff' }}>
                  ₹{l.effective_price.toLocaleString()}
                </td>

                <td style={{ padding: '16px', verticalAlign: 'top' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#f59e0b', fontWeight: 600 }}>
                    <Star size={14} fill="#f59e0b" />
                    <span>{l.seller_rating ? `${l.seller_rating}` : 'N/A'}</span>
                  </div>
                </td>

                <td style={{ padding: '16px', verticalAlign: 'top', fontSize: '0.85rem', color: '#cbd5e1' }}>
                  {l.warranty || '1 Year'}
                </td>

                <td style={{ padding: '16px', verticalAlign: 'top', fontSize: '0.85rem', color: l.condition === 'New' ? '#10b981' : '#f59e0b' }}>
                  {l.condition}
                </td>

                <td style={{ padding: '16px', verticalAlign: 'top' }}>
                  <span style={{
                    padding: '6px 12px',
                    borderRadius: '8px',
                    backgroundColor: isWinner ? '#10b981' : 'rgba(99, 102, 241, 0.2)',
                    color: '#ffffff',
                    fontWeight: 800,
                    fontSize: '0.9rem'
                  }}>
                    {score.toFixed(1)}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
