/**
 * Household Planning Engine (MSM: menu + package sizes + pantry/expiry + up to two markets).
 * Candidates come only through safety, never from catalog's raw product list; decisions go to audit (08 §3.a).
 * Event interfaces (catalog/pantry/household :: events) are added here when those events exist.
 */
@ApplicationModule(allowedDependencies = {"safety", "audit"})
package com.nutriscan.planning;

import org.springframework.modulith.ApplicationModule;
