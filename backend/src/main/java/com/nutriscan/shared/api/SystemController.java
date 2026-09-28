package com.nutriscan.shared.api;

import org.springframework.boot.info.BuildProperties;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** System endpoints of contracts/openapi/system.yaml. Paths come from the contract; ContractConformanceTests holds them together. */
@RestController
@RequestMapping("/api/system")
class SystemController {

    private final BuildProperties build;
    private final DatabaseProbe database;

    // BuildProperties is required: without build info (springBoot.buildInfo) the application does not start,
    // instead of reporting a made-up version.
    SystemController(BuildProperties build, DatabaseProbe database) {
        this.build = build;
        this.database = database;
    }

    @GetMapping("/ping")
    PingResponse ping() {
        return new PingResponse(build.getVersion(), database.check());
    }
}
