import React from 'react';
import { Sliders, RefreshCw, ToggleLeft, ToggleRight } from 'lucide-react';
import type { Weights } from '../types';

interface ControlsProps {
  weights: Weights;
  crossPlatform: boolean;
  onWeightsChange: (newWeights: Weights) => void;
  onCrossPlatformToggle: (val: boolean) => void;
  onReset: () => void;
  isRecalculating?: boolean;
}

export const Controls: React.FC<ControlsProps> = ({
  weights,
  crossPlatform,
  onWeightsChange,
  onCrossPlatformToggle,
  onReset,
  isRecalculating = false
}) => {
  const toPercent = (val: number) => (val <= 1 ? Math.round(val * 100) : Math.round(val));

  const currentPercents: Record<keyof Weights, number> = {
    price: toPercent(weights.price),
    seller: toPercent(weights.seller),
    warranty: toPercent(weights.warranty),
    delivery: toPercent(weights.delivery)
  };

  const totalWeight =
    currentPercents.price +
    currentPercents.seller +
    currentPercents.warranty +
    currentPercents.delivery;

  const handleSliderChange = (changedKey: keyof Weights, rawVal: number) => {
    const newVal = Math.max(0, Math.min(100, Math.round(rawVal)));
    const otherKeys = (['price', 'seller', 'warranty', 'delivery'] as (keyof Weights)[]).filter(
      (k) => k !== changedKey
    );

    const remainingNew = 100 - newVal;
    const otherSum = otherKeys.reduce((acc, k) => acc + currentPercents[k], 0);

    const updated: Record<keyof Weights, number> = {
      ...currentPercents,
      [changedKey]: newVal
    };

    if (otherSum > 0) {
      let sumAllocated = 0;
      otherKeys.forEach((k) => {
        const allocated = Math.max(0, Math.round((currentPercents[k] / otherSum) * remainingNew));
        updated[k] = allocated;
        sumAllocated += allocated;
      });

      const diff = remainingNew - sumAllocated;
      if (diff !== 0) {
        let targetKey = otherKeys[0];
        for (const k of otherKeys) {
          if (updated[k] > updated[targetKey]) {
            targetKey = k;
          }
        }
        updated[targetKey] = Math.max(0, updated[targetKey] + diff);
      }
    } else {
      const share = Math.floor(remainingNew / otherKeys.length);
      let sumAllocated = 0;
      otherKeys.forEach((k) => {
        updated[k] = share;
        sumAllocated += share;
      });
      const diff = remainingNew - sumAllocated;
      if (diff !== 0) {
        updated[otherKeys[0]] = Math.max(0, updated[otherKeys[0]] + diff);
      }
    }

    onWeightsChange(updated);
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', margin: '24px 0' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Sliders size={20} color="#6366f1" />
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#ffffff', margin: 0 }}>
            Custom Value Weight Tuning
          </h3>
          <div
            style={{
              background: totalWeight === 100 ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
              border: totalWeight === 100 ? '1px solid #10b981' : '1px solid #f43f5e',
              color: totalWeight === 100 ? '#10b981' : '#f43f5e',
              padding: '4px 12px',
              borderRadius: '9999px',
              fontSize: '0.8rem',
              fontWeight: 700
            }}
          >
            Total Weight: {totalWeight}%
          </div>
          {isRecalculating && (
            <span style={{ fontSize: '0.75rem', color: '#6366f1', fontWeight: 600 }}>Recalculating...</span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {/* Cross Platform Toggle */}
          <button
            onClick={() => onCrossPlatformToggle(!crossPlatform)}
            style={{
              background: crossPlatform ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255, 255, 255, 0.04)',
              border: crossPlatform ? '1px solid #6366f1' : '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: '9999px',
              padding: '6px 14px',
              color: '#ffffff',
              fontSize: '0.85rem',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            {crossPlatform ? <ToggleRight size={20} color="#6366f1" /> : <ToggleLeft size={20} color="#94a3b8" />}
            <span>Cross-Platform Outlets: {crossPlatform ? 'ON' : 'OFF'}</span>
          </button>

          {/* Reset Weights */}
          <button
            onClick={onReset}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#94a3b8',
              fontSize: '0.85rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}
          >
            <RefreshCw size={14} /> Reset Defaults
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
        {/* Price Weight */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '6px' }}>
            <span>Price Weight</span>
            <span style={{ color: '#6366f1' }}>{currentPercents.price}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="1"
            value={currentPercents.price}
            onChange={(e) => handleSliderChange('price', parseFloat(e.target.value))}
            style={{ width: '100%', accentColor: '#6366f1', cursor: 'pointer' }}
          />
        </div>

        {/* Seller Weight */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '6px' }}>
            <span>Seller Weight</span>
            <span style={{ color: '#f59e0b' }}>{currentPercents.seller}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="1"
            value={currentPercents.seller}
            onChange={(e) => handleSliderChange('seller', parseFloat(e.target.value))}
            style={{ width: '100%', accentColor: '#f59e0b', cursor: 'pointer' }}
          />
        </div>

        {/* Warranty Weight */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '6px' }}>
            <span>Warranty Weight</span>
            <span style={{ color: '#a855f7' }}>{currentPercents.warranty}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="1"
            value={currentPercents.warranty}
            onChange={(e) => handleSliderChange('warranty', parseFloat(e.target.value))}
            style={{ width: '100%', accentColor: '#a855f7', cursor: 'pointer' }}
          />
        </div>

        {/* Delivery Weight */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '6px' }}>
            <span>Delivery Weight</span>
            <span style={{ color: '#10b981' }}>{currentPercents.delivery}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="1"
            value={currentPercents.delivery}
            onChange={(e) => handleSliderChange('delivery', parseFloat(e.target.value))}
            style={{ width: '100%', accentColor: '#10b981', cursor: 'pointer' }}
          />
        </div>
      </div>
    </div>
  );
};
