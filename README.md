# DealLens AI — AI Product Listing Comparator

> **Find the best deal, not just the lowest price.**

DealLens AI is a full-stack product comparison engine designed to solve the common e-commerce trap where the listing with the lowest base price turns out to be worse due to high delivery charges, poor seller ratings, missing warranty, or hidden fees.

---

## 📌 Problem

When shopping online across multiple marketplaces:
1. **Misleading Base Prices**: Products listing at low base prices often add hidden delivery charges at checkout.
2. **Apple-to-Oranges Comparison**: Marketplaces list products under different titles (`"iPhone 15 128 GB"` vs `"Apple iPhone 15 128-Gigabyte"`).
3. **Hidden Quality Trade-offs**: A cheaper listing might come from an unrated seller with only a 3-month seller warranty, whereas a slightly higher price listing offers a brand-new product with 12 months manufacturer warranty and 4.8★ rating.

---

## 💡 Solution

DealLens AI normalizes specifications across platforms, verifies product matching via a 3-level hybrid matcher (Hard Constraints + Token Similarity), calculates **Effective Price** (`Price + Delivery Fee`), scores listings across weighted value factors (Price, Seller Rating, Warranty, Delivery Speed & Cost), and generates natural language explanations using AI.

---

## 🏗 Architecture & Orchestration

```
User Query / Controls (Frontend: React + Vite + TS)
          │
          ▼  POST /api/compare
┌─────────────────────────────────────────────────────────┐
│              FastAPI Orchestration Pipeline              │
├─────────────────────────────────────────────────────────┤
│  1. Search Adapter       ➜ Demo Marketplaces (A, B, C)  │
│  2. Spec Extraction      ➜ Title & Description Parser   │
│  3. Normalizer           ➜ 128 GB ➜ 128GB, Free ➜ ₹0    │
│  4. Hybrid Matcher       ➜ Hard Constraints & Similarity│
│  5. Value Scorer         ➜ Price, Seller, Warranty, Fee │
│  6. AI Engine            ➜ LLM / Fact-Based Fallback    │
└─────────────────────────────────────────────────────────┘
          │
          ▼  SQLite Database Storage (deallens.db)
```

---

## ⚙️ Matching & Scoring Algorithms

### 1. Hybrid Product Matcher
- **Level 1 (Hard Constraints)**: Checks for critical attribute mismatches (`Model`, `Storage`, `RAM`, `Brand`, `Sub-model variants` like Pro/Max/Ultra). Any mismatch immediate rejects the match.
- **Level 2 (Normalized Token Similarity)**: Jaccard token set similarity over cleaned title text.
- **Level 3 (Attribute Overlap)**: Weighted similarity ratio.

### 2. Deterministic Scoring Engine
All numerical scoring remains **100% deterministic Python backend logic**. The LLM never invents or overrides scores.

$$\text{Effective Price} = \text{Price} + \text{Delivery Fee}$$

**Default Weights**:
- **Price Score** ($50\%$): Relative ratio compared to minimum effective price in set.
- **Seller Rating Score** ($25\%$): Scale of seller rating ($0 - 5.0\star$).
- **Warranty Score** ($15\%$): Ratio based on warranty months ($12\text{ months} = 100$).
- **Delivery Score** ($10\%$): Delivery speed bonus minus delivery fee penalty.

---

## 🤖 AI Architecture & Fallback Mode

- **LLM Mode**: Activated when `LLM_API_KEY` is configured in environment. Calls OpenAI/compatible API to format natural language summaries.
- **Deterministic Fallback Mode**: Activated when `LLM_API_KEY` is empty or API call fails. Generates structured fact-based explanation (`AI mode: Deterministic fallback`).

---

## 🚀 Benchmark Demo Products

1. **iPhone 15 128GB**
   - **Listing A**: ₹49,999 + ₹0 Delivery = **₹49,999** (4.5★ rating)
   - **Listing B**: ₹47,999 + ₹99 Delivery = **₹48,098** (4.8★ rating) 🏆 *Recommended Winner*
   - **Listing C**: ₹51,499 + ₹0 Delivery = **₹51,499** (4.2★ rating)
2. **Samsung Galaxy S24**
3. **Sony WH-1000XM5**
4. **MacBook Air M3**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Backend status check |
| `GET` | `/api/demo-queries` | List of demo benchmark queries |
| `POST` | `/api/search` | Raw marketplace search |
| `POST` | `/api/compare` | Primary orchestrator endpoint |
| `POST` | `/api/extract` | Extract structured attributes from raw text |
| `POST` | `/api/match` | Compare two listings for hard constraint mismatches |
| `GET` | `/api/comparisons/{id}` | Retrieve saved comparison from SQLite |

---

## 💻 Installation & Local Run

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Setup Backend
```bash
# From workspace root
cd backend
pip install -r requirements.txt

# Start FastAPI backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Setup Frontend
```bash
# In a new terminal window
cd frontend
npm install

# Start Vite dev server
npm run dev
```

The frontend runs at `http://localhost:5173` and communicates with backend at `http://localhost:8000`.

---

## 🧪 Testing

Run the automated pytest test suite covering effective price calculations, normalization, hybrid matching, scoring, recommendation, missing data resilience, and API integration:

```bash
# From workspace root
python -m pytest
```

---

## 🔮 Future Improvements
- Multi-currency conversion support.
- Real-world browser/API marketplace scrapers for Amazon, Flipkart, OLX with proxy rotation.
- Historical price trend tracking graphs.
