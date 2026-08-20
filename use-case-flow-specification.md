# Use-Case Flow Specification

**Use Case:** UC-06 — Invoke Mock Endpoint
**Primary Actor:** QA Engineer
**Related Requirements:** FR-002, FR-003, FR-004
**Included:** Validate Request Schema  **Extended by:** Simulate Response Latency

---

## Brief Description
The QA Engineer sends an HTTP request to a generated mock endpoint. The system matches the request
to a route defined in the OpenAPI specification, validates the request against the operation schema,
produces a schema-compliant JSON response, optionally applies a configured latency, returns the
response, and records the exchange in the request log.

## Preconditions
1. A valid OpenAPI 3.0 specification has been imported and parsed (FR-001).
2. The mock server is running and its endpoints have been generated and are live (FR-002).
3. The QA Engineer knows the base URL and has network access to the mock server.

## Postconditions
**On success:**
1. An HTTP response with a schema-compliant body and the appropriate status code is returned to the caller.
2. The request and response metadata (method, path, status, timestamp, latency) are recorded in the request log.

**On failure:**
1. An appropriate `4xx` (validation) or `404` (no matching route) response is returned.
2. The failed request and its rejection reason are recorded in the request log.

---

## Main Success Scenario
1. The QA Engineer sends an HTTP request (method + path + optional params/body) to a mock endpoint.
2. The system matches the request to a route and operation defined in the specification.
3. The system **includes → Validate Request Schema**: it checks path/query parameters, headers, and
   the request body against the operation's declared schema, and confirms the request is valid.
4. The system generates a randomized JSON payload that conforms to the operation's declared response
   schema, and selects the appropriate success status code (e.g., `200`/`201`).
5. **`«extend»` → Simulate Response Latency:** *if* a latency value is configured for this endpoint,
   the system waits for the configured delay before responding.
6. The system returns the HTTP response to the QA Engineer.
7. The system records the request/response exchange in the request log.

## Alternate Flow

### A1 — Request Fails Schema Validation
*Triggered at step 3 when the request does not conform to the schema (e.g., a required field is missing
or a field has the wrong data type).*

1. The system halts response generation for the invalid request.
2. The system builds a `400 Bad Request` response containing a validation error report that identifies
   the offending field(s) and the reason for rejection.
3. The system returns the `400` response to the QA Engineer.
4. The system records the rejected request and its validation error in the request log.
5. The use case ends. *(The QA Engineer may correct the request and retry, returning to step 1 of the
   Main Success Scenario.)*
