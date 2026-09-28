/**
 * Privacy Gate: the single egress for external LLM calls (K06, K18). Depends on no domain module.
 */
@ApplicationModule(allowedDependencies = {})
package com.nutriscan.privacy;

import org.springframework.modulith.ApplicationModule;
