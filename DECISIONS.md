# Ana Fast-Lane — Implementation Decisions

## Project

**Name:** Ana Fast-Lane: From Report to Temporary Preservation

**Vacuum:** Restitution

**Lens:** Operator

**Core question:**  
How fast can a verified fraud report become operational action?

---

## Locked Product Boundary

This MVP is a simulated prototype for evaluating whether one specific reported fraudulent transfer can qualify for a temporary preservation action.

The product is designed around Restitution rather than generic fraud detection.

It does not attempt to:

- prove the full fraud case;
- determine recipient guilt;
- reimburse Ana;
- freeze real funds;
- freeze an entire account;
- become a generic scam or deepfake detector;
- allow AI to authorize preservation.

The authority principle remains:

**AI interprets → independent data corroborates → deterministic rules authorize**

Ana's report or uploaded evidence alone must never authorize preservation.

---

## Phase 1 — Security Floor + Project Skeleton

### Synthetic data only

The MVP will use synthetic data only.

No real:

- SPEI records;
- bank records;
- users;
- recipient accounts;
- WhatsApp data;
- institutional signals;
- personal financial information

will be used.

### No persistent personal-data storage

The MVP will not persist user-submitted personal data.

Temporary application state may later use Streamlit session state, but no database will be introduced for the MVP.

### No database

No database is required for the locked MVP.

Local synthetic JSON or CSV files will be used in later phases.

### No Supabase

Supabase will not be used.

Because Supabase is not used, Row Level Security (RLS) is not applicable.

### No authentication

Authentication is not required because the MVP does not store persistent personal data and is a synthetic demonstration.

### Secrets

No API keys, credentials, or secrets may be stored in source code or committed to GitHub.

Future local secrets must be stored in:

`.streamlit/secrets.toml`

This file is excluded through `.gitignore`.

Production secrets will later use Streamlit Community Cloud Secrets.

### AI

Gemini integration is intentionally not included in Phase 1.

AI will be added only in the later evidence-structuring phase and will never receive authority to authorize preservation.

---

## Prototype Constants

The following rules are locked for later implementation:

- Preservation eligibility window: 30 minutes after transfer
- Simulated hold duration: 15 minutes
- Hold scope: reported transaction only

These are prototype rules and must not be represented as real SPEI or bank rules.

---

## Simulation Labeling

The application must clearly communicate that it is a simulated prototype.

It must never imply connection to:

- Banco de México;
- SPEI infrastructure;
- a real bank;
- police;
- a real recipient account.

---

## Scope Status

### Phase 1

Status: In progress

Includes:

- Streamlit project skeleton
- security floor
- repository structure
- initial product-boundary UI
- initial implementation decision log

Does not include:

- synthetic transaction records;
- receiving-side signals;
- transaction verification;
- timeliness logic;
- Gemini;
- deterministic preservation logic;
- countdown;
- expiry;
- escalation.

---

## Deployment Log

### Deploy 1

Not completed yet.

### Deploy 2

Not completed yet.

---

## Session Close

Not completed yet.

---

## Phase 2 — Synthetic Institutional Environment

Status: Completed

### Synthetic transaction data

Created:

`data/transactions.json`

The dataset contains the three locked demo cases:

- ANA_CASE_1
- ANA_CASE_2
- ANA_CASE_3

Each transaction is explicitly synthetic and contains only prototype data.

No real SPEI, banking, personal, recipient, or institutional data is used.

### Independent receiving-side signals

Created:

`data/receiving_signals.json`

Receiving-side signals are intentionally stored separately from Ana's report and from the transaction dataset.

This separation preserves the locked authority principle:

**Ana's allegation alone cannot create the independent evidence required for preservation.**

The receiving-side signal dataset contains:

- ANA_CASE_1 → `pre_existing_internal_risk_flag`
- ANA_CASE_2 → `none`
- ANA_CASE_3 → `recent_independent_fraud_report`

All receiving-side institutional signals are synthetic and marked:

`"simulated": true`

### Locked demo behavior

The synthetic data supports the following future deterministic outcomes:

- Case 1 → fast + corroborated
- Case 2 → fast + uncorroborated
- Case 3 → too late

No preservation decision logic has been implemented in this phase.

### Scope boundary

Phase 2 does not include:

- transaction verification logic;
- timeliness logic;
- Gemini integration;
- AI evidence structuring;
- preservation authorization;
- countdown;
- expiry;
- escalation.

