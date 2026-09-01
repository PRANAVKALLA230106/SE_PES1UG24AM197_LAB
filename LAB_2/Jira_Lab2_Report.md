# Lab 2 — Agile Backlog Creation & Sprint Simulation in Jira

**Project:** OpenAPI Mock Server Generator
**Jira Space Key:** OMSG
**Student:** Pranav Kalla — PES1UG24AM197

---

## 1. Overview

Using the Functional and Non-Functional Requirements defined in Lab 1, the
requirements were translated into an Agile backlog of 5 Epics and 16 User
Stories, estimated using Fibonacci story points, prioritized, and executed
across two 1-week sprints in Jira.

## 2. From Requirements to Epics

Each Epic groups related Functional Requirements from Lab 1. Non-Functional
Requirements (NFR-001, NFR-002) were folded into a dedicated Epic (Epic 5)
since they represent cross-cutting performance and reliability concerns
rather than user-facing features.

| Epic | Jira ID | Source Requirement(s) | Priority |
|---|---|---|---|
| Specification Ingestion & Validation | OMSG-1 | FR-001 | High |
| Mock Endpoint Generation | OMSG-2 | FR-002 | High |
| Request Validation | OMSG-3 | FR-003 | High |
| Response Configuration | OMSG-4 | FR-004, FR-005 | Medium |
| Performance & Reliability | OMSG-5 | NFR-001, NFR-002 | High |

## 3. Epics and User Stories

### Epic 1: Specification Ingestion & Validation (OMSG-1)
*Enable the API Developer to import, parse, and validate OpenAPI 3.0 specs
before mock generation.*

| ID | Story | Points | Priority |
|---|---|---|---|
| OMSG-6 | As an API Developer, I want to upload an OpenAPI 3.0 spec file (YAML/JSON) or import via URL, so that the system can generate mocks from it. | 5 | High |
| OMSG-7 | As an API Developer, I want the system to validate the spec's structural conformance to OpenAPI 3.0, so that I know it's parseable before proceeding. | 8 | High |
| OMSG-8 | As an API Developer, I want descriptive error messages with the location of syntax/schema errors, so that I can quickly fix a malformed spec. | 3 | Medium |

### Epic 2: Mock Endpoint Generation (OMSG-2)
*Automatically generate live, schema-accurate mock REST endpoints from the
parsed spec.*

| ID | Story | Points | Priority |
|---|---|---|---|
| OMSG-9 | As an API Developer, I want the system to auto-create mock endpoints for every path/method in my spec, so that I don't configure each one manually. | 8 | High |
| OMSG-10 | As a QA Engineer, I want mock endpoints to return randomized JSON responses matching the declared schema, so that I can test against realistic data. | 8 | High |
| OMSG-11 | As a QA Engineer, I want undefined paths to return 404, so that I can verify my client handles unknown endpoints correctly. | 2 | Medium |

### Epic 3: Request Validation (OMSG-3)
*Validate incoming requests against schema and surface errors.*

| ID | Story | Points | Priority |
|---|---|---|---|
| OMSG-12 | As a QA Engineer, I want incoming requests validated against the declared schema (params, headers, body), so that I catch contract violations early. | 8 | High |
| OMSG-13 | As a QA Engineer, I want a 400 response with detailed validation errors on an invalid request, so that I know exactly what's wrong. | 3 | High |
| OMSG-14 | As a QA Engineer, I want to view a log of requests/responses (including rejected ones), so that I can review my test session history. | 5 | Medium |

### Epic 4: Response Configuration (OMSG-4)
*Let developers customize mock behavior — latency and overrides — to
emulate real-world conditions.*

| ID | Story | Points | Priority |
|---|---|---|---|
| OMSG-15 | As an API Developer, I want to set fixed or randomized latency globally or per-endpoint, so that I can simulate real network conditions. | 5 | Medium |
| OMSG-16 | As an API Developer, I want to override an endpoint's response with a custom payload, so that I can simulate specific business scenarios. | 5 | Medium |
| OMSG-17 | As an API Developer, I want to force a specific status code (e.g., 401, 429, 500) on an endpoint, so that I can test my client's error handling. | 2 | Medium |

### Epic 5: Performance & Reliability (OMSG-5)
*Ensure the mock server is fast, stable, and secure under load.*

| ID | Story | Points | Priority |
|---|---|---|---|
| OMSG-18 | As an API Developer, I want the mock server to sustain ≥1,000 req/s, so that it doesn't bottleneck CI pipelines. | 13 | High |
| OMSG-19 | As a QA Engineer, I want configured latency to stay accurate within ±10ms under peak load, so that my results are trustworthy. | 8 | High |
| OMSG-20 | As an API Developer, I want malformed or oversized (>5MB) spec uploads rejected gracefully, so that the server never crashes. | 5 | High |
| OMSG-21 | As an API Developer, I want each mock instance isolated with sanitized inputs, so that no injection or data leak occurs. | 8 | High |

**Total backlog size:** 5 Epics, 16 User Stories, 84 story points.

## 4. Estimation Approach (Planning Poker)

Story points were assigned using the Fibonacci sequence (1, 2, 3, 5, 8, 13),
reflecting effort, complexity, and uncertainty rather than raw time.
Parsing/validation and load-related stories (OMSG-7, OMSG-9, OMSG-10,
OMSG-12, OMSG-18, OMSG-19, OMSG-21) were scored higher due to genuine
technical uncertainty (schema validation edge cases, concurrency, load
behaviour). Simple routing/status-code behaviours (OMSG-11, OMSG-17) were
scored lowest. Priority was carried over from the FR/NFR priority levels in
Lab 1, with a few supporting stories (OMSG-8, OMSG-14) set to Medium since
they refine rather than define core functionality.

## 5. Jira Board Setup

A Scrum-type space ("OpenAPI Mock Server Generator", key `OMSG`) was created
in Jira with a Backlog, Board, and Reports view. All 5 Epics were created
first, followed by 16 User Stories linked to their respective Epics via the
Epic field.

**List view — all 5 Epics with their linked User Stories nested underneath,
showing status and priority (2 screenshots covering the full scrollable
list):**

![Epics and Stories — part 1](screenshots/01a_epics_stories_list_view_part1.png)
![Epics and Stories — part 2](screenshots/01b_epics_stories_list_view_part2.png)

---
*See `Sprint_Summary.md` for sprint execution, burndown charts, and final
outcomes.*
