package com.nutriscan.shared.api;

/** Body of GET /api/system/ping; mirrors contracts/openapi/system.yaml#PingResponse. */
record PingResponse(String version, DatabaseStatus database) {
}
