/**
 * Constraint-aware recommendation. Candidates pass through safety first; decisions go to audit (08 §3.a).
 */
@ApplicationModule(allowedDependencies = {"safety", "audit"})
package com.nutriscan.recommendation;

import org.springframework.modulith.ApplicationModule;
