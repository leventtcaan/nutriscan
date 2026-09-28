/**
 * Label/receipt reading (demo lane). Model calls leave only through privacy (08 §3.a: privacy -> vision).
 */
@ApplicationModule(allowedDependencies = {"privacy"})
package com.nutriscan.vision;

import org.springframework.modulith.ApplicationModule;
