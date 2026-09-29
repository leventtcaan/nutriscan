package com.nutriscan.shared;

/**
 * Outcome of checking an item against a household member's constraints; mirrors contracts/openapi/shared.yaml#Verdict.
 * There is deliberately no "safe" value. Missing, stale, conflicting or unrecognised data yields
 * {@link #COULD_NOT_VERIFY}, never a more permissive value (S8, K03). Serialized by name, never by ordinal (K20).
 */
public enum Verdict {
    NOT_SUITABLE,
    CAUTION,
    NO_CONFLICT_FOUND,
    COULD_NOT_VERIFY
}
