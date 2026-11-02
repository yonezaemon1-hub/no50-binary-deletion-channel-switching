# No.50: Finite-Length Switching and Limitations of Recursive Constructions in Binary Deletion Channels

Ryutaro Yonezu — Independent Researcher  
Version **v1.0** · November 2, 2026 · **Preprint** · **All rights reserved**

This package is the v1.0 publication artifact. Actual publication completion and public URLs are confirmed separately in the repository and publication receipt after registration.

## Established finite-length results

The exact minimum total-variation distance between one-trace deletion-channel laws is certified over the full deletion-probability range for binary input lengths four through eight. The counts concern changes of the **optimizing distance polynomial**, rather than identities of pairs with the same polynomial.

| Input length | Interior polynomial switches |
| --- | ---: |
| 4 | 1 |
| 5 | 1 |
| 6 | 2 |
| 7 | 3 |
| 8 | 3 |

The computer-assisted proof uses exact integer subsequence counts, coefficientwise domination, rational Bernstein inequalities, and algebraic root isolation. A fixed-length local-stability lemma is included without a novelty claim.

## Failed proof strategy and unresolved conjecture

- Unbounded growth of switching complexity was **not proved**.
- Universal preservation of global optimality at the same deletion probability under common-bit insertion is **false**: all 256 insertion operations from the two length-seven optimizers at q=4/5 fail to reach the length-eight optimum at that same q.
- This counterexample **does not disprove** the unbounded-switching conjecture itself.
- Migration of optimality to a different deletion-probability interval was observed in a specific example. It is **not a general theorem** and provides no proved recurrence for all lengths.
- Exploratory calculations for lengths 9–12 and length 16 are outside the accepted claims and certificates.

The failed generalization is part of the research record; it has not been removed or represented as a successful general theorem.

## Audit and reproduction status

- Mathematics: **Finite-length results PASS** (computer-assisted).
- Independent AI audit: **PASS for finite-length results**, using the outcome supplied in the author's publication instruction.
- Windows PowerShell reproduction: **PASS for v0.2.1**, reported by the author on 2026-11-02 with `ALL PASS: HASH + FINITE PROOFS + INDEPENDENT TV CHECK`.
- Complete external-auditor and Windows transcripts were not included in the supplied ZIP; these supplied results are distinct from this release's accompanying rerun logs.
- General conjecture: **UNPROVEN**.
- Novelty: **INCONCLUSIVE**. This preprint has **not undergone human peer review**.

Novelty has not been conclusively established. This preprint has not undergone human peer review. The conjectured unbounded growth in switching complexity remains unproved.

## Files and reproduction

- `paper/No50_v1.0_PREPRINT_20261102.pdf` and `.md`: publication PDF and matching manuscript.
- `code/verify_no50.py`: n=4,5 exact certificates, n=7 witness checks, and the 256-operation counterexample.
- `code/verify_envelope_n6_n8.py`: all-parameter finite envelopes for n=6,7,8.
- `code/independent_mask_audit.py`: a separate deletion-mask implementation, checking exhaustive TV minima at 12 rational checkpoints. These checkpoints do not independently prove the whole parameter interval.
- `evidence/`: the three frozen original JSON files.
- `run_audit_windows.ps1`: the unchanged fail-closed Windows PowerShell audit script.
- `audit/RESEARCH_CHRONOLOGY_JA.md` and the other historical audit documents: original research and failure records, preserved unchanged.
- `frozen/`: the exact original v0.2.1 ZIP, preserving all earlier documents, title and status labels.
- `audit/RELEASE_V1_METADATA_AND_AUDIT.md`: current audit provenance and metadata changes.
- `audit/PROTECTED_SOURCE_SHA256.json`: protected source-file and mathematical-body hashes.
- `SHA256SUMS.txt`: all shipped files except itself. Generated `audit_output/` is excluded.

On Windows PowerShell 5.1 with Python 3.10 or later, run from the extracted package root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_audit_windows.ps1
```

The script checks the manifest before running Python, writes only under `audit_output/`, and stops on any error. Each generated JSON must match its corresponding frozen JSON **byte for byte**. No third-party Python package, GPU, internet access or paid API is required.

The script and the Python verifiers retain historical v0.2/AUDIT HOLD console labels to preserve the audited code byte for byte. They refer to their original development stage. Current version, audit provenance, and publication confirmation belong to `STATUS.txt`, this README, and the separate publication receipt.

## Rights and claim limits

Copyright (c) 2026 Ryutaro Yonezu. **All rights reserved.** No open-source or Creative Commons license is granted. Classical subsequence-deck methods, the elementary certification technique and local stability are not claimed as new. See `references/SOURCES.md` and the manuscript references. No priority guarantee, human peer-review claim, or general unbounded-switch theorem is made.
