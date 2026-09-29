package com.nutriscan.contract;

import static com.atlassian.oai.validator.mockmvc.OpenApiValidationMatchers.openApi;
import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.atlassian.oai.validator.OpenApiInteractionValidator;
import com.nutriscan.NutriScanApplication;
import com.nutriscan.shared.Verdict;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.mvc.method.RequestMappingInfo;
import org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.json.JsonMapper;

/**
 * AB#149 AC2: a difference between the contract (contracts/openapi) and the running application fails a test.
 * Responses are checked field by field against the schemas; the endpoint lists are compared in both directions.
 */
@SpringBootTest
@AutoConfigureMockMvc
class ContractConformanceTests {

    // Built once: parsing the contract and its $refs is the expensive part.
    private static final OpenApiInteractionValidator CONTRACT = OpenApiInteractionValidator
            .createForSpecificationUrl(ContractFiles.ENTRY_POINT.toAbsolutePath().toUri().toString())
            .build();

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private RequestMappingHandlerMapping handlerMapping;

    @Autowired
    private JsonMapper jsonMapper;

    @Test
    void pingResponseConformsToContract() throws Exception {
        mockMvc.perform(get("/api/system/ping"))
                .andExpect(status().isOk())
                .andExpect(openApi().isValid(CONTRACT));
    }

    @Test
    void errorBodyCarriesContractProblemFields() throws Exception {
        // The validator only checks declared operations, so an error from an undeclared path is checked here
        // against the required fields of the shared Problem schema.
        String body = mockMvc.perform(get("/api/system/no-such-endpoint"))
                .andExpect(status().isNotFound())
                .andExpect(content().contentType(MediaType.APPLICATION_PROBLEM_JSON))
                .andReturn().getResponse().getContentAsString();
        List<String> required = ContractFiles.read(ContractFiles.SHARED)
                .at("/components/schemas/Problem/required").valueStream().map(JsonNode::asString).toList();

        assertThat(jsonMapper.readTree(body).propertyNames()).containsAll(required);
    }

    @Test
    void everyContractOperationIsImplemented() {
        assertThat(implementedOperations()).containsAll(ContractFiles.operations());
    }

    @Test
    void everyEndpointIsInContract() {
        assertThat(ContractFiles.operations()).containsAll(implementedOperations());
    }

    @Test
    void verdictSerializesAsNameNotOrdinal() {
        // The application's own mapper, so a global setting such as WRITE_ENUMS_USING_INDEX would be caught (K20).
        assertThat(jsonMapper.writeValueAsString(Verdict.COULD_NOT_VERIFY)).isEqualTo("\"COULD_NOT_VERIFY\"");
    }

    /** Endpoints of our own controllers as "GET /api/system/ping"; framework handlers such as /error are skipped. */
    private Set<String> implementedOperations() {
        String ownPackage = NutriScanApplication.class.getPackageName();
        Set<String> operations = new TreeSet<>();
        handlerMapping.getHandlerMethods().forEach((RequestMappingInfo info, HandlerMethod handler) -> {
            if (!handler.getBeanType().getPackageName().startsWith(ownPackage)) {
                return;
            }
            // A mapping without a method restriction answers every method; the contract never allows that.
            assertThat(info.getMethodsCondition().getMethods()).as("HTTP method of %s", handler).isNotEmpty();
            info.getMethodsCondition().getMethods().forEach(method -> info.getPatternValues()
                    .forEach(path -> operations.add(method.name() + " " + path)));
        });
        return operations;
    }
}
