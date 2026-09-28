/**
 * LLM orchestration; never decides (K01). Calls planning tools, reaches the LLM only via privacy (08 §3.a).
 */
@ApplicationModule(allowedDependencies = {"privacy", "planning"})
package com.nutriscan.assistant;

import org.springframework.modulith.ApplicationModule;
