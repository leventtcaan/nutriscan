package com.nutriscan.architecture;

import static org.assertj.core.api.Assertions.assertThat;

import com.nutriscan.NutriScanApplication;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;

class ModularityTests {

    // The module map agreed in plan/calisma-akisi.md §8 and AGENTS.md (directory map).
    private static final List<String> EXPECTED_MODULES = List.of(
            "assistant", "audit", "catalog", "consent", "household", "identity", "pantry",
            "planning", "privacy", "recommendation", "safety", "shared", "vision");

    private final ApplicationModules modules = ApplicationModules.of(NutriScanApplication.class);

    @Test
    void verifiesModuleBoundaries() {
        // No cycles, no access to another module's internals, only allowed dependencies.
        modules.verify();
    }

    @Test
    void moduleListMatchesAgreedMap() {
        List<String> actual = modules.stream()
                .map(module -> module.getIdentifier().toString())
                .toList();

        assertThat(actual).containsExactlyInAnyOrderElementsOf(EXPECTED_MODULES);
    }
}
