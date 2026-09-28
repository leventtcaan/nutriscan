/**
 * Shared kernel. Base package: common value types such as {@link com.nutriscan.shared.Verdict}, the only part other
 * modules may use. Sub-package {@code api}: system endpoints (contracts/openapi/system.yaml), internal.
 * Depends on nothing; every module may use it (see @Modulithic).
 */
@ApplicationModule(allowedDependencies = {})
package com.nutriscan.shared;

import org.springframework.modulith.ApplicationModule;
