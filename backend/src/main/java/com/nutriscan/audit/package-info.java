/**
 * Append-only decision log. Consumer of every decision-making module; depends on none of them.
 */
@ApplicationModule(allowedDependencies = {})
package com.nutriscan.audit;

import org.springframework.modulith.ApplicationModule;
