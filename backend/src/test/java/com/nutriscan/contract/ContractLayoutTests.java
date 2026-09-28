package com.nutriscan.contract;

import static org.assertj.core.api.Assertions.assertThat;

import com.nutriscan.NutriScanApplication;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModule;
import org.springframework.modulith.core.ApplicationModules;

/** contracts/openapi/modules holds exactly one fragment per backend module (the shared module uses shared.yaml). */
class ContractLayoutTests {

    @Test
    void everyModuleHasContractFragment() throws IOException {
        ApplicationModules modules = ApplicationModules.of(NutriScanApplication.class);
        List<String> expected = modules.stream()
                .filter(module -> !modules.getSharedModules().contains(module))
                .map(ApplicationModule::getIdentifier)
                .map(Object::toString)
                .toList();

        List<String> fragments;
        try (Stream<Path> files = Files.list(ContractFiles.MODULES)) {
            fragments = files.map(file -> file.getFileName().toString().replaceFirst("\\.yaml$", "")).toList();
        }

        assertThat(fragments).containsExactlyInAnyOrderElementsOf(expected);
    }
}
