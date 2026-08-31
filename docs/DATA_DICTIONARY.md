# Data dictionary

| Layer | Directory | Unit / content | Public status |
|---|---|---|---|
| Frozen results | `data/processed/results/` | Phase 23 and GLM adjudication objects and freeze receipts | Public |
| Figure source data | `data/processed/source_data/` | CSV, JSON and figure-specific XLSX workbooks | Public |
| Frozen statistics | `data/processed/statistics/` | Documentation and public sufficient-statistic layer | Public |
| Typed missingness | `data/processed/typed_missingness/` | Registered failure/missingness categories; not encoded as zero | Public |
| Failure ledger | `data/processed/failure_ledger/` | Append-only failure evidence and descriptive counts | Public |
| Raw trajectories | `data/raw/` plus controlled archive | Request, response, tool and terminal evidence | De-identified public subset where permitted; full reviewer-only |
| Assignment material | controlled archive | Post-unblinding maps, commitments and joins | Reviewer-only; public derivative hashes |
| Hidden-answer material | controlled/private archive | Sealed tests/truth and integrity evidence | Reviewer-only where permitted; otherwise private |
| Secrets/private keys | never released | Credentials and decryption material | Private |

Every row-level failure remains typed. `NOT_IDENTIFIED` is not encoded as zero, and complete-case filtering may not rescue a frozen result.
