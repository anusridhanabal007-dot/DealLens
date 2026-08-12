export interface Listing {
  id: string;
  platform: string;
  product_name: string;
  brand?: string;
  model?: string;
  variant?: string;
  storage?: string;
  ram?: string;
  color?: string;
  condition: string;
  price: number;
  currency: string;
  delivery_fee: number;
  effective_price: number;
  seller_name?: string;
  seller_rating?: number;
  seller_review_count?: number;
  warranty?: string;
  warranty_months?: number;
  return_policy?: string;
  delivery_days?: number;
  availability: string;
  important_specifications?: Record<string, string>;
  product_url?: string;
  image_url?: string;
  source_type: string;
}

export interface RecommendationDetail {
  winner_listing_id: string;
  overall_score: number;
  confidence: number;
  reasons: string[];
  trade_offs: string[];
  ai_explanation: string;
  ai_mode: string; // "LLM" | "Deterministic fallback"
}

export interface ListingScores {
  price_score: number;
  seller_score: number;
  warranty_score: number;
  delivery_score: number;
  overall_score: number;
}

export interface ComparisonResponse {
  id: string;
  query: string;
  canonical_product: string;
  matched: boolean;
  match_confidence: number;
  total_listings: number;
  listings: Listing[];
  scores: Record<string, ListingScores>;
  recommendation: RecommendationDetail;
  normalized_specs: Record<string, Record<string, string>>;
}

export interface Weights {
  price: number;
  seller: number;
  warranty: number;
  delivery: number;
}
