# backend/ — AGENTS.md

Spring Boot 4.1 + Spring Modulith 2.1 modular monolith, Java 25, Gradle 9 (Kotlin DSL). Root rules: `../AGENTS.md`.

## Commands
- Build + all tests: `./gradlew build` (always the wrapper, never a system `gradle`)
- Tests only: `./gradlew test`

## Rules
- Every direct sub-package of `com.nutriscan` is a module; the list is fixed by `ModularityTests` (owners: `plan/calisma-akisi.md` §8).
- Each module's `package-info.java` declares `allowedDependencies` explicitly. Omitting it means "anything allowed";
  widening a list is a reviewed change (owner of the depending module approves).
- `shared` is a shared module (`@Modulithic`): every module may use it, it depends on nothing.
- Versions live only in `gradle/libs.versions.toml`; `VersionCatalogTests` fails on inline versions. Library versions
  come from the Spring Boot / Spring Modulith BOMs.
- Types in a module's base package are its API; sub-packages are internal and invisible to other modules.
