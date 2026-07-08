# MaoField D708 Extra SubPro A/E Identity Check Node19 Delivery

## Delivery

- Date verified: `2026-07-08 12:45 CST`
- Source host: node36
- Destination host: node19 (`192.168.31.19`)
- Destination directory:
  `C:\Users\amd\Desktop\MaoField_D708_ExtraSubPro_AE_IdentityCheck_20260708_1245`
- Follow-up direct desktop copies added after PI reported the files were not
  visible at desktop root:
  `C:\Users\amd\Desktop`

Delivered files:

```text
MaoField_PRO_D708_ExtraSubPro_AE_IdentityCheck_20260708_1245.zip
START_HERE_SUBPRO_A_FINITE_MATH_IDENTITY_CHECK_20260708.md
START_HERE_SUBPRO_E_REDTEAM_IDENTITY_CHECK_20260708.md
SHA256SUMS_20260708_1245_extra_subpro_ae_identity_check.txt
```

## Readback

Remote node19 readback reported:

```text
MaoField_PRO_D708_ExtraSubPro_AE_IdentityCheck_20260708_1245.zip  279587
SHA256SUMS_20260708_1245_extra_subpro_ae_identity_check.txt          377
START_HERE_SUBPRO_A_FINITE_MATH_IDENTITY_CHECK_20260708.md          3750
START_HERE_SUBPRO_E_REDTEAM_IDENTITY_CHECK_20260708.md              3236
```

Remote SHA256 readback:

```text
ZIP_SHA256=60829B2365577D77FF63237E7C9CF9315BF1D068634BA2B43B1D93C2860236CB
PROMPT_A_SHA256=E8DD772CCF96B56000D0D61B1B88947CC0B676CEB822D9BD982CCB7AE3F27801
PROMPT_E_SHA256=6B38C0EB71604AD425FD207B0D721A404B9F49B1E9F2B590149577736841A540
```

These match the canonical source hashes.

## Follow-Up Desktop Root Copy

At `2026-07-08 13:09 CST`, the same four files were copied from the delivery
subdirectory to the node19 desktop root for easier manual selection:

```text
C:\Users\amd\Desktop\MaoField_PRO_D708_ExtraSubPro_AE_IdentityCheck_20260708_1245.zip
C:\Users\amd\Desktop\START_HERE_SUBPRO_A_FINITE_MATH_IDENTITY_CHECK_20260708.md
C:\Users\amd\Desktop\START_HERE_SUBPRO_E_REDTEAM_IDENTITY_CHECK_20260708.md
C:\Users\amd\Desktop\SHA256SUMS_20260708_1245_extra_subpro_ae_identity_check.txt
```

Desktop-root readback:

```text
MaoField_PRO_D708_ExtraSubPro_AE_IdentityCheck_20260708_1245.zip  279587
SHA256SUMS_20260708_1245_extra_subpro_ae_identity_check.txt          377
START_HERE_SUBPRO_A_FINITE_MATH_IDENTITY_CHECK_20260708.md          3750
START_HERE_SUBPRO_E_REDTEAM_IDENTITY_CHECK_20260708.md              3236
ZIP_SHA256=60829B2365577D77FF63237E7C9CF9315BF1D068634BA2B43B1D93C2860236CB
```

## Use

Use the same zip for both extra Pro sessions.

- Paste `START_HERE_SUBPRO_A_FINITE_MATH_IDENTITY_CHECK_20260708.md` into the
  finite-math review session.
- Paste `START_HERE_SUBPRO_E_REDTEAM_IDENTITY_CHECK_20260708.md` into the
  red-team review session.

Both sessions must use the attached zip for MaoField repository facts.
