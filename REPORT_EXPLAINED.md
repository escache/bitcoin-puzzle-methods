# Bitcoin research — explained method inventory

244 entries. This expands the historical inventory with method-specific mechanisms and actual implementation behavior. Source review is not a rerun or certification of historical claims.

## Reading the pipeline

A candidate is an integer k. The public point is Q=k*G on secp256k1. For P2PKH, serialize Q, apply SHA-256 then RIPEMD-160, and compare with the target address payload. Left-padding k to 32 bytes changes its encoding, not its value. A public address is not the same input as the full public point required by an interval discrete-log solver.

Generating a candidate, checking a candidate, searching an interval completely, and predicting a smaller interval are four different operations. A million records may describe a million partitions but only one tested representative in each.

## Important implementation findings

- The active checker performs real public-point/HASH160 comparisons and reuses incremental public points for speed.
- The inspected CTheory D1 CUDA kernel is a stub returning unavailable/error; readiness flags are not kernel implementation evidence.
- The ECDLP simulation runs real BSGS only in configured small-range branches. Larger Shor/hybrid outcomes are random model draws with modeled times; they are not key recoveries.
- Statistical tests consume disclosed keys and null controls. Their output is evidence about a model, not an unknown scalar.

## Working vocabulary

- **Scalar/private key:** an integer; leading zero padding is a fixed-width byte representation.
- **Public point:** k times the curve generator; required for kangaroo/BSGS.
- **Address hash:** hash of a serialized public point, not the point itself.
- **Shard:** a chosen interval or work unit, not automatically a tested key.
- **Root/remainder:** coordinates encoding an integer; smaller coordinates do not automatically mean less total uncertainty.
- **Prior:** an assumed/predicted distribution used to allocate effort; it must be independently validated.
- **Containment:** the answer lies in a proposed set, checked afterward using a known answer.
- **Oracle:** extra information supplied to a test; when synthetic it must not be represented as discovered data.
- **Synthetic test:** deliberately constructed data with known ground truth.
- **Held-out:** excluded from the fit; repeated prior access can still make an experiment retrospective.
- **p-value/evidence score:** a statistic under stated null assumptions, not a probability that a target interval is correct.
- **Backend:** the implementation doing computation; replacing Python with Rust/CUDA changes speed, not the target equation.

## Verification, sampling and live search

### M001 — Public puzzle corpus verification

**Evidence:** Executed record

**How it works.** A candidate scalar determines a public point and address hash. Recomputing those values detects an incorrect published key or mismatched database row.

**What is actually done.** Read filled private-key rows, derive the recorded public-key format, and compare with stored point/HASH160 fields. Empty rows remain unknown; passing the check does not discover their keys.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Recorded public scalars are checked against secp256k1 points and HASH160; validates the dataset, not a prediction.

**Sources.** [S133: FEASIBILITY_REVALIDATION_20260918.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/FEASIBILITY_REVALIDATION_20260918.md); [S024: backtest.py](/home/arialmohan/puzzle71-educational/backtest.py)

### M002 — Small-range exhaustive address search

**Evidence:** Executed record

**How it works.** Enumerate every integer in a genuinely small interval and accept only an address match. Exhaustion gives a complete answer for that interval.

**What is actually done.** The educational tests scan puzzles 1-10 directly. Their keys are already public and used afterward to validate the results; this demonstrates a correct checker at small scale.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Puzzles 1-10 scanned completely; each yielded the expected published key. Small-range recovery is not an unknown-key breakthrough.

**Sources.** [S023: BACKTEST.md](/home/arialmohan/puzzle71-educational/BACKTEST.md); [S024: backtest.py](/home/arialmohan/puzzle71-educational/backtest.py)

### M003 — Full-range seeded sampling backtests

**Evidence:** Executed record

**How it works.** A seeded sampler chooses a reproducible order of candidates. The verifier stops when a candidate produces the target address.

**What is actually done.** Saved subprocess backtests run the actual checker on small solved puzzles and compare recovered values afterward. Counts describe work until a match, not a learned shortcut.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Actual address checkers recovered small published puzzles; seeded search order does not establish predictive narrowing.

**Sources.** [S021: ACTUAL_BACKTEST.md](/home/arialmohan/puzzle71-educational/ACTUAL_BACKTEST.md); [S025: backtest_continuous_17_32.py](/home/arialmohan/puzzle71-educational/backtest_continuous_17_32.py)

### M004 — Uniform within-shard representatives

**Evidence:** Executed record

**How it works.** Divide an interval into nonoverlapping shards and select one integer uniformly within each. This spreads a batch over the advertised range.

**What is actually done.** The corrected generator uses integer randrange calls. One record is one sampled candidate plus its shard boundaries; no other integer in that shard is thereby checked.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Samples one integer per disjoint interval; representative checks do not exhaust their shard.

**Sources.** [S026: candidate_sampling.py](/home/arialmohan/puzzle71-educational/candidate_sampling.py); [S011: pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py)

### M005 — Exact integer partition coverage

**Evidence:** Executed record

**How it works.** Integer division places adjoining boundaries so the first shard starts at the lower limit and the last ends at the upper limit.

**What is actually done.** The corrected partitions function distributes the interval across the requested record count. Tests enumerate small examples to check every integer appears exactly once in the intervals.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Gap-free inclusive intervals replace biased single-key records. Exhaustive small-range checks verify the partition arithmetic.

**Sources.** [S017: test_pipeline.py](/home/arialmohan/puzzle71-corrected/test_pipeline.py); [S003: README.md](/home/arialmohan/puzzle71-corrected/README.md)

### M006 — No-repeat affine shard permutations

**Evidence:** Implemented

**How it works.** An affine permutation visits offsets using (offset + index*stride) modulo shard size. A coprime stride prevents repetition before exhausting the shard.

**What is actually done.** The samplers store per-shard offsets, strides and a traversal position. They reconstruct candidates without storing all previously visited keys; this improves coverage accounting, not target likelihood.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Coprime strides enumerate each shard without a visited-key set; retains full support.

**Sources.** [S026: candidate_sampling.py](/home/arialmohan/puzzle71-educational/candidate_sampling.py); [S031: test_unique_sampling.py](/home/arialmohan/puzzle71-educational/test_unique_sampling.py)

### M007 — One-million sample-key verification

**Evidence:** Executed record

**How it works.** Derive both public-key serializations for each stored sample and compare their HASH160 values with the decoded target hash.

**What is actually done.** The verifier read the million-record JSONL file, padded each sample_key to 32 bytes, and performed two comparisons per scalar. The saved report records no match.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** One million explicit samples checked in both public-key serializations; no target match.

**Sources.** [S018: verification-1M.json](/home/arialmohan/puzzle71-corrected/verification-1M.json)

### M008 — Range-start and range-end verification

**Evidence:** Executed record

**How it works.** A range boundary is itself a possible private scalar and can be checked exactly like a sample. Checking it does not search its neighboring integers.

**What is actually done.** The endpoint run read range_start and range_end from every record and checked both address formats. It performed two million scalar checks, separately from the earlier samples.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Two million endpoint entries checked in both address formats; no target match. Interiors were not searched.

**Sources.** [S019: verification-boundaries-1M.json](/home/arialmohan/puzzle71-corrected/verification-boundaries-1M.json)

### M009 — Generate-and-verify streaming batches

**Evidence:** Executed record

**How it works.** Generate a candidate, verify it immediately, then discard it unless it matches. Memory does not grow with the batch size.

**What is actually done.** stream_check.py samples one key per partition and saves aggregate counts, a deterministic stream digest and any matches. The seed permits regeneration without a large candidate file.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** One million additional samples checked immediately without a large dataset; no matches in the saved batch.

**Sources.** [S016: stream_check.py](/home/arialmohan/puzzle71-corrected/stream_check.py); [S015: stream-verification-20261019.json](/home/arialmohan/puzzle71-corrected/stream-verification-20261019.json)

### M010 — Continuous affine full-support search

**Evidence:** Live snapshot

**How it works.** Apply one odd-stride affine permutation to all 2^70 interval offsets. Each offset occurs once over a complete cycle.

**What is actually done.** continuous_stream.py generates keys indefinitely until stopped, matched or exhausted. It checkpoints counters and permutation parameters; the process performs actual address checks, not predictor training.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Checkpointed local worker checks an affine permutation of the 70-unknown-bit interval. Status is mutable and must be time-stamped.

**Sources.** [S007: continuous_stream.py](/home/arialmohan/puzzle71-corrected/continuous_stream.py); [S006: status.json](/home/arialmohan/puzzle71-corrected/continuous-run/status.json)

### M011 — Incremental public-point verification

**Evidence:** Executed record

**How it works.** If the next scalar differs by delta, its public point is the old point plus delta*G. Reusing that point avoids repeated full scalar multiplication.

**What is actually done.** point_walk.py caches the two step points needed by the affine traversal, including wraparound. It still serializes and hashes every point; the candidate sequence is unchanged.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Same scalar sequence verified using cached point increments; 900 comparison cases and paired benchmarks passed.

**Sources.** [S013: point_walk.py](/home/arialmohan/puzzle71-corrected/point_walk.py); [S012: point-walk-benchmark.json](/home/arialmohan/puzzle71-corrected/point-walk-benchmark.json)

### M012 — Checkpoint resume and scalar cross-checks

**Evidence:** Implemented

**How it works.** Saving traversal state allows a restart at the next unchecked position. Independent scalar multiplication can detect incremental-point drift.

**What is actually done.** The worker writes an atomic status file and retains its offset/stride across restarts. The optimized version checks the first and each 10,000th point against the original verifier.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Live optimization resumes the exact saved position and compares against full scalar multiplication every 10,000 entries.

**Sources.** [S007: continuous_stream.py](/home/arialmohan/puzzle71-corrected/continuous_stream.py); [S004: WORKING_NOTES.md](/home/arialmohan/puzzle71-corrected/WORKING_NOTES.md)

### M013 — FUSED priority-band traversal with fallback

**Evidence:** Executed record

**How it works.** Search a forecast band first, then its complement. This can improve order under a good predictor without permanently excluding any key.

**What is actually done.** The fixed-budget educational comparison used affine permutations within the band and fallback regions. It checked bounded prefixes, not every integer in the forecast band.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Fixed-budget test retained complementary regions; 286,720 checks across both methods found no keys.

**Sources.** [S030: REPORT.md](/home/arialmohan/puzzle71-educational/computations/blind-fused-30-64-20261018/REPORT.md)

### M014 — Advanced selective FUSED/Delta2 adapter

**Evidence:** Executed record

**How it works.** Turn predicted root/coefficient/remainder combinations into scalar intervals and sample those hypotheses instead of the entire range.

**What is actually done.** The adapter froze training data, retained its natural hypothesis list and checked one representative per shard. A later containment check found that most known evaluation keys were outside those selected intervals.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Selected 12,515 hypothesis shards across puzzles 30-64; only 1/35 known targets was contained.

**Sources.** [S029: REPORT.md](/home/arialmohan/puzzle71-educational/computations/advanced-selective-30-64-20261018/REPORT.md)

### M015 — CPU scalar versus point-walk benchmarking

**Evidence:** Executed record

**How it works.** Compare two verifiers on identical scalar streams. Matching outputs isolate performance changes from candidate-selection differences.

**What is actually done.** The point-walk benchmark compared exact points and hashes, then timed alternating paired trials with matching stream digests. It measures local throughput, not a higher probability per tested key.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Measured acceleration is computational, not evidence of a more likely candidate distribution.

**Sources.** [S005: benchmark_point_walk.py](/home/arialmohan/puzzle71-corrected/benchmark_point_walk.py); [S028: benchmark_point_walk.py](/home/arialmohan/puzzle71-educational/checks/benchmark_point_walk.py)

### M016 — Mock distributed key-generation network

**Evidence:** Implemented

**How it works.** A coordinator hands work units to generator nodes while optional checker nodes consume results. Pull-based scheduling balances unequal workers.

**What is actually done.** mock_keyspace_network.py runs bounded practice batches using processes or threads. Its counters and coverage checks demonstrate orchestration; the mock network is not evidence of a full 71-bit sweep.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Pull-based process/thread workers and checker queues exercise scheduling on bounded mock work; not a full puzzle solve.

**Sources.** [S130: mock_keyspace_network.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/mock_keyspace_network.py); [S077: README.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/README.md)

### M017 — 32-byte padding and dual-format P2PKH checks

**Evidence:** Executed record

**How it works.** A scalar is encoded as exactly 32 big-endian bytes, multiplied by G, serialized and hashed. P2PKH comparisons use the address's decoded 20-byte hash.

**What is actually done.** Existing checkers use key.to_bytes(32,'big'), known scalar-one vectors and compressed/uncompressed formats. They compare HASH160 directly rather than Base58-encoding every generated address, an equivalent target check.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Left-padded scalar inputs, compressed/uncompressed public keys and known scalar-one address vectors guard verifier correctness.

**Sources.** [S020: verify_samples.py](/home/arialmohan/puzzle71-corrected/verify_samples.py); [S027: check_keys.py](/home/arialmohan/puzzle71-educational/check_keys.py)

### M018 — Synthetic fixtures versus disclosed puzzle data

**Evidence:** Executed record

**How it works.** A synthetic fixture can validate pipeline logic because its generation rule is known. It must remain separate from actual published puzzle secrets.

**What is actually done.** PEC37 tools generate synthetic chains and compare them with disclosed puzzle data. Successful synthetic reconstruction tests the fixture rule; it cannot populate undisclosed puzzle-key rows.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** PEC37 stores synthetic 1-160 chains separately and compares them with actual disclosed keys. Synthetic keys are not puzzle recoveries.

**Sources.** [S261: evaluate_synthetic_chain.py](/home/arialmohan/workspace/projects/pec37/tools/evaluate_synthetic_chain.py); [S260: synthetic_chain_evaluation.csv](/home/arialmohan/workspace/projects/pec37/data/synthetic_chain_evaluation.csv)

### M019 — Empirical bit-vote and position forecasting

**Evidence:** Executed record

**How it works.** Train simple position trends or majority votes for fractional bit positions, then evaluate them on later known keys.

**What is actually done.** empirical_key_forensics.py uses disclosed keys, exact rational regressions and bit-vote diagnostics. It measures retrospective prediction accuracy; it does not search unknown Bitcoin addresses.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Retrospective generator-forensics tests fractional-bit votes, exact regressions and baseline predictors on disclosed keys.

**Sources.** [S258: empirical_key_forensics.py](/home/arialmohan/workspace/projects/pec37/data/empirical_key_forensics.py); [S257: empirical_key_forensics.json](/home/arialmohan/workspace/projects/pec37/data/empirical_key_forensics.json)

### M020 — Five-index scale/transition analysis

**Evidence:** Executed record

**How it works.** Normalize every-fifth-puzzle keys to comparable interval positions and ask whether one predicts the next better than a baseline.

**What is actually done.** The downloaded result file records lag correlation, permutation tests, prefix Hamming distances and held-out transition errors. These are saved statistical results, not additional private-key discoveries.

**Inputs needed.** A declared integer interval, target address or public point, candidate-generation parameters and checkpoint/output settings.

**What the result means.** Normalized positions, lag correlations, Hamming similarity and held-out transition forecasts are recorded; no new key is recovered.

**Sources.** [S001: bitcoin_scale5_results.json](/home/arialmohan/Downloads/bitcoin_scale5_results.json)

## Kangaroo, interval ECDLP and execution backends

### M021 — Binary distinguished-point parsing

**Evidence:** Executed record

**How it works.** Distinguished-point dumps encode selected curve points and possibly walk distances. Recovering their layout is necessary before collision algebra has meaning.

**What is actually done.** The parser scans bit/byte layouts, checks candidate x-coordinates and extracts metadata slices. Later scripts test interpretations; a parseable integer is not automatically a valid walk distance.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Extract curve x-coordinates, candidate metadata and distance fields from the supplied binary. Interpretation of metadata remains a hypothesis.

**Sources.** [S102: dp_parser.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/dp_parser.py); [S171: non_bruteforce_audit_20260831.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/non_bruteforce_audit_20260831.md)

### M022 — Tame/wild collision recovery

**Evidence:** Implemented

**How it works.** A tame walk starts from a known scalar; a wild walk starts from the target point. Their meeting relates recorded distances and yields a candidate scalar.

**What is actually done.** collision.py groups same-x entries, tries tame/wild assignments and derives candidates. Because x alone has two point parities, the final scalar must pass exact public-key verification.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Same-point opposite-herd distances yield a scalar when the walk origins and distances are valid. No real target collision is established here.

**Sources.** [S097: collision.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/collision.py); [S077: README.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/README.md)

### M023 — Single-process bounded Pollard kangaroo

**Evidence:** Implemented

**How it works.** Pollard kangaroo uses deterministic pseudo-random jumps so tame and wild walks can merge. Distinguished points reduce the amount of stored walk data.

**What is actually done.** kangaroo.py implements bounded CPU walks, jump tables, point selection and verification. It requires the target public point and a budget; an address hash cannot initialize its wild walk.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Standard interval discrete-log implementation for targets with known public points.

**Sources.** [S109: kangaroo.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/kangaroo.py)

### M024 — Separated tame and wild phases

**Evidence:** Implemented

**How it works.** Build the tame table once, save it, and later walk from the target until a compatible distinguished point is reached.

**What is actually done.** phase.py exposes separate tame and wild commands and table export/loading. This supports separate machines or stages without converting a missing public key into an ECDLP target.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Persist a tame distinguished-point table and search from the target in a separate phase.

**Sources.** [S113: phase.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/phase.py); [S224: ctheory_phase_solver.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/ctheory_phase_solver.py)

### M025 — JeanLucPons / RCKangaroo export

**Evidence:** Implemented

**How it works.** External interval solvers need bounds, a target point and runtime settings in their expected configuration format.

**What is actually done.** Export scripts write JeanLucPons/RCKangaroo inputs from puzzle or slot metadata. They prepare jobs; whether the external executable ran and found a match requires separate logs.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Generate solver configuration files for public-key interval targets; configuration existence is not execution evidence.

**Sources.** [S105: export.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/export.py); [S225: export_ctheory_gpu_d1.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/export_ctheory_gpu_d1.py)

### M026 — Direct D1 interval kangaroo

**Evidence:** Implemented

**How it works.** If k=base+D1, then Q-base*G=D1*G. A known base converts recovery into a smaller interval discrete log.

**What is actually done.** D1 solvers construct the shifted point from guessed root/coefficient coordinates. A wrong base usually makes the true key absent from that interval, so leaf cost alone is incomplete.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Subtract a hypothesized scalar base and search the D1 leaf; useful only if the hypothesized coordinates are correct.

**Sources.** [S129: wrapped_kangaroo.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/wrapped_kangaroo.py); [S152: d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

### M027 — Wrapped CT multi-target kangaroo

**Evidence:** Audited/corrected

**How it works.** Share walks or targets across several related base hypotheses, attempting to reuse work instead of solving each independently.

**What is actually done.** Wrapped-CT code constructs multiple shifted targets. Historical audits inspect span/setup growth and find that the advertised tiny-span benefit does not transfer unconditionally to high-index targets.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Historical small-span speed claims fail on large required spans; later audits reject unconditional recovery-cost reductions.

**Sources.** [S129: wrapped_kangaroo.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/wrapped_kangaroo.py); [S152: d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

### M028 — CPU banded baby-step/giant-step D1 hunts

**Evidence:** Executed record

**How it works.** BSGS stores small point multiples, then subtracts larger multiples from the target to find a match in a bounded interval.

**What is actually done.** cpu_band_d1_hunt.py builds baby tables for selected D1 bands and scans giant steps. Saved deployments used CPU work even on some GPU-equipped hosts; that is not a CUDA benchmark.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Bounded D1-band runs are documented; CPU tasks on GPU-equipped pods must not be described as GPU kernel execution.

**Sources.** [S223: cpu_band_d1_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/cpu_band_d1_hunt.py); [S132: CTHEORY_MATH_REVIEW_20260920.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/CTHEORY_MATH_REVIEW_20260920.md)

### M029 — Prior-weighted stratified kangaroo

**Evidence:** Implemented

**How it works.** Split a known-point interval into strata and allocate more tame-walk effort where a supplied prior assigns greater probability.

**What is actually done.** pwsk.py builds a smoothed histogram, assigns budgets using prior mass and width, and searches against a shared wild herd. Its benefit depends on the supplied prior actually predicting targets.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Reweights interval effort when a genuine prior exists; flat priors reduce to ordinary allocation. Prior quality is unestablished for the unknown puzzle.

**Sources.** [S116: pwsk.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/pwsk.py); [S091: demo_pwsk.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/demo_pwsk.py)

### M030 — Prior-weighted GPU slot budgets

**Evidence:** Implemented

**How it works.** Reweight work across already constructed slots without changing what each slot represents. Higher prior mass receives a larger hop budget.

**What is actually done.** pwsk_budget.py combines FUSED-distance and optional D1 histogram weights, rounds allocations and annotates manifests. It changes scheduling, not the set of possible scalar equations.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Allocate existing slot budgets using FUSED distance or empirical D1 histograms without changing slot geometry.

**Sources.** [S117: pwsk_budget.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/pwsk_budget.py)

### M031 — Rust native herd stepping

**Evidence:** Implemented

**How it works.** Move repeated curve-walk operations out of the Python interpreter into compiled native code. The mathematical search remains the same.

**What is actually done.** The Rust extension provides herd stepping and native lookup operations called by the Python runtime. Actual speed must come from a build-specific benchmark, not merely the presence of Rust source.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Native backend reduces interpreter overhead while preserving interval-search semantics.

**Sources.** [S242: lib.rs](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/rust/kangaroo_fast/src/lib.rs); [S121: base.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/runtime/base.py)

### M032 — Coincurve/libsecp256k1 fast backend

**Evidence:** Implemented

**How it works.** Call optimized libsecp256k1 operations through a Python binding instead of performing every field operation in Python.

**What is actually done.** fast_ec.py selects accelerated scalar multiplication, point addition and optional native herd routines. It is a backend substitution, not an algorithm that predicts private keys.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Accelerated point arithmetic replaces pure Python operations; it does not reduce unknown key entropy.

**Sources.** [S106: fast_ec.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/fast_ec.py); [S081: benchmark_cpu_ec.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/benchmarks/benchmark_cpu_ec.py)

### M033 — GPU modular herd/D1 backends

**Evidence:** Implementation/stub mix

**How it works.** GPU kernels would execute many curve steps concurrently. A backend interface alone is insufficient; the device search must actually be implemented.

**What is actually done.** The inspected CTheory d1_search CUDA file returns unavailable/error and zeroes its output. The Python registry can report ready from markers/environment flags, which do not by themselves prove a working kernel.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Backend registries and CUDA files exist, but readiness and actual execution differ by module. Do not infer a complete device implementation from a registry.

**Sources.** [S120: backends_cuda.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/runtime/backends_cuda.py); [S090: d1_search.cu](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/cuda/ctheory_modules/d1_search/d1_search.cu)

### M034 — GPU throughput and cost calibration

**Evidence:** Executed record

**How it works.** Parse actual solver rates, discard warmup effects and combine measured work rates with declared operation counts.

**What is actually done.** gpu_bench.py extracts throughput from logs and computes estimates. Other tables contain assumed rates/prices; those must not be confused with current hardware measurements or target success probabilities.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Parse measured solver logs separately from hardcoded estimates; historical prices and throughput are not current quotations.

**Sources.** [S107: gpu_bench.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/gpu_bench.py); [S254: GPU-Deployment.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/GPU-Deployment.md)

### M035 — RunPod/Vultr sharding and orchestration

**Evidence:** Implemented

**How it works.** Partition solver jobs across remote workers, transfer manifests, run executables and collect outputs/checkpoints.

**What is actually done.** Deployment scripts and playbooks implement build/start/status procedures. This review documents those artifacts without launching instances or treating a successful cloud allocation as a successful key search.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Deployment runbooks, work-unit manifests and recovery scripts coordinate bounded jobs; availability is distinct from a successful search.

**Sources.** [S247: GPU_PLAYBOOK.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/vultr/GPU_PLAYBOOK.md); [S254: GPU-Deployment.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/GPU-Deployment.md)

### M036 — Bounded ECDLP certificates and slot gates

**Evidence:** Implemented

**How it works.** Attach a machine-readable statement of bounds, target, provenance and job identity so a result can be checked against its declared task.

**What is actually done.** BEC and slot gates seal manifests and validate fields. They can attest what was searched, but cannot certify that a heuristic guess contains the unknown key.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Certifies declared bounds and evidence metadata; a certificate is not proof that the target lies in a guessed slot.

**Sources.** [S094: bec.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bec.py); [S123: slot_contract.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/slot_contract.py)

### M037 — Miss ladder and complement widening

**Evidence:** Implemented

**How it works.** After a prioritized search misses, enlarge the hypothesis set in an explicit order rather than silently assuming the key was impossible.

**What is actually done.** miss_ladder.py plans complement, lattice and classical-range fallbacks. Following the ladder spends additional work; it does not retroactively make the first narrow guess complete.

**Inputs needed.** A known target public point and scalar bounds; solver/backend configuration. Address hashes alone do not supply the wild-walk point.

**What the result means.** Follow a failed narrow search with complement/full-range fallbacks, rather than treating heuristic misses as exclusions.

**Sources.** [S111: miss_ladder.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/miss_ladder.py)

## CTheory decompositions and scalar geometry

### M038 — Cubic scalar decomposition

**Evidence:** Audited/corrected

**How it works.** Set R1=floor(cuberoot(k)), divide k-R1^3 by R1^2, and retain quotient C1 and remainder D1. This exactly re-encodes k.

**What is actually done.** The code reconstructs known scalars from those digits and checks bounds. For an unknown key the digits are also unknown; an exact identity does not disclose them from the address.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Exact reconstruction of known integers works; the representation itself supplies no unknown digits or entropy reduction.

**Sources.** [S099: ctheory.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/ctheory.py); [S135: PUZZLE_STATUS_NOTE.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PUZZLE_STATUS_NOTE.md)

### M039 — Five-level R1/R2/S3/S4/S5 tower

**Evidence:** Implemented

**How it works.** Reapply root/division decompositions to R1 and later components, producing a hierarchy of smaller coordinates.

**What is actually done.** The tower code computes R2 and S-level quantities, some from bit-length formulas. Its tables describe known-key coordinates or target-size anchors, not independently observed secret digits.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Recursive roots and coefficients organize scalar coordinates; high levels often depend only on advertised bit width.

**Sources.** [S219: analyze_ctheory_decompose.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/analyze_ctheory_decompose.py)

### M040 — Exact root bounds and coefficient feasibility

**Evidence:** Executed record

**How it works.** Integer roots and inequality bounds determine which digit combinations could reconstruct an integer inside the advertised interval.

**What is actually done.** Exact arithmetic helpers enumerate feasible roots, clip remainders and verify reconstruction. They reject impossible combinations, while still retaining every feasible unknown scalar unless a separate heuristic cuts further.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Integer roots, coefficient limits, clipping and reconstruction are tested arithmetically.

**Sources.** [S100: ctheory_arithmetic.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/ctheory_arithmetic.py); [S087: ctheory_math_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_math_20260920.py)

### M041 — Phase-2 Delta2 enumeration

**Evidence:** Implemented

**How it works.** Given R2 and C2, each Delta2 selects an R1 through R1=R2^3+C2*R2^2+Delta2.

**What is actually done.** Phase-2 routines compute feasible Delta2 bounds and enumerate or stride through them. The smaller-looking parameter still represents many distinct scalar bases that may each require a D1 search.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Enumerate feasible R1 values within each R2/C2 hypothesis; this is a search coordinate, not an independently observed point.

**Sources.** [S114: phase2.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/phase2.py)

### M042 — Phase-2 public-key-guided light probes

**Evidence:** Implemented

**How it works.** For a guessed Delta2, build the corresponding shifted public point and test a small D1 budget before investing in a full leaf hunt.

**What is actually done.** phase2_search.py ranks hints, constructs Phase-3 candidates and optionally probes them. It does not extract Delta2 directly from Q; every probe remains conditional on its guessed coordinates.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Construct D1 targets from Delta2 guesses and run bounded probes; no independent Delta2 oracle is obtained.

**Sources.** [S115: phase2_search.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/phase2_search.py)

### M043 — Puzzle-bound clipping of D1

**Evidence:** Executed record

**How it works.** Intersect a leaf's D1 limits with the public puzzle bounds after subtracting its proposed base.

**What is actually done.** The audit measures how often clipping truly shortens D1. At high indices the public interval often contains the whole leaf, so the original D1 uncertainty remains.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Historical audit records no useful narrowing for its high-index sample; advertised puzzle bounds are too broad at this leaf scale.

**Sources.** [S152: d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

### M044 — D1 high-index ratio bands

**Evidence:** Executed record

**How it works.** Estimate normalized D1 positions from solved examples and prioritize a common ratio band for new slots.

**What is actually done.** Historical high-index min/max or leave-one-out bands were exported as search presets. Their reduced width is real for the chosen band, but held-out misses show it is not guaranteed containment.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Calibrated narrow bands reduce width conditionally but miss held-out keys; their complement is required for complete support.

**Sources.** [S152: d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

### M045 — Two-phase D1 band/complement policy

**Evidence:** Implemented

**How it works.** Search the ratio band first; if it misses, search all remaining D1 values. This preserves eventual full leaf coverage.

**What is actually done.** Preset builders generate phase-one and complementary phase-two jobs. The combined policy restores eligibility but can cost more than a single unpartitioned interval search.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Prioritize a calibrated band and search its remainder after a miss. Union coverage restores full range rather than reducing entropy.

**Sources.** [S101: d1_narrowing.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/d1_narrowing.py); [S152: d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

### M046 — Recursive remainder/sub-digit decomposition

**Evidence:** Executed record

**How it works.** Decompose a remainder again into its own root, coefficient and residual, then repeat recursively.

**What is actually done.** Backtests count subdigits and compare their distributions with equally transformed random integers. Most apparent simplification is a change of coordinates; omitted subdigits remain unknown.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Deeper splits were compared with random controls; apparent digit biases can arise from the map itself.

**Sources.** [S153: deeper_decomposition_limits.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/deeper_decomposition_limits.md)

### M047 — All-known-key slot containment

**Evidence:** Executed record

**How it works.** A complete hypothesis includes every base digit needed to define the final searched interval. Test whether the published answer lies in that interval.

**What is actually done.** Backtest scripts evaluate known-key slot containment after candidate construction. Knowing the answer for evaluation must not leak into hint generation or be reported as an actual cryptographic recovery.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Check whether a generated complete slot includes a published answer; containment is not independent discovery of that answer.

**Sources.** [S080: backtest_all_keys_slots.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/backtest_all_keys_slots.py); [S136: all_keys_slot_backtest.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/all_keys_slot_backtest.md)

### M048 — Post-slot square-root cost scaling

**Evidence:** Implemented

**How it works.** Kangaroo leaf work scales roughly with the square root of its interval width, conditional on the correct target interval.

**What is actually done.** slot_scaling.py reports D1 leaf costs and related floor bounds. A real plan must additionally count all root/remainder hypotheses and its probability of including the correct leaf.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Count leaf cost conditional on a correct slot; audits warn against omitting the number of unknown slots.

**Sources.** [S124: slot_scaling.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/slot_scaling.py)

### M049 — Constraint-satisfaction slot construction

**Evidence:** Executed record

**How it works.** Express digit domains and interval inequalities as constraints, then select variable orderings to prune impossible partial assignments.

**What is actually done.** CSP modules compare fixed, minimum-remaining-values and degree strategies. They reduce wasted inconsistent tuples but do not add new information about which consistent tuple is the secret.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Exact feasibility graph with fixed, MRV and degree orderings; pruning invalid tuples does not predict the valid target tuple.

**Sources.** [S098: solver.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/csp/solver.py); [S150: csp_ordering_backtest.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/csp_ordering_backtest.md)

### M050 — Gamma-band and lattice narrowing presets

**Evidence:** Executed record

**How it works.** Intersect feasible roots with selected gamma bands, FUSED tolerance bands or a two-stage union.

**What is actually done.** Preset reports count surviving R2 values and measure known-key coverage. A large candidate reduction can simply mean many true keys were excluded by the heuristic.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Compare full lattice, gamma restrictions and FUSED intersections; stronger cuts reduce measured target coverage.

**Sources.** [S183: search_narrowing_ladder.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/search_narrowing_ladder.md)

### M051 — Tiered minimal/narrow/focus/lattice exports

**Evidence:** Executed record

**How it works.** Package different breadths of the same hypothesis family as minimal, narrow, focus or full-lattice tiers.

**What is actually done.** Exporters select/cap slots, sometimes with diversity rules. Saved calibration reports explicitly check whether the known true R2 and full tuple were omitted from each exported job set.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Saved manifests can exclude the known calibration target; a valid export is not proof of target inclusion.

**Sources.** [S151: ctheory_phase_ab_summary.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/ctheory_phase_ab_summary.md)

### M052 — Anchor/TRAILING-centered slot construction

**Evidence:** Implemented

**How it works.** Use a supplied metadata number as a plausible center, or derive CTheory coordinates from it to define nearby slots.

**What is actually done.** wrapped_export.py constructs anchor and TRAILING jobs. They are guesses informed by an artifact, not proven high bits or offsets of the target scalar.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Metadata-centered guesses are explicit hypotheses and require cryptographic verification.

**Sources.** [S128: wrapped_export.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/wrapped_export.py)

### M053 — GLV scalar decomposition and endomorphism

**Evidence:** Executed record

**How it works.** The secp256k1 endomorphism permits k congruent to r1+lambda*r2 modulo group order, with a related point map.

**What is actually done.** EC decomposition code verifies scalar and point identities and can accelerate multiplication. Computing a split of a known scalar does not recover that scalar from a public point.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Correct arithmetic acceleration checked on known points; often degenerate for small scalars and not a generic entropy cut.

**Sources.** [S202: analyze_ec_decompose.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/analyze_ec_decompose.py); [S139: bip32_glv_probe.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/bip32_glv_probe.md)

### M054 — GLV splitting specifically on D1

**Evidence:** Audited/corrected

**How it works.** Attempt to apply the same balanced GLV split to the much smaller D1 scalar instead of a full-width scalar.

**What is actually done.** The D1 audit checks the resulting parts and finds degeneration: one component can retain effectively the original small scalar. A nominal two-part representation supplies no automatic search-width reduction.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Leaf scalars far below group order do not obtain the advertised balanced split; no free narrowing follows.

**Sources.** [S152: d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

### M055 — Exact value atlas and hierarchy visualizations

**Evidence:** Implemented

**How it works.** Export hierarchy values with explicit types, sizes and relationships so arithmetic and hypothesis ranges can be inspected visually.

**What is actually done.** build_value_atlas writes exact data tables and separate plotting-friendly values. The atlas explains known quantities; a chart that looks clustered is not an independent predictor.

**Inputs needed.** Known integers for decomposition tests, or target bounds plus hypothesized root/coefficient digits; a public point for shifted-point searches.

**What the result means.** Typed exports, scientific plots and offline views expose values and bounds; visualization itself is not a predictor.

**Sources.** [S083: build_value_atlas_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/build_value_atlas_20260920.py)

## Predictors, held-out validation and corrective audits

### M056 — FUSED global/local R2 regression

**Evidence:** Executed record

**How it works.** Fit root growth globally and locally, then blend forecasts and sequence terms to predict R2 for a target index.

**What is actually done.** ctheory.py combines fitted constants with backward-looking anchors. Audits refit or exclude known answers to measure leakage; a forecast supplies a root guess, not Delta2 or D1.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Historical blends forecast ninth roots; narrow transformed error must be converted to actual scalar coverage.

**Sources.** [S221: backtest_ctheory.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/backtest_ctheory.py); [S163: heldout_r2_vs_midpoint.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/heldout_r2_vs_midpoint.md)

### M057 — Gap-five sequence extrapolation

**Evidence:** Executed record

**How it works.** Use the regularly spaced disclosed high-index keys to estimate trends or differences five puzzle numbers apart.

**What is actually done.** research.py extrapolates gap-five R2/remainder hints. Later controls run the same fitting on synthetic corpora to test whether apparent predictability exceeds the interval geometry alone.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Forecast R2 or remainder ratios from every-fifth-puzzle sequences; tested against forward-only and uniform controls.

**Sources.** [S119: research.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/research.py); [S085: ctheory_forward_null_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_forward_null_20260920.py)

### M058 — Strategic Delta2 ratio hints

**Evidence:** Audited/corrected

**How it works.** Reuse normalized Delta2 ratios from calibration keys to propose a short list of exact Delta2 values.

**What is actually done.** Historical code could include the evaluated key's own ratio, making recovery self-confirming. Corrected exclusion removes that shortcut and exposes the much weaker blind exact-hint performance.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Target-in-calibration leakage explained the old 7/7 result; corrected blind high-index results were 0/7.

**Sources.** [S134: PRIVATE_KEY_RELATION_AUDIT_20260919.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PRIVATE_KEY_RELATION_AUDIT_20260919.md)

### M059 — Leave-one-out full-slot backtest

**Evidence:** Executed record

**How it works.** Hide one key from every calibration source, build its full slot list, then reveal the answer only to score containment.

**What is actually done.** The corrected LOO report separately counts R2, C2, Delta2 and C1 success. Coarse root coverage cannot compensate for a missing exact Delta2 coordinate.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Corrected full-slot requirements fail in the documented seven high-index holdouts, despite coarse R2 coverage.

**Sources.** [S141: blind_loo_backtest_20260919.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/blind_loo_backtest_20260919.md)

### M060 — Past-only FUSED versus midpoint

**Evidence:** Executed record

**How it works.** Compare a learned R2 forecast with the ninth root of the scalar interval midpoint using equal tolerances and actual scalar mass.

**What is actually done.** The comparison reports root error and coverage for past-only, LOO and production fits. Later solved keys or fixed full-corpus coefficients can make an ostensibly held-out fit optimistic.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Same-band comparisons show that transformed midpoint baselines can rival or beat apparent R2 coverage.

**Sources.** [S163: heldout_r2_vs_midpoint.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/heldout_r2_vs_midpoint.md)

### M061 — Correct uniform null for ninth-root clustering

**Evidence:** Audited/corrected

**How it works.** Transform uniform random scalars through the same ninth-root map as the real keys before comparing clustering.

**What is actually done.** The chat-audit experiment derives the transformed baseline and simulates matched-bit-width keys. It corrects an earlier null that mistakenly treated the compressed root coordinate as nearly uniform.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Uniform scalars naturally cluster after ninth-root transformation; an earlier overly broad null standard deviation was corrected.

**Sources.** [S068: REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md)

### M062 — Forward-only synthetic-corpus null

**Evidence:** Executed record

**How it works.** Run the entire forward-fitting procedure on synthetic uniform corpora, not just a single fixed prediction under a new null.

**What is actually done.** The frozen experiment counts exact covered scalar fractions and compares aggregate hits-minus-coverage with replicated null corpora. This tests that named predictor under stated historical-index conventions.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Repeat the predictor-fitting process on uniform synthetic keys and count exact scalar coverage.

**Sources.** [S085: ctheory_forward_null_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_forward_null_20260920.py); [S131: CTHEORY_FORWARD_RESEARCH_20260920.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/CTHEORY_FORWARD_RESEARCH_20260920.md)

### M063 — Family-wise forward R2 grid

**Evidence:** Executed record

**How it works.** When many cutoffs, widths and forecasts are examined, compare the best-looking observed result with equally selected null results.

**What is actually done.** The family-wise script searches its declared model grid on both observed and synthetic keys. Adjusted evidence is weaker than quoting the smallest unadjusted p-value.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Test selection across FUSED, gap-five, midpoint, cutoffs and window widths with family-wise controls.

**Sources.** [S084: ctheory_forward_familywise_20261008.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_forward_familywise_20261008.py)

### M064 — Contiguous-slice selection adjustment

**Evidence:** Executed record

**How it works.** A favorable consecutive slice can be selected by chance. The null comparison must also search candidate slices.

**What is actually done.** The slice-family script evaluates contiguous tier ranges and selection-adjusts their scores. It measures the effect of choosing a convenient evaluation interval after seeing outcomes.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Compare best-looking index slices with similarly selected synthetic controls; guards against picking favorable subsequences.

**Sources.** [S086: ctheory_forward_slice_family_20261008.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_forward_slice_family_20261008.py)

### M065 — Remainder precision granted true roots

**Evidence:** Executed record

**How it works.** Give a predictor the true root coordinates to isolate whether it can predict the remaining offset accurately enough.

**What is actually done.** The precision audit compares predicted and true remainders in integer/key units. It is an oracle diagnostic, deliberately easier than an unknown-key attack, and still exposes large residual errors.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Measures exact offset-prediction errors even when root coordinates are supplied; coarse root prediction does not supply leaf precision.

**Sources.** [S088: ctheory_remainder_precision_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_remainder_precision_20260920.py)

### M066 — Oracle-versus-blind hunt comparison

**Evidence:** Audited/corrected

**How it works.** Separate three tasks: reconstruct from supplied digits, include the answer in a candidate interval, and actually discover it by target verification.

**What is actually done.** Saved audits rerun planner logic with target answers excluded and compare oracle/full-slot results. A true-key-assisted coordinate lookup is labeled oracle rather than blind recovery.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Distinguishes provided true coordinates, key containment, and actual address/public-point discovery.

**Sources.** [S222: backtest_hunt_pipeline.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/backtest_hunt_pipeline.py); [S066: OTHER_KEYS_AND_BACKTESTS.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/OTHER_KEYS_AND_BACKTESTS.md)

### M067 — Frozen ninth-root remainder window

**Evidence:** Executed record

**How it works.** Normalize the ninth-root bucket remainder, fit a two-bin window on training keys, then freeze it for later keys.

**What is actually done.** The recent exact experiment uses 16 bins and puzzles 17-32 for fitting, then tests 33-64. It records both hits and the actual fraction of scalar candidates selected.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Recent test trained on 17-32 and covered 7/32 evaluation keys; uncorrected p about 0.116, not convincing evidence.

**Sources.** [S009: REPORT.md](/home/arialmohan/puzzle71-corrected/ctheory-test/REPORT.md)

### M068 — Square/cube/ninth-root window family

**Evidence:** Executed record

**How it works.** Repeat the same declared window-fitting rule for square, cube, ninth-root and ordinary range coordinates at four widths.

**What is actually done.** extended.py tests 16 models, computes exact candidate counts and applies a multiple-model correction. It does not keep tuning windows after examining each evaluation result.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Sixteen frozen models across four nominal widths; none significant after multiple-model correction.

**Sources.** [S008: EXTENDED_REPORT.md](/home/arialmohan/puzzle71-corrected/ctheory-test/EXTENDED_REPORT.md)

### M069 — Walk-forward adaptive remainder windows

**Evidence:** Executed record

**How it works.** Before predicting each evaluation key, refit only on smaller indices, making every forecast independent of that target's stored answer.

**What is actually done.** The expanded study records per-key windows, actual coverage and sequential evidence scores. Previously inspected data still make this retrospective rather than pristine prospective validation.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Refit only on lower indices; final evidence scores did not exceed the family threshold.

**Sources.** [S010: results.json](/home/arialmohan/puzzle71-corrected/ctheory-test/extended-run/results.json)

### M070 — Self-improving CTheory parameter loop

**Evidence:** Implemented

**How it works.** Alternate measurement, statistical analysis and parameter changes to tune a search planner's hint/window budgets.

**What is actually done.** ctheory_sim adjusts r2_pct, hint counts, tier or slot limits from recorded performance. It optimizes the tested planner; biased/leaky metrics would teach it the wrong objective.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Measure/analyze/improve loop tunes hint budgets, R2 width and slots; usefulness is limited by honest target inclusion.

**Sources.** [S089: loop.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/ctheory_sim/loop.py); [S251: Branch-cursor-ctheory-self-improve-agents-ac93.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Branch-cursor-ctheory-self-improve-agents-ac93.md)

### M071 — R2 intervals as conditional search prioritization

**Evidence:** Executed record

**How it works.** A root band [a,b] corresponds exactly to scalars from a^9 through (b+1)^9-1, clipped to puzzle bounds.

**What is actually done.** Interval-analysis scripts export these regions and report held-out coverage. The conversion is exact, but whether the unknown target belongs to the forecast band remains a probabilistic hypothesis.

**Inputs needed.** Disclosed keys split into declared training/evaluation sets, target bit widths, fixed model choices and correctly matched null controls.

**What the result means.** Root forecast bands map to exact scalar intervals; reports distinguish conditional narrowing from guaranteed coverage and statistical advantage.

**Sources.** [S067: R2_SEARCH_INTERVALS.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/R2_SEARCH_INTERVALS.md); [S163: heldout_r2_vs_midpoint.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/heldout_r2_vs_midpoint.md)

## Root-difference, carry, interpolation and near-miss routes

### M072 — Root floor/midpoint/ceiling candidate anchors

**Evidence:** Executed record

**How it works.** Turn plausible root locations into concrete integers using floors, midpoints, ceilings or differences from disclosed roots.

**What is actually done.** The root-test engine builds a fixed catalog of anchor candidates without reading the target key. Each resulting scalar is checked against that target's actual HASH160.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Fixed root-band and root-difference candidate families checked against known and unknown targets.

**Sources.** [S050: test.py](/home/arialmohan/scratch/puzzle-root-solve-test/test.py); [S045: report.json](/home/arialmohan/scratch/puzzle-root-solve-test/report.json)

### M073 — Nearest-donor raw remainder carry

**Evidence:** Executed record

**How it works.** Express a donor key as donor_root^9 plus an offset, then place that same offset above a legal root for the target.

**What is actually done.** The nearest-donor candidate families transfer offsets from neighboring disclosed puzzle indices. They test an offset-inheritance hypothesis, not a consequence of ninth-root arithmetic.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Transfer a disclosed key remainder to target root hypotheses; saved unknown-target candidate set contains no matches.

**Sources.** [S050: test.py](/home/arialmohan/scratch/puzzle-root-solve-test/test.py); [S045: report.json](/home/arialmohan/scratch/puzzle-root-solve-test/report.json)

### M074 — All-donor carry over every legal ninth root

**Evidence:** Executed record

**How it works.** Broaden the carry test to every disclosed donor and every legal target root, eliminating the nearest-donor selection restriction.

**What is actually done.** exhaustive_carry.py enumerates the entire stated donor/root family and verifies candidates. Zero hits rejects those concrete carried candidates, not all possible remainder-generation laws.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Saved exhaustive-within-family report records 35,982,885 candidate checks and zero target matches.

**Sources.** [S041: exhaustive_carry.py](/home/arialmohan/scratch/puzzle-root-solve-test/exhaustive_carry.py); [S042: exhaustive_carry_report.json](/home/arialmohan/scratch/puzzle-root-solve-test/exhaustive_carry_report.json)

### M075 — Transferred within-bucket share

**Evidence:** Executed record

**How it works.** Transfer a fraction of a donor bucket rather than its raw offset so buckets of different sizes can be compared.

**What is actually done.** The code rescales each selected share by the target bucket width and rounds to an integer candidate. Any rounding and donor choice are part of the tested hypothesis.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Reuse disclosed normalized root-bucket shares at legal target roots; tests do not cover arbitrary offset functions.

**Sources.** [S041: exhaustive_carry.py](/home/arialmohan/scratch/puzzle-root-solve-test/exhaustive_carry.py)

### M076 — Smooth polynomial share in puzzle index

**Evidence:** Executed record

**How it works.** Assume normalized bucket share is a low-degree polynomial in puzzle index and use fitted values to generate target offsets.

**What is actually done.** smooth_share.py fits degrees 1-4, evaluates errors against a uniform-share baseline and checks candidates over legal target roots. Numerical fit quality is reported separately from address hits.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Degrees 1-4 predict bucket shares; saved per-degree unknown-target tests report no matches.

**Sources.** [S046: smooth_share.py](/home/arialmohan/scratch/puzzle-root-solve-test/smooth_share.py); [S047: smooth_share_report.json](/home/arialmohan/scratch/puzzle-root-solve-test/smooth_share_report.json)

### M077 — Two-dimensional index/root share surface

**Evidence:** Executed record

**How it works.** Include both puzzle index and legal root as inputs to a polynomial surface predicting the bucket share.

**What is actually done.** surface2d.py fits the declared low-degree surfaces on disclosed data and verifies reconstructed candidates. Additional model dimensions do not by themselves resolve an unknown remainder.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Fit share as a low-degree surface of index and root, then verify resulting candidates; no saved unknown-target hits.

**Sources.** [S048: surface2d.py](/home/arialmohan/scratch/puzzle-root-solve-test/surface2d.py); [S049: surface2d_report.json](/home/arialmohan/scratch/puzzle-root-solve-test/surface2d_report.json)

### M078 — Gap-fill normalized-position interpolation

**Evidence:** Executed record

**How it works.** Assume normalized interval position changes smoothly between the nearest disclosed neighbors. Interpolate that position into the target interval.

**What is actually done.** gap_fill.py creates one or more exact integer candidates from those neighboring positions. The hypothesis is smoothness; the verifier, not visual continuity, determines success.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Interpolate/extrapolate between disclosed neighboring puzzles and verify candidates; no recorded matches.

**Sources.** [S043: gap_fill.py](/home/arialmohan/scratch/puzzle-root-solve-test/gap_fill.py); [S044: gap_fill_report.json](/home/arialmohan/scratch/puzzle-root-solve-test/gap_fill_report.json)

### M079 — Gap-fill linear/geometric root interpolation

**Evidence:** Executed record

**How it works.** Interpolate roots linearly or geometrically, then map the forecast root back to an integer scalar.

**What is actually done.** The gap-fill test generates candidates from both root interpolation rules and clips to the target range. A nearby root can still correspond to a very large scalar error.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Interpolate root coordinates and reconstruct candidate powers; tested candidates did not recover unknown keys.

**Sources.** [S043: gap_fill.py](/home/arialmohan/scratch/puzzle-root-solve-test/gap_fill.py)

### M080 — Gap-fill log-key and raw-offset interpolation

**Evidence:** Executed record

**How it works.** Interpolate log2(key) or the raw ninth-root residual as an alternative notion of smooth progression.

**What is actually done.** The same bounded test reconstructs scalars under these assumptions and compares addresses. Log closeness or matching early values is not accepted as a recovered key.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Alternative smoothness assumptions tested against exact address hashes, not judged by numerical proximity alone.

**Sources.** [S043: gap_fill.py](/home/arialmohan/scratch/puzzle-root-solve-test/gap_fill.py)

### M081 — Near-miss anomaly testing

**Evidence:** Executed record

**How it works.** Judge proximity relative to the density and placement of the entire candidate set. Dense sets naturally create close numerical neighbors.

**What is actually done.** nearmiss_analysis.py holds the candidate geometry fixed, draws uniform targets in the same interval and compares minimum distances. This is a diagnostic of chance closeness, not a new candidate verifier.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Compare nearest-candidate distances with uniform targets against the same candidate geometry; closeness alone is not a verified key.

**Sources.** [S039: nearmiss_analysis.py](/home/arialmohan/scratch/nearmiss-20261008/nearmiss_analysis.py); [S040: nearmiss_results.json](/home/arialmohan/scratch/nearmiss-20261008/nearmiss_results.json)

### M082 — All-donor carry proximity null

**Evidence:** Executed record

**How it works.** Ask whether any donor-offset/root combination lands unusually near a held-out key compared with identical carry geometry under uniform targets.

**What is actually done.** all_donor_carry.py excludes that target from donor construction and computes observed versus null proximity. A favorable minimum is not an address match and may require selection adjustment.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Compare minimum carry distance to uniform controls while excluding the known target from its donor set.

**Sources.** [S038: all_donor_carry.py](/home/arialmohan/scratch/nearmiss-20261008/all_donor_carry.py); [S037: all_donor_carry.json](/home/arialmohan/scratch/nearmiss-20261008/all_donor_carry.json)

### M083 — Blind nth-root ladder address tests

**Evidence:** Executed record

**How it works.** Build nth-root scheduled anchors and difference-based forecasts without supplying the hidden scalar to the candidate generator.

**What is actually done.** The saved PEC37 test covers index-only, leave-one-out, random-holdout and unknown-target candidates. Reported matches are confined to tiny trivial intervals rather than scalable unknown-key recovery.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Index-only, leave-one-out and random holdout candidates mostly match only trivial tiny puzzles; no unknown-target matches recorded.

**Sources.** [S259: nth_root_blind_address_test.json](/home/arialmohan/workspace/projects/pec37/data/nth_root_blind_address_test.json)

### M084 — Exact polynomial/difference continuation

**Evidence:** Executed record

**How it works.** Fit exact rational polynomials to known scalars, roots or normalized positions, then evaluate them at held-out indices.

**What is actually done.** The atlas audit tests degrees 0-6 and multiple masking/encoding variants. It uses published answers afterward for scoring and checks target-derived addresses for concrete candidate attempts.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Degree 0-6 models of scalars, range positions and roots failed exact higher-index recovery in the saved tests.

**Sources.** [S071: check_routes.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/check_routes.py); [S068: REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md)

### M085 — Frozen candidate families on 77 unknown targets

**Evidence:** Executed record

**How it works.** Freeze a finite candidate recipe, apply it to every locally undisclosed puzzle, and compare each output with that puzzle's target hash.

**What is actually done.** all_unknown_check.py evaluates 77 database entries and saves candidate/target counts. A completed finite recipe search is not an exhaustive search of all their intervals.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Local all-unknown report records 2,744 distinct candidate/target checks and no matches.

**Sources.** [S069: all_unknown_check.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/all_unknown_check.py); [S066: OTHER_KEYS_AND_BACKTESTS.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/OTHER_KEYS_AND_BACKTESTS.md)

### M086 — Finite continuation attempts specifically for #140

**Evidence:** Executed record

**How it works.** Collect new finite leads specifically for a public-point target, derive candidate scalars or intervals and perform exact comparisons.

**What is actually done.** continue_140.py indexes archive clues, binary-derived numbers and signature relations. It records bounded attempts; finding a plausible story or interval does not count as discovering #140.

**Inputs needed.** Disclosed donor keys and target interval/index; target hashes for candidate verification, with hidden answers used only for evaluation.

**What the result means.** Archive leads and binary candidates were verified as bounded hypotheses, not exhaustive interval searches.

**Sources.** [S074: continue_140.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/continue_140.py); [S073: results.json](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/continuation-140-run/results.json)

## Generator reconstruction, masking and deterministic sequences

### M087 — Fixed affine/LCG key recurrence

**Evidence:** Executed record

**How it works.** A fixed affine recurrence maps the same low-bit input to the same output. Contradictory observed transitions can therefore reject that recurrence family.

**What is actually done.** The audit exhausts small modular coefficient pairs and gives an exact parity obstruction. It does not exclude hidden state, changing coefficients, discarded outputs or unrelated deterministic wallets.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Exact low-bit constraints reject the named fixed-parameter recurrence family; hidden state and different generators remain outside scope.

**Sources.** [S068: REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md); [S079: analyze_creator_generator.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/analyze_creator_generator.py)

### M088 — LFSR / Berlekamp-Massey reconstruction

**Evidence:** Recorded research

**How it works.** An LFSR predicts later bits from a fixed linear combination of earlier bits. Berlekamp-Massey finds a shortest recurrence fitting a supplied bitstream.

**What is actually done.** Archived generator work applies linear recurrence tests to concatenated known keys. Fitting the observed stream is insufficient unless the same state and output schedule predict unseen keys.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Historical generator review includes bitstream linear-recurrence tests; no transferable unknown-key generator established.

**Sources.** [S079: analyze_creator_generator.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/analyze_creator_generator.py); [S135: PUZZLE_STATUS_NOTE.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PUZZLE_STATUS_NOTE.md)

### M089 — Two-adic/Hensel polynomial recurrence

**Evidence:** Recorded research

**How it works.** A polynomial recurrence modulo powers of two can constrain parameters one bit at a time; lifting extends compatible low-bit solutions.

**What is actually done.** The generator catalog tests declared polynomial/2-adic forms against known puzzle transitions. It searches a restricted family, not all possible deterministic key generators.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Tests of squared-state and modular recurrence hypotheses are archived; finite failures are not impossibility theorems.

**Sources.** [S079: analyze_creator_generator.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/analyze_creator_generator.py); [S135: PUZZLE_STATUS_NOTE.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PUZZLE_STATUS_NOTE.md)

### M090 — Consecutive-difference factor patterns

**Evidence:** Recorded research

**How it works.** If consecutive keys share a multiplicative or arithmetic construction, their differences may expose common factors or repeated relations.

**What is actually done.** Historical reviews factor or compare disclosed differences and check proposed recurrences. The known interval sizes themselves create scale trends that must be distinguished from secret generator structure.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Search common factors or structured differences across published puzzle keys; no validated target predictor recorded.

**Sources.** [S135: PUZZLE_STATUS_NOTE.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PUZZLE_STATUS_NOTE.md)

### M091 — Hash-chain continuation

**Evidence:** Executed record

**How it works.** Hash a preceding key in a specified encoding, then mask the digest into the next puzzle's range.

**What is actually done.** Candidate scripts try SHA-256/double-hash, byte orders and minimal/32-byte lengths. Every recipe is deterministic; zero target matches applies to those encodings and transitions only.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** SHA-256/double-hash variants of previous keys, with endian/length choices and masks, failed named holdout and target checks.

**Sources.** [S070: candidate_models.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/candidate_models.py); [S068: REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md)

### M092 — Seed-plus-index hash/HMAC families

**Evidence:** Implemented

**How it works.** Derive a candidate from a small seed and an index encoding using hashing or HMAC, then compare many disclosed tiers.

**What is actually done.** hunt_multi_significant.py sweeps named seed families and tracks nontrivial matches. Matching a one- or two-bit puzzle is expected by chance and is not a recovered creator seed.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Score candidate seeds over different index encodings; requiring significant later-tier matches avoids trivial small-range coincidences.

**Sources.** [S092: hunt_multi_significant.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/hunt_multi_significant.py)

### M093 — Python MT19937 masked-key replay

**Evidence:** Implemented

**How it works.** Replay Python's seeded PRNG under a specific call schedule and force outputs into each tier.

**What is actually done.** The hunter tests randrange and getrandbits variants across disclosed keys. Exact software version, seeding and draw order are part of the hypothesis, not generic consequences of MT19937.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Test seeded randrange/getrandbits generation schedules against published puzzle keys.

**Sources.** [S092: hunt_multi_significant.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/hunt_multi_significant.py)

### M094 — Shared unmasked value, prefix and suffix tests

**Evidence:** Executed record

**How it works.** Re-masking one common integer would force predictable prefix/suffix agreement among tiers. Independent draws need not share those bits.

**What is actually done.** Known-key pair tests count overlap and compare aligned bits with random controls. They test the common-value construction; ordinary BIP32 child masking does not imply that same shared-value model.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Known-key overlap and random controls reject the tested common-prefix/suffix hypotheses, not every wallet generator.

**Sources.** [S167: key_masking_hypothesis.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/key_masking_hypothesis.md)

### M095 — CoinVault/mSIGNA BIP32 plus mask

**Evidence:** Executed record

**How it works.** BIP32 derives a child scalar using HMAC-SHA512 and chain codes; the proposed creator mask keeps the required leading bit and lower child bits.

**What is actually done.** The catalog tests supplied seed materials and CoinVault/mSIGNA-style paths, with synthetic positive controls. No tested catalog entry reproduces the nontrivial public puzzle sequence.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Bounded seed/path catalog did not reproduce nontrivial puzzle keys; synthetic known-wallet recovery validates the checker.

**Sources.** [S146: coinvault_bip32_oracle.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/coinvault_bip32_oracle.md)

### M096 — Electrum-v1 and Armory masking models

**Evidence:** Implemented

**How it works.** Historical deterministic wallets can derive children by algorithms different from BIP32. Apply each modeled derivation before the puzzle mask.

**What is actually done.** Dedicated Electrum-v1 and Armory scripts test those concrete wallet families. Their existence does not establish that the creator used either wallet or that its seed is enumerable.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Historical deterministic-wallet derivation families and creator-style masks have dedicated test scripts.

**Sources.** [S230: electrum_v1_mask_test.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/electrum_v1_mask_test.py); [S229: armory_mask_test.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/armory_mask_test.py)

### M097 — BIP32 child/index interval pairing

**Evidence:** Implemented

**How it works.** Treat child derivation indices as a pair such as start index and interval, and test path templates built from those integers.

**What is actually done.** child_wallet_interval_probe.py derives masked children for supplied seeds and compares public targets. A synthetic known-template test checks the probe; unknown creator provenance remains missing.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Enumerate path-template index/interval pairs under an explicitly supplied seed; synthetic self-test is separate from creator identification.

**Sources.** [S218: child_wallet_interval_probe.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/child_wallet_interval_probe.py)

### M098 — Supplied extended-key derivation leads

**Evidence:** Executed record

**How it works.** An explicitly supplied extended private node allows deterministic child derivation along a bounded list of relative paths.

**What is actually done.** The audit validates checksums, tests seven relative path families and index shifts, then compares initial nontrivial probe keys. It never prints or republishes the supplied secret nodes.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Three unique supplied leads tested over bounded relative paths/index shifts; no reproduction of nontrivial probe keys. Secrets are not included here.

**Sources.** [S072: check_wallet_leads.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/check_wallet_leads.py); [S076: wallet_lead_results.json](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/wallet_lead_results.json)

### M099 — Entropy-prefix and full-width constraints

**Evidence:** Implemented

**How it works.** A known source-entropy prefix or full-width relation could restrict which masked outputs are possible. It must be derived independently of the hidden key.

**What is actually done.** These scripts construct and score named prefix/full-width hypotheses. They do not turn a public difficulty interval into additional leaked secret bits without matching evidence.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Named candidate scripts examine how scalar masking and source entropy could constrain keys; no generic recovery follows.

**Sources.** [S231: entropy_prefix_test.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/entropy_prefix_test.py); [S232: fullwidth_constraint_test.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/fullwidth_constraint_test.py)

### M100 — CLI fingerprint and key clustering

**Evidence:** Executed record

**How it works.** A short fingerprint of known components can group similar CLI outputs or candidate tuples. It helps organize evidence and detect duplicate hypotheses.

**What is actually done.** set_bits.py and clustering tools compute partial masks, Hamming statistics and groups. A matching fingerprint is a lossy summary, not proof of an exact scalar or valid search cut.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Hamming, low-word masks and partial fingerprints organize known coordinates; not established target narrowing.

**Sources.** [S122: set_bits.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/set_bits.py); [S078: analyze_cli_clustering.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/analyze_cli_clustering.py)

### M101 — Popcount and aligned-bit distribution tests

**Evidence:** Executed record

**How it works.** Compare the number of set bits and aligned bit agreements with the distribution expected from uniform interval keys.

**What is actually done.** Reports measure popcounts, low-bit patterns and pairwise overlaps. Statistical similarity/difference concerns the tested corpus; it does not directly provide the unknown bits of the next key.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Known-key bit densities and overlap are compared with controls; observed appearance is not a scalar equation.

**Sources.** [S185: set_bits_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/set_bits_audit.md)

### M102 — Counter/small-affine early public-key relations

**Evidence:** Executed record

**How it works.** Small scalar relations are visible as public-point relations: alpha*P_i+beta*P_j+gamma*G equals the identity if the corresponding scalars satisfy them.

**What is actually done.** Early-key scripts sweep bounded coefficient and offset grids, including nonce-to-signer pairs. A genuine relation could help, but the saved finite sweeps report no such target recovery.

**Inputs needed.** A specifically defined generator/wallet recipe, seed/path hypotheses and known keys or public targets for independent comparison.

**What the result means.** Recorded all-pairs and focused early-key coefficient sweeps found no relation in their finite coefficient/offset bounds.

**Sources.** [S155: early_key_relations.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/early_key_relations.md); [S156: early_key_relations_focus.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/early_key_relations_focus.md)

## Firmware entropy and read-only wallet forensics

### M103 — Firmware-accurate Coldcard Yasmarang entropy-position analysis

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A specified firmware/software generation path, sanitized public address/index data and explicit read-only chain or balance evidence; no private keys are required or reproduced.

**What the result means.** Reconstructs the affected firmware path and identifies which seed registers and skip positions influence generated bytes; it does not establish wallet recovery or an address match.

**Sources.** [S061: entropy_position.py](/home/arialmohan/scratch/temp/entropy_position.py)

### M104 — Cold-boot entropy propagation and mixer analysis

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A specified firmware/software generation path, sanitized public address/index data and explicit read-only chain or balance evidence; no private keys are required or reproduced.

**What the result means.** Compares chip/mixer streams, skip lattices and post-hash behavior to distinguish low-entropy inputs from claims that the mixer itself creates an address family; no spend path or address matching is performed.

**Sources.** [S060: entropy_patterns.py](/home/arialmohan/scratch/temp/entropy_patterns.py)

### M105 — Local Coldcard wallet-generation replay

**Evidence:** Implemented

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A specified firmware/software generation path, sanitized public address/index data and explicit read-only chain or balance evidence; no private keys are required or reproduced.

**What the result means.** Replays explicit, sanitized initial states through Yasmarang, SHA-256 whitening and BIP-39 formatting for implementation analysis; generated examples are not evidence of a historical wallet seed.

**Sources.** [S059: coldcard_make_new_wallet.py](/home/arialmohan/scratch/temp/coldcard_make_new_wallet.py)

### M106 — Read-only funded-address membership analysis

**Evidence:** Implemented

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A specified firmware/software generation path, sanitized public address/index data and explicit read-only chain or balance evidence; no private keys are required or reproduced.

**What the result means.** Queries address status for local watchlists and classifies script types; membership is not proof of seed ownership, key recovery or a valid spend path.

**Sources.** [S062: funded_membership.py](/home/arialmohan/scratch/temp/funded_membership.py)

### M107 — Read-only residual-UTXO and drain-wave analysis

**Evidence:** Implemented

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A specified firmware/software generation path, sanitized public address/index data and explicit read-only chain or balance evidence; no private keys are required or reproduced.

**What the result means.** Compares remaining UTXOs and observed drain timing/amount shape against a declared block boundary; chain observations do not identify a private key.

**Sources.** [S063: residual_utxo.py](/home/arialmohan/scratch/temp/residual_utxo.py)

### M108 — Pre-drain co-input and address-cluster analysis

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A specified firmware/software generation path, sanitized public address/index data and explicit read-only chain or balance evidence; no private keys are required or reproduced.

**What the result means.** Groups watchlist addresses by shared pre-drain transaction inputs and separates those from later sweep co-inputs; the saved result is chain evidence, not proof of common seed derivation.

**Sources.** [S065: seed_addr_cluster.py](/home/arialmohan/scratch/temp/seed_addr_cluster.py); [S064: seed_addr_cluster.json](/home/arialmohan/scratch/temp/seed_addr_cluster.json)

### M109 — Bounded Coldcard entropy-grid enumeration against a funded-address dump

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A specified firmware/software generation path, sanitized public address/index data and explicit read-only chain or balance evidence; no private keys are required or reproduced.

**What the result means.** A bounded Python/Rust-style replay enumerated 300 modeled wallets across explicit UID, SysTick, skip and reseed grids, deriving BIP44/49/84 receive/change paths and comparing against a dated address-balance dump; listed hits validate membership only and do not establish seed ownership or exhaustive coverage.

**Sources.** [S052: check_experiments_vs_balance.py](/home/arialmohan/scratch/temp/coldcard_enum/check_experiments_vs_balance.py); [S053: coldcard_experiments_vs_balance.json](/home/arialmohan/scratch/temp/coldcard_enum/logs/coldcard_experiments_vs_balance.json)

### M110 — Rust Coldcard address-derivation backend

**Evidence:** Implemented

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A specified firmware/software generation path, sanitized public address/index data and explicit read-only chain or balance evidence; no private keys are required or reproduced.

**What the result means.** Native implementation covers Yasmarang output, BIP-39/BIP-32 derivation and P2PKH/P2WPKH address encoding for bounded enumeration; backend existence is not proof of a historical match.

**Sources.** [S055: yasmarang.rs](/home/arialmohan/scratch/temp/coldcard_enum/src/yasmarang.rs); [S054: derive.rs](/home/arialmohan/scratch/temp/coldcard_enum/src/derive.rs); [S051: Cargo.toml](/home/arialmohan/scratch/temp/coldcard_enum/Cargo.toml)

### M111 — Coldcard entropy statistical variation sweep

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A specified firmware/software generation path, sanitized public address/index data and explicit read-only chain or balance evidence; no private keys are required or reproduced.

**What the result means.** Saved 65,536-sample windows report unique outputs, zero observed collisions and near-balanced first-byte/bit statistics under synthetic register variations; this measures the modeled output distribution, not wallet recovery.

**Sources.** [S057: stats-range-output.txt](/home/arialmohan/scratch/temp/coldcard_enum/stats-range-output.txt); [S056: stats-continuous-output.txt](/home/arialmohan/scratch/temp/coldcard_enum/stats-continuous-output.txt); [S058: stats-variations-output.txt](/home/arialmohan/scratch/temp/coldcard_enum/stats-variations-output.txt)

## Dated generator and decomposition follow-up audits

### M112 — All-unknown-target generator matrix

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** Ten fully specified SplitMix64/Lehmer models were checked against 770 unknown-target identities, plus 97,216 low-bit-consistent candidates where feasible; zero matches, with prior solved-key failures limiting interpretation.

**Sources.** [S206: generator_all_unknown_targets_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/generator_all_unknown_targets_20261020.py); [S160: generator_all_unknown_targets_report_20261020.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/generator_all_unknown_targets_report_20261020.md)

### M113 — Wallace LCG masked-word backtest

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** All 2^17 states compatible with the Puzzle #65 low-word constraint were tested under 17/18-word packing; survivors fell to zero by tier 67 under the stated mask and schedule.

**Sources.** [S216: wallace_lcg_mask_backtest_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/wallace_lcg_mask_backtest_20261020.py); [S194: wallace_lcg_mask_backtest_20261020.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/wallace_lcg_mask_backtest_20261020.json)

### M114 — Park-Miller packed-word target checks

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** Lehmer multipliers 16807/48271 with 8/9-word packing and both orders were checked against #66, #71 and #140; candidate target identities did not match.

**Sources.** [S210: park_miller_target_check_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/park_miller_target_check_20261020.py); [S174: park_miller_target_check_20261020.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/park_miller_target_check_20261020.json)

### M115 — SplitMix64 masked-sequence target checks

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** One-draw low-64-bit candidates and four-draw word orders were checked against target HASH160s; evaluated candidates produced no matches.

**Sources.** [S214: splitmix64_target_check_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/splitmix64_target_check_20261020.py); [S188: splitmix64_target_check_20261020.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/splitmix64_target_check_20261020.json)

### M116 — Lagged-RNG multiword wallet-key audit

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** 16/32/64-bit word widths and both assembly orders were compared with archived lagged recurrences; the listed contiguous layouts failed their available equations, while underdetermined layouts remain untested.

**Sources.** [S205: archive_rng_wordstream_check_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/archive_rng_wordstream_check_20261020.py); [S138: archive_rng_wordstream_audit_20261020.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/archive_rng_wordstream_audit_20261020.md)

### M117 — Half-generator cross-curve coordinate analysis

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** Verified the half-generator relation and a repeated internal x-coordinate pattern across four standard curves; the known generator relabeling does not reduce the Bitcoin puzzle discrete-log search space.

**Sources.** [S207: half_generator_cross_curve_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/half_generator_cross_curve_20261020.py); [S162: half_generator_cross_curve_report_20261020.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/half_generator_cross_curve_report_20261020.md)

### M118 — Deeper remainder/permutation-tree null calibration

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** Sixty-four nonconstant features were compared with 3,000 range-matched control corpora; the observed family maximum was not unusual, so no beacon was established.

**Sources.** [S211: remainder_tree_beacon_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/remainder_tree_beacon_20261020.py); [S180: remainder_tree_beacon_report_20261020.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/remainder_tree_beacon_report_20261020.md)

### M119 — Low-bit affine and linear-state generator audit

**Evidence:** Audited/corrected

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** Direct affine recurrence and at-most-32-bit binary-linear-state families fail under the stated mask and indexing assumptions; this does not exclude wider, nonlinear, hashed or skipped-state generators.

**Sources.** [S201: affine_lowbits_check_20261019.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/affine_lowbits_check_20261019.py); [S209: lowbit_linear_state_20261019.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/lowbit_linear_state_20261019.py); [S169: lowbit_generator_audit_20261019.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/lowbit_generator_audit_20261019.md)

### M120 — Unknown-parameter inventory through Puzzle #160

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** Enumerates which coordinates are publicly constrained versus unknown across 77 unsolved tiers; fixed high decomposition coordinates are range consequences, not recovered private-key information.

**Sources.** [S215: unknown_parameter_inventory_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/unknown_parameter_inventory_20261020.py); [S193: unknown_parameter_inventory_20261020.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/unknown_parameter_inventory_20261020.json)

### M121 — Index-offset holdout and coefficient-interval audits

**Evidence:** Executed record

**How it works.** The method is defined by the named evidence files and recorded scope.

**What is actually done.** The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

**Inputs needed.** A fixed generator/decomposition hypothesis, declared solved/unsolved corpus, target identity checks and range-matched controls where statistical claims are made.

**What the result means.** Tests index-based offset models on held-out tiers and enumerates exact decomposition coefficient possibilities over unsolved intervals; bounded intervals do not identify a scalar.

**Sources.** [S208: index_offset_holdout_20261019.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/index_offset_holdout_20261019.py); [S166: index_offset_holdout_20261019.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/index_offset_holdout_20261019.json); [S145: coefficient_interval_audit_20261019.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/coefficient_interval_audit_20261019.md)

## Sparse keys, bit walks and synthesis orbits

### M122 — Sparse ORIG decomposition and peel chain

**Evidence:** Executed record

**How it works.** Describe a supplied sparse integer as a few shifted terms plus a tail, then reverse those terms to expose nested smaller values.

**What is actually done.** The ORIG investigation verifies its exact decomposition and peel chain to tiny public keys. Constructing an integer around a known tail does not explain generation of later independent puzzles.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** A constructed sparse scalar peels to tiny known puzzle values; this does not generate the numbered puzzle sequence.

**Sources.** [S187: sparse_key_investigate.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/sparse_key_investigate.md)

### M123 — Nested previous-key tail grow/peel

**Evidence:** Audited/corrected

**How it works.** Build the next sparse value by embedding the previous entire value under a new frame, and reverse that operation by peeling the frame.

**What is actually done.** The audit compares this recursive rule with the actual fixed-tail expression. They coincide at one chosen step but produce different subsequent integers, exposing a conflated model.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Distinguishes nested-tail updates from fixed-tail co-shifts; the two agree at one construction step, not generally.

**Sources.** [S186: sparse_key_hardthink.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/sparse_key_hardthink.md)

### M124 — Fixed-tail co-shift family

**Evidence:** Implemented

**How it works.** Keep a small tail constant while shifting selected high and middle terms together. This defines a precise sparse family.

**What is actually done.** sparse_key_coshift.py generates that family's members. Reversibility within the constructed family is a program property, not evidence that numbered Bitcoin puzzles lie on its orbit.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Exact sparse-key program shifts its frame while preserving the tail; valid program structure is not a Bitcoin predictor.

**Sources.** [S238: sparse_key_coshift.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_coshift.py); [S186: sparse_key_hardthink.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/sparse_key_hardthink.md)

### M125 — Sparse bit-learning and dial-in grids

**Evidence:** Executed record

**How it works.** Fit simple frame positions, bit rules or mid/gap parameters to known sparse values and test whether they extend across puzzle keys.

**What is actually done.** Bit-learning and dial-in scripts sweep bounded templates and report coverage. The later investigation separates fitted tiny-key coincidences from actual unseen-address hits.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Learn/test mid, gap, bit and frame variants; archived investigation reports poor known-key recall and no unknown address hits.

**Sources.** [S236: sparse_key_bitlearn.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_bitlearn.py); [S240: sparse_key_dial_in.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_dial_in.py); [S187: sparse_key_investigate.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/sparse_key_investigate.md)

### M126 — Sparse XOR-tail / delta / Bloom variants

**Evidence:** Executed record

**How it works.** Change the recurrence using XOR tails, deltas or Bloom-filter-assisted membership screening and compare its generated values with targets.

**What is actually done.** These are alternative sparse candidate recipes. A Bloom hit is only a screening event; the scalar still needs exact address verification, and saved summaries do not establish a transferable generator.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Alternate sparse generative families were tested without establishing a transferable key-generation rule.

**Sources.** [S241: sparse_key_xor_tail.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_xor_tail.py); [S239: sparse_key_delta_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_delta_hunt.py); [S237: sparse_key_bloom.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_bloom.py)

### M127 — Gray-code range and anchor walks

**Evidence:** Implemented

**How it works.** Gray code orders bitstrings so adjacent offsets differ in one bit; adding or XORing offsets around an anchor defines a traversal.

**What is actually done.** bit_flip_hunt.py provides range and anchor variants. They visit specified candidates in a different order and do not prove the key is near the selected anchor.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Enumerate Gray offsets around range floors or metadata anchors; this changes order rather than entropy.

**Sources.** [S095: bit_flip_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bit_flip_hunt.py)

### M128 — BFS Hamming balls and previous-key XOR

**Evidence:** Implemented

**How it works.** Enumerate all masks up to a chosen Hamming weight around a seed, or XOR selected bits into a previous known key.

**What is actually done.** BFS/previous-key routines search bounded neighborhoods. A completed neighborhood search says nothing about integers outside that radius unless independent target-distance information exists.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Check bounded low-Hamming-distance neighborhoods around seeds or prior keys; completeness is limited to that neighborhood.

**Sources.** [S095: bit_flip_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bit_flip_hunt.py)

### M129 — TRAILING-mask and FUSED-D1 bit flips

**Evidence:** Implemented

**How it works.** Choose flip positions from TRAILING bits or apply flips within a D1 coordinate derived from a FUSED anchor.

**What is actually done.** These methods impose a candidate-selection hypothesis on where the unknown bits differ. Their bounds are computational choices, not leaked bit positions from the target.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Restrict flipped positions or anchor the D1 coordinate; target inclusion is unproven.

**Sources.** [S095: bit_flip_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bit_flip_hunt.py)

### M130 — Dual-mask byte/bit and Gray-PDEP walks

**Evidence:** Implemented

**How it works.** Deposit counter bits into chosen mask positions; optionally Gray-code the counter so consecutive deposits change sparsely.

**What is actually done.** dual_mask_seq.py implements byte- and bit-index complementary-mask schedules. The masks describe allowed moves; their symbolic organization does not create missing target information.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Deposit counter bits into complementary masks, including Gray ordering; these are deterministic traversal families.

**Sources.** [S103: dual_mask_seq.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/dual_mask_seq.py)

### M131 — Gosper constant-weight and byte-lane variants

**Evidence:** Implemented

**How it works.** Gosper's rule enumerates masks of fixed Hamming weight. A byte-lane walk substitutes every byte value at one position.

**What is actually done.** The bit-flip engine generates these candidate families around anchors and verifies addresses. Their coverage is explicitly restricted to the selected mask weights or byte substitutions.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Visit fixed-weight XOR masks or replace individual bytes; no claim that these neighborhoods contain the target.

**Sources.** [S095: bit_flip_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bit_flip_hunt.py); [S103: dual_mask_seq.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/dual_mask_seq.py)

### M132 — Shift-shell and suffix Hamming hunts

**Evidence:** Implemented

**How it works.** Search literal scalar shells around a metadata distance, or flip a limited number of bits in a chosen suffix.

**What is actually done.** hunt_shift_windows.py tests distance shells, a 106-bit suffix neighborhood and small TRAILING gaps. Each is a bounded anchor hypothesis, not an exhaustive private-key interval search.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Search metadata-distance shells, suffix flips and literal TRAILING gaps around selected anchors.

**Sources.** [S093: hunt_shift_windows.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/hunt_shift_windows.py)

### M133 — Synthesis transformation orbit engine

**Evidence:** Implemented

**How it works.** Apply a registry of deterministic mixing transformations repeatedly to produce candidate orbits, then rank the resulting integers.

**What is actually done.** The synthesis script's capture/decay/catalyst names denote ordinary bit/arithmetic operations. It generates and scores candidate scalars; the names do not represent physical or quantum processes.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Hybrid orbit, capture/decay/catalyst/moderator transformations rank unused-byte novelty; terminology does not imply quantum physics.

**Sources.** [S233: synthesis_puzzle71_solver.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/synthesis_puzzle71_solver.py)

### M134 — Unused-byte novelty scoring

**Evidence:** Executed record

**How it works.** Count byte positions whose values have not appeared in the solved-key corpus, favoring combinations labeled novel.

**What is actually done.** The orbit batch verifier tests the actual scalar against the address. High novelty scores do not measure target agreement; some archived candidates were even below the valid puzzle interval.

**Inputs needed.** An anchor/seed, explicit transformation or mask rules, bounded traversal settings and the target hash for a real candidate check.

**What the result means.** Score 8/9 or 9/9 measures byte novelty, not target agreement. Archived 1,800-candidate verification had zero hits.

**Sources.** [S173: orbit_candidates_report.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/orbit_candidates_report.md)

## HP-RTE, topology and pattern-avoidance experiments

### M135 — Original HP-RTE weighted shard sampling

**Evidence:** Audited/corrected

**How it works.** The original recipe samples a key, derives a byte/nibble label and uses its assigned weight to move the output into a biased subrange.

**What is actually done.** Historical code uses floating-point offsets, and successive versions exclude different parts of the interval. The repaired generator removes that unsupported exclusion and uses exact integer sampling.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Historical float-based biased generator excludes part of the advertised interval; corrected pipeline uses full-support integer partitions.

**Sources.** [S002: bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [S003: README.md](/home/arialmohan/puzzle71-corrected/README.md)

### M136 — Two-byte rotation and four-hex-tree claims

**Evidence:** Audited/corrected

**How it works.** Rotate a byte string to change which byte is inspected. A genuine four-hex tree would also define branching and traversal over four hex digits.

**What is actually done.** The supplied generator rotates by two bytes, not two hex characters. Its tree-depth name is not used to implement the claimed tree partitioning.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Rotation exists, but original tree-depth configuration did not implement the claimed tree search.

**Sources.** [S002: bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [S003: README.md](/home/arialmohan/puzzle71-corrected/README.md)

### M137 — Million-record JSON/JSONL generation

**Evidence:** Executed record

**How it works.** Serialize one record per generated candidate or interval. JSONL allows records to be written one at a time.

**What is actually done.** The corrected run wrote a million descriptive records, then separately verified their sample keys and boundaries. File size and record count measure storage and generation, not exhaustive cryptographic coverage.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Large record counts are data-generation work, not cryptographic search coverage; streaming JSONL avoids all-record memory use.

**Sources.** [S014: run-1M.log](/home/arialmohan/puzzle71-corrected/run-1M.log); [S003: README.md](/home/arialmohan/puzzle71-corrected/README.md)

### M138 — Weighted modular-diameter diversity

**Evidence:** Audited/corrected

**How it works.** The old statistic computes pairwise numeric spread and multiplies it by a subset-dependent average bias weight.

**What is actually done.** The original uint64 conversion cannot hold 71-bit scalars; unsigned subtraction also wraps. Fixing integer overflow alone does not prove that the weighted expression satisfies diversity axioms.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** uint64 overflow, unsigned differences and unproved subset weights invalidate original diversity claims.

**Sources.** [S002: bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [S022: AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md)

### M139 — Finite-sample Cauchy/convergence claims

**Evidence:** Audited/corrected

**How it works.** True Cauchyness and convergence require bounds over arbitrary sufficiently late terms of an infinite sequence, with the proposed limit included for convergence.

**What is actually done.** The old functions sample subsets of a finite whole history and compare an arbitrary threshold. They are finite clustering tests mislabeled as asymptotic guarantees and cannot locate an unknown private key.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Sampling a finite history is not an asymptotic tail criterion; clustering cannot identify the unknown scalar.

**Sources.** [S022: AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md); [S003: README.md](/home/arialmohan/puzzle71-corrected/README.md)

### M140 — Exact ordinary diameter diagnostic

**Evidence:** Executed record

**How it works.** Diameter is the largest value minus the smallest. With fixed normalization it describes a finite sample's coordinate spread exactly.

**What is actually done.** The corrected script computes integer min/max without an all-pairs matrix. It labels the result descriptively and makes no claim of convergence toward the cryptographic target.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Integer max-minus-min measures sample spread without claiming convergence or cryptographic proximity.

**Sources.** [S011: pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py); [S017: test_pipeline.py](/home/arialmohan/puzzle71-corrected/test_pipeline.py)

### M141 — Cantor-like finite-stage constructions

**Evidence:** Audited/corrected

**How it works.** Repeatedly remove a middle interval from each remaining closed interval, tracking exact rational endpoints and total surviving length.

**What is actually done.** The corrected example removes half at every stage; after eight stages length is 1/256. The infinite limit has zero measure, unlike the earlier claimed fat-Cantor interpretation.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Exact rational construction corrects historical measure calculations; constant half-removal tends to zero measure.

**Sources.** [S011: pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py); [S003: README.md](/home/arialmohan/puzzle71-corrected/README.md)

### M142 — Cantor-to-keyspace homeomorphism claim

**Evidence:** Audited/corrected

**How it works.** A homeomorphism must be a continuous bijection with a continuous inverse. An infinite Cantor set cannot be bijective with a finite integer keyspace.

**What is actually done.** The earlier function merely scales floating coordinates into sample min/max bounds and rounds to integers. It is a lossy candidate map, not the source paper's homeomorphism construction.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Rounding real samples to finite keys is not a homeomorphism from an infinite Cantor set.

**Sources.** [S022: AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md); [S003: README.md](/home/arialmohan/puzzle71-corrected/README.md)

### M143 — Byte-value arithmetic-progression avoidance

**Evidence:** Executed record

**How it works.** Search the set of distinct byte values for a nonconstant arithmetic progression such as 10,20,30. Every requested term must be present.

**What is actually done.** Corrected code extracts nine actual bytes, ignores order/multiplicity for this test, and records a Boolean label. It does not treat pattern avoidance as evidence that the key is more likely.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Corrected diagnostic detects nonconstant APs among byte values; it is not used to discard search candidates.

**Sources.** [S011: pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py); [S017: test_pipeline.py](/home/arialmohan/puzzle71-corrected/test_pipeline.py)

### M144 — Monochromatic byte-position progression checks

**Evidence:** Executed record

**How it works.** Treat byte positions as the arithmetic progression and ask whether equally spaced positions carry the same byte value.

**What is actually done.** The corrected predicate differs deliberately from value-set APs. Repeated byte values can trigger a positional pattern even when the value set has no nonconstant arithmetic progression.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Equal bytes at equally spaced positions are distinguished from APs in the values themselves.

**Sources.** [S011: pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py)

### M145 — Double-AP and RamseyScript subset claims

**Evidence:** Audited/corrected

**How it works.** Ramsey search recursively extends combinatorial objects while rejecting forbidden structures; a faithful interpreter must implement the specified objects and filter semantics.

**What is actually done.** The historical class lacks a real parser and uses an unrelated parity placeholder for double APs. Its general k-AP detector can accept an incomplete progression; later versions repair only some defects.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Historical code uses placeholders and incomplete language semantics; original filter claims do not establish a cryptographic advantage.

**Sources.** [S002: bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [S022: AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md)

### M146 — Pattern-label eligibility correction

**Evidence:** Executed record

**How it works.** Keep pattern classification as metadata while preserving eligibility of every integer in the advertised interval.

**What is actually done.** Educational and corrected pipelines do not discard a candidate for an AP label. Known-key tests separately measure label preferences and full-range eligibility, which must not be conflated.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Backtests retain all candidates while reporting pattern labels; eligibility is not evidence that a pattern predicts keys.

**Sources.** [S024: backtest.py](/home/arialmohan/puzzle71-educational/backtest.py); [S023: BACKTEST.md](/home/arialmohan/puzzle71-educational/BACKTEST.md)

### M147 — Classical hyper-phase Q1-Q9 formulas

**Evidence:** Audited/corrected

**How it works.** Evaluate trigonometric/exponential recurrence formulas indexed by state and bit position, then compare a magnitude with a chosen threshold.

**What is actually done.** These are classical numerical calculations. Earlier versions omit states; later formulas fill them but still neither ingest the target hash nor construct a quantum circuit or valid key-extraction equation.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Numerical toy formulas have no demonstrated target relation; no quantum circuit or recovery is implemented.

**Sources.** [S002: bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [S022: AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md)

### M148 — Bit-position periodic table / CFSG labels

**Evidence:** Conversation proposal

**How it works.** Organize bit indices into a table with powers of two, symbolic families and heuristic scores. Such a table can be an interface for diagnostics.

**What is actually done.** The supplied transcript assigns random simulated biases and CFSG-inspired labels. For bits below 71, reducing 2^b modulo the large group order changes nothing; no hidden algebraic advantage follows.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Supplied transcript uses simulated random biases and organizational labels; no local validated cryptanalytic result was established.

**Sources.** [S003: README.md](/home/arialmohan/puzzle71-corrected/README.md)

### M149 — BPK-TSP and million-process architecture

**Evidence:** Conversation proposal

**How it works.** A scheduler could distribute generation, verification and artifact collection across workers, with hardware-specific executors.

**What is actually done.** BPK-TSP, million-process and FPGA claims are architectural narrative in the supplied material. Concrete implementations elsewhere are documented separately; this entry has no corroborated complete large-scale execution.

**Inputs needed.** Candidate integers/bytes and explicitly defined numerical or pattern rules; mathematical diagnostics do not themselves supply target information.

**What the result means.** Scheduling and FPGA/massive-process claims in supplied reports are proposals without corroborated execution evidence in this inventory.

**Sources.** [S003: README.md](/home/arialmohan/puzzle71-corrected/README.md)

## ECDSA, nonce relations and signature-data searches

### M150 — Aranyn Block-1 manual-nonce binding

**Evidence:** Executed record

**How it works.** ECDSA gives s*w=z+r*d modulo the group order when the signing nonce is chosen as the Block-1 scalar w.

**What is actually done.** The code verifies the signature and derives w=A+B*d. Substituting that relation back into the same signature adds no independent equation; one unknown scalar remains behind public-point multiplication.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** One signature gives an affine relation between two scalar names but leaves an ECDLP-equivalent unknown.

**Sources.** [S149: crypto_non_bruteforce_methods.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/crypto_non_bruteforce_methods.md)

### M151 — Puzzle-160 nonce/signing-key relation

**Evidence:** Implemented

**How it works.** If an ECDSA nonce is the Puzzle-160 key, knowledge of either that nonce or the signer scalar determines the other algebraically.

**What is actually done.** user_signature.py supplies the forward/reverse formulas and known public-point checks. Neither published relation alone reveals an undisclosed nonce; solving for it still requires new information or ECDLP work.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Recover one scalar if the other is supplied; the published relation does not independently reveal either unknown key.

**Sources.** [S127: user_signature.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/user_signature.py)

### M152 — Cross-signature #160 / Block-1 linear relations

**Evidence:** Implemented

**How it works.** Combine the two affine signature relations and test small coefficients directly on their public points.

**What is actually done.** The relation search sweeps specified alpha/beta/gamma families and verifies candidate equations. This can detect a genuine small relation without knowing either scalar, but cannot assume one exists.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Search bounded small coefficients visible on public points; any result would need independent target verification.

**Sources.** [S213: search_160_block1_relation.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/search_160_block1_relation.py); [S179: relation_160_block1.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/relation_160_block1.md)

### M153 — ECDSA nonce-reuse recovery

**Evidence:** Synthetic/recorded tests

**How it works.** Reusing the same nonce for different messages creates two equations with the same unknown nonce, allowing elimination and scalar recovery.

**What is actually done.** Synthetic sign/recover tests validate the algebra. Real harvested data are grouped by signer and r; the archived samples did not provide the required exploitable reuse pair.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Algebraic recovery works in planted examples; harvested real signatures showed no matching reuse groups in recorded samples.

**Sources.** [S104: ecdsa_affine_nonce.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/ecdsa_affine_nonce.py); [S147: counter_nonce_analysis.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/counter_nonce_analysis.md)

### M154 — Known affine-related nonce recovery

**Evidence:** Synthetic tests

**How it works.** A known relation k2=a*k1+b between two ECDSA nonces supplies an extra equation that makes the signer scalar solvable.

**What is actually done.** ecdsa_affine_nonce.py creates controlled affine signature pairs and recovers the planted key. The puzzle target does not gain that relation merely because the implementation works on planted examples.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Synthetic signature pairs validate the formula when the nonce relation is actually known. Applicability requires such a pair.

**Sources.** [S104: ecdsa_affine_nonce.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/ecdsa_affine_nonce.py); [S220: backtest_arxiv_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/backtest_arxiv_methods.py)

### M155 — Counter nonces and small offset relation tests

**Evidence:** Executed record

**How it works.** Guess tiny nonce values or small differences between two nonce values, then use ECDSA equations to derive a signer candidate.

**What is actually done.** Recorded scans test declared nonce and offset ranges against harvested signatures and verify candidates. A null result covers those guesses, not arbitrary unknown nonce relations.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Archived harvested-signature scans tested tiny nonces and bounded offsets; no verified wallet-key recovery reported.

**Sources.** [S147: counter_nonce_analysis.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/counter_nonce_analysis.md)

### M156 — Hidden-number/partial-MSB nonce leakage models

**Evidence:** Synthetic/applicability

**How it works.** Multiple signatures with known nonce bits create inequalities that can support Hidden Number Problem/lattice recovery or smaller interval searches.

**What is actually done.** The registry models synthetic MSB leaks and required bit budgets. The available target data do not include the corresponding independent bit leaks or adequate applicable signatures.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Synthetic bounds and applicability checks exist; the target signatures do not supply the required leakage measurements.

**Sources.** [S108: joc_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/joc_methods.py); [S149: crypto_non_bruteforce_methods.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/crypto_non_bruteforce_methods.md)

### M157 — Polynonce/half-half/side-channel possibilities

**Evidence:** Applicability review

**How it works.** Polynomial nonce recurrences, concatenated half-nonces or measured side-channel leakage provide special extra structure beyond ordinary ECDSA.

**What is actually done.** The literature mapping checks whether those prerequisites exist. This is an applicability review; it does not execute a successful lattice/side-channel attack on a single ordinary signature.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Reviewed as conditional attacks; missing signatures, special nonce structure or measurements block their use on the cited target.

**Sources.** [S149: crypto_non_bruteforce_methods.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/crypto_non_bruteforce_methods.md)

### M158 — ECDSA versus Schnorr/BIP340 checks

**Evidence:** Executed record

**How it works.** Schnorr and ECDSA use different equations and message challenges. A signature must satisfy the correct scheme's verification relation.

**What is actually done.** The comparison derives Schnorr/BIP340 challenges and tests forced interpretations of the ECDSA constants. Reinterpreting bytes under another scheme does not provide a second valid signature equation.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Forced reinterpretations and challenge consistency are compared; changing signature labels does not create a new independent equation.

**Sources.** [S212: schnorr_ecdsa_aranyn_compare.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/schnorr_ecdsa_aranyn_compare.py); [S182: schnorr_ecdsa_aranyn_compare.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/schnorr_ecdsa_aranyn_compare.md)

### M159 — Early coinbase signature harvesting

**Evidence:** Executed record

**How it works.** Extract signature data from spent early coinbase outputs and identify the signer/public point needed for nonce analysis.

**What is actually done.** Harvesters follow actual spends, parse signatures and group them for reuse/target-r tests. The saved 51-signature sample provides data, not previously unknown recovered wallet keys.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Saved report records 51 signatures and no nonce-reuse recovery; the graph is a data source, not a solve.

**Sources.** [S154: early_coinbase_sig_harvest.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/early_coinbase_sig_harvest.md)

### M160 — Descendant/graph signature expansion

**Evidence:** Implemented

**How it works.** Follow descendants and consolidation transactions to collect more signatures associated with the original outputs.

**What is actually done.** Graph/descendant tools expand a bounded transaction frontier. Additional transaction relationships can increase the sample but do not prove that every downstream signer shares a private scalar.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Expand UTXO descendants and consolidation transactions to obtain additional signature samples.

**Sources.** [S227: harvest_early_coinbase_descendants.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/harvest/harvest_early_coinbase_descendants.py); [S228: harvest_early_coinbase_graph.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/harvest/harvest_early_coinbase_graph.py)

### M161 — BTCparser sleeping/whale sweep signatures

**Evidence:** Executed record

**How it works.** Use sleeping-address or whale-sweep indexes to select transactions likely to contain useful signature collections.

**What is actually done.** The BTCparser sweep parses indexed blocks and selected spend transactions, then tests collected r values. It is a bounded data-gathering strategy, not evidence of biased nonces.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Saved sweep harvested 151 signatures with no reuse groups or target-r hits in that sample.

**Sources.** [S143: btcparser_sweep_signature_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/btcparser_sweep_signature_scan.md)

### M162 — Lattice-candidate sufficiency scan

**Evidence:** Executed record

**How it works.** Count usable signatures per signer before attempting attacks that require repeated nonce information or leakage.

**What is actually done.** The lattice-candidate report groups 184 signatures into wallets and finds none meeting its multi-signature threshold. No target lattice recovery is performed simply by detecting that data are insufficient.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Saved report has 184 signatures but no wallet with the required multi-signature count; no lattice recovery executed.

**Sources.** [S168: lattice_candidate_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/lattice_candidate_scan.md)

### M163 — SegWit/testnet target-r scans

**Evidence:** Executed record

**How it works.** Search additional witness and testnet signature data for the same nonce x-coordinate or related target public material.

**What is actually done.** Dedicated scans compare parsed r values in their fetched samples. Matching a signature field would need scheme and signer verification; absence in a sample is not a global chain proof.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Search archived alternate-chain and witness signatures for the manual-nonce x-coordinate; finite scan scope only.

**Sources.** [S184: segwit_aranyn_r_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/segwit_aranyn_r_scan.md); [S189: testnet_aranyn_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/testnet_aranyn_scan.md)

### M164 — Signed-message and fork public-key leaks

**Evidence:** Implemented

**How it works.** Extra signed messages or fork spends may reveal a public point or an independently usable signature absent from the current target record.

**What is actually done.** Search scripts look for that public material. They do not obtain private keys from a public-point leak alone; they may only enable a different, still expensive recovery method.

**Inputs needed.** Valid signature scalars and message hashes tied to known public keys; additional relations/leakage when the selected attack requires them.

**What the result means.** Search additional public signature/pubkey material; utility depends on finding independently applicable data.

**Sources.** [S235: search_signed_bitcoin_messages.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/scans/search_signed_bitcoin_messages.py); [S234: scan_fork_pubkey_leaks.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/scans/scan_fork_pubkey_leaks.py)

## On-chain, metadata and clue relationships

### M165 — DP metadata distances and signed collision variants

**Evidence:** Executed record

**How it works.** Interpret candidate metadata slices as walk distances and test whether they satisfy the claimed tame/wild public-point equations.

**What is actually done.** Archived scans vary bit widths, signs, starts and collision formulas. A distance-looking field is rejected unless its derived point or scalar matches the target.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Archived metadata-width, start-point, sign and collision-formula tests found no verified puzzle scalar.

**Sources.** [S171: non_bruteforce_audit_20260831.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/non_bruteforce_audit_20260831.md)

### M166 — DP x-coordinates as candidate public keys

**Evidence:** Executed record

**How it works.** A valid x-coordinate has up to two curve-point lifts, each yielding a possible compressed public key and address hash.

**What is actually done.** The binary audit checks both parities against puzzle targets. This tests whether the dump literally contains the target public key, not whether arbitrary points can be inverted into scalars.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Both point parities were checked against puzzle addresses; no match in the recorded binary sample.

**Sources.** [S171: non_bruteforce_audit_20260831.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/non_bruteforce_audit_20260831.md)

### M167 — TRAILING / LOW71 / bit-slice anchors

**Evidence:** Executed record

**How it works.** Slice or reinterpret a trailing metadata integer to produce anchor scalars for selected puzzle widths.

**What is actually done.** LOW71, low/high pieces and literal TRAILING values are checked as concrete candidates. Their bit length or range membership alone is not evidence of target identity.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Numerical range coincidence is separate from address correctness; recorded anchor checks failed target verification.

**Sources.** [S137: any_relation_report.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/any_relation_report.md); [S171: non_bruteforce_audit_20260831.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/non_bruteforce_audit_20260831.md)

### M168 — Leading-zero public-key collection analysis

**Evidence:** Implemented

**How it works.** Analyze a collection selected for leading-zero x-coordinate masks, then search membership, pairwise offsets and small public-point relations.

**What is actually done.** The script compares known corpora, GLV transforms, linear combinations, bounded BSGS differences and generator recipes. Mask rarity must be evaluated conditional on the deliberate point-selection rule.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Tests mask statistics, membership, pairwise differences, GLV relations, linear combinations and bounded BSGS offsets.

**Sources.** [S203: analyze_leading_zero_pubs.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/analyze_leading_zero_pubs.py)

### M169 — Cross-artifact relation bundles

**Evidence:** Implemented

**How it works.** Bundle source hashes, parsed values and named relationships so later investigations can trace every clue to its artifact.

**What is actually done.** relation_bundle.py packages DP/TRAILING/CTheory hypotheses and metadata. It preserves evidence lineage without claiming that colocated numbers imply a key equation.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Package DP, metadata and CTheory evidence without claiming that correlated artifacts reveal a key.

**Sources.** [S118: relation_bundle.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/relation_bundle.py)

### M170 — Genesis/early-coinbase relationship graph

**Evidence:** Executed record

**How it works.** Build a graph linking early blocks, output public keys, spends and known puzzle entities.

**What is actually done.** The relationship mapper collects public points and transaction edges. A shared transaction or funder is a graph link; recovering a shared scalar requires separate cryptographic evidence.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Map published public points and spending relationships; shared transactions need not imply shared private keys.

**Sources.** [S144: chain_relationship_map.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/chain_relationship_map.md)

### M171 — Puzzle-135 sweep/fanout tracing

**Evidence:** Executed record

**How it works.** Follow the known Puzzle-135 spending destination forward and backward to identify related addresses or messages.

**What is actually done.** The fanout script tags puzzle neighbors and summarizes transaction flows. It tracks an observed sweep; it does not establish that this local code discovered the spent key.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Follow sweep destinations, funding and tagged puzzle neighbors; movement of funds is not local proof of solving the puzzle.

**Sources.** [S158: fanout_puzzle135.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/fanout_puzzle135.md)

### M172 — 0.99-BTC fanout cluster tracing

**Evidence:** Executed record

**How it works.** Detect transactions with repeated 0.99-BTC outputs and traverse their funding/fanout neighbors.

**What is actually done.** The crawler uses explicit output-count/value thresholds and bounded BFS expansion. This identifies a transaction pattern or cluster, not an algebraic relation among its private keys.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Breadth-first funding/output graph searches and message scans are archived.

**Sources.** [S159: follow_099_fanouts.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/follow_099_fanouts.md); [S157: fanout_cc6f_trace.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/fanout_cc6f_trace.md)

### M173 — Sender relay / OP_RETURN / extra-data clues

**Evidence:** Executed record

**How it works.** Decode message-bearing transaction fields and follow a relay chain for possible puzzle instructions or artifacts.

**What is actually done.** Sender tools parse OP_RETURN, inspect extra data and search references. Public text is treated as a lead requiring verification, not executable instructions or proven secret leakage.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Decode message relays and scan transaction fields for key fragments or target relations.

**Sources.** [S190: trace_sender_extended.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/trace_sender_extended.md); [S191: trace_sender_extra_data_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/trace_sender_extra_data_scan.md)

### M174 — Early spent-block number encodings

**Evidence:** Implemented

**How it works.** Convert lists of spent block numbers or transaction fields into candidate encodings and compare with known puzzle clues.

**What is actually done.** The analyzer tests stated integer/string representations and inspects spends. Finding readable text or a similar hex fragment is exploratory evidence, not a verified key.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Test block-index encodings and inspect spends for puzzle-like hexadecimal data.

**Sources.** [S204: analyze_spent_block_encoding.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/analyze_spent_block_encoding.py)

### M175 — Hub-address and recoverability scans

**Evidence:** Executed record

**How it works.** Query selected addresses and outputs to find spends, public keys, old funds or other data relevant to recoverability hypotheses.

**What is actually done.** Saved scans summarize activity and candidate opportunities. They do not freshly establish present balances, authority over wallets or a successful cryptographic recovery.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Address/UTXO activity scans identify data leads; no present ownership or balance conclusions are newly verified here.

**Sources.** [S164: hub_3EEJF_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/hub_3EEJF_scan.md); [S178: recoverable_bitcoin_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/recoverable_bitcoin_scan.md)

### M176 — Puzzle reflection and unlock relationship scans

**Evidence:** Executed record

**How it works.** Look for reflected labels, addresses or tier relationships suggesting that one puzzle might encode information useful for another.

**What is actually done.** Reports enumerate tested correspondences and unlocking ideas. A relation between labels is distinct from a demonstrated scalar transformation that reproduces both targets.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Compare puzzle labels, addresses and transaction relationships; no validated universal unlocking rule established.

**Sources.** [S176: puzzle_reflection_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/puzzle_reflection_scan.md); [S177: puzzle_unlock_relationships.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/puzzle_unlock_relationships.md)

### M177 — Historical website/archive and directory searches

**Evidence:** Executed record

**How it works.** Search historical sites and directory/archive listings for original challenge files, creator software or missing public parameters.

**What is actually done.** Triage scripts save candidate links and matches. The inventory records those searches without treating every archived webpage as authenticated creator provenance or a successful lead.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Old Bitcoin sites, indexes and Drive leads were triaged for relevant artifacts.

**Sources.** [S172: old_bitcoin_sites_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/old_bitcoin_sites_scan.md); [S165: index_of_directories_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/index_of_directories_scan.md); [S161: google_drive_puzz_triage.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/google_drive_puzz_triage.md)

### M178 — Time-Will-Tell phrase/path hypotheses

**Evidence:** Implemented/branch record

**How it works.** Try bounded interpretations of an explicitly supplied recovery phrase, including word-subset and passphrase/path choices.

**What is actually done.** The branch implementation checks selected mnemonic and HD-wallet variants against named targets. Private phrases are omitted from the report, and unrun full search coverage is not inferred.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Bounded mnemonic subset, passphrase and derivation-path tests are documented; private phrases are excluded from this report.

**Sources.** [S217: crack_time_will_tell_seed.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/chain/crack_time_will_tell_seed.py); [S253: Branch-cursor-time-will-tell-seed-b049.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Branch-cursor-time-will-tell-seed-b049.md)

### M179 — Complete chat-lead indexing and candidate extraction

**Evidence:** Executed record

**How it works.** Index complete available user/assistant messages, distinguish speakers and extract only relevant candidate claims or supplied leads.

**What is actually done.** Existing audit scripts preserve source hashes, locators and redacted witnesses. Chat assertions can guide tests, but a model's claim of running code is not substituted for execution artifacts.

**Inputs needed.** Published transaction/block data, binary artifacts or archived messages and a fixed target comparison. External facts need separate authentication.

**What the result means.** Existing speaker-aware source index covers 685 matching conversations; assistant assertions are not execution evidence.

**Sources.** [S068: REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md); [S075: scan_chats.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/scan_chats.py)

## Weak-entropy wallet and PRNG research

### M180 — Milk Sad raw MT19937 seed expansion

**Evidence:** Recorded GPU sweep

**How it works.** Reproduce the exact weak MT19937 entropy stream produced from a 32-bit libbitcoin seed, then derive the corresponding scalar/public point.

**What is actually done.** Native and CUDA implementations mirror the modeled software path. The saved raw-entropy sweep compares supported address hashes with a dated funded index, rather than attacking arbitrary secure seeds.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Archived report claims full 32-bit seed sweep with zero funded-index hits; this inventory does not rerun or independently certify that sweep.

**Sources.** [S170: milksad_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/milksad_cuda_sweep.md); [S249: weak_entropy_prng.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_prng.py)

### M181 — Milk Sad BIP39/BIP44/49/84 derivations

**Evidence:** Recorded GPU sweep

**How it works.** Turn the weak entropy into a BIP39 mnemonic seed, derive specified HD paths and compare supported address types.

**What is actually done.** The archived sweep covers declared BIP44/49/84 account paths and serializations. PBKDF2 and child derivation make this substantially different from checking the raw entropy as a scalar.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Archived mnemonic and derivation-path sweep reports zero funded-index hits; bounded historical index and path coverage only.

**Sources.** [S170: milksad_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/milksad_cuda_sweep.md); [S250: weak_entropy_wallet.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_wallet.py)

### M182 — Profanity MT19937-64 base-key replay

**Evidence:** Recorded GPU sweep

**How it works.** Replay Profanity's small seed expansion to reconstruct its base scalar under a specified output word order.

**What is actually done.** Saved CUDA results enumerate base seeds in both orders and check three hash variants. Offset-zero coverage does not automatically cover keys reached by later vanity-search increments.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Archived report enumerates both word orders over 32-bit seeds with zero funded-index hits at offset zero.

**Sources.** [S175: profanity_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/profanity_cuda_sweep.md)

### M183 — Profanity incremental offset grinding

**Evidence:** Branch/implementation

**How it works.** Starting from a reconstructed weak base key, add small scalar offsets and reuse point additions to check nearby vanity-search states efficiently.

**What is actually done.** The branch adds offset-window flags and remote sharding scripts. Its documentation explicitly separates Python-side tests from real-GPU compile/verification that was still outstanding there.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Extends base keys with small scalar offsets. Branch notes explicitly say real-GPU compile/verification was not yet done there.

**Sources.** [S252: Branch-cursor-profanity-offset-grind-8a23.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Branch-cursor-profanity-offset-grind-8a23.md)

### M184 — Java util.Random replay

**Evidence:** Implemented/registry

**How it works.** Java Random updates a 48-bit linear-congruential state; nextBytes exposes a particular sequence of output bytes.

**What is actually done.** The model reproduces those bytes from a candidate explicit seed. Timestamp-window enumeration tests only programs that really seeded and consumed that generator in the modeled way.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Models the 48-bit LCG and timestamp-seeded nextBytes path; registered runtime vectors distinguish model fidelity from a recovery.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M185 — Java SUN SHA1PRNG low-entropy seed replay

**Evidence:** Implemented/registry

**How it works.** SUN SHA1PRNG with an explicit low-entropy seed evolves deterministic SHA-1-derived state and emits predictable bytes.

**What is actually done.** The implementation reproduces setSeed byte order and signed state updates. It does not assume every SecureRandom call is weak; normal unobserved platform entropy changes the problem.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Deterministic setSeed model is present; not every Java/Android wallet follows that path.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M186 — glibc rand/random byte-fill replay

**Evidence:** Implemented/registry

**How it works.** glibc rand/random uses additive-feedback state; truncating its outputs to bytes can make keys reproducible from a small seed.

**What is actually done.** The family model initializes and warms the state, then emits low bytes under the catalog's byte-fill recipe. Generator fidelity is tested separately from applicability to a target wallet.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Models clock-seeded additive-feedback output truncated into key bytes.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M187 — Lehmer minstd_rand0 replay

**Evidence:** Implemented/registry

**How it works.** minstd_rand0 multiplies state by 16807 modulo 2^31-1. An enumerable state determines the byte stream.

**What is actually done.** The registry wraps this Lehmer generator into candidate key bytes and runtime vectors. The attack premise is misuse for wallet entropy, not a weakness of secp256k1 itself.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Models multiplier 16807 weak-generator key bytes.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M188 — Lehmer minstd_rand replay

**Evidence:** Implemented/registry

**How it works.** minstd_rand uses multiplier 48271 with the same prime modulus, producing a different deterministic stream.

**What is actually done.** The model keeps this family separate because seed replay with the wrong multiplier produces different keys. A sweep must identify the exact generator and byte extraction recipe it covers.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Models multiplier 48271 key-byte generation, separately from minstd_rand0.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M189 — AVR/Arduino rand replay

**Evidence:** Implemented/registry

**How it works.** Embedded sketches may derive key bytes from a deterministic rand stream seeded by millis or limited sensor readings.

**What is actually done.** The AVR/Arduino model implements the stated Lehmer-style stream under candidate seeds. It does not model unknown hardware noise measurements or every embedded random library.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Models weak embedded Lehmer-style output under enumerable seeds.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M190 — Modern PHP MT19937 byte-fill replay

**Evidence:** Implemented/registry

**How it works.** Modern PHP mt_rand uses MT19937 and particular range-output rules. Repeated byte requests determine a key from its seed.

**What is actually done.** The implementation emits bytes under modern mode and compares with runtime vectors. A generic MT19937 sequence with different range scaling is not the same candidate family.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** PHP 7.1+ generator/range semantics are modeled separately from legacy PHP.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M191 — Legacy PHP broken-twist replay

**Evidence:** Implemented/registry

**How it works.** Older PHP used a different twist/range behavior, so a small seed produces a distinct key stream from modern PHP.

**What is actually done.** A separate legacy mode reproduces that behavior. Historical weakness labels alone are insufficient without matching the actual PHP version and key-generation recipe.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Models the older mt_rand twist and range-scaling behavior, not covered by ordinary MT19937 assumptions.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M192 — PHPCoinAddress legacy and modern keygen

**Evidence:** Implemented/registry

**How it works.** PHPCoinAddress applies its own bounded byte calls, including a special first-byte range, around PHP's generator.

**What is actually done.** Dedicated wrappers reproduce those calls for both old and modern modes. Replaying plain mt_rand bytes would omit this wallet-specific transformation and could miss its generated keys.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Dedicated first-byte/range rules are modeled under both PHP generator modes.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M193 — V8 MWC1616 / Randstorm-era byte fill

**Evidence:** Implemented/registry

**How it works.** Old V8 Math.random combines multiply-with-carry state; weakly seeded outputs can be reproduced and packed into key bytes.

**What is actually done.** The registry supplies the historical MWC1616 byte-fill model. A full Randstorm wallet route may include additional entropy mixing and consumption order not implied by that one modeled stream.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Historical JavaScript Math.random byte generation model; a vulnerable-family model is not attribution to a target wallet.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M194 — V8 xorshift128 state recovery

**Evidence:** Implemented

**How it works.** Observed floating Math.random outputs expose some generator bits. Constraint solving can recover compatible xorshift state under the modeled engine order.

**What is actually done.** The source contains forward generation and state-recovery helpers. It requires actual usable observations; no such target observations are created by merely knowing a Bitcoin address.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Recovers generator state from observed Math.random outputs under the modeled engine semantics; no target observations established here.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M195 — .NET System.Random replay

**Evidence:** Implemented/registry

**How it works.** Explicitly seeded .NET System.Random evolves subtractive state; low-entropy TickCount-style seeds allow replay.

**What is actually done.** The model reproduces the framework-compatible byte stream and supports runtime vectors. Newer runtime semantics or additional entropy require a different model.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Models explicitly seeded subtractive generator and TickCount-style seed scope.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M196 — Timestamp/UUID hash-derived keys

**Evidence:** Implemented

**How it works.** Hashing a predictable timestamp or weak UUID produces a full-length string but retains the small input uncertainty.

**What is actually done.** The catalog hashes selected second/millisecond and weak-UUID encodings into candidate keys. It searches their input choices, not the full 256-bit digest space.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** SHA-256 clock, millisecond and weak-UUID key recipes are modeled as bounded generator hypotheses.

**Sources.** [S248: weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

### M197 — Early-2009 clock-window seed replay

**Evidence:** Executed record

**How it works.** Guess creation-time values, feed them into named weak generators/encodings and compare with early coinbase public keys.

**What is actually done.** The widest saved clock-window run checks its finite 2008-2009 range and reports no matches. Actual OpenSSL machine-state seeding is not reproduced by these timestamp hypotheses.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Widest saved report records 250,581,618 tested keys and no early-coinbase target recovery; true machine-state entropy is not enumerated.

**Sources.** [S142: block1_keygen_seed_sweep_2008.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/block1_keygen_seed_sweep_2008.md)

### M198 — Weak-entropy multi-family CUDA sweep

**Evidence:** Recorded GPU sweep

**How it works.** Parallel GPU threads map seeds through PRNG, curve multiplication and hash comparison against a supported address index.

**What is actually done.** Archived multi-family runs report seed counts and planted-index detection checks. Their coverage is bounded by the selected generator families, seed intervals and supported address encodings.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Saved report claims 27.5 billion seeds and zero funded-index hits, with planted-index detection tests. Historical record, not rerun here.

**Sources.** [S195: weak_entropy_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/weak_entropy_cuda_sweep.md)

### M199 — Bloom plus sorted funded-address index

**Evidence:** Implemented

**How it works.** A Bloom filter rapidly rejects most nonmembers; positive candidates then undergo exact lookup in a sorted hash160 index.

**What is actually done.** build_loyce_index.py constructs the index and GPU code performs membership checks. Bloom positives alone are not hits; the source index's date and skipped address types limit conclusions.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Probabilistic prefilter backed by exact lookup; index date and supported address types bound conclusions.

**Sources.** [S082: build_loyce_index.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/build_loyce_index.py); [S195: weak_entropy_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/weak_entropy_cuda_sweep.md)

### M200 — Weak-RNG repository-source triage

**Evidence:** Executed record

**How it works.** Search wallet source for weak RNG calls and correlate findings with known disclosures and affected versions.

**What is actually done.** Curated repository scans record references and matching lines. A weak RNG in tests, an old dependency or a non-keygen path is not automatic evidence that current wallet keys are vulnerable.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Pattern hits and disclosures locate candidate implementations; historical/current refs and dependency bugs must be distinguished.

**Sources.** [S196: weak_entropy_repos.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/weak_entropy_repos.md); [S197: weak_entropy_unverified.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/weak_entropy_unverified.md)

### M201 — Recoverable-hit rederivation/address-type audit

**Evidence:** Audited/corrected

**How it works.** Recompute the complete derivation and exact address type before accepting a scanner's proposed recovery.

**What is actually done.** verify_scan_hits.py rejects candidates whose derivation or P2PKH/P2SH/witness interpretation does not match. It corrects the earlier tendency to label raw index associations as recovered wallets.

**Inputs needed.** An exact vulnerable software-generation recipe and bounded seed/state assumptions; a dated target/index for replay verification.

**What the result means.** Recompute candidate addresses and reject type mismatches before reporting a recovery; prior raw hits were not all valid.

**Sources.** [S246: verify_scan_hits.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/verify_scan_hits.py); [S256: Weak-Entropy-Research.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Weak-Entropy-Research.md)

## Exploratory number theory, statistics and literature-inspired probes

### M202 — Digital-root puzzle-index association

**Evidence:** Executed record

**How it works.** Reduce a scalar's decimal digits repeatedly and compare the result with a puzzle-index rule.

**What is actually done.** The creative-theory report counts observed matches and compares with controls. A small digital-root match imposes at most a weak residue condition, not the scalar's full value.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** One of thirteen archived creative theories; report marks it nonsignificant, not a recovered-key method.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M203 — Public-key x-coordinate steganography

**Evidence:** Executed record

**How it works.** Compare selected low bits or XOR patterns of k and the public x-coordinate for signs of intentional embedded information.

**What is actually done.** The report summarizes bit statistics against random keys. Public multiplication is nonlinear; apparent low-bit similarity must predict unseen scalars before it can guide recovery.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Compare key/public-coordinate low-bit relations with random controls; no convincing result recorded.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M204 — Zeckendorf/Fibonacci sparsity

**Evidence:** Executed record

**How it works.** Represent integers as sums of nonadjacent Fibonacci numbers and measure how sparse that representation is.

**What is actually done.** The code compares known-key weights with random-key weights. Changing numeral systems can change visible sparsity without reducing the number of possible keys.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Compare Fibonacci representation weights with random keys; no significant anomaly reported.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M205 — Low-discrepancy / Halton-like tier placement

**Evidence:** Executed record

**How it works.** Normalize key positions to [0,1) and measure gaps or star discrepancy against structured low-discrepancy schedules.

**What is actually done.** The creative report compares its discrepancy statistic with random controls. Evenly spread finite observations do not establish a deterministic next-key schedule.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Compare normalized-position discrepancy; no significant deterministic schedule established.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M206 — Benford leading digits of roots

**Evidence:** Executed record

**How it works.** Compare first decimal digits of root values with a Benford-type reference distribution.

**What is actually done.** The report computes frequency/test summaries for known roots and controls. Agreement or disagreement is a distribution diagnostic, not enough information to determine unknown remainder digits.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Root first-digit distribution compared with controls; no convincing signal reported.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M207 — Taxicab sums of two cubes

**Evidence:** Executed record

**How it works.** Search whether a scalar is a sum of two integer cubes, potentially exposing a special generator family.

**What is actually done.** The creative report counts representations on disclosed keys and random controls. A special representation would still need independent evidence that the target was generated by that family.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Search special cube-sum representations of known keys; no transferable high-index key relation.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M208 — Polynomial in puzzle number

**Evidence:** Executed record

**How it works.** Fit a low-degree function of puzzle number and forecast later key positions or values.

**What is actually done.** The creative theory uses leave-one-out error versus controls; separate exact continuation tests verify concrete candidates. A polynomial fitting all known points has no automatic predictive authority.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Leave-one-out prediction compared with random keys; fitting known data does not determine the next scalar.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M209 — Consecutive bit-Jaccard similarity

**Evidence:** Executed record

**How it works.** View set-bit positions as sets and compute intersection divided by union for consecutive puzzle keys.

**What is actually done.** The report compares mean Jaccard overlap with random tier-matched keys. Similarity caused by bit widths must not be mistaken for inherited secret bits.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Bit-set overlap compared with random controls; no significant inheritance relation reported.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M210 — Mersenne-adjacent margin hypothesis

**Evidence:** Executed record

**How it works.** Measure whether keys lie unusually close to powers of two or all-ones Mersenne-style boundaries.

**What is actually done.** The creative test compares normalized margins with uniform controls. Small margins would identify a candidate region only under a validated generator prior.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Distances to power-of-two boundaries compared with random ranges.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M211 — Shared CRT residue / digital modular biases

**Evidence:** Executed record

**How it works.** Count small-modulus residues and ask whether a common congruence distinguishes disclosed keys from random intervals.

**What is actually done.** The report examines frequencies such as residues modulo three. Several weak residue preferences can arise by chance; they do not justify applying an unvalidated CRT restriction to the target.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Small-modulus residue frequencies examined; exploratory bias is not proof of a target constraint.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M212 — Collatz stopping-time association

**Evidence:** Executed record

**How it works.** Map each key through the Collatz iteration and compare stopping-time statistics.

**What is actually done.** The creative report evaluates known and random keys under the same rule. The transformed statistic is not shown to be invertible from a target address or predictive of its scalar.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Compare stopping statistics with random-key controls; no predictive result reported.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M213 — Brainwallet/BIP39 phrase schedule

**Evidence:** Executed record

**How it works.** Hash or derive keys from a fixed catalog of phrases/mnemonics and apply the puzzle's interval mask.

**What is actually done.** The creative family checks whether a phrase schedule reproduces significant known tiers. Tiny-tier coincidences are separated from evidence that one phrase generates later unknown keys.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Catalog phrase-derived keys and masked tiers tested; archived creative report records no nontrivial hits.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M214 — Solve-date scalar encoding

**Evidence:** Executed record

**How it works.** Encode dates in scalars or compare normalized scalar positions with date-related numbers.

**What is actually done.** The report counts date-pattern matches and errors over known solve records. Solve date can reflect search effort rather than generation, so correlation would require independent validation.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Test date patterns in keys; no significant association recorded.

**Sources.** [S148: creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

### M215 — UniMath-inspired arithmetic identities

**Evidence:** Executed record

**How it works.** Re-express arithmetic facts such as Euclidean division and reconstruction as executable exact assertions on known data.

**What is actually done.** unimath_corpora.py mirrors named mathematical ideas in Python. Passing these checks validates that implementation and corpus, not a machine-checked Agda proof or an unknown-key extractor.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Exact division, reconstruction, congruence and remainder assertions on known keys; arithmetic checks are not an Agda proof or prediction.

**Sources.** [S125: unimath_corpora.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/unimath_corpora.py); [S192: unimath_corpora.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/unimath_corpora.md)

### M216 — Residue/Legendre/coefficient distribution controls

**Evidence:** Implemented

**How it works.** Compare coefficient, residue, Legendre-symbol and remainder distributions with matched random samples.

**What is actually done.** unimath_insights.py produces statistical summaries and controls. It tests distributional hypotheses rather than deriving new bits directly from the target public point.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Random controls and KS/chi-square-style summaries distinguish transformation artifacts from candidate key bias.

**Sources.** [S126: unimath_insights.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/unimath_insights.py)

### M217 — DP hashing/birthday/URAND jump probes

**Evidence:** Implemented

**How it works.** Measure hash-table collisions, birthday behavior and candidate jump tables to improve practical walk mechanics.

**What is actually done.** Bitsavers-inspired probes model open addressing and first-collision counts, then compare URAND-derived jumps. These are solver engineering experiments, not secret-generator observations.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Bitsavers-inspired hash-table, collision and jump-distribution experiments assess solver mechanics.

**Sources.** [S096: bitsavers_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bitsavers_methods.py); [S140: bitsavers_methods_backtest.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/bitsavers_methods_backtest.md)

### M218 — Regression SVD/subset/interval arithmetic variants

**Evidence:** Implemented

**How it works.** Refit numerical predictors using alternative regression subsets/SVD and propagate rounding intervals through formulas.

**What is actually done.** The historical methods module compares fit stability, numerical bounds and selected regressions. It can diagnose approximation error but cannot manufacture predictive information absent from the data.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Historical numerical-method variants audit R2 fits and rounding; not new information about the target.

**Sources.** [S096: bitsavers_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bitsavers_methods.py)

### M219 — MOV and finite-field index-calculus applicability

**Evidence:** Applicability review

**How it works.** MOV reduces certain elliptic-curve logs to finite fields when the embedding degree is suitably small; index calculus has domain-specific requirements.

**What is actually done.** The registry estimates/checks applicability for secp256k1 and records why named structural attacks do not straightforwardly apply. It is not an executed transfer solving the target log.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Registry checks distinguish attacks requiring unsuitable curve structure from applicable interval methods.

**Sources.** [S112: oreilly_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/oreilly_methods.py)

### M220 — DDL preprocessing tradeoff bounds

**Evidence:** Synthetic/applicability

**How it works.** Restricted discrete-log methods trade preprocessing, memory and online work under stated target/setup assumptions.

**What is actually done.** The JoC module evaluates heuristic DDL bounds and synthetic scenarios. Estimated online savings must include required preprocessing and oracles before being compared with an actual puzzle search.

**Inputs needed.** Disclosed puzzle data, a precisely named statistic or attack prerequisite and appropriate random/control data.

**What the result means.** Analysis estimates restricted discrete-log tradeoffs under additional setup assumptions; no blind puzzle recovery demonstrated.

**Sources.** [S108: joc_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/joc_methods.py)

## Modular differences and general transformation frameworks

### M221 — Finite modular difference triangles

**Evidence:** Executed record

**How it works.** Repeatedly subtract neighboring residues modulo m; finite rows shrink by one entry at each level.

**What is actually done.** The experiment follows declared polynomial/exponential residue families through their full finite triangles. Reaching zero on supplied samples does not determine an unknown continuation without a recurrence assumption.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Exact finite-row experiments track polynomial/exponential residues through all levels; they do not reconstruct an unknown puzzle key.

**Sources.** [S036: REPORT.md](/home/arialmohan/scratch/modular-difference-levels/REPORT.md)

### M222 — Cyclic difference orbit classification

**Evidence:** Executed record

**How it works.** Wrap the difference operator cyclically so row length stays fixed, then detect exact zero or repeated states in a finite state graph.

**What is actually done.** The saved study enumerates all starting rows within its declared small configurations and classifies their orbits. This is an exhaustive finite dynamics result, not cryptographic inversion.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Exhaustive finite study classified 19,617 starting rows over 35 configurations into zero/cycles.

**Sources.** [S036: REPORT.md](/home/arialmohan/scratch/modular-difference-levels/REPORT.md)

### M223 — Signed quotient hierarchy with common-factor removal

**Evidence:** Executed record

**How it works.** Keep signed integer differences and divide a row by m whenever every entry shares that factor before taking the next difference.

**What is actually done.** The quotient experiment records divisions and exact normalized states. Removing common factors exposes structure but can still leave growing values or unresolved trajectories.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Remove factors of the full modulus before continuing signed differences; zero, cycle and capped outcomes remain separate.

**Sources.** [S034: QUOTIENT_REPORT.md](/home/arialmohan/scratch/modular-difference-levels/QUOTIENT_REPORT.md)

### M224 — 256-level quotient continuation

**Evidence:** Executed record

**How it works.** Extend the same bounded quotient experiment to more levels without changing the starting rows or normalization rule.

**What is actually done.** The 256-level survey compares outcomes with the earlier 128-level cap. Capped rows remain unresolved; lack of termination by the cap is not proof of infinite nontermination.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Saved survey records 163 zero, 600 cycles and 18,854 unresolved rows; no new resolutions after the earlier cap.

**Sources.** [S035: QUOTIENT_REPORT_256.md](/home/arialmohan/scratch/modular-difference-levels/QUOTIENT_REPORT_256.md)

### M225 — All-value magnitude/growth tracking

**Evidence:** Executed record

**How it works.** Track magnitudes, signs, divisibility and growth of every entry across every difference level, including after an earlier event.

**What is actually done.** The all-values run records more than 23 million observations and reports extreme bit lengths. It measures behavior of those exact finite trajectories, not secret-key information gained.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** More than 23 million entry observations distinguish growth from termination; unresolved finite caps are not nontermination proofs.

**Sources.** [S032: ALL_VALUES_REPORT_256.md](/home/arialmohan/scratch/modular-difference-levels/ALL_VALUES_REPORT_256.md)

### M226 — Inverse-difference kernel/anchor tests

**Evidence:** Executed record

**How it works.** Group all starting rows that produce the same observed difference row. Additional anchors can select among these inverse candidates.

**What is actually done.** inverse_capability.py exhaustively counts compatible inputs in small finite systems. If several remain, the transformed row alone has lost information and cannot uniquely reconstruct the original.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Enumerate compatible starting rows; anchors can resolve lost constants, but the residual hierarchy supplies no missing observations.

**Sources.** [S033: INVERSE_CAPABILITY_REPORT.md](/home/arialmohan/scratch/modular-difference-levels/INVERSE_CAPABILITY_REPORT.md)

### M227 — Deterministic index, byte and bit evolution

**Evidence:** Implemented

**How it works.** Define reversible or simple deterministic maps from an index into bitstrings, including increments and fixed byte/bit changes.

**What is actually done.** The unified framework executes registered sequence maps on artificial states. It generates controlled trajectories rather than learning the unknown puzzle creator's generation rule.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Unified framework includes index mapping, linear increments, byte/bit steps and monotonic traversal; code is not an unknown-key predictor.

**Sources.** [S226: unified_keyspace_framework_algorithm.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/frameworks/unified_keyspace_framework_algorithm.py)

### M228 — Masking, rotation and coupled sequences

**Evidence:** Implemented

**How it works.** Apply masks, rotate bit positions or couple two evolving states according to an explicit deterministic rule.

**What is actually done.** Registered transforms create particular orbits; some masks are lossy. Comparing their shapes cannot establish that a real target key belongs to one of those orbits.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Unified framework includes mask application, dual-sequence coupling, mask rotation and structured 256-step schedules.

**Sources.** [S226: unified_keyspace_framework_algorithm.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/frameworks/unified_keyspace_framework_algorithm.py)

### M229 — First/second-difference and drift schedulers

**Evidence:** Implemented

**How it works.** Measure first/second differences and choose the next transformation based on drift or entropy summaries.

**What is actually done.** The framework's schedulers switch among existing maps using their configured rules. Adaptation optimizes trajectory diagnostics; it is not rewarded by an independently discovered target-key relation.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Analyze trajectory differences or switch transformations using entropy thresholds; diagnostic evolution is not key recovery.

**Sources.** [S226: unified_keyspace_framework_algorithm.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/frameworks/unified_keyspace_framework_algorithm.py)

### M230 — Entropy, cycles, compression and spectral diagnostics

**Evidence:** Executed record

**How it works.** Compute bit entropy, compression, cycles, nearest-neighbor spacings and spectral summaries, then compare with random trajectories.

**What is actually done.** Classical arrays and statistics produce these measurements. Quantum-chaos terminology denotes analogy/diagnostics, not a quantum computation or an inverse map from address hashes to private scalars.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Compare deterministic trajectories with uniform controls, including cycle tests, spacings and spectral summaries; no quantum execution implied.

**Sources.** [S226: unified_keyspace_framework_algorithm.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/frameworks/unified_keyspace_framework_algorithm.py); [S181: revelation_discovery.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/revelation_discovery.md)

### M231 — Four-dimensional key/public/address visualization

**Evidence:** Implemented

**How it works.** Place scalar, public-point and address-hash objects into shared visualization coordinates and connect their derivation edges.

**What is actually done.** keyspace_4d.py supports raw/ring-style layouts. Normalized coordinates can illustrate hashing's loss of visible geometry without revealing an exploitable inverse relationship.

**Inputs needed.** Explicit finite rows or generated state trajectories, arithmetic conventions, transformation parameters and finite resource limits.

**What the result means.** Display scalar-to-point-to-hash relationships in alternate layouts; no invertible address-to-scalar map is established.

**Sources.** [S110: keyspace_4d.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/keyspace_4d.py)

## Shor, classical factoring and quantum-resource research

### M232 — Classical BSGS multiplicative-order finder

**Evidence:** Executed record

**How it works.** BSGS finds an exponent r with a^r=1 modulo N by matching stored small powers against larger steps.

**What is actually done.** Classical Python/native order routines operate on bounded integer examples. In the factoring reduction they replace the quantum order-finding oracle; no QFT is executed.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Exact small-integer order traces and backend comparisons; stands in for an order oracle, not a quantum device.

**Sources.** [S264: RUN_REPORT_2026-09-09.md](/home/arialmohan/workspace/research/shor-quantum-research/RUN_REPORT_2026-09-09.md)

### M233 — Brent cycle-detection order finder

**Evidence:** Executed record

**How it works.** Brent's cycle detector follows repeated multiplication modulo N while using a low-memory schedule to detect a return period.

**What is actually done.** The implementation measures this classical order finder against shared small inputs. Its runtime grows with the period and should not be mistaken for Shor's quantum complexity.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Classical linear-period comparison backend; measured on bounded small semiprimes.

**Sources.** [S263: FACTORING_RUN_REPORT_2026-10-10.md](/home/arialmohan/workspace/research/shor-quantum-research/FACTORING_RUN_REPORT_2026-10-10.md)

### M234 — Kangaroo multiplicative-order finder

**Evidence:** Executed record

**How it works.** Search successively larger exponent intervals with collision walks to locate a multiple/order relation.

**What is actually done.** The classical kangaroo order backend is benchmarked separately from elliptic-curve kangaroo. Matching the name does not mean these factoring experiments recovered Bitcoin private keys.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Expanding exponent-interval method compared with BSGS and Brent; not a secp256k1 scalar recovery.

**Sources.** [S263: FACTORING_RUN_REPORT_2026-10-10.md](/home/arialmohan/workspace/research/shor-quantum-research/FACTORING_RUN_REPORT_2026-10-10.md)

### M235 — Pollard-rho factoring fast path

**Evidence:** Executed record

**How it works.** Pollard rho searches for a nontrivial common divisor through repeated modular iteration and cycle-related gcds.

**What is actually done.** The high-level factor command can take this shortcut before order finding. Its reported factorization of 3233 is correctly labeled rho, not evidence of quantum or even BSGS execution on that path.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Canonical factor command reports its shortcut explicitly; factoring 3233 must not be relabeled as a quantum Shor run.

**Sources.** [S264: RUN_REPORT_2026-09-09.md](/home/arialmohan/workspace/research/shor-quantum-research/RUN_REPORT_2026-09-09.md)

### M236 — Python/GMP/Rust controlled order benchmarks

**Evidence:** Executed record

**How it works.** Hold modulus, base and repetition schedule fixed while replacing the order-finding arithmetic backend.

**What is actually done.** The saved matrix records per-backend times and verifies identical orders. This isolates local implementation constants; differences across operand sizes are not a clean universal scaling-law estimate.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Shared modulus/base backend matrix records finite speedups; source/runtime differences are pinned in historical manifests.

**Sources.** [S262: BACKEND_MATRIX_2026-09-10.md](/home/arialmohan/workspace/research/shor-quantum-research/BACKEND_MATRIX_2026-09-10.md)

### M237 — Adaptive Shor simulation trial budgets

**Evidence:** Executed record

**How it works.** Measure trial success, compute a confidence-aware required budget and adjust the number of repetitions to meet a target.

**What is actually done.** The factoring loop changes trial counts and ramps a bounded test size. The feedback improves a classical experimental procedure, not the underlying cryptographic problem's entropy.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Empirical/analysis/improvement loop adjusts trial counts with Wilson-bound and runtime metrics.

**Sources.** [S263: FACTORING_RUN_REPORT_2026-10-10.md](/home/arialmohan/workspace/research/shor-quantum-research/FACTORING_RUN_REPORT_2026-10-10.md); [S244: loop.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/shor_sim/loop.py)

### M238 — UCB/EWMA/early-stop method selection

**Evidence:** Branch/implementation

**How it works.** An upper-confidence policy explores backend choices while EWMA smooths noisy measurements and early stopping limits unnecessary trials.

**What is actually done.** Archive modules describe/use these policy choices within simulation loops. Better simulated reward can reflect assumptions in the model and needs real execution validation before any cryptanalytic interpretation.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Archive describes adaptive backend policy and smoothing; simulator optimization is not target-scale quantum cryptanalysis.

**Sources.** [S255: Shor-Simulation.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Shor-Simulation.md)

### M239 — Semiprime-per-puzzle circuit/manifest analogy

**Evidence:** Audited/corrected

**How it works.** Construct a deterministic semiprime challenge from puzzle data to illustrate a comparable input size for factoring-resource calculations.

**What is actually done.** Circuit/manifest commands prepare that separate factoring task. A factor of the constructed integer is not mathematically shown to disclose the original elliptic-curve scalar.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Factoring challenges derived from puzzle data are resource-scale analogies, not reductions recovering puzzle scalars.

**Sources.** [S255: Shor-Simulation.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Shor-Simulation.md)

### M240 — secp256k1 quantum ECDLP resource mode

**Evidence:** Implemented/model

**How it works.** The ECDLP mode combines real small-range BSGS with a probability-and-time oracle model beyond configured exact limits.

**What is actually done.** In shor_sim/ecdsa.py, exact branches call the BSGS routine; larger Shor/hybrid trials draw success from rng.random() and return formula-based elapsed time. Even the small kangaroo-labeled profile calls BSGS in its exact branch.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Models the relevant discrete-log task separately from integer factoring; no executed target-scale quantum circuit is established.

**Sources.** [S243: ecdsa.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/shor_sim/ecdsa.py)

### M241 — 520-logical-qubit resource sensitivity model

**Evidence:** Audited/corrected

**How it works.** Estimate logical resources under a simplified model and vary physical error/architecture assumptions to see their effect.

**What is actually done.** The standalone audit identifies omitted reversible-arithmetic workspace and other architecture costs. A 520-qubit headline is a sensitivity-model output, not a complete executable Bitcoin-breaking circuit.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Standalone audit excludes required reversible workspace and full architecture; headline counts are not a complete Bitcoin-breaking machine.

**Sources.** [S198: AUDIT.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/papers/standalone_520_qubit/AUDIT.md)

### M242 — Surface-code/platform timing estimates

**Evidence:** Implemented/model

**How it works.** Map logical operation counts to physical qubits and runtime using code distance, gate/cycle assumptions and platform parameters.

**What is actually done.** quantum.py calculates resource estimates for chosen profiles. The outputs are model-dependent arithmetic, not measured throughput on an available quantum computer.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Compare physical errors, distances and cycle times for several platforms; estimates depend on explicit architecture assumptions.

**Sources.** [S245: quantum.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/shor_sim/quantum.py); [S255: Shor-Simulation.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Shor-Simulation.md)

### M243 — Wolfram/mask sensitivity extensions

**Evidence:** Implemented/model

**How it works.** Feed alternative masks, assumptions or external analytical outputs into the resource/sensitivity model and compare derived estimates.

**What is actually done.** The standalone Wolfram-named modules implement follow-up model calculations. They do not construct or execute a target-sized quantum state evolution that reveals a puzzle key.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Standalone modules explore model sensitivity and follow-up calculations, not recovered puzzle keys.

**Sources.** [S199: wolfram_masks.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/papers/standalone_520_qubit/shor_sim/wolfram_masks.py); [S200: wolfram_mix.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/papers/standalone_520_qubit/shor_sim/wolfram_mix.py)

### M244 — Train/holdout adaptive-trial study

**Evidence:** Executed record

**How it works.** Freeze a trial-budget policy on one stream, then evaluate it on additional held-out random streams to check whether tuning generalizes.

**What is actually done.** The latest factoring report records its bounded train/holdout trials and limitations. Repeated success on small semiprimes validates that experiment, not quantum-scale secp256k1 recovery.

**Inputs needed.** Small integer/order inputs for real classical tests, or explicit oracle/resource parameters for simulations and estimates.

**What the result means.** Latest factoring report includes additional controlled trial streams; conclusions remain limited to classical simulation.

**Sources.** [S263: FACTORING_RUN_REPORT_2026-10-10.md](/home/arialmohan/workspace/research/shor-quantum-research/FACTORING_RUN_REPORT_2026-10-10.md)

