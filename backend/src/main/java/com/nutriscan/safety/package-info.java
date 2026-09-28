/**
 * Rule engine (allergens + health conditions, four verdicts). Records decisions in audit (08 §3.a contracts table).
 */
@ApplicationModule(allowedDependencies = {"audit"})
package com.nutriscan.safety;

import org.springframework.modulith.ApplicationModule;
