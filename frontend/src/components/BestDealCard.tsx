import React from 'react';
import { Award, Shield, Star, Truck, Check } from 'lucide-react';
import type { Listing, ListingScores } from '../types';

interface BestDealCardProps {
  winnerListing: Listing;
  winnerScores: ListingScores;
  canonicalProduct: string;
  matchConfidence: number;
}

export const BestDealCard: React.FC<BestDealCardProps> = ({
  winnerListing,
  winnerScores,
  canonicalProduct,
  matchConfidence
}) => {
  return (
    <div
      className="glass-panel glow-animation"
      style={{
        padding: '28px',
        borderRadius: '20px',
        border: '2px solid rgba(16, 185, 129, 0.5)',
        background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.9) 100%)',
        position: 'relative',
        overflow: 'hidden',
        boxShadow: '0 16px 40px rgba(16, 185, 129, 0.15)'
      }}
    >
      {/* Top Banner */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            color: '#ffffff',
            padding: '6px 16px',
            borderRadius: '9999px',
            fontSize: '0.85rem',
            fontWeight: 800,
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            boxShadow: '0 4px 12px rgba(16, 185, 129, 0.3)'
          }}>
            <Award size={18} />
            <span>BEST OVERALL DEAL</span>
          </div>

          <span className="shimmer-badge" style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '6px', color: '#f59e0b', fontWeight: 700 }}>
            DEMO DATA
          </span>
        </div>

        <div style={{ fontSize: '0.82rem', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Check size={14} color="#10b981" />
          Match Confidence: <strong style={{ color: '#ffffff' }}>{Math.round(matchConfidence * 100)}%</strong>
        </div>
      </div>

      {/* Main Content Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px', alignItems: 'center' }}>
        {/* Left Side: Product Info */}
        <div>
          <div style={{ fontSize: '0.85rem', color: '#10b981', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            {winnerListing.platform}
          </div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#ffffff', margin: '4px 0 8px 0', lineHeight: 1.2 }}>
            {canonicalProduct || winnerListing.product_name}
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '16px' }}>
            Listing ID: <code style={{ color: '#a855f7' }}>{winnerListing.id}</code> ({winnerListing.condition})
          </p>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', marginTop: '12px' }}>
            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '10px 14px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Star size={14} color="#f59e0b" /> Seller Rating
              </div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', marginTop: '2px' }}>
                {winnerListing.seller_rating ? `${winnerListing.seller_rating}★` : 'N/A'}
                <span style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 400, marginLeft: '4px' }}>
                  ({winnerListing.seller_name})
                </span>
              </div>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '10px 14px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Shield size={14} color="#6366f1" /> Warranty
              </div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', marginTop: '2px' }}>
                {winnerListing.warranty || '1 Year'}
              </div>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.04)', padding: '10px 14px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Truck size={14} color="#38bdf8" /> Delivery
              </div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', marginTop: '2px' }}>
                {winnerListing.delivery_fee > 0 ? `₹${winnerListing.delivery_fee.toLocaleString()}` : 'Free'}
              </div>
            </div>
          </div>
        </div>

        {/* Right Side: Effective Price & Score Badge */}
        <div style={{
          background: 'rgba(15, 23, 42, 0.8)',
          borderRadius: '16px',
          padding: '24px',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase' }}>
            Effective Price (Price + Delivery)
          </div>
          <div style={{ fontSize: '2.4rem', fontWeight: 900, color: '#10b981', margin: '4px 0' }}>
            ₹{winnerListing.effective_price.toLocaleString()}
          </div>
          <div style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: '16px' }}>
            Listing Price: ₹{winnerListing.price.toLocaleString()} {winnerListing.delivery_fee > 0 ? `+ ₹${winnerListing.delivery_fee} delivery` : '(Free Delivery)'}
          </div>

          <div style={{
            background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%)',
            padding: '12px',
            borderRadius: '12px',
            border: '1px solid rgba(99, 102, 241, 0.4)'
          }}>
            <div style={{ fontSize: '0.75rem', color: '#cbd5e1', fontWeight: 600 }}>OVERALL SCORE</div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#ffffff' }}>
              {winnerScores.overall_score.toFixed(1)} <span style={{ fontSize: '1rem', color: '#94a3b8', fontWeight: 500 }}>/ 100</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
