package com.nutriscan.contract;

import static org.assertj.core.api.Assertions.assertThat;

import com.nutriscan.shared.Verdict;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.jupiter.api.Test;
import tools.jackson.databind.JsonNode;

/** AB#149 AC1: the verdict has exactly four values and none of them means "safe" (red line 1, K02). */
class VerdictContractTests {

    @Test
    void contractVerdictEnumMatchesJava() {
        JsonNode contractValues = ContractFiles.read(ContractFiles.SHARED).at("/components/schemas/Verdict/enum");
        List<String> javaValues = Arrays.stream(Verdict.values()).map(Enum::name).toList();

        assertThat(contractValues.valueStream().map(JsonNode::asString).toList())
                .containsExactlyInAnyOrderElementsOf(javaValues)
                .containsExactlyInAnyOrder("NOT_SUITABLE", "CAUTION", "NO_CONFLICT_FOUND", "COULD_NOT_VERIFY");
    }

    @Test
    void noSafeValueInAnyContractEnum() {
        List<String> enumValues = new ArrayList<>();
        ContractFiles.allFiles().forEach(file -> collectEnumValues(ContractFiles.read(file), enumValues));

        assertThat(enumValues).as("enum values found in contracts/openapi").isNotEmpty();
        // Substring match: SAFE, SAFE_TO_EAT and UNSAFE are all rejected; no value may be phrased as safety.
        assertThat(enumValues).noneMatch(value -> value.contains("SAFE"));
    }

    private static void collectEnumValues(JsonNode node, List<String> into) {
        if (node.isObject() && node.get("enum") instanceof JsonNode values && values.isArray()) {
            values.valueStream().map(JsonNode::asString).forEach(into::add);
        }
        node.valueStream().forEach(child -> collectEnumValues(child, into));
    }
}
