plugins {
    java
    alias(libs.plugins.spring.boot)
}

group = "com.nutriscan"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(libs.versions.java.get())
    }
}

springBoot {
    // META-INF/build-info.properties → BuildProperties; /api/system/ping reports its version.
    // Without "time" the file is identical across builds, so the Gradle build cache stays effective.
    buildInfo {
        excludes = setOf("time")
    }
}

repositories {
    mavenCentral()
}

dependencies {
    // BOMs pin every transitive version; nothing below declares its own.
    implementation(platform(libs.spring.boot.bom))
    implementation(platform(libs.spring.modulith.bom))

    implementation(libs.spring.boot.starter)
    implementation(libs.spring.boot.starter.webmvc)
    implementation(libs.spring.modulith.starter.core)

    testImplementation(libs.spring.boot.starter.test)
    testImplementation(libs.spring.boot.starter.webmvc.test)
    testImplementation(libs.jackson.dataformat.yaml)
    testImplementation(libs.openapi.request.validator.mockmvc)
    testImplementation(libs.spring.modulith.starter.test)
    testRuntimeOnly(libs.junit.platform.launcher)
}

// The API contract lives outside this Gradle project (contracts/AGENTS.md).
val contractsDir = file("../contracts/openapi")

tasks.test {
    useJUnitPlatform()
    // Declared as an input: a contract-only change must re-run the contract tests, not reuse a cached result.
    inputs.dir(contractsDir).withPathSensitivity(PathSensitivity.RELATIVE).withPropertyName("contracts")
    systemProperty("nutriscan.contracts.dir", contractsDir.relativeTo(projectDir).path)
}
