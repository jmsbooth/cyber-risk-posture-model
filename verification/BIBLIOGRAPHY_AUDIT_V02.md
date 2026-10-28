# CRPI bibliography integrity review, draft v0.2

**Disposition:** internal citation-key checks completed; source-by-source scholarly verification is still a publication gate. This file is not a representation that all 30 references have been externally validated.

## Automated source integrity

The revised manuscript references 30 bibliography identifiers. Run `python scripts/check_publication_source.py` to ensure all cited identifiers are defined, labels and references resolve, source section order remains intact, and the manuscript uses SOE instead of the legacy USOM label. This static check does **not** prove the listed publications exist or that the surrounding claims are properly attributed.

## Publisher/standards checks already completed

- NIST SP 800-55 Volume 1, *Measurement Guide for Information Security: Volume 1 - Identifying and Selecting Measures* (December 2024), official record: https://csrc.nist.gov/pubs/sp/800/55/v1/final. Manuscript title corrected.
- NIST SP 800-55 Volume 2, *Measurement Guide for Information Security: Volume 2 - Developing an Information Security Measurement Program* (December 2024), official record: https://csrc.nist.gov/pubs/sp/800/55/v2/final. Manuscript title corrected.
- NIST IR 8286 Revision 1, *Integrating Cybersecurity and Enterprise Risk Management (ERM)* (December 2025), official record: https://csrc.nist.gov/pubs/ir/8286/r1/final.
- DRIMAX (2026), published article DOI: https://doi.org/10.1016/j.cose.2026.105061; bibliography record is consistent with the publisher listing at https://www.sciencedirect.com/science/article/pii/S0167404826002373.

## Required remaining audit

Before a public release, verify **each** bibliography item against its publisher or standard owner for exact author order, title, publication edition, year, volume, pages or article identifier, DOI/URL, and the claim that its citation actually supports. Pay special attention to the novelty comparison with dynamic-risk work, historical versions of CIS Controls/CVSS/EPSS and the provenance and limitations of the public CVE and KEV count series.

Do not mark the manuscript *externally source-verified* until this item-level audit and reviewer confirmation are complete.
