# contracts/ — AGENTS.md

Single source of truth for every interface between components. Root rules: `../AGENTS.md`.
Contract-first: the contract is written and approved first; the backend conforms to it and the TypeScript
client (`packages/api-client`) is generated from it.

## Layout
- `openapi/openapi.yaml` — the only entry point (OpenAPI 3.1). Tools read this file alone.
- `openapi/shared.yaml` — components every module reuses: `Verdict`, `Problem`, `PageMetadata`, paging parameters, error responses.
- `openapi/system.yaml` — `/api/system/*` (served by backend `shared.api`).
- `openapi/modules/<module>.yaml` — one fragment per backend module (same names as `backend/` modules).
  Fragments hold `paths` and `components` only; add a path there, then reference it from `openapi.yaml`
  with a JSON pointer (`./modules/safety.yaml#/paths/~1api~1…`).

## Rules
1. A module writes only to its own fragment; shared schemas only in `shared.yaml`.
2. Identifiers are English. Paths start with `/api/`. Every operation has an `operationId` and a tag.
3. Enums are strings in `UPPER_SNAKE_CASE`, never integers; meaning must not depend on order (K20).
4. A verdict is always `shared.yaml#/components/schemas/Verdict`. No value named or meaning "safe"
   anywhere (red line 1, K02); uncertainty maps to `COULD_NOT_VERIFY` (S8, K03).
5. Errors: RFC 9457 `application/problem+json` using the `Problem` schema and the shared responses.
6. Paged lists: object with `content` (item array) and `page` (`PageMetadata`); query parameters `PageNumber`, `PageSize`.
7. Response objects set `additionalProperties: false`, so an extra field in the implementation fails the contract test.
8. Thresholds, defaults and limits are server configuration, not contract values.
9. Examples use synthetic data only; no health data, no real names or identifiers (K18, K19).
10. Do not invent names: if a field or value is not in this contract, the glossary or a schema, ask.

## Changing the contract (`plan/calisma-akisi.md` §6, `arastirma/08-ekip-calisma-modeli.md` §3.e)
- Contract changes go in their own PR with the `contract-change` label, before the implementation PR.
- Owner: the providing module's owner (`plan/calisma-akisi.md` §8); consumer approval is required.
- Additive change (new path, new optional field, new response) is the fast path. Breaking change
  (removing or renaming anything, new required request field, narrowing a type or enum) needs both owners
  and a migration note; CI runs `oasdiff breaking` (arrives with A1.2-b).
- Generated code (`packages/api-client`) is never edited by hand; regenerate it.

## Checks
- Contract ↔ backend conformance: `cd backend && ./gradlew test` (contract tests live in
  `backend/src/test/java/com/nutriscan/contract/`). A contract change re-runs them even when no Java changed.
