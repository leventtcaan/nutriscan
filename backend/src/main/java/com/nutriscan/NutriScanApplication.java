package com.nutriscan;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.modulith.Modulithic;

/**
 * Every direct sub-package of {@code com.nutriscan} is an application module (Spring Modulith).
 * {@code shared} is declared a shared module, so every module may depend on it without listing it.
 */
@SpringBootApplication
@Modulithic(sharedModules = "shared")
public class NutriScanApplication {

    public static void main(String[] args) {
        SpringApplication.run(NutriScanApplication.class, args);
    }
}
