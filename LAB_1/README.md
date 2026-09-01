# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Course:** Software Engineering — PES University, Dept. of CSE
**Problem Statement #41 — Developer Tools & IT Operations**
**Project:** OpenAPI Mock Server Generator

A developer-productivity tool that ingests OpenAPI 3.0 (YAML/JSON) specifications, generates dynamic
mock REST endpoints with schema validation, and simulates configurable response latency.

**Actors / Stakeholders:** API Developer, QA Engineer

---

## Deliverables

| # | Deliverable | File |
|---|---|---|
| 1 | Complete Requirements Table (5 FRs + 2 NFRs) | [`requirements.md`](requirements.md) |
| 2 | UML Use-Case Diagram (with `«include»` and `«extend»`) | [`use-case-diagram.md`](use-case-diagram.md) · [PNG](diagrams/use-case-diagram.png) · [SVG](diagrams/use-case-diagram.svg) |
| 3 | Use-Case Flow Specification (Invoke Mock Endpoint) | [`use-case-flow-specification.md`](use-case-flow-specification.md) |

## Folder Structure
```
Problem41_OpenAPI_Mock_Server_Generator/
├── README.md
├── requirements.md
├── use-case-diagram.md
├── use-case-flow-specification.md
└── diagrams/
    ├── use-case-diagram.svg
    └── use-case-diagram.png
```

## Requirements at a Glance
| ID | Title | Type | Priority |
|---|---|---|---|
| FR-001 | Ingest & Parse OpenAPI Specification | Functional | High |
| FR-002 | Generate Dynamic Mock Endpoints | Functional | High |
| FR-003 | Validate Incoming Request Against Schema | Functional | High |
| FR-004 | Configure Simulated Response Latency | Functional | Medium |
| FR-005 | Configure Custom Responses & Status Codes | Functional | Medium |
| NFR-001 | Throughput & Latency Accuracy | Performance | High |
| NFR-002 | Reliability & Security | Reliability & Security | High |

## Use-Case Relationships Modelled
- `«include»` — *Import OpenAPI Spec* includes *Validate Specification*
- `«include»` — *Invoke Mock Endpoint* includes *Validate Request Schema*
- `«extend»` — *Simulate Response Latency* extends *Invoke Mock Endpoint*
