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


---

## Phase 6 — Hold Lifecycle + Streamlit Outcome UI

Status: Completed

### Streamlit outcome UI

Updated:

`app.py`

The prototype flow now supports the three locked demo outcomes:

- ANA_CASE_1 → `TEMPORARY HOLD ACTIVE — SIMULATED`
- ANA_CASE_2 → `Report verified · temporary preservation not authorized`
- ANA_CASE_3 → `Preservation unavailable · restitution review continues`

Ana's transaction fields remain visible after demo-case prefilling.

The UI includes:

- transaction/reference ID;
- amount;
- recipient;
- transfer age;
- narrative;
- screenshot upload;
- simulated prototype labeling;
- preservation/restitution separation.

### Temporary simulated hold lifecycle

Added hold lifecycle logic to:

`preservation.py`

States:

- `ACTIVE`
- `EXPIRED`
- `ESCALATED`

The locked hold duration remains:

`15 minutes`

### Countdown

Eligible cases display a countdown in `MM:SS` format.

The countdown appears only when the deterministic decision produces an eligible simulated hold.

### Expiry

If the simulated hold reaches the 15-minute limit:

`Hold expired · simulated funds released`

Expiry is explicitly labeled as simulated.

### Escalation

If stronger synthetic evidence appears before expiry:

`Escalated to Human Reviewer — simulated`

Human review does not imply:

- guilt;
- final fraud determination;
- final restitution.

### Mutual exclusivity

Expiry and escalation are mutually exclusive.

### Demo controls

The UI includes simulation controls so lifecycle behavior can be demonstrated without waiting 15 real minutes.

These controls support:

- simulated time near expiry;
- simulated stronger evidence;
- simulated hold expiry.

### Visual verification

Manually verified in the local Streamlit UI:

- Case 1 reaches temporary simulated hold;
- countdown appears;
- stronger evidence produces simulated escalation;
- expiry produces simulated funds release;
- Case 2 reaches no hold + institutional review;
- Case 3 reaches preservation unavailable;
- Case 2 and Case 3 show no countdown.

### Tests

Full test suite result:

`31 passed`

### Scope boundary

Phase 6 still does not include:

- final real screenshot-to-Gemini UI connection;
- final deployed Streamlit version;
- Deploy 1 / Deploy 2 completion;
- final Session Close.


---

## Phase 7 — Real Screenshot-to-Gemini UI Integration

Status: Completed

### Real UI evidence flow

The Streamlit UI now sends the uploaded screenshot and Ana's narrative to the AI evidence layer.

The live flow is:

`Ana screenshot + narrative → Gemini evidence structuring → local validation → deterministic preservation rule`

The AI output does not directly authorize preservation.

### Locked authority boundary

The implementation preserves:

**AI interprets → independent data corroborates → deterministic rules authorize**

AI can only produce structured evidence fields.

The final preservation decision remains in deterministic Python logic.

### Case 1 live verification

Manually verified in the Streamlit UI using synthetic Case 1 evidence:

- reported amount matched;
- reported context matched;
- `evidence_consistent = true`;
- independent receiving-side signal was present;
- deterministic rule produced:

`TEMPORARY HOLD ACTIVE — SIMULATED`

### Safe failure behavior

During integration testing, temporary API failures including:

- `ServerError`
- `ReadTimeout`
- `ClientError`

were observed.

The evidence layer continued to fail safely with:

`evidence_consistent = false`

and did not authorize automatic preservation.

### Resilience adjustments

The Gemini evidence layer now includes:

- 60-second request timeout;
- one retry for transient `ServerError`;
- one retry for transient `ReadTimeout`;
- local JSON validation;
- forbidden authorization-field rejection;
- safe failure when validation or API processing fails.

### AI limitations

Gemini may identify evidence consistency and extract transaction details, but it does not:

- establish deceptive intent;
- validate screenshot authenticity independently;
- determine recipient guilt;
- prove the full fraud case;
- authorize preservation.

### Scope status

The core MVP product flow is now implemented locally.

Remaining work:

- Streamlit Community Cloud deployment;
- deployment secrets configuration;
- final mechanical test pass;
- final Session Close in `DECISIONS.md`.


---

## Deployment Constraint — Gemini API Quota

During Streamlit Community Cloud deployment testing, the deployed app returned:

`429 RESOURCE_EXHAUSTED`

from the Gemini API.

This indicates an external API quota / rate-limit constraint.

The deployed application itself successfully:

- loaded from GitHub;
- started in Streamlit Community Cloud;
- loaded the configured Gemini secret;
- submitted the Gemini API request;
- handled the API failure safely.

The failure occurred after the request reached Gemini.

### Safety behavior

When Gemini returned the quota error, the evidence layer produced:

`ai_status = safe_failure`

and:

`evidence_consistent = false`

The deterministic preservation engine therefore did not authorize an automatic hold.

This confirms that an external AI availability or quota failure cannot bypass the product's authority boundary.

### Local end-to-end verification

Before deployment, the full live flow was successfully verified locally using synthetic Case 1 evidence:

`Screenshot + narrative → Gemini → structured evidence → local validation → independent receiving-side signal → deterministic preservation rule`

The verified Case 1 output included:

- `matches_reported_amount = true`;
- `matches_reported_context = true`;
- `evidence_consistent = true`;
- independent receiving-side signal present;
- `TEMPORARY HOLD ACTIVE — SIMULATED`.

### Deployment status

Streamlit Community Cloud deployment: Completed

Core app deployment: Working

Gemini live processing in cloud: Temporarily constrained by external API quota

This does not change the MVP's:

- product logic;
- deterministic authorization rule;
- security boundary;
- synthetic-data scope;
- preservation/restitution separation.


---

## Session Close

Status: Completed

### Final implementation status

The Ana Fast-Lane MVP is implemented.

The completed flow is:

`Ana report → transaction verification → timeliness → Gemini evidence structuring → independent receiving-side signal → deterministic preservation rule → simulated outcome`

### Locked demo outcomes

The implemented product supports the three locked demo cases:

- ANA_CASE_1 → `TEMPORARY HOLD ACTIVE — SIMULATED`
- ANA_CASE_2 → `Report verified · temporary preservation not authorized` + institutional review
- ANA_CASE_3 → `Preservation unavailable · restitution review continues`

### Hold lifecycle

For eligible simulated holds, the product supports:

- `ACTIVE`
- `EXPIRED`
- `ESCALATED`

The simulated hold:

- lasts 15 minutes;
- applies only to the reported transaction;
- is reversible;
- auto-expires;
- remains separate from restitution.

### Authority boundary

The final implementation preserves:

**AI interprets → independent data corroborates → deterministic rules authorize**

AI never directly authorizes preservation.

### Security floor

Final security constraints:

- synthetic data only;
- no database;
- no Supabase;
- no authentication;
- no real banking integration;
- no real SPEI integration;
- no persistent personal-data storage;
- no secrets in source code;
- Gemini secret stored outside the repository;
- AI/API failure produces safe failure;
- no account-wide freeze;
- no guilt determination;
- preservation ≠ restitution.

### Testing

Final automated test suite:

`31 passed`

Manual local verification completed for:

- Case 1;
- Case 2;
- Case 3;
- countdown;
- expiry;
- escalation;
- real screenshot-to-Gemini processing;
- deterministic preservation authorization.

### Deployment

Streamlit Community Cloud deployment completed.

The deployed application successfully loads and runs from GitHub.

During cloud Gemini testing, the Gemini API returned:

`429 RESOURCE_EXHAUSTED`

This is documented as an external API quota constraint.

The application handled the condition safely and did not authorize preservation.

### Final status

Core MVP: Completed

Local end-to-end flow: Verified

Streamlit deployment: Completed

External Gemini cloud quota: Documented constraint

Session: Closed


---

## Persona Test — Ana

Status: Completed

### Persona tested

Ana was tested as the target user for the Week 3 Restitution MVP.

The persona was instructed to react only as a stressed Mexican SPEI user who had just realized she was deceived into making a fraudulent transfer.

The test focused on whether Ana could understand:

- what the product was asking her to do;
- whether any action had already happened;
- what a temporary hold meant;
- whether preservation meant recovery;
- what happened when preservation was unavailable;
- what she should do next.

### Main findings

The core operational logic was understandable once the outcome was shown.

Ana correctly understood that:

- temporary preservation is different from recovering the money;
- a successful hold means the money is temporarily prevented from moving;
- a failed automatic hold does not necessarily mean the report is false;
- missing the fast preservation window does not mean the broader review is over.

The largest usability gap was language and next-step clarity rather than decision logic.

### Main confusion points

Ana found the following language too technical or inappropriate for a victim-facing interface:

- Fast-Lane
- corroborated / uncorroborated
- temporary preservation
- restitution
- operational action
- Evidence structured by AI
- independent receiving-side signal
- simulated receiving-side signal
- demo-case terminology
- technical prototype rules
- AI JSON output

Ana also repeatedly asked:

- Has my report already been submitted?
- Is anything happening to my money yet?
- What do I do now?
- Who is reviewing the case?
- What happens when the countdown reaches zero?
- Does a hold mean I already recovered the money?

### Successful hold finding

On the temporary hold screen, Ana understood that the funds were temporarily preserved and that this did not mean the money had already returned to her account.

The countdown communicated urgency, but required an explanation of what happens at expiry.

### No-hold finding

When no automatic hold was available, Ana understood that the funds were not currently protected.

However, she needed explicit reassurance that:

`This does not mean your report is false.`

She also needed a clear next step rather than an abstract institutional-review state.

### Too-late finding

Ana understood that the fast preservation path was no longer available after the prototype eligibility window.

Importantly, she also understood that the broader effort to recover the money could continue.

This outcome communicated the preservation / recovery distinction more clearly than the original technical wording.

### UI changes implemented after persona testing

Updated `app.py` to:

- reduce technical language in Ana's primary flow;
- hide the demo-case selector inside an expander;
- hide demo lifecycle controls inside an expander;
- remove visible AI JSON from the victim-facing result flow;
- change the narrative to first-person language;
- confirm when evidence has been received;
- explain what screenshot evidence can be uploaded;
- replace technical preservation/restitution wording with plain-language explanations;
- explicitly state that temporary preservation does not mean the money has been recovered;
- add `What happens now?` guidance to outcome screens;
- explain countdown expiry;
- clarify that missing independent evidence does not mean the report is false;
- explain that a late report can still continue through broader review;
- simplify minutes from decimal values to whole minutes.

### Persona-test conclusion

The test did not identify a need to change the locked deterministic decision logic.

The main improvement opportunity was translating internal system states into immediate, human next steps.

Final usability conclusion:

`Ana understands the operational logic once the outcome is shown, but the interface must translate system states into plain-language next steps for a person in crisis.`

