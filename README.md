# InternMatch AI – Personalized Internship Recommendation & Readiness

An explainable, adaptive, end-to-end AI platform that connects internship recommendation with target-specific skill-gap analysis, personalized preparation roadmaps, adaptive mock interview practice, and continuously updated internship readiness.

---

## 1. Product Philosophy & Closed-Loop Architecture

> Existing systems often help students **FIND** opportunities. **InternMatch AI helps students become READY for the opportunity they are most likely to succeed in.**

```
Student Profile
  │
  ▼
AI Resume / Profile Analysis
  │
  ▼
Staged Recommendation Engine (Baseline TF-IDF / Semantic Dense / Hybrid Ranker)
  │
  ▼
Explainable Match Score (Skills %, Projects %, Education %, Preferences %)
  │
  ▼
Target-Specific Skill Gap Analysis (Critical, Important, Useful)
  │
  ▼
Personalized Preparation Roadmap (Prerequisite Sequencing & Verified Resources)
  │
  ▼
Adaptive AI Mock Interview Studio (Multi-Dimensional Rubric Evaluation)
  │
  ▼
Internship Readiness Index (IRI) Computation (0 - 100 Composite Score)
  │
  ▼
Closed-Loop Feedback: Demonstrated Progress Updates Profile & Re-ranks Opportunities
```

---

## 2. Mathematical & Algorithmic Foundations

### 2.1 Staged Recommendation Models
1. **Baseline Model:** TF-IDF token vectorizer + Cosine Similarity over student and job documents.
2. **Semantic Dense Model:** Dense vector representations enriched with taxonomic category metadata and semantic sub-tokens.
3. **Hybrid Ranker (Authoritative):**
   $$\text{Score}_{\text{hybrid}} = 0.35 S_{\text{req\_skills}} + 0.25 S_{\text{semantic}} + 0.15 S_{\text{projects}} + 0.10 S_{\text{pref\_skills}} + 0.10 S_{\text{education}} + 0.05 S_{\text{preferences}}$$
   * Mathematically bounded between $0.00$ and $100.00$.
   * **Explainability Layer:** Decomposes the score into verifiable factor attributions and synthesizes human-readable justifications grounded in exact matched skills and key gaps.

### 2.2 Skill Normalization & Taxonomy
* Standardized skill dictionary inspired by **ESCO** and **O\*NET**.
* Normalizes synonyms and aliases (e.g., `["js", "ecmascript"] -> "JavaScript"`, `["fastapi", "fast-api"] -> "FastAPI"`).
* Categorized across `Languages`, `Frameworks`, `Databases`, `DevOps & Cloud`, `Data & AI`, `Software Engineering`, and `Soft Skills`.

### 2.3 Internship Readiness Index (IRI)
An interpretable, reproducible composite indicator on a $0 - 100$ scale (**never a hiring probability**):
$$\text{IRI} = 0.35 \times \text{SkillCoverage} + 0.20 \times \text{ProjectEvidence} + 0.15 \times \text{RoadmapProgress} + 0.20 \times \text{InterviewPerformance} + 0.10 \times \text{ProfileCompleteness}$$
* **SkillCoverage ($0-100$):** Weighted ratio of possessed vs. required & preferred skills.
* **ProjectEvidence ($0-100$):** Relevance of student projects to target stack.
* **RoadmapProgress ($0-100$):** Percentage of preparation roadmap items completed.
* **InterviewPerformance ($0-100$):** Average rubric score from adaptive mock interviews.
* **ProfileCompleteness ($0-100$):** Profile data availability.

### 2.4 Closed-Loop Feedback
When a student completes a roadmap milestone or scores high on a mock interview question, the coordinator:
1. Records/upgrades the competency in the student profile with provenance (`learning_progress` or `interview_verified`).
2. Recalculates the student's Internship Readiness Index (IRI).
3. Adapts recommendation scores based on newly demonstrated competencies.

---

## 3. Technology Baseline

* **Frontend:** Next.js 14 App Router, TypeScript, Tailwind CSS, Lucide icons.
* **Backend:** Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async), Scikit-Learn, NumPy.
* **Database:** Supabase / PostgreSQL schema with migrations/DDL (`backend/database/schema.sql`) and a flexible async repository supporting both live Supabase and local persistent SQLite.

---

## 4. Getting Started & Running Locally

### Prerequisites
* Python 3.11 (`py` or `python`)
* Node.js v18+ and `npm`

### Backend Setup
```bash
# 1. Create and activate virtual environment
py -3.11 -m venv .venv
.\.venv\Scripts\activate   # On Windows PowerShell

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Start FastAPI server
uvicorn backend.main:app --reload --port 8000
```
API Documentation will be live at `http://127.0.0.1:8000/docs`.

### Frontend Setup
```bash
# In /frontend directory
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 5. Verification & Test Suite

### Running Python Unit & Integration Tests (19 Tests)
```bash
.\.venv\Scripts\python.exe -m pytest backend/tests -v
```
Verifies:
* Skill taxonomy alias resolution and text extraction
* TF-IDF baseline and Semantic dense recommenders
* Hybrid multi-factor ranking and explainability math
* Skill gap categorization (Critical vs Important vs Useful)
* Prerequisite-ordered roadmap sequencing
* Adaptive mock interview rubric scoring
* Internship Readiness Index (IRI) calculation
* Closed-loop feedback propagation
* All FastAPI REST API endpoints

### Running Full End-to-End User Journey Simulation
```bash
.\.venv\Scripts\python.exe scripts/verify_e2e.py
```
Exercises all 13 phases of the student lifecycle:
`Profile -> Resume Parse -> Recommender Comparison -> Target Selection -> Skill Gap -> Roadmap -> Milestone Completion -> Interview Practice -> IRI Increase -> Application Tracker -> Dashboard Aggregation`.

### Running Frontend Type-Check & Production Build
```bash
cd frontend
npm run type-check
npm run build
```
Compiled with zero TypeScript errors and generates optimized server/client chunks.
