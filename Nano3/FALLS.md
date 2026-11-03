# Named falls and corrections

## FALL-001 — Incomplete run-record template in v0.1.0

- **Detected:** 2026-10-28, during a coverage review of the package created in this work session.
- **Previous release:** `LOVE-OPERATIONAL-TEST-KIT-0.1.0.zip`
- **Previous ZIP SHA-256:** `3b2fd54f0826f4e327d35e6b3b3ed7e5342ff6a4e94e7993d0c62991e44a580b`
- **Defect:** `RUN-RECORD-TEMPLATE.json` contained only one case record (`LOVE-001`) despite defining 12 probes. A user could have treated the template as complete and omitted the other 11 cases.
- **Impact:** the template did not itself enforce complete case coverage; the validator checked only that the `cases` field was a list. It did not catch the missing 11 records.
- **Correction in v0.1.1:** provide one `NOT_RUN` record for every probe; validate unique case IDs, exact coverage against `probes.json`, and required fields for every run record. Add regression tests that reject missing or duplicate case records.
- **Preservation:** v0.1.0 ZIP remains unchanged under its original checksum. v0.1.1 is a new release; this entry is not retroactively rewritten into the previous ZIP.

This record documents a defect in the kit itself. It is not a model failure and it does not establish the kit's scientific validity.
