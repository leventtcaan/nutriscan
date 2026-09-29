# backend/ — AGENTS.md

Spring Boot 4.1 + Spring Modulith 2.1 modular monolith, Java 25, Gradle 9 (Kotlin DSL). Root rules: `../AGENTS.md`.

## Commands
- Build + all tests: `./gradlew build` (always the wrapper, never a system `gradle`)
- Tests only: `./gradlew test`

## Rules
- Every direct sub-package of `com.nutriscan` is a module; the list is fixed by `ModularityTests` (owners: `plan/calisma-akisi.md` §8).
- Each module's `package-info.java` declares `allowedDependencies` explicitly. Omitting it means "anything allowed";
  widening a list is a reviewed change (owner of the depending module approves).
- `shared` is a shared module (`@Modulithic`): every module may use the types in its **base package** (Modulith grants
  shared modules only their unnamed interface), it depends on nothing. `shared.api` (system endpoints) is internal.
- Versions live only in `gradle/libs.versions.toml`; `VersionCatalogTests` fails on inline versions. Library versions
  come from the Spring Boot / Spring Modulith BOMs.
- Types in a module's base package are its API; sub-packages are internal and invisible to other modules.
- HTTP endpoints follow `../contracts/openapi` (contract-first, `../contracts/AGENTS.md`). `com.nutriscan.contract` tests
  fail when a response, an endpoint or an enum differs from the contract; change the contract first, then the code.
