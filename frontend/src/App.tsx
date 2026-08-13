import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { HeroSearch } from './components/HeroSearch';
import { PipelineProgress } from './components/PipelineProgress';
import { BestDealCard } from './components/BestDealCard';
import { RecommendationExplanation } from './components/RecommendationExplanation';
import { Controls } from './components/Controls';
import { ScoreVisualization } from './components/ScoreVisualization';
import { ComparisonTable } from './components/ComparisonTable';
import { SpecComparison } from './components/SpecComparison';

import type { ComparisonResponse, Weights } from './types';

const API_BASE_URL = 'http://localhost:8000';

const DEFAULT_WEIGHTS: Weights = {
  price: 0.50,
  seller: 0.25,
  warranty: 0.15,
  delivery: 0.10
};

export const App: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [demoQueries, setDemoQueries] = useState<string[]>([
    'iPhone 15 128GB',
    'Samsung Galaxy S24',
    'Sony WH-1000XM5',
    'MacBook Air M3'
  ]);

  const [currentQuery, setCurrentQuery] = useState('iPhone 15 128GB');
  const [weights, setWeights] = useState<Weights>(DEFAULT_WEIGHTS);
  const [crossPlatform, setCrossPlatform] = useState(false);

  const [isLoading, setIsLoading] = useState(false);
  const [isRecalculating, setIsRecalculating] = useState(false);
  const [comparisonResult, setComparisonResult] = useState<ComparisonResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Check health and demo queries on mount
  useEffect(() => {
    fetch(`${API_BASE_URL}/health`)
      .then((res) => res.json())
      .then(() => setApiStatus('online'))
      .catch(() => setApiStatus('offline'));

    fetch(`${API_BASE_URL}/api/demo-queries`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setDemoQueries(data);
        }
      })
      .catch(() => {});
  }, []);

  // Fetch comparison from real backend API
  const runComparison = async (queryToRun: string, currentWeights: Weights, cross: boolean) => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/compare`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query: queryToRun,
          weights: currentWeights,
          cross_platform: cross
        })
      });

      if (!response.ok) {
        let errText = `API Error (${response.status}): ${response.statusText}`;
        try {
          const errData = await response.json();
          if (errData && errData.detail) {
            errText = typeof errData.detail === 'string' ? errData.detail : JSON.stringify(errData.detail);
          }
        } catch (_) {}
        throw new Error(errText);
      }

      const data: ComparisonResponse = await response.json();
      setComparisonResult(data);
    } catch (err: any) {
      console.error(err);
      if (err.message && err.message.includes('Failed to fetch')) {
        setErrorMsg('Unable to connect to DealLens AI backend server. Please ensure FastAPI is running on http://localhost:8000.');
      } else {
        setErrorMsg(err.message || 'Failed to connect to backend server.');
      }
    } finally {
      setIsLoading(false);
      setIsRecalculating(false);
    }
  };

  // Initial comparison load
  useEffect(() => {
    runComparison(currentQuery, weights, crossPlatform);
  }, []);

  const handleSearch = (newQuery: string) => {
    setCurrentQuery(newQuery);
    runComparison(newQuery, weights, crossPlatform);
  };

  const handleWeightsChange = (newWeights: Weights) => {
    setWeights(newWeights);
    setIsRecalculating(true);
    runComparison(currentQuery, newWeights, crossPlatform);
  };

  const handleCrossPlatformToggle = (val: boolean) => {
    setCrossPlatform(val);
    runComparison(currentQuery, weights, val);
  };

  const handleResetWeights = () => {
    setWeights(DEFAULT_WEIGHTS);
    runComparison(currentQuery, DEFAULT_WEIGHTS, crossPlatform);
  };

  // Find winner listing object and winner scores
  const winnerListing = comparisonResult?.listings.find(
    (l) => l.id === comparisonResult.recommendation.winner_listing_id
  );
  const winnerScores = comparisonResult && winnerListing
    ? comparisonResult.scores[winnerListing.id]
    : null;

  return (
    <div style={{ minHeight: '100vh', paddingBottom: '60px' }}>
      <Navbar apiStatus={apiStatus} />

      <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 24px' }}>
        <HeroSearch onSearch={handleSearch} isLoading={isLoading} demoQueries={demoQueries} />

        <PipelineProgress isLoading={isLoading} />

        {errorMsg && (
          <div style={{
            background: 'rgba(244, 63, 94, 0.1)',
            border: '1px solid #f43f5e',
            color: '#f43f5e',
            padding: '16px 20px',
            borderRadius: '12px',
            margin: '24px 0',
            textAlign: 'center'
          }}>
            {errorMsg}
          </div>
        )}

        {!isLoading && comparisonResult && winnerListing && winnerScores && (
          <div style={{ animation: 'fadeIn 0.5s ease-in' }}>
            <BestDealCard
              winnerListing={winnerListing}
              winnerScores={winnerScores}
              canonicalProduct={comparisonResult.canonical_product}
              matchConfidence={comparisonResult.match_confidence}
            />

            <RecommendationExplanation recommendation={comparisonResult.recommendation} />

            <Controls
              weights={weights}
              crossPlatform={crossPlatform}
              onWeightsChange={handleWeightsChange}
              onCrossPlatformToggle={handleCrossPlatformToggle}
              onReset={handleResetWeights}
              isRecalculating={isRecalculating}
            />

            <ScoreVisualization
              listings={comparisonResult.listings}
              scoresMap={comparisonResult.scores}
              winnerId={comparisonResult.recommendation.winner_listing_id}
            />

            <ComparisonTable
              listings={comparisonResult.listings}
              scoresMap={comparisonResult.scores}
              winnerId={comparisonResult.recommendation.winner_listing_id}
            />

            <SpecComparison
              listings={comparisonResult.listings}
              normalizedSpecs={comparisonResult.normalized_specs}
            />
          </div>
        )}
      </main>

      <footer style={{ textAlign: 'center', padding: '24px', color: '#64748b', fontSize: '0.85rem' }}>
        DealLens AI Comparator • Built for full-stack autonomous product comparison demonstration.
      </footer>
    </div>
  );
};

export default App;
