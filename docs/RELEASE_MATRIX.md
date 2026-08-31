# Public / reviewer-only / private release matrix

| Material | Public | Reviewer-only | Private / never release | Reason |
|---|---:|---:|---:|---|
| Manuscript, Supplement, figures and source-data tables | Yes | Yes | No | Core paper materials; original data/docs under CC BY 4.0 |
| Frozen contracts, claims and processed result JSON | Yes | Yes | No | Claim and analysis auditability |
| Figure, validator and offline analysis code | Yes | Yes | No | Apache-2.0 code reproduces public checks and displays |
| Redistributable requests/responses | Where permitted | Yes | No | Provider terms may constrain public release |
| Raw trajectories and post-unblinding assignments | De-identified subset or hashes | Yes | No | Full audit under controlled access |
| Sealed hidden-answer material | No | Where permitted and secure | Yes otherwise | Preserve integrity and comply with restrictions |
| API keys, DPAPI/private keys, credentials | No | No | Yes | Security |
| Editorial correspondence | No | No | Yes | Confidentiality |

The reviewer-only tier is governed by `docs/CONTROLLED_ACCESS_POLICY.md`; complete requests receive a response within 14 business days. This repository contains only the future public tier and explanatory placeholders for the other tiers. It does not contain reviewer-only archives, credentials, private keys, restricted provider content or reusable hidden answers.

