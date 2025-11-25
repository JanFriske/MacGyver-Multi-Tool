# QA & Validation Strategy for Internationalization

## 1. Objective
Ensure that all 98+ supported languages and dialects are functional, structurally complete, and correctly displayed in the UI. Eliminate "fallback errors" where German text appears in other languages.

## 2. Automated Audit (Implemented)
We have developed `scripts/audit_translations.py` to systematically check all language files against the master `de.json`.

### Audit Criteria:
1.  **Missing Keys:** Keys present in `de.json` but missing in the target language.
2.  **Suspicious Identity:** Values that are identical to the German original (indicating potential copy-paste errors or failed translation), excluding short words/numbers.
3.  **Structure:** JSON validity (already handled by `validate_languages.py`).

### Current Findings:
*   **English (`en`):** Structurally complete. `menu.tools` exists and differs from German. (Investigation into UI display issue ongoing).
*   **Other Languages:** Many languages are missing ~20-30 keys (likely the new `menu_languages` block and recent tool additions).

## 3. Remediation Plan

### Step 1: Fix Missing Keys (Batch Processing)
*   **Action:** Create `scripts/fill_missing_keys.py`.
*   **Logic:** For every missing key in a language file, inject the value from `en.json` (English) as a better fallback than German. Mark these injected values with a prefix like `[EN]` or just use the English text to ensure functionality.
*   **Target:** Eliminate all "MISSING" errors in the audit report.

### Step 2: Investigate "Werkzeuge" Bug
*   **Problem:** English UI shows "Werkzeuge" despite `en.json` containing "Tools".
*   **Hypothesis:** Race condition in UI update or caching issue.
*   **Action:** Instrument `view.py` with debug logging to trace the `tr()` call for `menu.tools` during runtime.

### Step 3: Visual Verification
*   **Action:** Manually verify a subset of diverse languages:
    *   **Tier 1:** English, French, Spanish (Standard LTR).
    *   **Tier 2:** Arabic, Hebrew (RTL support check).
    *   **Tier 3:** Chinese, Japanese (Font rendering check).
    *   **Tier 4:** German Dialects (Dialect authenticity check).

## 4. Prevention
*   **Pre-Commit Hook:** Run `audit_translations.py` before committing changes to `i18n/translations`.
*   **Fallback Mechanism:** Ensure `I18nService` falls back to English if German is not the target language.
