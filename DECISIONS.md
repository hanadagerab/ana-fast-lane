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


---

## Phase 3 — Transaction Verification + Timeliness

Status: Completed

### Transaction verification

Created:

`verification.py`

The module verifies Ana's reported transaction against the local synthetic transaction dataset.

Verification requires:

- transaction reference exists;
- transaction is marked as existing;
- reference matches;
- amount matches;
- recipient matches.

If verification fails, processing stops with:

`Stop: transaction cannot be verified`

No preservation path continues after transaction verification failure.

### Timeliness

The prototype preservation eligibility window is locked at:

`30 minutes`

Rules:

- transfer age <= 30 minutes → timely
- transfer age > 30 minutes → not timely

This is a prototype rule and is not represented as a real SPEI or bank rule.

### Locked demo behavior

The current deterministic results are:

- ANA_CASE_1 → transaction verified + timely
- ANA_CASE_2 → transaction verified + timely
- ANA_CASE_3 → transaction verified + too late

For ANA_CASE_3, the preservation path stops at the timeliness stage with:

`Preservation unavailable · restitution review continues`

### Tests

Created:

`tests/test_verification.py`

The Phase 3 test suite validates:

- Case 1 verification;
- Case 2 verification;
- Case 3 verification;
- transaction mismatch blocking;
- unknown reference blocking;
- exactly 30 minutes remaining timely;
- more than 30 minutes becoming untimely;
- Case 1 verified + timely;
- Case 2 verified + timely;
- Case 3 verified + too late;
- failed verification stopping before timeliness.

Test result:

`11 passed`

### Scope boundary

Phase 3 does not include:

- Gemini integration;
- AI evidence structuring;
- receiving-side signal lookup logic;
- deterministic preservation authorization;
- simulated hold state;
- countdown;
- expiry;
- escalation.


### Implementation compromise — Gemini model availability

The locked implementation target was Gemini 2.5 Flash.

During implementation, Google returned a 404 stating that Gemini 2.5 Flash is no longer available to new users.

The MVP therefore uses:

`gemini-3.6-flash`

This change affects only model availability.

It does not change:

- the product scope;
- the evidence-structuring function;
- the authority boundary;
- the deterministic preservation logic;
- the rule that AI cannot authorize a hold;
- the requirement for independent receiving-side evidence.

---

## Phase 4 — AI Evidence Structuring

Status: Completed

### Evidence structuring module

Created:

`evidence.py`

The AI component is limited to:

- extracting information from the uploaded screenshot;
- summarizing Ana's narrative;
- identifying relevant evidence facts;
- comparing evidence with the reported amount and context;
- assessing internal consistency;
- stating limitations.

The AI cannot:

- authorize preservation;
- recommend a hold;
- determine recipient guilt;
- determine that fraud legally occurred;
- freeze an account;
- reimburse Ana;
- override deterministic application rules.

The authority principle remains:

**AI interprets → independent data corroborates → deterministic rules authorize**

### Prompt injection protection

Text inside screenshots is treated as untrusted evidence content.

Instructions embedded inside an uploaded image cannot change application rules or authorize preservation.

### Safe failure

If AI output is unavailable, malformed, invalid, or fails local validation, the system returns:

`ai_status = safe_failure`

and:

`evidence_consistent = false`

This means AI failure cannot support automatic preservation.

### Local validation

Provider-side structured schema enforcement was removed after implementation testing showed instability with image input.

The application instead:

1. requests JSON output from Gemini;
2. parses the returned JSON locally;
3. validates the expected evidence fields;
4. rejects forbidden authorization or guilt fields;
5. fails safely if validation fails.

This preserves the authority boundary while avoiding provider-side schema instability.

### Gemini model implementation compromise

The locked implementation target was:

`gemini-2.5-flash`

During implementation, the Gemini API returned a 404 indicating that Gemini 2.5 Flash was not available to this new API user.

The MVP therefore uses:

`gemini-3.6-flash`

This change is limited to model availability.

It does not change:

- product scope;
- evidence-structuring responsibilities;
- authority boundaries;
- deterministic preservation logic;
- the requirement for independent receiving-side evidence;
- the rule that AI cannot authorize a hold.

### Secrets

The Gemini API key is stored locally in:

`.streamlit/secrets.toml`

This file is excluded from Git through `.gitignore`.

The API key is not stored in source code or committed to the repository.

### Timeout

Gemini requests use a 30-second timeout.

If the request does not complete successfully, the evidence layer fails safely.

### Phase 4 integration result

Verified:

- Gemini API connection works;
- image input works;
- JSON output works;
- evidence output passes local validation;
- invalid or unavailable evidence fails safely;
- AI cannot authorize preservation.

### Scope boundary

Phase 4 does not include:

- independent receiving-side signal lookup logic;
- deterministic preservation authorization;
- simulated hold state;
- countdown;
- expiry;
- escalation.


---

## Phase 5 — Independent Receiving-Side Signal + Deterministic Preservation Rule

Status: Completed

### Independent receiving-side signal lookup

Created receiving-side lookup logic in:

`preservation.py`

Receiving-side signals are loaded from:

`data/receiving_signals.json`

This dataset remains separate from Ana's report and from transaction verification data.

The lookup supports the locked signal types:

- `pre_existing_internal_risk_flag`
- `recent_independent_fraud_report`
- `unusual_incoming_payment_velocity`
- `none`

The current locked demo cases resolve as:

- ANA_CASE_1 → independent signal present
- ANA_CASE_2 → no independent signal
- ANA_CASE_3 → independent signal present

All institutional signals remain explicitly simulated.

### Deterministic preservation rule

The preservation rule is implemented in Python.

The locked rule is:

`hold_eligible = transaction_verified AND timely AND evidence_consistent AND independent_receiving_signal`

AI does not authorize preservation.

Ana's allegation alone does not authorize preservation.

### Decision order

The deterministic rule evaluates the report in this order:

1. transaction verification;
2. timeliness;
3. AI evidence consistency;
4. independent receiving-side evidence.

Outcomes:

- transaction not verified → `Stop: transaction cannot be verified`
- report too late → `Preservation unavailable · restitution review continues`
- evidence inconsistent or AI fails safely → `No automatic hold`
- independent evidence missing → `Report verified · temporary preservation not authorized`
- all four conditions true → `TEMPORARY HOLD ACTIVE — SIMULATED`

### Locked demo behavior

The deterministic demo behavior is:

- ANA_CASE_1 → temporary simulated hold
- ANA_CASE_2 → no hold + institutional review requested
- ANA_CASE_3 → preservation unavailable

### Transaction-specific scope

Any eligible simulated hold applies only to:

- the reported transaction reference;
- the reported transaction amount.

No account-wide freeze or account-wide action exists.

### Tests

Created:

`tests/test_preservation.py`

The Phase 5 test suite validates:

- Case 1 receiving-side signal present;
- Case 2 receiving-side signal absent;
- Case 3 receiving-side signal present;
- unknown reference has no independent signal;
- transaction failure blocks preservation;
- late report blocks preservation even with independent evidence;
- inconsistent AI evidence blocks automatic hold;
- no independent signal blocks preservation;
- Case 1 reaches temporary simulated hold;
- Case 2 reaches no hold + review;
- Case 3 reaches preservation unavailable;
- AI evidence cannot replace independent receiving-side evidence;
- hold scope is reported transaction only;
- all four locked conditions are required.

Test result:

`14 passed`

### Scope boundary

Phase 5 does not include:

- final Streamlit outcome screens;
- countdown;
- ACTIVE / EXPIRED / ESCALATED hold lifecycle;
- simulated expiry;
- simulated escalation;
- final deployed UI.

