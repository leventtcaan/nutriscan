package com.nutriscan.contract;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.TreeSet;
import java.util.stream.Stream;
import tools.jackson.databind.JsonNode;
import tools.jackson.dataformat.yaml.YAMLMapper;

/** Reads the API contract (contracts/openapi) as YAML trees. Its location comes from the Gradle test task. */
final class ContractFiles {

    static final Path DIR = Path.of(Objects.requireNonNull(System.getProperty("nutriscan.contracts.dir"),
            "nutriscan.contracts.dir is not set; run the tests through Gradle (build.gradle.kts, tasks.test)"));
    static final Path ENTRY_POINT = DIR.resolve("openapi.yaml");
    static final Path SHARED = DIR.resolve("shared.yaml");
    static final Path MODULES = DIR.resolve("modules");

    // Operation keys of an OpenAPI 3.1 path item; the other keys (summary, parameters, ...) are not operations.
    private static final Set<String> HTTP_METHODS =
            Set.of("get", "put", "post", "delete", "options", "head", "patch", "trace");

    private static final YAMLMapper YAML = YAMLMapper.builder().build();

    private ContractFiles() {
    }

    static JsonNode read(Path file) {
        return YAML.readTree(file.toFile());
    }

    static List<Path> allFiles() {
        try (Stream<Path> files = Files.walk(DIR)) {
            return files.filter(file -> file.toString().endsWith(".yaml")).sorted().toList();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    /** Every operation the contract declares, as "GET /api/system/ping". */
    static Set<String> operations() {
        Set<String> operations = new TreeSet<>();
        for (Map.Entry<String, JsonNode> path : read(ENTRY_POINT).get("paths").properties()) {
            JsonNode pathItem = resolve(path.getValue(), ENTRY_POINT);
            for (String key : pathItem.propertyNames()) {
                if (HTTP_METHODS.contains(key)) {
                    operations.add(key.toUpperCase(Locale.ROOT) + " " + path.getKey());
                }
            }
        }
        return operations;
    }

    /** Follows a "$ref" such as ./system.yaml#/paths/~1api~1system~1ping; other nodes are returned as they are. */
    private static JsonNode resolve(JsonNode node, Path from) {
        JsonNode ref = node.get("$ref");
        if (ref == null) {
            return node;
        }
        String[] fileAndPointer = ref.asString().split("#", 2);
        Path file = fileAndPointer[0].isEmpty() ? from : from.resolveSibling(fileAndPointer[0]).normalize();
        JsonNode target = read(file).at(fileAndPointer[1]);
        if (target.isMissingNode()) {
            throw new IllegalStateException("Unresolvable $ref " + ref.asString() + " in " + from);
        }
        return target;
    }
}
