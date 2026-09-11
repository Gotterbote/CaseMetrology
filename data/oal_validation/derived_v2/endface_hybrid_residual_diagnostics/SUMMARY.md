# Endface-Hybrid V2 Residual Diagnostics

**Diagnostic only. No estimator parameters are changed by this analysis.**

## Population-level tail

- PCA pooled P95 pairwise repositioning: 0.003994 in
- Hybrid pooled P95 pairwise repositioning: 0.003021 in
- Hybrid pairwise differences <= 0.001 in: 109/180
- Hybrid pairwise differences <= 0.002 in: 147/180
- Hybrid pairwise differences > 0.002 in: 33/180
- Hybrid pairwise differences > 0.003 in: 12/180
- Specimens with hybrid range <= 0.002 in: 40/60
- Specimens with hybrid range > 0.002 in: 20/60
- Specimens with hybrid range > 0.003 in: 10/60
- Specimens with hybrid range > 0.004 in: 2/60

## PCA-versus-hybrid association

- Specimen range Pearson correlation: 0.8755
- Specimen range Spearman correlation: 0.7746
- Within-specimen centered observation Pearson correlation: 0.9068
- Within-specimen centered observation Spearman correlation: 0.8676

High centered-observation correlation means the two different estimators tend to move in the same direction on the same physical placement, which is evidence for a shared placement/pose component rather than independent endpoint noise.

## Upper-tail concentration

- Nearest-rank P95 upper-tail observations considered: 10
- Unique specimens contributing to PCA upper tail: 8
- Unique specimens contributing to hybrid upper tail: 8
- Specimens present in both estimator upper tails: 5
- Overlap specimen IDs: 48, 70, 106, 189, 194

### Hybrid upper-tail observations

- Part 48, rounds 1-3: 0.004557 in
- Part 106, rounds 1-3: 0.004205 in
- Part 70, rounds 2-3: 0.003938 in
- Part 75, rounds 2-3: 0.003818 in
- Part 48, rounds 1-2: 0.003772 in
- Part 189, rounds 2-3: 0.003452 in
- Part 118, rounds 2-3: 0.003279 in
- Part 194, rounds 2-3: 0.003256 in
- Part 118, rounds 1-2: 0.003099 in
- Part 221, rounds 1-2: 0.003021 in

## Fifteen largest hybrid specimen ranges

- Part 48 (near_usl_in_spec): hybrid 0.004557 in; PCA 0.004245 in; change -0.000312 in
- Part 106 (above_usl): hybrid 0.004205 in; PCA 0.005199 in; change +0.000994 in
- Part 70 (near_usl_in_spec): hybrid 0.003938 in; PCA 0.004823 in; change +0.000885 in
- Part 75 (below_lsl): hybrid 0.003818 in; PCA 0.003663 in; change -0.000154 in
- Part 189 (central_nominal): hybrid 0.003452 in; PCA 0.004024 in; change +0.000573 in
- Part 118 (near_usl_in_spec): hybrid 0.003279 in; PCA 0.003654 in; change +0.000375 in
- Part 194 (near_lsl_in_spec): hybrid 0.003256 in; PCA 0.004728 in; change +0.001471 in
- Part 221 (near_lsl_in_spec): hybrid 0.003021 in; PCA 0.003671 in; change +0.000650 in
- Part 127 (central_nominal): hybrid 0.003014 in; PCA 0.002869 in; change -0.000146 in
- Part 51 (above_usl): hybrid 0.003004 in; PCA 0.002973 in; change -0.000031 in
- Part 15 (near_usl_in_spec): hybrid 0.002980 in; PCA 0.003564 in; change +0.000584 in
- Part 30 (near_usl_in_spec): hybrid 0.002962 in; PCA 0.004018 in; change +0.001056 in
- Part 225 (near_usl_in_spec): hybrid 0.002917 in; PCA 0.003994 in; change +0.001077 in
- Part 85 (below_lsl): hybrid 0.002806 in; PCA 0.004121 in; change +0.001316 in
- Part 69 (near_usl_in_spec): hybrid 0.002530 in; PCA 0.003931 in; change +0.001401 in

## Ten largest specimen-level improvements

- Part 151: PCA 0.002588 in -> hybrid 0.000325 in (+0.002263 in)
- Part 200: PCA 0.002430 in -> hybrid 0.000678 in (+0.001752 in)
- Part 136: PCA 0.002067 in -> hybrid 0.000418 in (+0.001649 in)
- Part 194: PCA 0.004728 in -> hybrid 0.003256 in (+0.001471 in)
- Part 69: PCA 0.003931 in -> hybrid 0.002530 in (+0.001401 in)
- Part 85: PCA 0.004121 in -> hybrid 0.002806 in (+0.001316 in)
- Part 161: PCA 0.003188 in -> hybrid 0.002006 in (+0.001181 in)
- Part 219: PCA 0.002607 in -> hybrid 0.001505 in (+0.001102 in)
- Part 215: PCA 0.002094 in -> hybrid 0.001007 in (+0.001087 in)
- Part 225: PCA 0.003994 in -> hybrid 0.002917 in (+0.001077 in)

## Specimens worsened by the hybrid

- Part 131: PCA 0.001334 in -> hybrid 0.002135 in (-0.000801 in)
- Part 233: PCA 0.000521 in -> hybrid 0.001044 in (-0.000523 in)
- Part 123: PCA 0.000274 in -> hybrid 0.000687 in (-0.000413 in)
- Part 204: PCA 0.000857 in -> hybrid 0.001258 in (-0.000401 in)
- Part 172: PCA 0.000865 in -> hybrid 0.001198 in (-0.000333 in)
- Part 48: PCA 0.004245 in -> hybrid 0.004557 in (-0.000312 in)
- Part 53: PCA 0.001852 in -> hybrid 0.002069 in (-0.000217 in)
- Part 188: PCA 0.000466 in -> hybrid 0.000676 in (-0.000210 in)
- Part 75: PCA 0.003663 in -> hybrid 0.003818 in (-0.000154 in)
- Part 127: PCA 0.002869 in -> hybrid 0.003014 in (-0.000146 in)
- Part 72: PCA 0.001389 in -> hybrid 0.001472 in (-0.000083 in)
- Part 86: PCA 0.000728 in -> hybrid 0.000795 in (-0.000067 in)
- Part 9: PCA 0.000614 in -> hybrid 0.000645 in (-0.000031 in)
- Part 51: PCA 0.002973 in -> hybrid 0.003004 in (-0.000031 in)
- Part 100: PCA 0.001632 in -> hybrid 0.001654 in (-0.000022 in)

## Round-pair comparison

- Rounds 1-2: hybrid mean signed +0.000192 in; P95 abs 0.002996 in; max abs 0.003772 in
- Rounds 1-3: hybrid mean signed +0.000083 in; P95 abs 0.002980 in; max abs 0.004557 in
- Rounds 2-3: hybrid mean signed -0.000108 in; P95 abs 0.003279 in; max abs 0.003938 in

## Stratum comparison

- above_usl: n=8; P95 pairwise 0.003004 in; max pairwise 0.004205 in
- below_lsl: n=8; P95 pairwise 0.002806 in; max pairwise 0.003818 in
- central_nominal: n=16; P95 pairwise 0.002996 in; max pairwise 0.003452 in
- near_lsl_in_spec: n=14; P95 pairwise 0.002419 in; max pairwise 0.003256 in
- near_usl_in_spec: n=14; P95 pairwise 0.003772 in; max pairwise 0.004557 in

## Interpretation guardrail

This analysis is intended only to localize the residual error mechanism. It must not be used to change the already-frozen endface-hybrid estimator parameters. Any new software hypothesis should be physically motivated and developed on non-formal development data before prospective validation.
