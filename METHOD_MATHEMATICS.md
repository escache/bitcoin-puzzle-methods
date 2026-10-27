# Mathematics for 244 inventory methods
Editorial mathematical formulations tied to the inventory explanations and local evidence. Symbols are local to each entry. These are not claims of new theorems or additional historical execution.

## M001 — Public puzzle corpus verification

A candidate scalar determines a public point and address hash. Recomputing those values detects an incorrect published key or mismatched database row.

Read filled private-key rows, derive the recorded public-key format, and compare with stored point/HASH160 fields. Empty rows remain unknown; passing the check does not discover their keys.

$$
Q=kG,\quad h=\mathrm{HASH160}(\mathrm{ser}(Q))
$$

G is the curve generator; ser is the declared public-key serialization. Compare Q or h with the recorded target.

Recorded public scalars are checked against secp256k1 points and HASH160; validates the dataset, not a prediction.

Sources: [FEASIBILITY_REVALIDATION_20260918.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/FEASIBILITY_REVALIDATION_20260918.md); [backtest.py](/home/arialmohan/puzzle71-educational/backtest.py)

## M002 — Small-range exhaustive address search

Enumerate every integer in a genuinely small interval and accept only an address match. Exhaustion gives a complete answer for that interval.

The educational tests scan puzzles 1-10 directly. Their keys are already public and used afterward to validate the results; this demonstrates a correct checker at small scale.

$$
\mathcal{K}=\{L,L+1,\ldots,U\},\quad W=U-L+1
$$

An exhaustive scan checks all W scalars in the inclusive interval; each candidate requires an exact target comparison.

Puzzles 1-10 scanned completely; each yielded the expected published key. Small-range recovery is not an unknown-key breakthrough.

Sources: [BACKTEST.md](/home/arialmohan/puzzle71-educational/BACKTEST.md); [backtest.py](/home/arialmohan/puzzle71-educational/backtest.py)

## M003 — Full-range seeded sampling backtests

A seeded sampler chooses a reproducible order of candidates. The verifier stops when a candidate produces the target address.

Saved subprocess backtests run the actual checker on small solved puzzles and compare recovered values afterward. Counts describe work until a match, not a learned shortcut.

$$
k_t\sim\mathrm{Unif}\{L,\ldots,U\},\quad \Pr(\mathrm{hit\ in}\ t)=1-(1-1/W)^t
$$

W=U-L+1. The probability is the ideal independent, with-replacement baseline for one fixed target; the saved sampler determines the actual sequence.

Actual address checkers recovered small published puzzles; seeded search order does not establish predictive narrowing.

Sources: [ACTUAL_BACKTEST.md](/home/arialmohan/puzzle71-educational/ACTUAL_BACKTEST.md); [backtest_continuous_17_32.py](/home/arialmohan/puzzle71-educational/backtest_continuous_17_32.py)

## M004 — Uniform within-shard representatives

Divide an interval into nonoverlapping shards and select one integer uniformly within each. This spreads a batch over the advertised range.

The corrected generator uses integer randrange calls. One record is one sampled candidate plus its shard boundaries; no other integer in that shard is thereby checked.

$$
k_i\sim\mathrm{Unif}\{b_i,\ldots,b_{i+1}-1\}
$$

One sampled representative is drawn from each nonempty shard. The rest of that shard remains unchecked.

Samples one integer per disjoint interval; representative checks do not exhaust their shard.

Sources: [candidate_sampling.py](/home/arialmohan/puzzle71-educational/candidate_sampling.py); [pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py)

## M005 — Exact integer partition coverage

Integer division places adjoining boundaries so the first shard starts at the lower limit and the last ends at the upper limit.

The corrected partitions function distributes the interval across the requested record count. Tests enumerate small examples to check every integer appears exactly once in the intervals.

$$
b_i=L+\left\lfloor\frac{iW}{s}\right\rfloor,\quad I_i=[b_i,b_{i+1})
$$

W=U-L+1 and s is the number of shards. These half-open integer intervals partition [L,U+1); empty shards require handling when s exceeds W.

Gap-free inclusive intervals replace biased single-key records. Exhaustive small-range checks verify the partition arithmetic.

Sources: [test_pipeline.py](/home/arialmohan/puzzle71-corrected/test_pipeline.py); [README.md](/home/arialmohan/puzzle71-corrected/README.md)

## M006 — No-repeat affine shard permutations

An affine permutation visits offsets using (offset + index*stride) modulo shard size. A coprime stride prevents repetition before exhausting the shard.

The samplers store per-shard offsets, strides and a traversal position. They reconstruct candidates without storing all previously visited keys; this improves coverage accounting, not target likelihood.

$$
k_{i,t}=b_i+(a_i+tq_i\;\mathrm{mod}\;w_i),\quad \gcd(q_i,w_i)=1
$$

A shard has width w_i. Its coprime stride q_i visits every offset exactly once before repeating.

Coprime strides enumerate each shard without a visited-key set; retains full support.

Sources: [candidate_sampling.py](/home/arialmohan/puzzle71-educational/candidate_sampling.py); [test_unique_sampling.py](/home/arialmohan/puzzle71-educational/test_unique_sampling.py)

## M007 — One-million sample-key verification

Derive both public-key serializations for each stored sample and compare their HASH160 values with the decoded target hash.

The verifier read the million-record JSONL file, padded each sample_key to 32 bytes, and performed two comparisons per scalar. The saved report records no match.

$$
h_{i,f}=\mathrm{HASH160}(\mathrm{ser}_f(k_iG)),\quad f\in\{c,u\}
$$

c and u denote compressed and uncompressed formats. Each stored sample produces two hash comparisons, not a search of its whole shard.

One million explicit samples checked in both public-key serializations; no target match.

Sources: [verification-1M.json](/home/arialmohan/puzzle71-corrected/verification-1M.json)

## M008 — Range-start and range-end verification

A range boundary is itself a possible private scalar and can be checked exactly like a sample. Checking it does not search its neighboring integers.

The endpoint run read range_start and range_end from every record and checked both address formats. It performed two million scalar checks, separately from the earlier samples.

$$
\mathcal{C}=\bigcup_i\{L_i,U_i\}
$$

Check the endpoints of each inclusive record interval. Duplicated endpoints do not represent new scalar coverage.

Two million endpoint entries checked in both address formats; no target match. Interiors were not searched.

Sources: [verification-boundaries-1M.json](/home/arialmohan/puzzle71-corrected/verification-boundaries-1M.json)

## M009 — Generate-and-verify streaming batches

Generate a candidate, verify it immediately, then discard it unless it matches. Memory does not grow with the batch size.

stream_check.py samples one key per partition and saves aggregate counts, a deterministic stream digest and any matches. The seed permits regeneration without a large candidate file.

$$
k_t=F(s,t),\quad A_t=\mathbf{1}\{h(k_t)=h_*\}
$$

A deterministic seed s and position t regenerate the candidate stream; A_t records an exact target-hash match.

One million additional samples checked immediately without a large dataset; no matches in the saved batch.

Sources: [stream_check.py](/home/arialmohan/puzzle71-corrected/stream_check.py); [stream-verification-20261019.json](/home/arialmohan/puzzle71-corrected/stream-verification-20261019.json)

## M010 — Continuous affine full-support search

Apply one odd-stride affine permutation to all 2^70 interval offsets. Each offset occurs once over a complete cycle.

continuous_stream.py generates keys indefinitely until stopped, matched or exhausted. It checkpoints counters and permutation parameters; the process performs actual address checks, not predictor training.

$$
k_t=L+(a+tq\;\mathrm{mod}\;2^{70}),\quad q\;\mathrm{odd}
$$

An odd stride permutes all offsets of the 71-bit puzzle interval. Only the traversed prefix has been checked before completion.

Checkpointed local worker checks an affine permutation of the 70-unknown-bit interval. Status is mutable and must be time-stamped.

Sources: [continuous_stream.py](/home/arialmohan/puzzle71-corrected/continuous_stream.py); [status.json](/home/arialmohan/puzzle71-corrected/continuous-run/status.json)

## M011 — Incremental public-point verification

If the next scalar differs by delta, its public point is the old point plus delta*G. Reusing that point avoids repeated full scalar multiplication.

point_walk.py caches the two step points needed by the affine traversal, including wraparound. It still serializes and hashes every point; the candidate sequence is unchanged.

$$
Q_{t+1}=Q_t+(k_{t+1}-k_t)G
$$

Reusing the previous public point replaces a new scalar multiplication with a point addition; serialization and hashing still occur.

Same scalar sequence verified using cached point increments; 900 comparison cases and paired benchmarks passed.

Sources: [point_walk.py](/home/arialmohan/puzzle71-corrected/point_walk.py); [point-walk-benchmark.json](/home/arialmohan/puzzle71-corrected/point-walk-benchmark.json)

## M012 — Checkpoint resume and scalar cross-checks

Saving traversal state allows a restart at the next unchecked position. Independent scalar multiplication can detect incremental-point drift.

The worker writes an atomic status file and retains its offset/stride across restarts. The optimized version checks the first and each 10,000th point against the original verifier.

$$
\sigma_t=(t,a,q),\quad Q_t\stackrel{?}{=}k_tG
$$

The checkpoint stores the next traversal position and permutation parameters; periodic independent multiplication checks point-walk consistency.

Live optimization resumes the exact saved position and compares against full scalar multiplication every 10,000 entries.

Sources: [continuous_stream.py](/home/arialmohan/puzzle71-corrected/continuous_stream.py); [WORKING_NOTES.md](/home/arialmohan/puzzle71-corrected/WORKING_NOTES.md)

## M013 — FUSED priority-band traversal with fallback

Search a forecast band first, then its complement. This can improve order under a good predictor without permanently excluding any key.

The fixed-budget educational comparison used affine permutations within the band and fallback regions. It checked bounded prefixes, not every integer in the forecast band.

$$
I=B\,\dot\cup\,(I\setminus B)
$$

B is the forecast band. Traversing B followed by its complement retains complete support when both parts are eventually exhausted.

Fixed-budget test retained complementary regions; 286,720 checks across both methods found no keys.

Sources: [REPORT.md](/home/arialmohan/puzzle71-educational/computations/blind-fused-30-64-20261018/REPORT.md)

## M014 — Advanced selective FUSED/Delta2 adapter

Turn predicted root/coefficient/remainder combinations into scalar intervals and sample those hypotheses instead of the entire range.

The adapter froze training data, retained its natural hypothesis list and checked one representative per shard. A later containment check found that most known evaluation keys were outside those selected intervals.

$$
\mathcal{C}=\bigcup_{\theta\in\Theta}[L_\theta,U_\theta]
$$

Each root/coefficient/remainder hypothesis theta defines an interval. Verify target containment separately from samples drawn within those intervals.

Selected 12,515 hypothesis shards across puzzles 30-64; only 1/35 known targets was contained.

Sources: [REPORT.md](/home/arialmohan/puzzle71-educational/computations/advanced-selective-30-64-20261018/REPORT.md)

## M015 — CPU scalar versus point-walk benchmarking

Compare two verifiers on identical scalar streams. Matching outputs isolate performance changes from candidate-selection differences.

The point-walk benchmark compared exact points and hashes, then timed alternating paired trials with matching stream digests. It measures local throughput, not a higher probability per tested key.

$$
v=\frac{N_{\mathrm{checks}}}{t},\quad S=\frac{t_{\mathrm{scalar}}}{t_{\mathrm{walk}}}
$$

Compare elapsed times on identical candidate streams and verified outputs. S measures implementation speedup, not a change in success per candidate.

Measured acceleration is computational, not evidence of a more likely candidate distribution.

Sources: [benchmark_point_walk.py](/home/arialmohan/puzzle71-corrected/benchmark_point_walk.py); [benchmark_point_walk.py](/home/arialmohan/puzzle71-educational/checks/benchmark_point_walk.py)

## M016 — Mock distributed key-generation network

A coordinator hands work units to generator nodes while optional checker nodes consume results. Pull-based scheduling balances unequal workers.

mock_keyspace_network.py runs bounded practice batches using processes or threads. Its counters and coverage checks demonstrate orchestration; the mock network is not evidence of a full 71-bit sweep.

$$
N_{\mathrm{total}}=\sum_{j=1}^{p}N_j
$$

Worker counts may be added as distinct coverage only when work units are disjoint or duplicate checks are removed.

Pull-based process/thread workers and checker queues exercise scheduling on bounded mock work; not a full puzzle solve.

Sources: [mock_keyspace_network.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/mock_keyspace_network.py); [README.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/README.md)

## M017 — 32-byte padding and dual-format P2PKH checks

A scalar is encoded as exactly 32 big-endian bytes, multiplied by G, serialized and hashed. P2PKH comparisons use the address's decoded 20-byte hash.

Existing checkers use key.to_bytes(32,'big'), known scalar-one vectors and compressed/uncompressed formats. They compare HASH160 directly rather than Base58-encoding every generated address, an equivalent target check.

$$
b=\mathrm{I2OSP}(k,32),\quad h_f=\mathrm{HASH160}(\mathrm{ser}_f(kG))
$$

I2OSP writes exactly 32 big-endian bytes. Leading zero padding preserves the scalar; f selects the public-key format.

Left-padded scalar inputs, compressed/uncompressed public keys and known scalar-one address vectors guard verifier correctness.

Sources: [verify_samples.py](/home/arialmohan/puzzle71-corrected/verify_samples.py); [check_keys.py](/home/arialmohan/puzzle71-educational/check_keys.py)

## M018 — Synthetic fixtures versus disclosed puzzle data

A synthetic fixture can validate pipeline logic because its generation rule is known. It must remain separate from actual published puzzle secrets.

PEC37 tools generate synthetic chains and compare them with disclosed puzzle data. Successful synthetic reconstruction tests the fixture rule; it cannot populate undisclosed puzzle-key rows.

$$
k_i^{\mathrm{syn}}=F(s,i),\quad \widehat{k}_i\stackrel{?}{=}k_i^{\mathrm{syn}}
$$

A known fixture generator supplies synthetic ground truth. Agreement validates that fixture pipeline, separately from disclosed puzzle observations.

PEC37 stores synthetic 1-160 chains separately and compares them with actual disclosed keys. Synthetic keys are not puzzle recoveries.

Sources: [evaluate_synthetic_chain.py](/home/arialmohan/workspace/projects/pec37/tools/evaluate_synthetic_chain.py); [synthetic_chain_evaluation.csv](/home/arialmohan/workspace/projects/pec37/data/synthetic_chain_evaluation.csv)

## M019 — Empirical bit-vote and position forecasting

Train simple position trends or majority votes for fractional bit positions, then evaluate them on later known keys.

empirical_key_forensics.py uses disclosed keys, exact rational regressions and bit-vote diagnostics. It measures retrospective prediction accuracy; it does not search unknown Bitcoin addresses.

$$
\widehat b_j=\mathbf{1}\!\left\{\sum_{i\in T}b_{ij}>\frac{\lvert T\rvert}{2}\right\}
$$

This illustrates a majority bit predictor trained on T; positional regressions are alternative rules. Evaluate each on later, excluded observations.

Retrospective generator-forensics tests fractional-bit votes, exact regressions and baseline predictors on disclosed keys.

Sources: [empirical_key_forensics.py](/home/arialmohan/workspace/projects/pec37/data/empirical_key_forensics.py); [empirical_key_forensics.json](/home/arialmohan/workspace/projects/pec37/data/empirical_key_forensics.json)

## M020 — Five-index scale/transition analysis

Normalize every-fifth-puzzle keys to comparable interval positions and ask whether one predicts the next better than a baseline.

The downloaded result file records lag correlation, permutation tests, prefix Hamming distances and held-out transition errors. These are saved statistical results, not additional private-key discoveries.

$$
u_i=\frac{k_i-2^{i-1}}{2^{i-1}},\quad \rho_5=\mathrm{Corr}(u_i,u_{i+5})
$$

Normalize scalars to their tier positions before testing every-fifth-index transitions. The correlation is descriptive until held-out prediction is assessed.

Normalized positions, lag correlations, Hamming similarity and held-out transition forecasts are recorded; no new key is recovered.

Sources: [bitcoin_scale5_results.json](/home/arialmohan/Downloads/bitcoin_scale5_results.json)

## M021 — Binary distinguished-point parsing

Distinguished-point dumps encode selected curve points and possibly walk distances. Recovering their layout is necessary before collision algebra has meaning.

The parser scans bit/byte layouts, checks candidate x-coordinates and extracts metadata slices. Later scripts test interpretations; a parseable integer is not automatically a valid walk distance.

$$
x=\sum_{j=0}^{w-1}b_j2^{8j}
$$

This is a little-endian interpretation of w bytes; reverse ordering for big endian. Candidate layouts need length, curve-point and distance consistency checks.

Extract curve x-coordinates, candidate metadata and distance fields from the supplied binary. Interpretation of metadata remains a hypothesis.

Sources: [dp_parser.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/dp_parser.py); [non_bruteforce_audit_20260831.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/non_bruteforce_audit_20260831.md)

## M022 — Tame/wild collision recovery

A tame walk starts from a known scalar; a wild walk starts from the target point. Their meeting relates recorded distances and yields a candidate scalar.

collision.py groups same-x entries, tries tame/wild assignments and derives candidates. Because x alone has two point parities, the final scalar must pass exact public-key verification.

$$
tG=Q+wG\quad\Longrightarrow\quad k\equiv t-w\pmod n
$$

Q=kG, n is the subgroup order, and t,w are total tame/wild scalar coordinates at a same-point collision. Same-x observations also require testing the opposite sign.

Same-point opposite-herd distances yield a scalar when the walk origins and distances are valid. No real target collision is established here.

Sources: [collision.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/collision.py); [README.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/README.md)

## M023 — Single-process bounded Pollard kangaroo

Pollard kangaroo uses deterministic pseudo-random jumps so tame and wild walks can merge. Distinguished points reduce the amount of stored walk data.

kangaroo.py implements bounded CPU walks, jump tables, point selection and verification. It requires the target public point and a budget; an address hash cannot initialize its wild walk.

$$
X_{t+1}=X_t+s(X_t)G,\quad d_{t+1}=d_t+s(X_t)
$$

The point-selected jump s updates both the walk and its tracked scalar distance. Bounded interval kangaroo has expected work proportional to the square root of interval width.

Standard interval discrete-log implementation for targets with known public points.

Sources: [kangaroo.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/kangaroo.py)

## M024 — Separated tame and wild phases

Build the tame table once, save it, and later walk from the target until a compatible distinguished point is reached.

phase.py exposes separate tame and wild commands and table export/loading. This supports separate machines or stages without converting a missing public key into an ECDLP target.

$$
\mathcal{T}=\{(X_t,d_t):X_t\in\mathcal{D}\}
$$

Store tame distinguished points in table T, then match compatible wild points. D is the declared distinguished-point predicate, not every visited point.

Persist a tame distinguished-point table and search from the target in a separate phase.

Sources: [phase.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/phase.py); [ctheory_phase_solver.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/ctheory_phase_solver.py)

## M025 — JeanLucPons / RCKangaroo export

External interval solvers need bounds, a target point and runtime settings in their expected configuration format.

Export scripts write JeanLucPons/RCKangaroo inputs from puzzle or slot metadata. They prepare jobs; whether the external executable ran and found a match requires separate logs.

$$
\mathcal{J}=(Q,L,U),\quad Q=kG,\quad L\leq k\leq U
$$

The exported solver job declares the target point and inclusive scalar bounds. A configuration file is not a completed interval search.

Generate solver configuration files for public-key interval targets; configuration existence is not execution evidence.

Sources: [export.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/export.py); [export_ctheory_gpu_d1.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/export_ctheory_gpu_d1.py)

## M026 — Direct D1 interval kangaroo

If k=base+D1, then Q-base*G=D1*G. A known base converts recovery into a smaller interval discrete log.

D1 solvers construct the shifted point from guessed root/coefficient coordinates. A wrong base usually makes the true key absent from that interval, so leaf cost alone is incomplete.

$$
B=R_1^3+C_1R_1^2,\quad Q_D=Q-BG=D_1G
$$

Fixing the correct R1,C1 turns the target into a bounded D1 discrete log. The equation does not determine those higher coordinates.

Subtract a hypothesized scalar base and search the D1 leaf; useful only if the hypothesized coordinates are correct.

Sources: [wrapped_kangaroo.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/wrapped_kangaroo.py); [d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

## M027 — Wrapped CT multi-target kangaroo

Share walks or targets across several related base hypotheses, attempting to reuse work instead of solving each independently.

Wrapped-CT code constructs multiple shifted targets. Historical audits inspect span/setup growth and find that the advertised tiny-span benefit does not transfer unconditionally to high-index targets.

$$
Q_j=Q-B_jG=(k-B_j)G
$$

Each proposed wrapped base B_j defines a shifted residual. Its assumed short search interval must actually contain k-B_j; historical span assumptions failed at high tiers.

Historical small-span speed claims fail on large required spans; later audits reject unconditional recovery-cost reductions.

Sources: [wrapped_kangaroo.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/wrapped_kangaroo.py); [d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

## M028 — CPU banded baby-step/giant-step D1 hunts

BSGS stores small point multiples, then subtracts larger multiples from the target to find a match in a bounded interval.

cpu_band_d1_hunt.py builds baby tables for selected D1 bands and scans giant steps. Saved deployments used CPU work even on some GPU-equipped hosts; that is not a CUDA benchmark.

$$
Q'=(D-a)G,\quad D-a=im+j,\quad m=\lceil\sqrt{W}\rceil
$$

For D in [a,a+W), match Q'-imG with jG using baby steps and giant steps. This is conditional on the chosen residual band.

Bounded D1-band runs are documented; CPU tasks on GPU-equipped pods must not be described as GPU kernel execution.

Sources: [cpu_band_d1_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/cpu_band_d1_hunt.py); [CTHEORY_MATH_REVIEW_20260920.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/CTHEORY_MATH_REVIEW_20260920.md)

## M029 — Prior-weighted stratified kangaroo

Split a known-point interval into strata and allocate more tame-walk effort where a supplied prior assigns greater probability.

pwsk.py builds a smoothed histogram, assigns budgets using prior mass and width, and searches against a shared wild herd. Its benefit depends on the supplied prior actually predicting targets.

$$
\Pr(k\in I_i)=p_i,\quad \sum_i p_i=1
$$

A justified prior assigns probability masses to disjoint strata I_i and guides effort. The formula declares the required prior; it does not establish one for the puzzle.

Reweights interval effort when a genuine prior exists; flat priors reduce to ordinary allocation. Prior quality is unestablished for the unknown puzzle.

Sources: [pwsk.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/pwsk.py); [demo_pwsk.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/demo_pwsk.py)

## M030 — Prior-weighted GPU slot budgets

Reweight work across already constructed slots without changing what each slot represents. Higher prior mass receives a larger hop budget.

pwsk_budget.py combines FUSED-distance and optional D1 histogram weights, rounds allocations and annotates manifests. It changes scheduling, not the set of possible scalar equations.

$$
B_i=B_{\mathrm{tot}}\frac{w_i}{\sum_jw_j}
$$

Nonnegative heuristic weights w_i distribute a total budget; integer rounding must preserve the budget. Reweighting does not alter the underlying slot geometry.

Allocate existing slot budgets using FUSED distance or empirical D1 histograms without changing slot geometry.

Sources: [pwsk_budget.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/pwsk_budget.py)

## M031 — Rust native herd stepping

Move repeated curve-walk operations out of the Python interpreter into compiled native code. The mathematical search remains the same.

The Rust extension provides herd stepping and native lookup operations called by the Python runtime. Actual speed must come from a build-specific benchmark, not merely the presence of Rust source.

$$
(X,d)\longmapsto(X+s(X)G,d+s(X))
$$

Native code performs the same herd transition as the reference walk. Performance changes must preserve point and distance agreement.

Native backend reduces interpreter overhead while preserving interval-search semantics.

Sources: [lib.rs](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/rust/kangaroo_fast/src/lib.rs); [base.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/runtime/base.py)

## M032 — Coincurve/libsecp256k1 fast backend

Call optimized libsecp256k1 operations through a Python binding instead of performing every field operation in Python.

fast_ec.py selects accelerated scalar multiplication, point addition and optional native herd routines. It is a backend substitution, not an algorithm that predicts private keys.

$$
\mathrm{mul}_{\mathrm{fast}}(k,G)=\mathrm{mul}_{\mathrm{ref}}(k,G)
$$

Equality of curve results is the backend contract. Faster multiplication changes elapsed cost, not the number of candidate scalars.

Accelerated point arithmetic replaces pure Python operations; it does not reduce unknown key entropy.

Sources: [fast_ec.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/fast_ec.py); [benchmark_cpu_ec.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/benchmarks/benchmark_cpu_ec.py)

## M033 — GPU modular herd/D1 backends

GPU kernels would execute many curve steps concurrently. A backend interface alone is insufficient; the device search must actually be implemented.

The inspected CTheory d1_search CUDA file returns unavailable/error and zeroes its output. The Python registry can report ready from markers/environment flags, which do not by themselves prove a working kernel.

$$
\mathcal{W}=\bigsqcup_{j=1}^{p}\mathcal{W}_j
$$

Parallel workers receive work-unit sets W_j. This is an allocation model; actual device readiness and execution require separate evidence.

Backend registries and CUDA files exist, but readiness and actual execution differ by module. Do not infer a complete device implementation from a registry.

Sources: [backends_cuda.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/runtime/backends_cuda.py); [d1_search.cu](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/cuda/ctheory_modules/d1_search/d1_search.cu)

## M034 — GPU throughput and cost calibration

Parse actual solver rates, discard warmup effects and combine measured work rates with declared operation counts.

gpu_bench.py extracts throughput from logs and computes estimates. Other tables contain assumed rates/prices; those must not be confused with current hardware measurements or target success probabilities.

$$
t=\frac{N_{\mathrm{ops}}}{v},\quad \mathrm{cost}=r_{\mathrm{hour}}\frac{t}{3600}
$$

Use measured operation throughput v and the dated hourly rate r. Historical estimates are conditional on their hardware and workload.

Parse measured solver logs separately from hardcoded estimates; historical prices and throughput are not current quotations.

Sources: [gpu_bench.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/gpu_bench.py); [GPU-Deployment.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/GPU-Deployment.md)

## M035 — RunPod/Vultr sharding and orchestration

Partition solver jobs across remote workers, transfer manifests, run executables and collect outputs/checkpoints.

Deployment scripts and playbooks implement build/start/status procedures. This review documents those artifacts without launching instances or treating a successful cloud allocation as a successful key search.

$$
\mathcal{J}=\{(Q_j,L_j,U_j,\mathrm{id}_j)\}_{j=1}^{s}
$$

A manifest assigns bounded jobs with stable identifiers for scheduling and recovery. Coverage depends on which jobs actually finish.

Deployment runbooks, work-unit manifests and recovery scripts coordinate bounded jobs; availability is distinct from a successful search.

Sources: [GPU_PLAYBOOK.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/vultr/GPU_PLAYBOOK.md); [GPU-Deployment.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/GPU-Deployment.md)

## M036 — Bounded ECDLP certificates and slot gates

Attach a machine-readable statement of bounds, target, provenance and job identity so a result can be checked against its declared task.

BEC and slot gates seal manifests and validate fields. They can attest what was searched, but cannot certify that a heuristic guess contains the unknown key.

$$
\mathcal{C}=(Q,L,U,\mathrm{provenance}),\quad \mathrm{verify}(k):kG=Q
$$

A certificate records the input contract and evidence. Recording bounds does not prove the unknown target is inside a guessed interval.

Certifies declared bounds and evidence metadata; a certificate is not proof that the target lies in a guessed slot.

Sources: [bec.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bec.py); [slot_contract.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/slot_contract.py)

## M037 — Miss ladder and complement widening

After a prioritized search misses, enlarge the hypothesis set in an explicit order rather than silently assuming the key was impossible.

miss_ladder.py plans complement, lattice and classical-range fallbacks. Following the ladder spends additional work; it does not retroactively make the first narrow guess complete.

$$
B_1\subseteq B_2\subseteq\cdots\subseteq I,\quad E_j=B_j\setminus B_{j-1}
$$

A miss ladder searches newly admitted regions E_j as bounds widen. Exhaustion of one region excludes only that region.

Follow a failed narrow search with complement/full-range fallbacks, rather than treating heuristic misses as exclusions.

Sources: [miss_ladder.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/miss_ladder.py)

## M038 — Cubic scalar decomposition

Set R1=floor(cuberoot(k)), divide k-R1^3 by R1^2, and retain quotient C1 and remainder D1. This exactly re-encodes k.

The code reconstructs known scalars from those digits and checks bounds. For an unknown key the digits are also unknown; an exact identity does not disclose them from the address.

$$
R=\lfloor\sqrt[3]{k}\rfloor,\quad k=R^3+CR^2+D,\quad 0\leq D<R^2
$$

C and D are the quotient and remainder of k-R^3 divided by R^2. The identity uniquely re-encodes a known positive integer.

Exact reconstruction of known integers works; the representation itself supplies no unknown digits or entropy reduction.

Sources: [ctheory.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/ctheory.py); [PUZZLE_STATUS_NOTE.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PUZZLE_STATUS_NOTE.md)

## M039 — Five-level R1/R2/S3/S4/S5 tower

Reapply root/division decompositions to R1 and later components, producing a hierarchy of smaller coordinates.

The tower code computes R2 and S-level quantities, some from bit-length formulas. Its tables describe known-key coordinates or target-size anchors, not independently observed secret digits.

$$
Y_{j-1}=Y_j^3+c_jY_j^2+d_j,\quad Y_0=k,\quad 1\leq j\leq5
$$

Y1,Y2,Y3,Y4,Y5 correspond to R1,R2,S3,S4,S5. Each Y_j is the floor cube root of the previous value; retain all remainders for reconstruction.

Recursive roots and coefficients organize scalar coordinates; high levels often depend only on advertised bit width.

Sources: [analyze_ctheory_decompose.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/analyze_ctheory_decompose.py)

## M040 — Exact root bounds and coefficient feasibility

Integer roots and inequality bounds determine which digit combinations could reconstruct an integer inside the advertised interval.

Exact arithmetic helpers enumerate feasible roots, clip remainders and verify reconstruction. They reject impossible combinations, while still retaining every feasible unknown scalar unless a separate heuristic cuts further.

$$
C_{\max}(R)=\left\lfloor\frac{(R+1)^3-R^3-1}{R^2}\right\rfloor
$$

The maximum coefficient comes from the last integer before the next cube. In particular, C=3 is possible even when R is large.

Integer roots, coefficient limits, clipping and reconstruction are tested arithmetically.

Sources: [ctheory_arithmetic.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/ctheory_arithmetic.py); [ctheory_math_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_math_20260920.py)

## M041 — Phase-2 Delta2 enumeration

Given R2 and C2, each Delta2 selects an R1 through R1=R2^3+C2*R2^2+Delta2.

Phase-2 routines compute feasible Delta2 bounds and enumerate or stride through them. The smaller-looking parameter still represents many distinct scalar bases that may each require a D1 search.

$$
R_1=R_2^3+C_2R_2^2+\Delta_2,\quad0\leq\Delta_2<R_2^2
$$

Enumerate feasible Delta2 values for each R2,C2 and intersect the resulting R1 possibilities with puzzle-range constraints.

Enumerate feasible R1 values within each R2/C2 hypothesis; this is a search coordinate, not an independently observed point.

Sources: [phase2.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/phase2.py)

## M042 — Phase-2 public-key-guided light probes

For a guessed Delta2, build the corresponding shifted public point and test a small D1 budget before investing in a full leaf hunt.

phase2_search.py ranks hints, constructs Phase-3 candidates and optionally probes them. It does not extract Delta2 directly from Q; every probe remains conditional on its guessed coordinates.

$$
Q_D=Q-(R_1^3+C_1R_1^2)G
$$

A Delta2 hypothesis determines R1 and hence this residual target. A short D1 probe tests that branch; Delta2 itself is not an independently supplied discrete log.

Construct D1 targets from Delta2 guesses and run bounded probes; no independent Delta2 oracle is obtained.

Sources: [phase2_search.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/phase2_search.py)

## M043 — Puzzle-bound clipping of D1

Intersect a leaf's D1 limits with the public puzzle bounds after subtracting its proposed base.

The audit measures how often clipping truly shortens D1. At high indices the public interval often contains the whole leaf, so the original D1 uncertainty remains.

$$
D_{\min}=\max(0,L-B),\quad D_{\max}=\min(R_1^2-1,U-B)
$$

B=R1^3+C1 R1^2. Clipping the D1 interval uses inclusive puzzle bounds [L,U]; an empty interval rejects the branch.

Historical audit records no useful narrowing for its high-index sample; advertised puzzle bounds are too broad at this leaf scale.

Sources: [d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

## M044 — D1 high-index ratio bands

Estimate normalized D1 positions from solved examples and prioritize a common ratio band for new slots.

Historical high-index min/max or leave-one-out bands were exported as search presets. Their reduced width is real for the chosen band, but held-out misses show it is not guaranteed containment.

$$
\rho=\frac{D_1}{R_1^2},\quad D_1\in[\lceil aR_1^2\rceil,\lfloor bR_1^2\rfloor]
$$

A calibrated ratio band [a,b] induces an integer D1 band, intersected with legal bounds. Its held-out containment must be measured.

Calibrated narrow bands reduce width conditionally but miss held-out keys; their complement is required for complete support.

Sources: [d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

## M045 — Two-phase D1 band/complement policy

Search the ratio band first; if it misses, search all remaining D1 values. This preserves eventual full leaf coverage.

Preset builders generate phase-one and complementary phase-two jobs. The combined policy restores eligibility but can cost more than a single unpartitioned interval search.

$$
\mathcal{D}=B\,\dot\cup\,(\mathcal{D}\setminus B)
$$

First search the selected D1 band B, then the rest of the legal D1 set. The union, rather than the initial band alone, supplies full coverage.

Prioritize a calibrated band and search its remainder after a miss. Union coverage restores full range rather than reducing entropy.

Sources: [d1_narrowing.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/d1_narrowing.py); [d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

## M046 — Recursive remainder/sub-digit decomposition

Decompose a remainder again into its own root, coefficient and residual, then repeat recursively.

Backtests count subdigits and compare their distributions with equally transformed random integers. Most apparent simplification is a change of coordinates; omitted subdigits remain unknown.

$$
d=u^3+au^2+\epsilon,\quad u=\lfloor\sqrt[3]{d}\rfloor,\quad0\leq\epsilon<u^2
$$

Apply the same decomposition to a positive remainder d; handle d=0 separately. The tuple retains the original remainder's information.

Deeper splits were compared with random controls; apparent digit biases can arise from the map itself.

Sources: [deeper_decomposition_limits.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/deeper_decomposition_limits.md)

## M047 — All-known-key slot containment

A complete hypothesis includes every base digit needed to define the final searched interval. Test whether the published answer lies in that interval.

Backtest scripts evaluate known-key slot containment after candidate construction. Knowing the answer for evaluation must not leak into hint generation or be reported as an actual cryptographic recovery.

$$
H=\sum_{i=1}^{m}\mathbf{1}\{k_i\in\mathcal{S}_i\}
$$

A slot-containment test counts published keys inside their generated scalar sets S_i. Inclusion is different from independently finding those keys.

Check whether a generated complete slot includes a published answer; containment is not independent discovery of that answer.

Sources: [backtest_all_keys_slots.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/backtest_all_keys_slots.py); [all_keys_slot_backtest.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/all_keys_slot_backtest.md)

## M048 — Post-slot square-root cost scaling

Kangaroo leaf work scales roughly with the square root of its interval width, conditional on the correct target interval.

slot_scaling.py reports D1 leaf costs and related floor bounds. A real plan must additionally count all root/remainder hypotheses and its probability of including the correct leaf.

$$
T_{\mathrm{total}}\asymp\sum_{j=1}^{s}\sqrt{W_j}
$$

W_j is the width of each separately searched residual interval. Counting only one leaf omits the work of finding the correct branch.

Count leaf cost conditional on a correct slot; audits warn against omitting the number of unknown slots.

Sources: [slot_scaling.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/slot_scaling.py)

## M049 — Constraint-satisfaction slot construction

Express digit domains and interval inequalities as constraints, then select variable orderings to prune impossible partial assignments.

CSP modules compare fixed, minimum-remaining-values and degree strategies. They reduce wasted inconsistent tuples but do not add new information about which consistent tuple is the secret.

$$
\mathcal{F}=\{\theta:g_a(\theta)\;\mathrm{holds\ for\ all}\ a\}
$$

A constraint solver retains tuples theta satisfying all declared arithmetic/range constraints. Variable ordering changes traversal cost, not which feasible tuple is the target.

Exact feasibility graph with fixed, MRV and degree orderings; pruning invalid tuples does not predict the valid target tuple.

Sources: [solver.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/csp/solver.py); [csp_ordering_backtest.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/csp_ordering_backtest.md)

## M050 — Gamma-band and lattice narrowing presets

Intersect feasible roots with selected gamma bands, FUSED tolerance bands or a two-stage union.

Preset reports count surviving R2 values and measure known-key coverage. A large candidate reduction can simply mean many true keys were excluded by the heuristic.

$$
\mathcal{R}_\gamma=\{S_3^3+\gamma S_3^2+\delta:0\leq\delta<S_3^2\}
$$

A fixed anchor and coefficient define an R2 band. Intersect with canonical-root, puzzle-range and predictor bounds before claiming coverage.

Compare full lattice, gamma restrictions and FUSED intersections; stronger cuts reduce measured target coverage.

Sources: [search_narrowing_ladder.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/search_narrowing_ladder.md)

## M051 — Tiered minimal/narrow/focus/lattice exports

Package different breadths of the same hypothesis family as minimal, narrow, focus or full-lattice tiers.

Exporters select/cap slots, sometimes with diversity rules. Saved calibration reports explicitly check whether the known true R2 and full tuple were omitted from each exported job set.

$$
\mathcal{S}_{\mathrm{preset}}=\bigcup_{j\in J_{\mathrm{preset}}}[L_j,U_j]
$$

Each export preset selects a job union. Calculate its scalar mass and known-key containment; the preset name does not imply guaranteed inclusion.

Saved manifests can exclude the known calibration target; a valid export is not proof of target inclusion.

Sources: [ctheory_phase_ab_summary.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/ctheory_phase_ab_summary.md)

## M052 — Anchor/TRAILING-centered slot construction

Use a supplied metadata number as a plausible center, or derive CTheory coordinates from it to define nearby slots.

wrapped_export.py constructs anchor and TRAILING jobs. They are guesses informed by an artifact, not proven high bits or offsets of the target scalar.

$$
\mathcal{B}(a,w)=\{k:\lvert k-a\rvert\leq w\}\cap I
$$

Metadata anchor a and radius w propose a scalar neighborhood. Its relation to the unknown scalar is a hypothesis requiring exact verification.

Metadata-centered guesses are explicit hypotheses and require cryptographic verification.

Sources: [wrapped_export.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/wrapped_export.py)

## M053 — GLV scalar decomposition and endomorphism

The secp256k1 endomorphism permits k congruent to r1+lambda*r2 modulo group order, with a related point map.

EC decomposition code verifies scalar and point identities and can accelerate multiplication. Computing a split of a known scalar does not recover that scalar from a public point.

$$
k\equiv k_1+\lambda k_2\pmod n,\quad kG=k_1G+k_2\phi(G)
$$

GLV uses the curve endomorphism phi with phi(G)=lambda G to accelerate arithmetic. The decomposition does not supply a new target equation.

Correct arithmetic acceleration checked on known points; often degenerate for small scalars and not a generic entropy cut.

Sources: [analyze_ec_decompose.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/analyze_ec_decompose.py); [bip32_glv_probe.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/bip32_glv_probe.md)

## M054 — GLV splitting specifically on D1

Attempt to apply the same balanced GLV split to the much smaller D1 scalar instead of a full-width scalar.

The D1 audit checks the resulting parts and finds degeneration: one component can retain effectively the original small scalar. A nominal two-part representation supplies no automatic search-width reduction.

$$
D_1\equiv d_a+\lambda d_b\pmod n
$$

Applying GLV to a small leaf D1 is the same modular scalar representation; a balanced small pair is not automatically obtained for that leaf scale.

Leaf scalars far below group order do not obtain the advertised balanced split; no free narrowing follows.

Sources: [d1_narrowing_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/d1_narrowing_audit.md)

## M055 — Exact value atlas and hierarchy visualizations

Export hierarchy values with explicit types, sizes and relationships so arithmetic and hypothesis ranges can be inspected visually.

build_value_atlas writes exact data tables and separate plotting-friendly values. The atlas explains known quantities; a chart that looks clustered is not an independent predictor.

$$
\mathcal{A}(k)=(R_1,C_1,D_1,R_2,C_2,\Delta_2,\ldots)
$$

The atlas exports exact coordinates and bounds for known inputs. Plotting A(k) does not infer A(k) from a target address.

Typed exports, scientific plots and offline views expose values and bounds; visualization itself is not a predictor.

Sources: [build_value_atlas_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/build_value_atlas_20260920.py)

## M056 — FUSED global/local R2 regression

Fit root growth globally and locally, then blend forecasts and sequence terms to predict R2 for a target index.

ctheory.py combines fitted constants with backward-looking anchors. Audits refit or exclude known answers to measure leakage; a forecast supplies a root guess, not Delta2 or D1.

$$
\log_2\widehat R_2(N)=\frac{\ell_g(N)+w\ell_l(N)}{1+w}
$$

This describes the global/local log-space anchor blend; ell_g and ell_l are fitted log2 root predictions. Other FUSED components depend on the implementation version.

Historical blends forecast ninth roots; narrow transformed error must be converted to actual scalar coverage.

Sources: [backtest_ctheory.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/backtest_ctheory.py); [heldout_r2_vs_midpoint.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/heldout_r2_vs_midpoint.md)

## M057 — Gap-five sequence extrapolation

Use the regularly spaced disclosed high-index keys to estimate trends or differences five puzzle numbers apart.

research.py extrapolates gap-five R2/remainder hints. Later controls run the same fitting on synthetic corpora to test whether apparent predictability exceeds the interval geometry alone.

$$
\widehat R_2(N)=\frac{R_2(N-5)^2}{R_2(N-10)}
$$

Geometric gap-five extrapolation needs both prior roots and a nonzero denominator. Its target root still requires held-out validation.

Forecast R2 or remainder ratios from every-fifth-puzzle sequences; tested against forward-only and uniform controls.

Sources: [research.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/research.py); [ctheory_forward_null_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_forward_null_20260920.py)

## M058 — Strategic Delta2 ratio hints

Reuse normalized Delta2 ratios from calibration keys to propose a short list of exact Delta2 values.

Historical code could include the evaluated key's own ratio, making recovery self-confirming. Corrected exclusion removes that shortcut and exposes the much weaker blind exact-hint performance.

$$
\widehat\Delta_2=\left\lfloor\rho_{\mathrm{train}}R_2^2\right\rfloor
$$

A previous normalized remainder ratio proposes Delta2. The target's own ratio must be excluded; rounding to an integer is not evidence of correctness.

Target-in-calibration leakage explained the old 7/7 result; corrected blind high-index results were 0/7.

Sources: [PRIVATE_KEY_RELATION_AUDIT_20260919.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PRIVATE_KEY_RELATION_AUDIT_20260919.md)

## M059 — Leave-one-out full-slot backtest

Hide one key from every calibration source, build its full slot list, then reveal the answer only to score containment.

The corrected LOO report separately counts R2, C2, Delta2 and C1 success. Coarse root coverage cannot compensate for a missing exact Delta2 coordinate.

$$
\widehat\theta_i=\mathrm{Fit}(\mathcal{D}\setminus\{i\}),\quad H=\sum_i\mathbf{1}\{k_i\in\mathcal{S}(\widehat\theta_i)\}
$$

Leave-one-out coverage evaluates the complete predicted slot. Hardcoded parameters fitted on the held-out target would still leak information.

Corrected full-slot requirements fail in the documented seven high-index holdouts, despite coarse R2 coverage.

Sources: [blind_loo_backtest_20260919.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/blind_loo_backtest_20260919.md)

## M060 — Past-only FUSED versus midpoint

Compare a learned R2 forecast with the ninth root of the scalar interval midpoint using equal tolerances and actual scalar mass.

The comparison reports root error and coverage for past-only, LOO and production fits. Later solved keys or fixed full-corpus coefficients can make an ostensibly held-out fit optimistic.

$$
\widehat R_{\mathrm{mid}}=\left\lfloor\frac{r_{\min}+r_{\max}}{2}\right\rfloor
$$

Compare the fitted rule with a declared midpoint baseline using the same root-band width. Translate both root bands back into scalar coverage.

Same-band comparisons show that transformed midpoint baselines can rival or beat apparent R2 coverage.

Sources: [heldout_r2_vs_midpoint.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/heldout_r2_vs_midpoint.md)

## M061 — Correct uniform null for ninth-root clustering

Transform uniform random scalars through the same ninth-root map as the real keys before comparing clustering.

The chat-audit experiment derives the transformed baseline and simulates matched-bit-width keys. It corrects an earlier null that mistakenly treated the compressed root coordinate as nearly uniform.

$$
\mathrm{E}[X^j]=\frac{18}{9+j}\left(1-2^{-(9+j)/9}\right),\quad X=U^{1/9}
$$

U is continuously uniform on [1/2,1); j=1,2 yields the transformed mean and variance. The discrete tier calculation weights exact ninth-root fibers.

Uniform scalars naturally cluster after ninth-root transformation; an earlier overly broad null standard deviation was corrected.

Sources: [REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md)

## M062 — Forward-only synthetic-corpus null

Run the entire forward-fitting procedure on synthetic uniform corpora, not just a single fixed prediction under a new null.

The frozen experiment counts exact covered scalar fractions and compares aggregate hits-minus-coverage with replicated null corpora. This tests that named predictor under stated historical-index conventions.

$$
T=\sum_i\left(\mathbf{1}\{k_i\in B_i\}-\frac{\lvert B_i\rvert}{\lvert I_i\rvert}\right)
$$

Refit the same forward-only procedure on synthetic tier-uniform corpora to calibrate T. B_i is the proposed scalar subset of tier I_i.

Repeat the predictor-fitting process on uniform synthetic keys and count exact scalar coverage.

Sources: [ctheory_forward_null_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_forward_null_20260920.py); [CTHEORY_FORWARD_RESEARCH_20260920.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/CTHEORY_FORWARD_RESEARCH_20260920.md)

## M063 — Family-wise forward R2 grid

When many cutoffs, widths and forecasts are examined, compare the best-looking observed result with equally selected null results.

The family-wise script searches its declared model grid on both observed and synthetic keys. Adjusted evidence is weaker than quoting the smallest unadjusted p-value.

$$
M=\max_{a\in\mathcal{A}}T_a,\quad \widehat p=\frac{1+\sum_q\mathbf{1}\{M_q\geq M_{\mathrm{obs}}\}}{B+1}
$$

Each of B synthetic replicates repeats the entire model grid A and its maximum selection. This calibrates the selected statistic, not a single prespecified rule.

Test selection across FUSED, gap-five, midpoint, cutoffs and window widths with family-wise controls.

Sources: [ctheory_forward_familywise_20261008.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_forward_familywise_20261008.py)

## M064 — Contiguous-slice selection adjustment

A favorable consecutive slice can be selected by chance. The null comparison must also search candidate slices.

The slice-family script evaluates contiguous tier ranges and selection-adjusts their scores. It measures the effect of choosing a convenient evaluation interval after seeing outcomes.

$$
M=\max_{[a,b]\in\mathcal{I}}T_{[a,b]}
$$

Search the declared family of contiguous index slices I; synthetic controls must repeat this same maximization to account for slice selection.

Compare best-looking index slices with similarly selected synthetic controls; guards against picking favorable subsequences.

Sources: [ctheory_forward_slice_family_20261008.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_forward_slice_family_20261008.py)

## M065 — Remainder precision granted true roots

Give a predictor the true root coordinates to isolate whether it can predict the remaining offset accurately enough.

The precision audit compares predicted and true remainders in integer/key units. It is an oracle diagnostic, deliberately easier than an unknown-key attack, and still exposes large residual errors.

$$
e_i=\lvert\widehat d_i-d_i\rvert,\quad \mathrm{hit}_i=\mathbf{1}\{d_i\in B_i\}
$$

True higher roots are supplied in this diagnostic. Exact remainder error and band containment measure the precision still missing under that favorable assumption.

Measures exact offset-prediction errors even when root coordinates are supplied; coarse root prediction does not supply leaf precision.

Sources: [ctheory_remainder_precision_20260920.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/checks/ctheory_remainder_precision_20260920.py)

## M066 — Oracle-versus-blind hunt comparison

Separate three tasks: reconstruct from supplied digits, include the answer in a candidate interval, and actually discover it by target verification.

Saved audits rerun planner logic with target answers excluded and compare oracle/full-slot results. A true-key-assisted coordinate lookup is labeled oracle rather than blind recovery.

$$
\mathcal{S}_{\mathrm{oracle}}=\mathcal{S}(\theta_{\mathrm{true}}),\quad\mathcal{S}_{\mathrm{blind}}=\mathcal{S}(\widehat\theta)
$$

Separate correctness conditional on true coordinates from prediction of those coordinates; each case still needs a verified target comparison.

Distinguishes provided true coordinates, key containment, and actual address/public-point discovery.

Sources: [backtest_hunt_pipeline.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/backtest_hunt_pipeline.py); [OTHER_KEYS_AND_BACKTESTS.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/OTHER_KEYS_AND_BACKTESTS.md)

## M067 — Frozen ninth-root remainder window

Normalize the ninth-root bucket remainder, fit a two-bin window on training keys, then freeze it for later keys.

The recent exact experiment uses 16 bins and puzzles 17-32 for fitting, then tests 33-64. It records both hits and the actual fraction of scalar candidates selected.

$$
r=\lfloor k^{1/9}\rfloor,\quad u=\frac{k-r^9}{(r+1)^9-r^9}
$$

Normalize the remainder within its exact ninth-root bucket. Fit a share window on the frozen training set and test it on excluded indices.

Recent test trained on 17-32 and covered 7/32 evaluation keys; uncorrected p about 0.116, not convincing evidence.

Sources: [REPORT.md](/home/arialmohan/puzzle71-corrected/ctheory-test/REPORT.md)

## M068 — Square/cube/ninth-root window family

Repeat the same declared window-fitting rule for square, cube, ninth-root and ordinary range coordinates at four widths.

extended.py tests 16 models, computes exact candidate counts and applies a multiple-model correction. It does not keep tuning windows after examining each evaluation result.

$$
r_b=\lfloor k^{1/b}\rfloor,\quad u_b=\frac{k-r_b^b}{(r_b+1)^b-r_b^b},\quad b\in\{2,3,9\}
$$

Compare frozen bucket-share models across exponents and widths. Correct the reported evidence for the full family that was tried.

Sixteen frozen models across four nominal widths; none significant after multiple-model correction.

Sources: [EXTENDED_REPORT.md](/home/arialmohan/puzzle71-corrected/ctheory-test/EXTENDED_REPORT.md)

## M069 — Walk-forward adaptive remainder windows

Before predicting each evaluation key, refit only on smaller indices, making every forecast independent of that target's stored answer.

The expanded study records per-key windows, actual coverage and sequential evidence scores. Previously inspected data still make this retrospective rather than pristine prospective validation.

$$
\theta_N=\mathrm{Fit}\{(i,k_i):i<N\},\quad B_N=\mathrm{Predict}(\theta_N,N)
$$

A walk-forward model excludes the current and future keys at each evaluation step. Its selected width and adaptation policy also require honest calibration.

Refit only on lower indices; final evidence scores did not exceed the family threshold.

Sources: [results.json](/home/arialmohan/puzzle71-corrected/ctheory-test/extended-run/results.json)

## M070 — Self-improving CTheory parameter loop

Alternate measurement, statistical analysis and parameter changes to tune a search planner's hint/window budgets.

ctheory_sim adjusts r2_pct, hint counts, tier or slot limits from recorded performance. It optimizes the tested planner; biased/leaky metrics would teach it the wrong objective.

$$
\theta_{t+1}=\mathrm{Update}(\theta_t,\mathrm{metrics}_t)
$$

theta contains hint budgets, widths and slot limits. Parameter adaptation is an optimization procedure; cryptographic progress requires measured target containment and verification.

Measure/analyze/improve loop tunes hint budgets, R2 width and slots; usefulness is limited by honest target inclusion.

Sources: [loop.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/ctheory_sim/loop.py); [Branch-cursor-ctheory-self-improve-agents-ac93.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Branch-cursor-ctheory-self-improve-agents-ac93.md)

## M071 — R2 intervals as conditional search prioritization

A root band [a,b] corresponds exactly to scalars from a^9 through (b+1)^9-1, clipped to puzzle bounds.

Interval-analysis scripts export these regions and report held-out coverage. The conversion is exact, but whether the unknown target belongs to the forecast band remains a probabilistic hypothesis.

$$
k\in[a^9,(b+1)^9)\cap I\quad\Longleftrightarrow\quad R_2\in\{a,\ldots,b\}
$$

The equivalence uses the canonical ninth-root coordinate and integer a,b. Count the clipped scalar interval to measure conditional coverage.

Root forecast bands map to exact scalar intervals; reports distinguish conditional narrowing from guaranteed coverage and statistical advantage.

Sources: [R2_SEARCH_INTERVALS.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/R2_SEARCH_INTERVALS.md); [heldout_r2_vs_midpoint.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/heldout_r2_vs_midpoint.md)

## M072 — Root floor/midpoint/ceiling candidate anchors

Turn plausible root locations into concrete integers using floors, midpoints, ceilings or differences from disclosed roots.

The root-test engine builds a fixed catalog of anchor candidates without reading the target key. Each resulting scalar is checked against that target's actual HASH160.

$$
a_{\mathrm{floor}}=r^b,\quad a_{\mathrm{mid}}=r^b+\left\lfloor\frac{(r+1)^b-r^b}{2}\right\rfloor
$$

r is a legal integer b-th root. Lower edge, midpoint and upper edge are candidate anchors; they do not exhaust the bucket.

Fixed root-band and root-difference candidate families checked against known and unknown targets.

Sources: [test.py](/home/arialmohan/scratch/puzzle-root-solve-test/test.py); [report.json](/home/arialmohan/scratch/puzzle-root-solve-test/report.json)

## M073 — Nearest-donor raw remainder carry

Express a donor key as donor_root^9 plus an offset, then place that same offset above a legal root for the target.

The nearest-donor candidate families transfer offsets from neighboring disclosed puzzle indices. They test an offset-inheritance hypothesis, not a consequence of ninth-root arithmetic.

$$
e_d=k_d-r_d^9,\quad\widehat k_t=r_t^9+e_d
$$

Transfer a donor's raw remainder to a target root hypothesis. Check interval and canonical-bucket membership, then verify the candidate address.

Transfer a disclosed key remainder to target root hypotheses; saved unknown-target candidate set contains no matches.

Sources: [test.py](/home/arialmohan/scratch/puzzle-root-solve-test/test.py); [report.json](/home/arialmohan/scratch/puzzle-root-solve-test/report.json)

## M074 — All-donor carry over every legal ninth root

Broaden the carry test to every disclosed donor and every legal target root, eliminating the nearest-donor selection restriction.

exhaustive_carry.py enumerates the entire stated donor/root family and verifies candidates. Zero hits rejects those concrete carried candidates, not all possible remainder-generation laws.

$$
\mathcal{C}_t=\{r^9+e_d:r\in\mathcal{R}_t,\ d\in\mathcal{D}\}\cap I_t
$$

Enumerate all declared donor remainders and legal target roots, removing duplicates. Exhaustion applies only to this candidate family.

Saved exhaustive-within-family report records 35,982,885 candidate checks and zero target matches.

Sources: [exhaustive_carry.py](/home/arialmohan/scratch/puzzle-root-solve-test/exhaustive_carry.py); [exhaustive_carry_report.json](/home/arialmohan/scratch/puzzle-root-solve-test/exhaustive_carry_report.json)

## M075 — Transferred within-bucket share

Transfer a fraction of a donor bucket rather than its raw offset so buckets of different sizes can be compared.

The code rescales each selected share by the target bucket width and rounds to an integer candidate. Any rounding and donor choice are part of the tested hypothesis.

$$
u_d=\frac{k_d-r_d^9}{(r_d+1)^9-r_d^9},\quad\widehat k_t=r_t^9+\lfloor u_d W_t\rfloor
$$

W_t=(r_t+1)^9-r_t^9. This transfers a normalized bucket share rather than an unchanged integer remainder.

Reuse disclosed normalized root-bucket shares at legal target roots; tests do not cover arbitrary offset functions.

Sources: [exhaustive_carry.py](/home/arialmohan/scratch/puzzle-root-solve-test/exhaustive_carry.py)

## M076 — Smooth polynomial share in puzzle index

Assume normalized bucket share is a low-degree polynomial in puzzle index and use fitted values to generate target offsets.

smooth_share.py fits degrees 1-4, evaluates errors against a uniform-share baseline and checks candidates over legal target roots. Numerical fit quality is reported separately from address hits.

$$
\widehat u(N)=\sum_{j=0}^{p}a_jN^j,\quad p\in\{1,2,3,4\}
$$

A fitted share polynomial proposes a target bucket position. Handle predictions outside [0,1) explicitly and verify reconstructed candidates.

Degrees 1-4 predict bucket shares; saved per-degree unknown-target tests report no matches.

Sources: [smooth_share.py](/home/arialmohan/scratch/puzzle-root-solve-test/smooth_share.py); [smooth_share_report.json](/home/arialmohan/scratch/puzzle-root-solve-test/smooth_share_report.json)

## M077 — Two-dimensional index/root share surface

Include both puzzle index and legal root as inputs to a polynomial surface predicting the bucket share.

surface2d.py fits the declared low-degree surfaces on disclosed data and verifies reconstructed candidates. Additional model dimensions do not by themselves resolve an unknown remainder.

$$
\widehat u(N,r)=\sum_{i+j\leq p}a_{ij}N^ir^j
$$

A low-degree surface uses both index and root. This is the model family, not a guarantee that an unknown bucket share lies on that surface.

Fit share as a low-degree surface of index and root, then verify resulting candidates; no saved unknown-target hits.

Sources: [surface2d.py](/home/arialmohan/scratch/puzzle-root-solve-test/surface2d.py); [surface2d_report.json](/home/arialmohan/scratch/puzzle-root-solve-test/surface2d_report.json)

## M078 — Gap-fill normalized-position interpolation

Assume normalized interval position changes smoothly between the nearest disclosed neighbors. Interpolate that position into the target interval.

gap_fill.py creates one or more exact integer candidates from those neighboring positions. The hypothesis is smoothness; the verifier, not visual continuity, determines success.

$$
u_t=(1-\alpha)u_a+\alpha u_b,\quad\alpha=\frac{t-a}{b-a}
$$

Interpolate normalized tier positions between disclosed indices a,b, or extrapolate when alpha is outside [0,1]. Convert to integers and verify.

Interpolate/extrapolate between disclosed neighboring puzzles and verify candidates; no recorded matches.

Sources: [gap_fill.py](/home/arialmohan/scratch/puzzle-root-solve-test/gap_fill.py); [gap_fill_report.json](/home/arialmohan/scratch/puzzle-root-solve-test/gap_fill_report.json)

## M079 — Gap-fill linear/geometric root interpolation

Interpolate roots linearly or geometrically, then map the forecast root back to an integer scalar.

The gap-fill test generates candidates from both root interpolation rules and clips to the target range. A nearby root can still correspond to a very large scalar error.

$$
\widehat r_t=(1-\alpha)r_a+\alpha r_b\quad\mathrm{or}\quad r_a^{1-\alpha}r_b^\alpha
$$

Linear and geometric interpolation are alternative root hypotheses. Integer rounding and reconstructed offsets determine the actual candidate set.

Interpolate root coordinates and reconstruct candidate powers; tested candidates did not recover unknown keys.

Sources: [gap_fill.py](/home/arialmohan/scratch/puzzle-root-solve-test/gap_fill.py)

## M080 — Gap-fill log-key and raw-offset interpolation

Interpolate log2(key) or the raw ninth-root residual as an alternative notion of smooth progression.

The same bounded test reconstructs scalars under these assumptions and compares addresses. Log closeness or matching early values is not accepted as a recovered key.

$$
\log\widehat k_t=(1-\alpha)\log k_a+\alpha\log k_b
$$

Log-key interpolation is one family; directly interpolating raw offsets is another. Neither smoothness assumption follows from address data.

Alternative smoothness assumptions tested against exact address hashes, not judged by numerical proximity alone.

Sources: [gap_fill.py](/home/arialmohan/scratch/puzzle-root-solve-test/gap_fill.py)

## M081 — Near-miss anomaly testing

Judge proximity relative to the density and placement of the entire candidate set. Dense sets naturally create close numerical neighbors.

nearmiss_analysis.py holds the candidate geometry fixed, draws uniform targets in the same interval and compares minimum distances. This is a diagnostic of chance closeness, not a new candidate verifier.

$$
\delta(k,\mathcal{C})=\min_{c\in\mathcal{C}}\lvert k-c\rvert
$$

Compare this nearest-candidate distance with distances of tier-uniform control targets against the same candidate geometry. A small distance is not a hash match.

Compare nearest-candidate distances with uniform targets against the same candidate geometry; closeness alone is not a verified key.

Sources: [nearmiss_analysis.py](/home/arialmohan/scratch/nearmiss-20261008/nearmiss_analysis.py); [nearmiss_results.json](/home/arialmohan/scratch/nearmiss-20261008/nearmiss_results.json)

## M082 — All-donor carry proximity null

Ask whether any donor-offset/root combination lands unusually near a held-out key compared with identical carry geometry under uniform targets.

all_donor_carry.py excludes that target from donor construction and computes observed versus null proximity. A favorable minimum is not an address match and may require selection adjustment.

$$
\delta_i=\min_{c\in\mathcal{C}(\mathcal{D}\setminus\{i\})}\lvert k_i-c\rvert
$$

Exclude the known target from its donor set before measuring proximity. Repeat donor construction and distance scoring for matched controls.

Compare minimum carry distance to uniform controls while excluding the known target from its donor set.

Sources: [all_donor_carry.py](/home/arialmohan/scratch/nearmiss-20261008/all_donor_carry.py); [all_donor_carry.json](/home/arialmohan/scratch/nearmiss-20261008/all_donor_carry.json)

## M083 — Blind nth-root ladder address tests

Build nth-root scheduled anchors and difference-based forecasts without supplying the hidden scalar to the candidate generator.

The saved PEC37 test covers index-only, leave-one-out, random-holdout and unknown-target candidates. Reported matches are confined to tiny trivial intervals rather than scalable unknown-key recovery.

$$
r_b=\lfloor k^{1/b}\rfloor,\quad \widehat k=\widehat r_b^{\,b}+\widehat e_b
$$

A root-ladder proposal must supply both the root estimate and remainder rule. Verify the resulting finite integer candidates exactly.

Index-only, leave-one-out and random holdout candidates mostly match only trivial tiny puzzles; no unknown-target matches recorded.

Sources: [nth_root_blind_address_test.json](/home/arialmohan/workspace/projects/pec37/data/nth_root_blind_address_test.json)

## M084 — Exact polynomial/difference continuation

Fit exact rational polynomials to known scalars, roots or normalized positions, then evaluate them at held-out indices.

The atlas audit tests degrees 0-6 and multiple masking/encoding variants. It uses published answers afterward for scoring and checks target-derived addresses for concrete candidate attempts.

$$
\Delta^{d+1}f(i)=0\quad\mathrm{for\ a\ degree}\ d\ \mathrm{polynomial}
$$

The identity applies on equally spaced indices. Fitting or continuing a low-degree polynomial is a hypothesis about the data-generating rule.

Degree 0-6 models of scalars, range positions and roots failed exact higher-index recovery in the saved tests.

Sources: [check_routes.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/check_routes.py); [REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md)

## M085 — Frozen candidate families on 77 unknown targets

Freeze a finite candidate recipe, apply it to every locally undisclosed puzzle, and compare each output with that puzzle's target hash.

all_unknown_check.py evaluates 77 database entries and saves candidate/target counts. A completed finite recipe search is not an exhaustive search of all their intervals.

$$
\mathcal{C}_i=\bigcup_{f\in\mathcal{F}}\mathcal{C}_{i,f},\quad H=\sum_i\sum_{k\in\mathcal{C}_i}\mathbf{1}\{h(k)=h_i\}
$$

Freeze the finite family F before checking unknown targets and deduplicate candidate/target pairs. Counts cover only that declared union.

Local all-unknown report records 2,744 distinct candidate/target checks and no matches.

Sources: [all_unknown_check.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/all_unknown_check.py); [OTHER_KEYS_AND_BACKTESTS.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/OTHER_KEYS_AND_BACKTESTS.md)

## M086 — Finite continuation attempts specifically for #140

Collect new finite leads specifically for a public-point target, derive candidate scalars or intervals and perform exact comparisons.

continue_140.py indexes archive clues, binary-derived numbers and signature relations. It records bounded attempts; finding a plausible story or interval does not count as discovering #140.

$$
\mathcal{C}_{140}=\{f(140):f\in\mathcal{F}_{\mathrm{declared}}\}\cap I_{140}
$$

These are finite continuation hypotheses and artifact-derived candidates. An unsuccessful test excludes these candidates, not the full tier.

Archive leads and binary candidates were verified as bounded hypotheses, not exhaustive interval searches.

Sources: [continue_140.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/continue_140.py); [results.json](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/continuation-140-run/results.json)

## M087 — Fixed affine/LCG key recurrence

A fixed affine recurrence maps the same low-bit input to the same output. Contradictory observed transitions can therefore reject that recurrence family.

The audit exhausts small modular coefficient pairs and gives an exact parity obstruction. It does not exclude hidden state, changing coefficients, discarded outputs or unrelated deterministic wallets.

$$
x_{t+1}\equiv ax_t+c\pmod{2^b}
$$

Fixed affine recurrence parameters must satisfy every applicable observed low-bit constraint under the declared masking and output schedule.

Exact low-bit constraints reject the named fixed-parameter recurrence family; hidden state and different generators remain outside scope.

Sources: [REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md); [analyze_creator_generator.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/analyze_creator_generator.py)

## M088 — LFSR / Berlekamp-Massey reconstruction

An LFSR predicts later bits from a fixed linear combination of earlier bits. Berlekamp-Massey finds a shortest recurrence fitting a supplied bitstream.

Archived generator work applies linear recurrence tests to concatenated known keys. Fitting the observed stream is insufficient unless the same state and output schedule predict unseen keys.

$$
s_t=\sum_{j=1}^{\ell}a_js_{t-j}\quad\mathrm{in}\ \mathbf{F}_2
$$

Berlekamp-Massey finds a shortest binary linear recurrence fitting the supplied stream. A compatible fit requires independent predictive validation.

Historical generator review includes bitstream linear-recurrence tests; no transferable unknown-key generator established.

Sources: [analyze_creator_generator.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/analyze_creator_generator.py); [PUZZLE_STATUS_NOTE.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PUZZLE_STATUS_NOTE.md)

## M089 — Two-adic/Hensel polynomial recurrence

A polynomial recurrence modulo powers of two can constrain parameters one bit at a time; lifting extends compatible low-bit solutions.

The generator catalog tests declared polynomial/2-adic forms against known puzzle transitions. It searches a restricted family, not all possible deterministic key generators.

$$
f(x_j)\equiv0\pmod{2^j},\quad x_{j+1}=x_j+\epsilon2^j
$$

For epsilon in {0,1}, test which lifts satisfy the polynomial congruence at the next precision. Applicability depends on the specified recurrence hypothesis.

Tests of squared-state and modular recurrence hypotheses are archived; finite failures are not impossibility theorems.

Sources: [analyze_creator_generator.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/analyze_creator_generator.py); [PUZZLE_STATUS_NOTE.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PUZZLE_STATUS_NOTE.md)

## M090 — Consecutive-difference factor patterns

If consecutive keys share a multiplicative or arithmetic construction, their differences may expose common factors or repeated relations.

Historical reviews factor or compare disclosed differences and check proposed recurrences. The known interval sizes themselves create scale trends that must be distinguished from secret generator structure.

$$
g=\gcd(k_2-k_1,k_3-k_2,\ldots)
$$

Common factors of observed differences can diagnose a proposed recurrence family. They do not by themselves predict a future key or establish a creator algorithm.

Search common factors or structured differences across published puzzle keys; no validated target predictor recorded.

Sources: [PUZZLE_STATUS_NOTE.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/PUZZLE_STATUS_NOTE.md)

## M091 — Hash-chain continuation

Hash a preceding key in a specified encoding, then mask the digest into the next puzzle's range.

Candidate scripts try SHA-256/double-hash, byte orders and minimal/32-byte lengths. Every recipe is deterministic; zero target matches applies to those encodings and transitions only.

$$
\widehat k_{i+1}=\mathrm{Mask}_{i+1}(H(\mathrm{enc}(k_i)))
$$

H, byte order, input length and masking are all part of the tested family. Different choices produce different candidate chains.

SHA-256/double-hash variants of previous keys, with endian/length choices and masks, failed named holdout and target checks.

Sources: [candidate_models.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/candidate_models.py); [REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md)

## M092 — Seed-plus-index hash/HMAC families

Derive a candidate from a small seed and an index encoding using hashing or HMAC, then compare many disclosed tiers.

hunt_multi_significant.py sweeps named seed families and tracks nontrivial matches. Matching a one- or two-bit puzzle is expected by chance and is not a recovered creator seed.

$$
\widehat k_i=\mathrm{Mask}_i(\mathrm{HMAC}_s(\mathrm{enc}(i)))
$$

A candidate seed s, index encoding and hash construction specify a reproducible family. Ordinary hash variants are separate hypotheses.

Score candidate seeds over different index encodings; requiring significant later-tier matches avoids trivial small-range coincidences.

Sources: [hunt_multi_significant.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/hunt_multi_significant.py)

## M093 — Python MT19937 masked-key replay

Replay Python's seeded PRNG under a specific call schedule and force outputs into each tier.

The hunter tests randrange and getrandbits variants across disclosed keys. Exact software version, seeding and draw order are part of the hypothesis, not generic consequences of MT19937.

$$
\widehat k_i=\mathrm{Mask}_i(\mathrm{MT19937}(s;\mathrm{schedule}_i))
$$

The seed, getrandbits/randrange recipe and prior output consumption determine each candidate. A generic MT label does not specify the stream.

Test seeded randrange/getrandbits generation schedules against published puzzle keys.

Sources: [hunt_multi_significant.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/hunt_multi_significant.py)

## M094 — Shared unmasked value, prefix and suffix tests

Re-masking one common integer would force predictable prefix/suffix agreement among tiers. Independent draws need not share those bits.

Known-key pair tests count overlap and compare aligned bits with random controls. They test the common-value construction; ordinary BIP32 child masking does not imply that same shared-value model.

$$
k_i\equiv K\pmod{2^{b_i}}
$$

A shared-unmasked-value hypothesis requires agreement on every jointly observed low bit. Prefix and suffix variants impose different overlap constraints.

Known-key overlap and random controls reject the tested common-prefix/suffix hypotheses, not every wallet generator.

Sources: [key_masking_hypothesis.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/key_masking_hypothesis.md)

## M095 — CoinVault/mSIGNA BIP32 plus mask

BIP32 derives a child scalar using HMAC-SHA512 and chain codes; the proposed creator mask keeps the required leading bit and lower child bits.

The catalog tests supplied seed materials and CoinVault/mSIGNA-style paths, with synthetic positive controls. No tested catalog entry reproduces the nontrivial public puzzle sequence.

$$
\widehat k_i=\mathrm{Mask}_i(\mathrm{CKD}(\mathrm{Master}(s),p_i))
$$

Reproduce the wallet's seed-to-master and BIP32 child path p_i exactly before applying the proposed puzzle mask.

Bounded seed/path catalog did not reproduce nontrivial puzzle keys; synthetic known-wallet recovery validates the checker.

Sources: [coinvault_bip32_oracle.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/coinvault_bip32_oracle.md)

## M096 — Electrum-v1 and Armory masking models

Historical deterministic wallets can derive children by algorithms different from BIP32. Apply each modeled derivation before the puzzle mask.

Dedicated Electrum-v1 and Armory scripts test those concrete wallet families. Their existence does not establish that the creator used either wallet or that its seed is enumerable.

$$
\widehat k_i=\mathrm{Mask}_i(\mathrm{Derive}_{\mathrm{wallet}}(s,i))
$$

Electrum-v1 and Armory have distinct historical derivation procedures. This interface states their required inputs without treating them as interchangeable.

Historical deterministic-wallet derivation families and creator-style masks have dedicated test scripts.

Sources: [electrum_v1_mask_test.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/electrum_v1_mask_test.py); [armory_mask_test.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/armory_mask_test.py)

## M097 — BIP32 child/index interval pairing

Treat child derivation indices as a pair such as start index and interval, and test path templates built from those integers.

child_wallet_interval_probe.py derives masked children for supplied seeds and compares public targets. A synthetic known-template test checks the probe; unknown creator provenance remains missing.

$$
(p,i,N)\longmapsto\mathrm{Mask}_N(\mathrm{CKD}(s,p/i))
$$

Enumerate the declared path templates, child indices and puzzle intervals under the supplied seed. Synthetic tests do not identify the puzzle creator's seed.

Enumerate path-template index/interval pairs under an explicitly supplied seed; synthetic self-test is separate from creator identification.

Sources: [child_wallet_interval_probe.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/child_wallet_interval_probe.py)

## M098 — Supplied extended-key derivation leads

An explicitly supplied extended private node allows deterministic child derivation along a bounded list of relative paths.

The audit validates checksums, tests seven relative path families and index shifts, then compares initial nontrivial probe keys. It never prints or republishes the supplied secret nodes.

$$
\mathcal{C}_N=\{\mathrm{Mask}_N(\mathrm{CKD}(x,p)):p\in\mathcal{P}\}
$$

x denotes the supplied extended-key lead, omitted from the report. P is a finite set of relative paths and shifts.

Three unique supplied leads tested over bounded relative paths/index shifts; no reproduction of nontrivial probe keys. Secrets are not included here.

Sources: [check_wallet_leads.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/check_wallet_leads.py); [wallet_lead_results.json](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/wallet_lead_results.json)

## M099 — Entropy-prefix and full-width constraints

A known source-entropy prefix or full-width relation could restrict which masked outputs are possible. It must be derived independently of the hidden key.

These scripts construct and score named prefix/full-width hypotheses. They do not turn a public difficulty interval into additional leaked secret bits without matching evidence.

$$
k_N=2^{N-1}+(K\;\mathrm{mod}\;2^{N-1})
$$

The creator-style mask fixes the leading interval bit and exposes low bits of a hypothetical source K. Full-width appearance does not prove full source entropy.

Named candidate scripts examine how scalar masking and source entropy could constrain keys; no generic recovery follows.

Sources: [entropy_prefix_test.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/entropy_prefix_test.py); [fullwidth_constraint_test.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/fullwidth_constraint_test.py)

## M100 — CLI fingerprint and key clustering

A short fingerprint of known components can group similar CLI outputs or candidate tuples. It helps organize evidence and detect duplicate hypotheses.

set_bits.py and clustering tools compute partial masks, Hamming statistics and groups. A matching fingerprint is a lossy summary, not proof of an exact scalar or valid search cut.

$$
d_H(x,y)=\mathrm{popcount}(x\mathbin{\oplus}y)
$$

Hamming distances and masked fingerprints compare aligned known coordinates. A cluster is descriptive unless it predicts independently verified targets.

Hamming, low-word masks and partial fingerprints organize known coordinates; not established target narrowing.

Sources: [set_bits.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/set_bits.py); [analyze_cli_clustering.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/analyze_cli_clustering.py)

## M101 — Popcount and aligned-bit distribution tests

Compare the number of set bits and aligned bit agreements with the distribution expected from uniform interval keys.

Reports measure popcounts, low-bit patterns and pairwise overlaps. Statistical similarity/difference concerns the tested corpus; it does not directly provide the unknown bits of the next key.

$$
w(k)=\sum_j b_j,\quad \widehat p_j=\frac{1}{m}\sum_i b_{ij}
$$

Popcount w and aligned-bit frequencies summarize disclosed keys; matched controls must respect tier widths and fixed leading bits.

Known-key bit densities and overlap are compared with controls; observed appearance is not a scalar equation.

Sources: [set_bits_audit.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/set_bits_audit.md)

## M102 — Counter/small-affine early public-key relations

Small scalar relations are visible as public-point relations: alpha*P_i+beta*P_j+gamma*G equals the identity if the corresponding scalars satisfy them.

Early-key scripts sweep bounded coefficient and offset grids, including nonce-to-signer pairs. A genuine relation could help, but the saved finite sweeps report no such target recovery.

$$
Q_j\stackrel{?}{=}aQ_i+bG
$$

Search only the declared coefficient and offset bounds. A verified relation would imply k_j congruent to a k_i+b modulo subgroup order n.

Recorded all-pairs and focused early-key coefficient sweeps found no relation in their finite coefficient/offset bounds.

Sources: [early_key_relations.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/early_key_relations.md); [early_key_relations_focus.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/early_key_relations_focus.md)

## M103 — Firmware-accurate Coldcard Yasmarang entropy-position analysis

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Reconstructs the affected firmware path and identifies which seed registers and skip positions influence generated bytes; it does not establish wallet recovery or an address match.

Sources: [entropy_position.py](/home/arialmohan/scratch/temp/entropy_position.py)

## M104 — Cold-boot entropy propagation and mixer analysis

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Compares chip/mixer streams, skip lattices and post-hash behavior to distinguish low-entropy inputs from claims that the mixer itself creates an address family; no spend path or address matching is performed.

Sources: [entropy_patterns.py](/home/arialmohan/scratch/temp/entropy_patterns.py)

## M105 — Local Coldcard wallet-generation replay

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Replays explicit, sanitized initial states through Yasmarang, SHA-256 whitening and BIP-39 formatting for implementation analysis; generated examples are not evidence of a historical wallet seed.

Sources: [coldcard_make_new_wallet.py](/home/arialmohan/scratch/temp/coldcard_make_new_wallet.py)

## M106 — Read-only funded-address membership analysis

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Queries address status for local watchlists and classifies script types; membership is not proof of seed ownership, key recovery or a valid spend path.

Sources: [funded_membership.py](/home/arialmohan/scratch/temp/funded_membership.py)

## M107 — Read-only residual-UTXO and drain-wave analysis

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Compares remaining UTXOs and observed drain timing/amount shape against a declared block boundary; chain observations do not identify a private key.

Sources: [residual_utxo.py](/home/arialmohan/scratch/temp/residual_utxo.py)

## M108 — Pre-drain co-input and address-cluster analysis

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Groups watchlist addresses by shared pre-drain transaction inputs and separates those from later sweep co-inputs; the saved result is chain evidence, not proof of common seed derivation.

Sources: [seed_addr_cluster.py](/home/arialmohan/scratch/temp/seed_addr_cluster.py); [seed_addr_cluster.json](/home/arialmohan/scratch/temp/seed_addr_cluster.json)

## M109 — Bounded Coldcard entropy-grid enumeration against a funded-address dump

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

A bounded Python/Rust-style replay enumerated 300 modeled wallets across explicit UID, SysTick, skip and reseed grids, deriving BIP44/49/84 receive/change paths and comparing against a dated address-balance dump; listed hits validate membership only and do not establish seed ownership or exhaustive coverage.

Sources: [check_experiments_vs_balance.py](/home/arialmohan/scratch/temp/coldcard_enum/check_experiments_vs_balance.py); [coldcard_experiments_vs_balance.json](/home/arialmohan/scratch/temp/coldcard_enum/logs/coldcard_experiments_vs_balance.json)

## M110 — Rust Coldcard address-derivation backend

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Native implementation covers Yasmarang output, BIP-39/BIP-32 derivation and P2PKH/P2WPKH address encoding for bounded enumeration; backend existence is not proof of a historical match.

Sources: [yasmarang.rs](/home/arialmohan/scratch/temp/coldcard_enum/src/yasmarang.rs); [derive.rs](/home/arialmohan/scratch/temp/coldcard_enum/src/derive.rs); [Cargo.toml](/home/arialmohan/scratch/temp/coldcard_enum/Cargo.toml)

## M111 — Coldcard entropy statistical variation sweep

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Saved 65,536-sample windows report unique outputs, zero observed collisions and near-balanced first-byte/bit statistics under synthetic register variations; this measures the modeled output distribution, not wallet recovery.

Sources: [stats-range-output.txt](/home/arialmohan/scratch/temp/coldcard_enum/stats-range-output.txt); [stats-continuous-output.txt](/home/arialmohan/scratch/temp/coldcard_enum/stats-continuous-output.txt); [stats-variations-output.txt](/home/arialmohan/scratch/temp/coldcard_enum/stats-variations-output.txt)

## M112 — All-unknown-target generator matrix

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Ten fully specified SplitMix64/Lehmer models were checked against 770 unknown-target identities, plus 97,216 low-bit-consistent candidates where feasible; zero matches, with prior solved-key failures limiting interpretation.

Sources: [generator_all_unknown_targets_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/generator_all_unknown_targets_20261020.py); [generator_all_unknown_targets_report_20261020.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/generator_all_unknown_targets_report_20261020.md)

## M113 — Wallace LCG masked-word backtest

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

All 2^17 states compatible with the Puzzle #65 low-word constraint were tested under 17/18-word packing; survivors fell to zero by tier 67 under the stated mask and schedule.

Sources: [wallace_lcg_mask_backtest_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/wallace_lcg_mask_backtest_20261020.py); [wallace_lcg_mask_backtest_20261020.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/wallace_lcg_mask_backtest_20261020.json)

## M114 — Park-Miller packed-word target checks

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Lehmer multipliers 16807/48271 with 8/9-word packing and both orders were checked against #66, #71 and #140; candidate target identities did not match.

Sources: [park_miller_target_check_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/park_miller_target_check_20261020.py); [park_miller_target_check_20261020.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/park_miller_target_check_20261020.json)

## M115 — SplitMix64 masked-sequence target checks

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

One-draw low-64-bit candidates and four-draw word orders were checked against target HASH160s; evaluated candidates produced no matches.

Sources: [splitmix64_target_check_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/splitmix64_target_check_20261020.py); [splitmix64_target_check_20261020.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/splitmix64_target_check_20261020.json)

## M116 — Lagged-RNG multiword wallet-key audit

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

16/32/64-bit word widths and both assembly orders were compared with archived lagged recurrences; the listed contiguous layouts failed their available equations, while underdetermined layouts remain untested.

Sources: [archive_rng_wordstream_check_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/archive_rng_wordstream_check_20261020.py); [archive_rng_wordstream_audit_20261020.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/archive_rng_wordstream_audit_20261020.md)

## M117 — Half-generator cross-curve coordinate analysis

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Verified the half-generator relation and a repeated internal x-coordinate pattern across four standard curves; the known generator relabeling does not reduce the Bitcoin puzzle discrete-log search space.

Sources: [half_generator_cross_curve_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/half_generator_cross_curve_20261020.py); [half_generator_cross_curve_report_20261020.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/half_generator_cross_curve_report_20261020.md)

## M118 — Deeper remainder/permutation-tree null calibration

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Sixty-four nonconstant features were compared with 3,000 range-matched control corpora; the observed family maximum was not unusual, so no beacon was established.

Sources: [remainder_tree_beacon_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/remainder_tree_beacon_20261020.py); [remainder_tree_beacon_report_20261020.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/remainder_tree_beacon_report_20261020.md)

## M119 — Low-bit affine and linear-state generator audit

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Direct affine recurrence and at-most-32-bit binary-linear-state families fail under the stated mask and indexing assumptions; this does not exclude wider, nonlinear, hashed or skipped-state generators.

Sources: [affine_lowbits_check_20261019.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/affine_lowbits_check_20261019.py); [lowbit_linear_state_20261019.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/lowbit_linear_state_20261019.py); [lowbit_generator_audit_20261019.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/lowbit_generator_audit_20261019.md)

## M120 — Unknown-parameter inventory through Puzzle #160

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Enumerates which coordinates are publicly constrained versus unknown across 77 unsolved tiers; fixed high decomposition coordinates are range consequences, not recovered private-key information.

Sources: [unknown_parameter_inventory_20261020.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/unknown_parameter_inventory_20261020.py); [unknown_parameter_inventory_20261020.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/unknown_parameter_inventory_20261020.json)

## M121 — Index-offset holdout and coefficient-interval audits

The method is defined by the named evidence files and recorded scope.

The inventory preserves the recorded finding; this explained edition does not rerun or independently certify the source.

No explicit formula has been editorially assigned to this newer method entry.

Tests index-based offset models on held-out tiers and enumerates exact decomposition coefficient possibilities over unsolved intervals; bounded intervals do not identify a scalar.

Sources: [index_offset_holdout_20261019.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/index_offset_holdout_20261019.py); [index_offset_holdout_20261019.json](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/index_offset_holdout_20261019.json); [coefficient_interval_audit_20261019.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/coefficient_interval_audit_20261019.md)

## M122 — Sparse ORIG decomposition and peel chain

Describe a supplied sparse integer as a few shifted terms plus a tail, then reverse those terms to expose nested smaller values.

The ORIG investigation verifies its exact decomposition and peel chain to tiny public keys. Constructing an integer around a known tail does not explain generation of later independent puzzles.

$$
k=\sum_{j\in S}2^j
$$

A sparse construction specifies a small set S of occupied bit positions. Peeling a chosen highest bit or block recovers the construction's tail, not a general puzzle sequence.

A constructed sparse scalar peels to tiny known puzzle values; this does not generate the numbered puzzle sequence.

Sources: [sparse_key_investigate.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/sparse_key_investigate.md)

## M123 — Nested previous-key tail grow/peel

Build the next sparse value by embedding the previous entire value under a new frame, and reverse that operation by peeling the frame.

The audit compares this recursive rule with the actual fixed-tail expression. They coincide at one chosen step but produce different subsequent integers, exposing a conflated model.

$$
k_{t+1}=2^{s_t}k_t+u_t
$$

A nested grow model shifts the entire previous key and appends a tail u_t smaller than 2^s_t. Peeling reverses this specified construction.

Distinguishes nested-tail updates from fixed-tail co-shifts; the two agree at one construction step, not generally.

Sources: [sparse_key_hardthink.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/sparse_key_hardthink.md)

## M124 — Fixed-tail co-shift family

Keep a small tail constant while shifting selected high and middle terms together. This defines a precise sparse family.

sparse_key_coshift.py generates that family's members. Reversibility within the constructed family is a program property, not evidence that numbered Bitcoin puzzles lie on its orbit.

$$
k_t=2^{s_t}F+u
$$

A fixed frame F is shifted while tail u stays fixed. This differs from shifting the complete prior key at every step.

Exact sparse-key program shifts its frame while preserving the tail; valid program structure is not a Bitcoin predictor.

Sources: [sparse_key_coshift.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_coshift.py); [sparse_key_hardthink.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/sparse_key_hardthink.md)

## M125 — Sparse bit-learning and dial-in grids

Fit simple frame positions, bit rules or mid/gap parameters to known sparse values and test whether they extend across puzzle keys.

Bit-learning and dial-in scripts sweep bounded templates and report coverage. The later investigation separates fitted tiny-key coincidences from actual unseen-address hits.

$$
\mathcal{C}=\{F(\theta):\theta\in\Theta_{\mathrm{grid}}\}
$$

theta selects frame, gap and bit parameters in a finite sparse family. Report exact recall and target checks across the declared grid.

Learn/test mid, gap, bit and frame variants; archived investigation reports poor known-key recall and no unknown address hits.

Sources: [sparse_key_bitlearn.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_bitlearn.py); [sparse_key_dial_in.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_dial_in.py); [sparse_key_investigate.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/sparse_key_investigate.md)

## M126 — Sparse XOR-tail / delta / Bloom variants

Change the recurrence using XOR tails, deltas or Bloom-filter-assisted membership screening and compare its generated values with targets.

These are alternative sparse candidate recipes. A Bloom hit is only a screening event; the scalar still needs exact address verification, and saved summaries do not establish a transferable generator.

$$
k=F(\theta)\mathbin{\oplus}\tau
$$

XOR tails tau and difference variants create alternative sparse candidate families. A Bloom prefilter needs exact membership confirmation afterward.

Alternate sparse generative families were tested without establishing a transferable key-generation rule.

Sources: [sparse_key_xor_tail.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_xor_tail.py); [sparse_key_delta_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_delta_hunt.py); [sparse_key_bloom.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/sparse_key_bloom.py)

## M127 — Gray-code range and anchor walks

Gray code orders bitstrings so adjacent offsets differ in one bit; adding or XORing offsets around an anchor defines a traversal.

bit_flip_hunt.py provides range and anchor variants. They visit specified candidates in a different order and do not prove the key is near the selected anchor.

$$
g(t)=t\mathbin{\oplus}\lfloor t/2\rfloor,\quad k_t=L+g(t)
$$

Binary-reflected Gray code visits all offsets of a complete power-of-two block. Clip or explicitly map offsets for other interval sizes.

Enumerate Gray offsets around range floors or metadata anchors; this changes order rather than entropy.

Sources: [bit_flip_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bit_flip_hunt.py)

## M128 — BFS Hamming balls and previous-key XOR

Enumerate all masks up to a chosen Hamming weight around a seed, or XOR selected bits into a previous known key.

BFS/previous-key routines search bounded neighborhoods. A completed neighborhood search says nothing about integers outside that radius unless independent target-distance information exists.

$$
\mathcal{B}_h(a)=\{a\mathbin{\oplus}e:\mathrm{popcount}(e)\leq h\}
$$

This bounded Hamming neighborhood has sum_{j=0}^h binomial(b,j) offsets for b eligible bit positions, before range clipping.

Check bounded low-Hamming-distance neighborhoods around seeds or prior keys; completeness is limited to that neighborhood.

Sources: [bit_flip_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bit_flip_hunt.py)

## M129 — TRAILING-mask and FUSED-D1 bit flips

Choose flip positions from TRAILING bits or apply flips within a D1 coordinate derived from a FUSED anchor.

These methods impose a candidate-selection hypothesis on where the unknown bits differ. Their bounds are computational choices, not leaked bit positions from the target.

$$
k=a\mathbin{\oplus}e,\quad e\mathbin{\&}\neg M=0
$$

The mask M declares which anchor bits may flip. A D1 version applies the flips to the residual coordinate before reconstructing the scalar.

Restrict flipped positions or anchor the D1 coordinate; target inclusion is unproven.

Sources: [bit_flip_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bit_flip_hunt.py)

## M130 — Dual-mask byte/bit and Gray-PDEP walks

Deposit counter bits into chosen mask positions; optionally Gray-code the counter so consecutive deposits change sparsely.

dual_mask_seq.py implements byte- and bit-index complementary-mask schedules. The masks describe allowed moves; their symbolic organization does not create missing target information.

$$
k=a\mathbin{\oplus}\mathrm{PDEP}(g(t),M)
$$

PDEP deposits successive counter bits into the set positions of M; Gray order g changes traversal. Complementary masks can define a product of such walks.

Deposit counter bits into complementary masks, including Gray ordering; these are deterministic traversal families.

Sources: [dual_mask_seq.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/dual_mask_seq.py)

## M131 — Gosper constant-weight and byte-lane variants

Gosper's rule enumerates masks of fixed Hamming weight. A byte-lane walk substitutes every byte value at one position.

The bit-flip engine generates these candidate families around anchors and verifies addresses. Their coverage is explicitly restricted to the selected mask weights or byte substitutions.

$$
E_h=\{e:\mathrm{popcount}(e)=h\},\quad\lvert E_h\rvert=\binom{b}{h}
$$

Gosper-style traversal enumerates constant-weight b-bit masks. Byte-lane replacement is a separate bounded neighborhood.

Visit fixed-weight XOR masks or replace individual bytes; no claim that these neighborhoods contain the target.

Sources: [bit_flip_hunt.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bit_flip_hunt.py); [dual_mask_seq.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/dual_mask_seq.py)

## M132 — Shift-shell and suffix Hamming hunts

Search literal scalar shells around a metadata distance, or flip a limited number of bits in a chosen suffix.

hunt_shift_windows.py tests distance shells, a 106-bit suffix neighborhood and small TRAILING gaps. Each is a bounded anchor hypothesis, not an exhaustive private-key interval search.

$$
\mathcal{C}=\{(a+\delta)\mathbin{\oplus}e:\delta\in D,\ e\in E\}\cap I
$$

D gives declared shift shells and E gives eligible suffix flips. Completeness refers only to this finite neighborhood.

Search metadata-distance shells, suffix flips and literal TRAILING gaps around selected anchors.

Sources: [hunt_shift_windows.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/hunt_shift_windows.py)

## M133 — Synthesis transformation orbit engine

Apply a registry of deterministic mixing transformations repeatedly to produce candidate orbits, then rank the resulting integers.

The synthesis script's capture/decay/catalyst names denote ordinary bit/arithmetic operations. It generates and scores candidate scalars; the names do not represent physical or quantum processes.

$$
\mathcal{O}_T(a)=\{f_t\circ\cdots\circ f_1(a):t\leq T,\ f_i\in\mathcal{F}\}
$$

The transformation catalog F and depth limit T define an orbit search. Ranking states by novelty does not give a target-key likelihood without validation.

Hybrid orbit, capture/decay/catalyst/moderator transformations rank unused-byte novelty; terminology does not imply quantum physics.

Sources: [synthesis_puzzle71_solver.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/puzzles/synthesis_puzzle71_solver.py)

## M134 — Unused-byte novelty scoring

Count byte positions whose values have not appeared in the solved-key corpus, favoring combinations labeled novel.

The orbit batch verifier tests the actual scalar against the address. High novelty scores do not measure target agreement; some archived candidates were even below the valid puzzle interval.

$$
\nu(k)=\sum_{j=1}^{m}\mathbf{1}\{b_j(k)\notin U\}
$$

This representative novelty score counts bytes outside the declared used-byte set U. Its meaning is byte novelty, not agreement with a Bitcoin target.

Score 8/9 or 9/9 measures byte novelty, not target agreement. Archived 1,800-candidate verification had zero hits.

Sources: [orbit_candidates_report.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/orbit_candidates_report.md)

## M135 — Original HP-RTE weighted shard sampling

The original recipe samples a key, derives a byte/nibble label and uses its assigned weight to move the output into a biased subrange.

Historical code uses floating-point offsets, and successive versions exclude different parts of the interval. The repaired generator removes that unsupported exclusion and uses exact integer sampling.

$$
\Pr(k\in S^c)=0\quad\mathrm{when}\quad\mathrm{support}(P)=S\subsetneq I
$$

A generator whose support S is a proper subset of the advertised interval cannot reach excluded candidates. The old weighted/float construction required a support audit.

Historical float-based biased generator excludes part of the advertised interval; corrected pipeline uses full-support integer partitions.

Sources: [bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [README.md](/home/arialmohan/puzzle71-corrected/README.md)

## M136 — Two-byte rotation and four-hex-tree claims

Rotate a byte string to change which byte is inspected. A genuine four-hex tree would also define branching and traversal over four hex digits.

The supplied generator rotates by two bytes, not two hex characters. Its tree-depth name is not used to implement the claimed tree partitioning.

$$
\mathrm{rot}_{16}(x,r)=((x\ll r)\mathbin{\vert}(x\gg(16-r)))\mathbin{\&}(2^{16}-1)
$$

For a 16-bit word and 0<r<16, rotation permutes bits. A claimed hexadecimal tree additionally needs explicit depth and branching coverage.

Rotation exists, but original tree-depth configuration did not implement the claimed tree search.

Sources: [bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [README.md](/home/arialmohan/puzzle71-corrected/README.md)

## M137 — Million-record JSON/JSONL generation

Serialize one record per generated candidate or interval. JSONL allows records to be written one at a time.

The corrected run wrote a million descriptive records, then separately verified their sample keys and boundaries. File size and record count measure storage and generation, not exhaustive cryptographic coverage.

$$
N_{\mathrm{records}}\neq N_{\mathrm{verified\ scalars}}\quad\mathrm{in\ general}
$$

A record can contain boundaries and samples without checking them. Verification counts require actual scalar-to-point/hash comparisons.

Large record counts are data-generation work, not cryptographic search coverage; streaming JSONL avoids all-record memory use.

Sources: [run-1M.log](/home/arialmohan/puzzle71-corrected/run-1M.log); [README.md](/home/arialmohan/puzzle71-corrected/README.md)

## M138 — Weighted modular-diameter diversity

The old statistic computes pairwise numeric spread and multiplies it by a subset-dependent average bias weight.

The original uint64 conversion cannot hold 71-bit scalars; unsigned subtraction also wraps. Fixing integer overflow alone does not prove that the weighted expression satisfies diversity axioms.

$$
d_m(x,y)=\min(r,m-r),\quad r=(x-y)\;\mathrm{mod}\;m
$$

This defines circular modular distance using exact integer subtraction. Weighted subset-diameter claims require separate definitions and cannot rely on overflowing unsigned arithmetic.

uint64 overflow, unsigned differences and unproved subset weights invalidate original diversity claims.

Sources: [bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md)

## M139 — Finite-sample Cauchy/convergence claims

True Cauchyness and convergence require bounds over arbitrary sufficiently late terms of an infinite sequence, with the proposed limit included for convergence.

The old functions sample subsets of a finite whole history and compare an arbitrary threshold. They are finite clustering tests mislabeled as asymptotic guarantees and cannot locate an unknown private key.

$$
\forall\epsilon>0\ \exists N\ \forall p,q\geq N:\lvert x_p-x_q\rvert<\epsilon
$$

This is the Cauchy tail criterion. A finite history cannot certify this universal statement without an argument controlling every future term.

Sampling a finite history is not an asymptotic tail criterion; clustering cannot identify the unknown scalar.

Sources: [AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md); [README.md](/home/arialmohan/puzzle71-corrected/README.md)

## M140 — Exact ordinary diameter diagnostic

Diameter is the largest value minus the smallest. With fixed normalization it describes a finite sample's coordinate spread exactly.

The corrected script computes integer min/max without an all-pairs matrix. It labels the result descriptively and makes no claim of convergence toward the cryptographic target.

$$
\mathrm{diam}(S)=\max S-\min S
$$

For a nonempty finite set of ordinary integers, exact max-minus-min measures its spread. It says nothing about distance to an unknown scalar.

Integer max-minus-min measures sample spread without claiming convergence or cryptographic proximity.

Sources: [pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py); [test_pipeline.py](/home/arialmohan/puzzle71-corrected/test_pipeline.py)

## M141 — Cantor-like finite-stage constructions

Repeatedly remove a middle interval from each remaining closed interval, tracking exact rational endpoints and total surviving length.

The corrected example removes half at every stage; after eight stages length is 1/256. The infinite limit has zero measure, unlike the earlier claimed fat-Cantor interpretation.

$$
\mu(C_n)=\prod_{j=1}^{n}(1-\alpha_j)
$$

In a construction removing fraction alpha_j of every surviving interval at stage j, the remaining total length is this product. Constant half-removal gives 2^-n.

Exact rational construction corrects historical measure calculations; constant half-removal tends to zero measure.

Sources: [pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py); [README.md](/home/arialmohan/puzzle71-corrected/README.md)

## M142 — Cantor-to-keyspace homeomorphism claim

A homeomorphism must be a continuous bijection with a continuous inverse. An infinite Cantor set cannot be bijective with a finite integer keyspace.

The earlier function merely scales floating coordinates into sample min/max bounds and rounds to integers. It is a lossy candidate map, not the source paper's homeomorphism construction.

$$
q(x)=\mathrm{round}(Ax+B)\in\mathcal{K}_{\mathrm{finite}}
$$

Quantization from an infinite real set to a finite key set cannot be injective and hence cannot be a homeomorphism.

Rounding real samples to finite keys is not a homeomorphism from an infinite Cantor set.

Sources: [AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md); [README.md](/home/arialmohan/puzzle71-corrected/README.md)

## M143 — Byte-value arithmetic-progression avoidance

Search the set of distinct byte values for a nonconstant arithmetic progression such as 10,20,30. Every requested term must be present.

Corrected code extracts nine actual bytes, ignores order/multiplicity for this test, and records a Boolean label. It does not treat pattern avoidance as evidence that the key is more likely.

$$
a+c=2b,\quad a,b,c\ \mathrm{distinct}
$$

This detects a nonconstant three-term arithmetic progression among byte values. Reporting its presence does not justify rejecting the key.

Corrected diagnostic detects nonconstant APs among byte values; it is not used to discard search candidates.

Sources: [pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py); [test_pipeline.py](/home/arialmohan/puzzle71-corrected/test_pipeline.py)

## M144 — Monochromatic byte-position progression checks

Treat byte positions as the arithmetic progression and ask whether equally spaced positions carry the same byte value.

The corrected predicate differs deliberately from value-set APs. Repeated byte values can trigger a positional pattern even when the value set has no nonconstant arithmetic progression.

$$
b_i=b_{i+d}=b_{i+2d},\quad d>0
$$

Equal bytes at equally spaced positions form a monochromatic position progression. This is different from arithmetic progression in the byte values.

Equal bytes at equally spaced positions are distinguished from APs in the values themselves.

Sources: [pipeline.py](/home/arialmohan/puzzle71-corrected/pipeline.py)

## M145 — Double-AP and RamseyScript subset claims

Ramsey search recursively extends combinatorial objects while rejecting forbidden structures; a faithful interpreter must implement the specified objects and filter semantics.

The historical class lacks a real parser and uses an unrelated parity placeholder for double APs. Its general k-AP detector can accept an incomplete progression; later versions repair only some defects.

$$
i+k=2j,\quad x_i+x_k=2x_j,\quad i<j<k
$$

A double progression imposes both position and value relations. This states the mathematical pattern; placeholder code does not establish a complete implementation or useful filter.

Historical code uses placeholders and incomplete language semantics; original filter claims do not establish a cryptographic advantage.

Sources: [bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md)

## M146 — Pattern-label eligibility correction

Keep pattern classification as metadata while preserving eligibility of every integer in the advertised interval.

Educational and corrected pipelines do not discard a candidate for an AP label. Known-key tests separately measure label preferences and full-range eligibility, which must not be conflated.

$$
\mathrm{eligible}(k)=1,\quad\ell(k)=\mathrm{patternLabel}(k)
$$

Keep labels as diagnostics while retaining every candidate. Eligibility and pattern observations are distinct from a learned target predictor.

Backtests retain all candidates while reporting pattern labels; eligibility is not evidence that a pattern predicts keys.

Sources: [backtest.py](/home/arialmohan/puzzle71-educational/backtest.py); [BACKTEST.md](/home/arialmohan/puzzle71-educational/BACKTEST.md)

## M147 — Classical hyper-phase Q1-Q9 formulas

Evaluate trigonometric/exponential recurrence formulas indexed by state and bit position, then compare a magnitude with a chosen threshold.

These are classical numerical calculations. Earlier versions omit states; later formulas fill them but still neither ingest the target hash nor construct a quantum circuit or valid key-extraction equation.

$$
z_j=F_j(x;\theta),\quad j=1,\ldots,9
$$

F_j denotes each archived classical Q1-Q9 numerical formula. These toy transforms have no verified scalar-extraction equation or executed quantum circuit in the inventory.

Numerical toy formulas have no demonstrated target relation; no quantum circuit or recovery is implemented.

Sources: [bitcoin_puzzle_71_master_pipeline.py](/home/arialmohan/bitcoin_puzzle_71_master_pipeline.py); [AUDIT.md](/home/arialmohan/puzzle71-educational/AUDIT.md)

## M148 — Bit-position periodic table / CFSG labels

Organize bit indices into a table with powers of two, symbolic families and heuristic scores. Such a table can be an interface for diagnostics.

The supplied transcript assigns random simulated biases and CFSG-inspired labels. For bits below 71, reducing 2^b modulo the large group order changes nothing; no hidden algebraic advantage follows.

$$
\widehat p_j=\frac{1}{m}\sum_{i=1}^{m}b_{ij}
$$

Per-position empirical biases can organize a table of bit labels. Simulated biases and group-theory labels do not establish a target-specific probability model.

Supplied transcript uses simulated random biases and organizational labels; no local validated cryptanalytic result was established.

Sources: [README.md](/home/arialmohan/puzzle71-corrected/README.md)

## M149 — BPK-TSP and million-process architecture

A scheduler could distribute generation, verification and artifact collection across workers, with hardware-specific executors.

BPK-TSP, million-process and FPGA claims are architectural narrative in the supplied material. Concrete implementations elsewhere are documented separately; this entry has no corroborated complete large-scale execution.

$$
T_{\mathrm{ideal}}\geq\frac{N_{\mathrm{work}}}{p\,v}
$$

With p workers and per-worker rate v, this idealized lower bound ignores coordination and hardware limits. Process-count proposals require measured throughput and coverage.

Scheduling and FPGA/massive-process claims in supplied reports are proposals without corroborated execution evidence in this inventory.

Sources: [README.md](/home/arialmohan/puzzle71-corrected/README.md)

## M150 — Aranyn Block-1 manual-nonce binding

ECDSA gives s*w=z+r*d modulo the group order when the signing nonce is chosen as the Block-1 scalar w.

The code verifies the signature and derives w=A+B*d. Substituting that relation back into the same signature adds no independent equation; one unknown scalar remains behind public-point multiplication.

$$
s\nu\equiv z+rd\pmod n
$$

A single ECDSA signature relates signing key d and nonce nu, with message scalar z and signature r,s. Renaming the two unknowns does not determine them.

One signature gives an affine relation between two scalar names but leaves an ECDLP-equivalent unknown.

Sources: [crypto_non_bruteforce_methods.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/crypto_non_bruteforce_methods.md)

## M151 — Puzzle-160 nonce/signing-key relation

If an ECDSA nonce is the Puzzle-160 key, knowledge of either that nonce or the signer scalar determines the other algebraically.

user_signature.py supplies the forward/reverse formulas and known public-point checks. Neither published relation alone reveals an undisclosed nonce; solving for it still requires new information or ECDLP work.

$$
d\equiv r^{-1}(s\nu-z)\pmod n
$$

One known nonce yields the signing scalar d when r is invertible. Without that extra input, the signature relation still has an unknown nonce.

Recover one scalar if the other is supplied; the published relation does not independently reveal either unknown key.

Sources: [user_signature.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/user_signature.py)

## M152 — Cross-signature #160 / Block-1 linear relations

Combine the two affine signature relations and test small coefficients directly on their public points.

The relation search sweeps specified alpha/beta/gamma families and verifies candidate equations. This can detect a genuine small relation without knowing either scalar, but cannot assume one exists.

$$
R_2\stackrel{?}{=}aR_1+bG
$$

R1 and R2 here are nonce points, not CTheory roots. A bounded public-point relation would constrain nonces; it must be found and verified rather than assumed.

Search bounded small coefficients visible on public points; any result would need independent target verification.

Sources: [search_160_block1_relation.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/search_160_block1_relation.py); [relation_160_block1.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/relation_160_block1.md)

## M153 — ECDSA nonce-reuse recovery

Reusing the same nonce for different messages creates two equations with the same unknown nonce, allowing elimination and scalar recovery.

Synthetic sign/recover tests validate the algebra. Real harvested data are grouped by signer and r; the archived samples did not provide the required exploitable reuse pair.

$$
\nu\equiv(z_1-z_2)(s_1-s_2)^{-1}\pmod n
$$

$$
d\equiv(s_1\nu-z_1)r^{-1}\pmod n
$$

These equations assume the same signing key, the same nonce, nonzero denominators and compatible signature signs. Repeated r alone also requires considering opposite nonce signs.

Algebraic recovery works in planted examples; harvested real signatures showed no matching reuse groups in recorded samples.

Sources: [ecdsa_affine_nonce.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/ecdsa_affine_nonce.py); [counter_nonce_analysis.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/counter_nonce_analysis.md)

## M154 — Known affine-related nonce recovery

A known relation k2=a*k1+b between two ECDSA nonces supplies an extra equation that makes the signer scalar solvable.

ecdsa_affine_nonce.py creates controlled affine signature pairs and recovers the planted key. The puzzle target does not gain that relation merely because the implementation works on planted examples.

$$
d\equiv\frac{s_1z_2-a s_2z_1-b s_1s_2}{a s_2r_1-s_1r_2}\pmod n
$$

Assume nonce relation nu2=a nu1+b and the same signing key; division means modular inversion of a nonzero denominator. The affine relation is required input.

Synthetic signature pairs validate the formula when the nonce relation is actually known. Applicability requires such a pair.

Sources: [ecdsa_affine_nonce.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/ecdsa_affine_nonce.py); [backtest_arxiv_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/ctheory/backtest_arxiv_methods.py)

## M155 — Counter nonces and small offset relation tests

Guess tiny nonce values or small differences between two nonce values, then use ECDSA equations to derive a signer candidate.

Recorded scans test declared nonce and offset ranges against harvested signatures and verify candidates. A null result covers those guesses, not arbitrary unknown nonce relations.

$$
\nu_2=\nu_1+\delta\pmod n,\quad\delta\in D
$$

Test a bounded offset set D under the ECDSA equations. Without an applicable signature pair, an offset hypothesis supplies no recovered key.

Archived harvested-signature scans tested tiny nonces and bounded offsets; no verified wallet-key recovery reported.

Sources: [counter_nonce_analysis.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/counter_nonce_analysis.md)

## M156 — Hidden-number/partial-MSB nonce leakage models

Multiple signatures with known nonce bits create inequalities that can support Hidden Number Problem/lattice recovery or smaller interval searches.

The registry models synthetic MSB leaks and required bit budgets. The available target data do not include the corresponding independent bit leaks or adequate applicable signatures.

$$
s_i\nu_i\equiv z_i+r_id\pmod n,\quad\lvert\nu_i-\widetilde\nu_i\rvert<B_i
$$

A partial-nonce hidden-number model combines signatures with genuine nonce estimates and error bounds. Signatures alone do not supply those leakage bounds.

Synthetic bounds and applicability checks exist; the target signatures do not supply the required leakage measurements.

Sources: [joc_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/joc_methods.py); [crypto_non_bruteforce_methods.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/crypto_non_bruteforce_methods.md)

## M157 — Polynonce/half-half/side-channel possibilities

Polynomial nonce recurrences, concatenated half-nonces or measured side-channel leakage provide special extra structure beyond ordinary ECDSA.

The literature mapping checks whether those prerequisites exist. This is an applicability review; it does not execute a successful lattice/side-channel attack on a single ordinary signature.

$$
\nu_{i+1}=f(\nu_i)\pmod n
$$

This represents a conditional structured-nonce family, such as a low-degree polynomial recurrence. Half-half and side-channel attacks have different required structure or measurements.

Reviewed as conditional attacks; missing signatures, special nonce structure or measurements block their use on the cited target.

Sources: [crypto_non_bruteforce_methods.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/crypto_non_bruteforce_methods.md)

## M158 — ECDSA versus Schnorr/BIP340 checks

Schnorr and ECDSA use different equations and message challenges. A signature must satisfy the correct scheme's verification relation.

The comparison derives Schnorr/BIP340 challenges and tests forced interpretations of the ECDSA constants. Reinterpreting bytes under another scheme does not provide a second valid signature equation.

$$
sG=R+eP\quad\mathrm{versus}\quad s\nu\equiv z+rd\pmod n
$$

The first is Schnorr verification with scheme-defined challenge e and point parity rules; the second is ECDSA. Reinterpreting bytes does not create another independent signature.

Forced reinterpretations and challenge consistency are compared; changing signature labels does not create a new independent equation.

Sources: [schnorr_ecdsa_aranyn_compare.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/schnorr_ecdsa_aranyn_compare.py); [schnorr_ecdsa_aranyn_compare.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/schnorr_ecdsa_aranyn_compare.md)

## M159 — Early coinbase signature harvesting

Extract signature data from spent early coinbase outputs and identify the signer/public point needed for nonce analysis.

Harvesters follow actual spends, parse signatures and group them for reuse/target-r tests. The saved 51-signature sample provides data, not previously unknown recovered wallet keys.

$$
\Sigma=\{(P_i,z_i,r_i,s_i,\mathrm{source}_i)\}_{i=1}^{m}
$$

Harvest signatures together with their exact signing public key and sighash context. A collected tuple is input to later tests, not a recovery result.

Saved report records 51 signatures and no nonce-reuse recovery; the graph is a data source, not a solve.

Sources: [early_coinbase_sig_harvest.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/early_coinbase_sig_harvest.md)

## M160 — Descendant/graph signature expansion

Follow descendants and consolidation transactions to collect more signatures associated with the original outputs.

Graph/descendant tools expand a bounded transaction frontier. Additional transaction relationships can increase the sample but do not prove that every downstream signer shares a private scalar.

$$
V_{t+1}=V_t\cup\{v:(u,v)\in E,\ u\in V_t\}
$$

Expand a transaction/UTXO graph from declared seeds, then extract usable signatures from reached spends. Define traversal depth and deduplicate transactions.

Expand UTXO descendants and consolidation transactions to obtain additional signature samples.

Sources: [harvest_early_coinbase_descendants.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/harvest/harvest_early_coinbase_descendants.py); [harvest_early_coinbase_graph.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/harvest/harvest_early_coinbase_graph.py)

## M161 — BTCparser sleeping/whale sweep signatures

Use sleeping-address or whale-sweep indexes to select transactions likely to contain useful signature collections.

The BTCparser sweep parses indexed blocks and selected spend transactions, then tests collected r values. It is a bounded data-gathering strategy, not evidence of biased nonces.

$$
\mathcal{G}_{P,r}=\{\sigma_i:P_i=P,\ r_i=r\}
$$

Group harvested signatures by signing key and nonce x-coordinate indicator r. Any proposed reuse group needs exact sighash and sign-aware verification.

Saved sweep harvested 151 signatures with no reuse groups or target-r hits in that sample.

Sources: [btcparser_sweep_signature_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/btcparser_sweep_signature_scan.md)

## M162 — Lattice-candidate sufficiency scan

Count usable signatures per signer before attempting attacks that require repeated nonce information or leakage.

The lattice-candidate report groups 184 signatures into wallets and finds none meeting its multi-signature threshold. No target lattice recovery is performed simply by detecting that data are insufficient.

$$
m_P=\#\{i:P_i=P\},\quad m_P\geq m_{\mathrm{required}}
$$

Count usable signatures per signer under a specified leakage model. Passing a count threshold is necessary for that model, not sufficient for lattice recovery.

Saved report has 184 signatures but no wallet with the required multi-signature count; no lattice recovery executed.

Sources: [lattice_candidate_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/lattice_candidate_scan.md)

## M163 — SegWit/testnet target-r scans

Search additional witness and testnet signature data for the same nonce x-coordinate or related target public material.

Dedicated scans compare parsed r values in their fetched samples. Matching a signature field would need scheme and signer verification; absence in a sample is not a global chain proof.

$$
r_i\stackrel{?}{=}r_*
$$

Search the declared chain/witness signature corpus for the target signature component. A match requires further signer and nonce-relation checks.

Search archived alternate-chain and witness signatures for the manual-nonce x-coordinate; finite scan scope only.

Sources: [segwit_aranyn_r_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/segwit_aranyn_r_scan.md); [testnet_aranyn_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/testnet_aranyn_scan.md)

## M164 — Signed-message and fork public-key leaks

Extra signed messages or fork spends may reveal a public point or an independently usable signature absent from the current target record.

Search scripts look for that public material. They do not obtain private keys from a public-point leak alone; they may only enable a different, still expensive recovery method.

$$
\mathrm{Verify}_{\mathrm{scheme}}(P,m,\sigma)=1
$$

Signed messages and fork records supply useful evidence only when parsed under the correct message digest, scheme and public key.

Search additional public signature/pubkey material; utility depends on finding independently applicable data.

Sources: [search_signed_bitcoin_messages.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/scans/search_signed_bitcoin_messages.py); [scan_fork_pubkey_leaks.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/scans/scan_fork_pubkey_leaks.py)

## M165 — DP metadata distances and signed collision variants

Interpret candidate metadata slices as walk distances and test whether they satisfy the claimed tame/wild public-point equations.

Archived scans vary bit widths, signs, starts and collision formulas. A distance-looking field is rejected unless its derived point or scalar matches the target.

$$
k\equiv\epsilon t-w\pmod n,\quad\epsilon\in\{-1,1\}
$$

At a same-x tame/wild record, epsilon accounts for point parity in tG=epsilon(Q+wG). Test declared distance layouts and verify each resulting scalar.

Archived metadata-width, start-point, sign and collision-formula tests found no verified puzzle scalar.

Sources: [non_bruteforce_audit_20260831.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/non_bruteforce_audit_20260831.md)

## M166 — DP x-coordinates as candidate public keys

A valid x-coordinate has up to two curve-point lifts, each yielding a possible compressed public key and address hash.

The binary audit checks both parities against puzzle targets. This tests whether the dump literally contains the target public key, not whether arbitrary points can be inverted into scalars.

$$
y^2\equiv x^3+7\pmod p
$$

A valid secp256k1 x-coordinate has candidate point parities y and -y. Serialize each valid point and compare its address hash; an arbitrary x need not lift.

Both point parities were checked against puzzle addresses; no match in the recorded binary sample.

Sources: [non_bruteforce_audit_20260831.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/non_bruteforce_audit_20260831.md)

## M167 — TRAILING / LOW71 / bit-slice anchors

Slice or reinterpret a trailing metadata integer to produce anchor scalars for selected puzzle widths.

LOW71, low/high pieces and literal TRAILING values are checked as concrete candidates. Their bit length or range membership alone is not evidence of target identity.

$$
a_b=2^{b-1}+(M\;\mathrm{mod}\;2^{b-1})
$$

A metadata word M can be masked into a b-bit puzzle interval. Being in range establishes no relation to the target hash.

Numerical range coincidence is separate from address correctness; recorded anchor checks failed target verification.

Sources: [any_relation_report.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/any_relation_report.md); [non_bruteforce_audit_20260831.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/non_bruteforce_audit_20260831.md)

## M168 — Leading-zero public-key collection analysis

Analyze a collection selected for leading-zero x-coordinate masks, then search membership, pairwise offsets and small public-point relations.

The script compares known corpora, GLV transforms, linear combinations, bounded BSGS differences and generator recipes. Mask rarity must be evaluated conditional on the deliberate point-selection rule.

$$
P_j\stackrel{?}{=}P_i+\delta G,\quad\delta\in D
$$

Bounded-offset and other point-relation tests need declared search sets. A collection selected for leading zero bits is not evidence of scalar proximity.

Tests mask statistics, membership, pairwise differences, GLV relations, linear combinations and bounded BSGS offsets.

Sources: [analyze_leading_zero_pubs.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/analyze_leading_zero_pubs.py)

## M169 — Cross-artifact relation bundles

Bundle source hashes, parsed values and named relationships so later investigations can trace every clue to its artifact.

relation_bundle.py packages DP/TRAILING/CTheory hypotheses and metadata. It preserves evidence lineage without claiming that colocated numbers imply a key equation.

$$
\mathcal{E}=\mathcal{E}_{\mathrm{DP}}\cup\mathcal{E}_{\mathrm{metadata}}\cup\mathcal{E}_{\mathrm{CT}}
$$

Bundle artifacts with their provenance and dependencies. Combining correlated evidence does not make it independent scalar information.

Package DP, metadata and CTheory evidence without claiming that correlated artifacts reveal a key.

Sources: [relation_bundle.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/relation_bundle.py)

## M170 — Genesis/early-coinbase relationship graph

Build a graph linking early blocks, output public keys, spends and known puzzle entities.

The relationship mapper collects public points and transaction edges. A shared transaction or funder is a graph link; recovering a shared scalar requires separate cryptographic evidence.

$$
\mathcal{G}=(V,E),\quad E\subseteq V\times V
$$

Nodes represent declared blocks, transactions or public-key objects; edges encode observed relationships. A graph edge does not imply equal private scalars.

Map published public points and spending relationships; shared transactions need not imply shared private keys.

Sources: [chain_relationship_map.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/chain_relationship_map.md)

## M171 — Puzzle-135 sweep/fanout tracing

Follow the known Puzzle-135 spending destination forward and backward to identify related addresses or messages.

The fanout script tags puzzle neighbors and summarizes transaction flows. It tracks an observed sweep; it does not establish that this local code discovered the spent key.

$$
\mathrm{Reach}_d(v)=\{u:\mathrm{dist}_{\mathcal{G}}(v,u)\leq d\}
$$

Follow bounded sweep/fanout relationships in the dated chain snapshot. Observed fund movement is distinct from a locally verified key-discovery event.

Follow sweep destinations, funding and tagged puzzle neighbors; movement of funds is not local proof of solving the puzzle.

Sources: [fanout_puzzle135.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/fanout_puzzle135.md)

## M172 — 0.99-BTC fanout cluster tracing

Detect transactions with repeated 0.99-BTC outputs and traverse their funding/fanout neighbors.

The crawler uses explicit output-count/value thresholds and bounded BFS expansion. This identifies a transaction pattern or cluster, not an algebraic relation among its private keys.

$$
E_{0.99}=\{(u,v)\in E:\mathrm{value}(u,v)=0.99\ \mathrm{BTC}\}
$$

This is an example value-conditioned graph filter. State the actual amount tolerance and traversal bounds used by the archived cluster scan.

Breadth-first funding/output graph searches and message scans are archived.

Sources: [follow_099_fanouts.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/follow_099_fanouts.md); [fanout_cc6f_trace.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/fanout_cc6f_trace.md)

## M173 — Sender relay / OP_RETURN / extra-data clues

Decode message-bearing transaction fields and follow a relay chain for possible puzzle instructions or artifacts.

Sender tools parse OP_RETURN, inspect extra data and search references. Public text is treated as a lead requiring verification, not executable instructions or proven secret leakage.

$$
\mathcal{M}=\{\mathrm{decode}(x):x\in\mathrm{payloads}(\mathcal{T})\}
$$

Decode declared transaction fields, including OP_RETURN payloads, and inspect for concrete candidate material. Decoded text alone is not a scalar relation.

Decode message relays and scan transaction fields for key fragments or target relations.

Sources: [trace_sender_extended.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/trace_sender_extended.md); [trace_sender_extra_data_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/trace_sender_extra_data_scan.md)

## M174 — Early spent-block number encodings

Convert lists of spent block numbers or transaction fields into candidate encodings and compare with known puzzle clues.

The analyzer tests stated integer/string representations and inspects spends. Finding readable text or a similar hex fragment is exploratory evidence, not a verified key.

$$
\mathcal{C}=\{\mathrm{Encode}_f(h):h\in\mathcal{H},\ f\in\mathcal{F}\}
$$

Test a bounded collection of block-height encodings and transformations. Exact candidate verification controls coincidences in hexadecimal representations.

Test block-index encodings and inspect spends for puzzle-like hexadecimal data.

Sources: [analyze_spent_block_encoding.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/analysis/analyze_spent_block_encoding.py)

## M175 — Hub-address and recoverability scans

Query selected addresses and outputs to find spends, public keys, old funds or other data relevant to recoverability hypotheses.

Saved scans summarize activity and candidate opportunities. They do not freshly establish present balances, authority over wallets or a successful cryptographic recovery.

$$
V(A)=\sum_{u\in\mathrm{UTXO}(A)}\mathrm{value}(u)
$$

This defines snapshot balance for address A. Activity or hub status can guide evidence collection but does not show possession or recoverability of its private key.

Address/UTXO activity scans identify data leads; no present ownership or balance conclusions are newly verified here.

Sources: [hub_3EEJF_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/hub_3EEJF_scan.md); [recoverable_bitcoin_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/recoverable_bitcoin_scan.md)

## M176 — Puzzle reflection and unlock relationship scans

Look for reflected labels, addresses or tier relationships suggesting that one puzzle might encode information useful for another.

Reports enumerate tested correspondences and unlocking ideas. A relation between labels is distinct from a demonstrated scalar transformation that reproduces both targets.

$$
\widehat Q_j=aQ_i+bG
$$

Reflection/unlock proposals need a specified mapping, such as this affine point hypothesis, and held-out exact checks. No universal relation is assumed.

Compare puzzle labels, addresses and transaction relationships; no validated universal unlocking rule established.

Sources: [puzzle_reflection_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/puzzle_reflection_scan.md); [puzzle_unlock_relationships.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/puzzle_unlock_relationships.md)

## M177 — Historical website/archive and directory searches

Search historical sites and directory/archive listings for original challenge files, creator software or missing public parameters.

Triage scripts save candidate links and matches. The inventory records those searches without treating every archived webpage as authenticated creator provenance or a successful lead.

$$
\mathcal{A}=\bigcup_{q\in\mathcal{Q}}\mathrm{Results}(q)
$$

A finite query catalog collects candidate public artifacts for source triage. Search-index coverage and relevance require separate assessment.

Old Bitcoin sites, indexes and Drive leads were triaged for relevant artifacts.

Sources: [old_bitcoin_sites_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/old_bitcoin_sites_scan.md); [index_of_directories_scan.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/index_of_directories_scan.md); [google_drive_puzz_triage.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/google_drive_puzz_triage.md)

## M178 — Time-Will-Tell phrase/path hypotheses

Try bounded interpretations of an explicitly supplied recovery phrase, including word-subset and passphrase/path choices.

The branch implementation checks selected mnemonic and HD-wallet variants against named targets. Private phrases are omitted from the report, and unrun full search coverage is not inferred.

$$
k_p=\mathrm{Derive}(\mathrm{Mnemonic},\mathrm{Passphrase},p)
$$

The phrase hypothesis is a bounded derivation-path experiment. Sensitive phrase material stays outside the report; successful derivation still requires an exact target match.

Bounded mnemonic subset, passphrase and derivation-path tests are documented; private phrases are excluded from this report.

Sources: [crack_time_will_tell_seed.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/chain/crack_time_will_tell_seed.py); [Branch-cursor-time-will-tell-seed-b049.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Branch-cursor-time-will-tell-seed-b049.md)

## M179 — Complete chat-lead indexing and candidate extraction

Index complete available user/assistant messages, distinguish speakers and extract only relevant candidate claims or supplied leads.

Existing audit scripts preserve source hashes, locators and redacted witnesses. Chat assertions can guide tests, but a model's claim of running code is not substituted for execution artifacts.

$$
\mathcal{L}=\{(\mathrm{speaker},\mathrm{source},\mathrm{candidate})\}
$$

Index extracted leads with speaker and source provenance. A statement in an assistant message is not itself a completed computation.

Existing speaker-aware source index covers 685 matching conversations; assistant assertions are not execution evidence.

Sources: [REPORT.md](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/REPORT.md); [scan_chats.py](/home/arialmohan/workspace/projects/conversation-atlas/research/bitcoin-puzzle-2026-10-02/scan_chats.py)

## M180 — Milk Sad raw MT19937 seed expansion

Reproduce the exact weak MT19937 entropy stream produced from a 32-bit libbitcoin seed, then derive the corresponding scalar/public point.

Native and CUDA implementations mirror the modeled software path. The saved raw-entropy sweep compares supported address hashes with a dated funded index, rather than attacking arbitrary secure seeds.

$$
e=\mathrm{MT19937}(s)_{0:256},\quad s\in\{0,\ldots,2^{32}-1\}
$$

The precise libbitcoin output extraction/order defines the 256 entropy bits e. A full-length output retains at most the enumerable seed uncertainty.

Archived report claims full 32-bit seed sweep with zero funded-index hits; this inventory does not rerun or independently certify that sweep.

Sources: [milksad_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/milksad_cuda_sweep.md); [weak_entropy_prng.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_prng.py)

## M181 — Milk Sad BIP39/BIP44/49/84 derivations

Turn the weak entropy into a BIP39 mnemonic seed, derive specified HD paths and compare supported address types.

The archived sweep covers declared BIP44/49/84 account paths and serializations. PBKDF2 and child derivation make this substantially different from checking the raw entropy as a scalar.

$$
\mathrm{seed}=\mathrm{PBKDF2}_{\mathrm{HMAC\!\!\!-SHA512}}(m,\mathrm{salt},2048)
$$

BIP39 mnemonic m comes from the modeled weak entropy; the salt includes the declared passphrase. Then derive the specified BIP44/49/84 paths and address encodings.

Archived mnemonic and derivation-path sweep reports zero funded-index hits; bounded historical index and path coverage only.

Sources: [milksad_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/milksad_cuda_sweep.md); [weak_entropy_wallet.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_wallet.py)

## M182 — Profanity MT19937-64 base-key replay

Replay Profanity's small seed expansion to reconstruct its base scalar under a specified output word order.

Saved CUDA results enumerate base seeds in both orders and check three hash variants. Offset-zero coverage does not automatically cover keys reached by later vanity-search increments.

$$
k_0=\mathrm{Pack}(\mathrm{MT19937\!\!-64}(s),\mathrm{wordOrder})
$$

Reproduce Profanity's exact base-key expansion for each candidate seed and output order. This equation concerns offset zero.

Archived report enumerates both word orders over 32-bit seeds with zero funded-index hits at offset zero.

Sources: [profanity_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/profanity_cuda_sweep.md)

## M183 — Profanity incremental offset grinding

Starting from a reconstructed weak base key, add small scalar offsets and reuse point additions to check nearby vanity-search states efficiently.

The branch adds offset-window flags and remote sharding scripts. Its documentation explicitly separates Python-side tests from real-GPU compile/verification that was still outstanding there.

$$
k_t=k_0+t\pmod n,\quad Q_{t+1}=Q_t+G
$$

Search declared incremental vanity offsets from each modeled weak base. Covered offsets and seed intervals must both be reported.

Extends base keys with small scalar offsets. Branch notes explicitly say real-GPU compile/verification was not yet done there.

Sources: [Branch-cursor-profanity-offset-grind-8a23.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Branch-cursor-profanity-offset-grind-8a23.md)

## M184 — Java util.Random replay

Java Random updates a 48-bit linear-congruential state; nextBytes exposes a particular sequence of output bytes.

The model reproduces those bytes from a candidate explicit seed. Timestamp-window enumeration tests only programs that really seeded and consumed that generator in the modeled way.

$$
x_{t+1}=(25214903917x_t+11)\;\mathrm{mod}\;2^{48}
$$

Java util.Random's state transition is deterministic; reproduce seed scrambling, output-bit extraction and nextBytes order to model a key.

Models the 48-bit LCG and timestamp-seeded nextBytes path; registered runtime vectors distinguish model fidelity from a recovery.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M185 — Java SUN SHA1PRNG low-entropy seed replay

SUN SHA1PRNG with an explicit low-entropy seed evolves deterministic SHA-1-derived state and emits predictable bytes.

The implementation reproduces setSeed byte order and signed state updates. It does not assume every SecureRandom call is weak; normal unobserved platform entropy changes the problem.

$$
(S_{t+1},o_t)=\mathrm{SUN\!\!-SHA1PRNG}(S_t)
$$

This denotes the implementation-specific signed state update and emitted bytes after explicit seed initialization. It is not a generic claim that all SHA-1 PRNG seeding is enumerable.

Deterministic setSeed model is present; not every Java/Android wallet follows that path.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M186 — glibc rand/random byte-fill replay

glibc rand/random uses additive-feedback state; truncating its outputs to bytes can make keys reproducible from a small seed.

The family model initializes and warms the state, then emits low bytes under the catalog's byte-fill recipe. Generator fidelity is tested separately from applicability to a target wallet.

$$
x_t=x_{t-31}+x_{t-3}\pmod{2^{32}},\quad o_t=x_t\gg1
$$

This describes the modeled default glibc additive-feedback stream after its prescribed initialization/warm-up; the key byte-fill rule must also match.

Models clock-seeded additive-feedback output truncated into key bytes.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M187 — Lehmer minstd_rand0 replay

minstd_rand0 multiplies state by 16807 modulo 2^31-1. An enumerable state determines the byte stream.

The registry wraps this Lehmer generator into candidate key bytes and runtime vectors. The attack premise is misuse for wallet entropy, not a weakness of secp256k1 itself.

$$
x_{t+1}=16807x_t\pmod{2^{31}-1}
$$

minstd_rand0 is a Lehmer generator. Specify seed normalization and byte extraction in addition to the recurrence.

Models multiplier 16807 weak-generator key bytes.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M188 — Lehmer minstd_rand replay

minstd_rand uses multiplier 48271 with the same prime modulus, producing a different deterministic stream.

The model keeps this family separate because seed replay with the wrong multiplier produces different keys. A sweep must identify the exact generator and byte extraction recipe it covers.

$$
x_{t+1}=48271x_t\pmod{2^{31}-1}
$$

minstd_rand uses a different multiplier from minstd_rand0. Their key streams are not interchangeable even with the same nominal seed.

Models multiplier 48271 key-byte generation, separately from minstd_rand0.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M189 — AVR/Arduino rand replay

Embedded sketches may derive key bytes from a deterministic rand stream seeded by millis or limited sensor readings.

The AVR/Arduino model implements the stated Lehmer-style stream under candidate seeds. It does not model unknown hardware noise measurements or every embedded random library.

$$
k=\mathrm{ByteFill}(\mathrm{PRNG}_{\mathrm{AVR}}(s))
$$

The embedded model depends on the exact library, seed range and rand-to-byte recipe. A timer or sensor hypothesis must specify those inputs.

Models weak embedded Lehmer-style output under enumerable seeds.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M190 — Modern PHP MT19937 byte-fill replay

Modern PHP mt_rand uses MT19937 and particular range-output rules. Repeated byte requests determine a key from its seed.

The implementation emits bytes under modern mode and compares with runtime vectors. A generic MT19937 sequence with different range scaling is not the same candidate family.

$$
k_j=\mathrm{PHP\!\!-range}(\mathrm{MT}_{\mathrm{modern}}(s),0,255)_j
$$

Each byte request consumes state according to the modern PHP range-sampling behavior. Generic MT words without that rule define a different family.

PHP 7.1+ generator/range semantics are modeled separately from legacy PHP.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M191 — Legacy PHP broken-twist replay

Older PHP used a different twist/range behavior, so a small seed produces a distinct key stream from modern PHP.

A separate legacy mode reproduces that behavior. Historical weakness labels alone are insufficient without matching the actual PHP version and key-generation recipe.

$$
k_j=\mathrm{PHP\!\!-range}(\mathrm{MT}_{\mathrm{legacy}}(s),0,255)_j
$$

The historical broken-twist mode and its range scaling need version-matched replay. Seed enumeration covers only that specified mode.

Models the older mt_rand twist and range-scaling behavior, not covered by ordinary MT19937 assumptions.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M192 — PHPCoinAddress legacy and modern keygen

PHPCoinAddress applies its own bounded byte calls, including a special first-byte range, around PHP's generator.

Dedicated wrappers reproduce those calls for both old and modern modes. Replaying plain mt_rand bytes would omit this wallet-specific transformation and could miss its generated keys.

$$
k_0\in A_{\mathrm{first}},\quad k_j=\mathrm{WalletByteCall}(s,j)
$$

PHPCoinAddress has wallet-specific first-byte bounds and subsequent calls. Reproduce those calls using the declared legacy or modern PHP mode.

Dedicated first-byte/range rules are modeled under both PHP generator modes.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M193 — V8 MWC1616 / Randstorm-era byte fill

Old V8 Math.random combines multiply-with-carry state; weakly seeded outputs can be reproduced and packed into key bytes.

The registry supplies the historical MWC1616 byte-fill model. A full Randstorm wallet route may include additional entropy mixing and consumption order not implied by that one modeled stream.

$$
x'=18030(x\mathbin{\&}65535)+(x\gg16)
$$

$$
y'=30903(y\mathbin{\&}65535)+(y\gg16)
$$

These are the historical V8 MWC1616 state updates with unsigned word arithmetic. The output packing, seeding and wallet entropy mixing must also be modeled.

Historical JavaScript Math.random byte generation model; a vulnerable-family model is not attribution to a target wallet.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M194 — V8 xorshift128 state recovery

Observed floating Math.random outputs expose some generator bits. Constraint solving can recover compatible xorshift state under the modeled engine order.

The source contains forward generation and state-recovery helpers. It requires actual usable observations; no such target observations are created by merely knowing a Bitcoin address.

$$
\mathcal{S}=\{s:\mathrm{Obs}(F^t(s))=y_t\ \mathrm{for\ all}\ t\}
$$

Recover compatible xorshift states from actual observed floating outputs y_t under the engine's output order. Without observations, the constraints are absent.

Recovers generator state from observed Math.random outputs under the modeled engine semantics; no target observations established here.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M195 — .NET System.Random replay

Explicitly seeded .NET System.Random evolves subtractive state; low-entropy TickCount-style seeds allow replay.

The model reproduces the framework-compatible byte stream and supports runtime vectors. Newer runtime semantics or additional entropy require a different model.

$$
(S_{t+1},o_t)=\mathrm{DotNetRandom}_{\mathrm{version}}(S_t)
$$

The historical subtractive-state algorithm and explicit seed determine the byte stream. State size, byte mapping and runtime version are part of the model.

Models explicitly seeded subtractive generator and TickCount-style seed scope.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M196 — Timestamp/UUID hash-derived keys

Hashing a predictable timestamp or weak UUID produces a full-length string but retains the small input uncertainty.

The catalog hashes selected second/millisecond and weak-UUID encodings into candidate keys. It searches their input choices, not the full 256-bit digest space.

$$
k=\mathrm{Int}(H(\mathrm{enc}(t,\mathrm{UUID})))
$$

Enumerate the declared low-entropy timestamp/UUID input choices. Hash output width does not enlarge the uncertainty in those inputs.

SHA-256 clock, millisecond and weak-UUID key recipes are modeled as bounded generator hypotheses.

Sources: [weak_entropy_families.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/weak_entropy_families.py)

## M197 — Early-2009 clock-window seed replay

Guess creation-time values, feed them into named weak generators/encodings and compare with early coinbase public keys.

The widest saved clock-window run checks its finite 2008-2009 range and reports no matches. Actual OpenSSL machine-state seeding is not reproduced by these timestamp hypotheses.

$$
\mathcal{C}=\{F_g(t):t\in[t_0,t_1],\ g\in\mathcal{G}\}
$$

A clock-window sweep combines a finite time range with named generator/encoding recipes G. It does not model arbitrary operating-system entropy.

Widest saved report records 250,581,618 tested keys and no early-coinbase target recovery; true machine-state entropy is not enumerated.

Sources: [block1_keygen_seed_sweep_2008.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/block1_keygen_seed_sweep_2008.md)

## M198 — Weak-entropy multi-family CUDA sweep

Parallel GPU threads map seeds through PRNG, curve multiplication and hash comparison against a supported address index.

Archived multi-family runs report seed counts and planted-index detection checks. Their coverage is bounded by the selected generator families, seed intervals and supported address encodings.

$$
\mathcal{C}=\bigcup_{g\in\mathcal{G}}\{F_g(s):s\in S_g\}
$$

GPU enumeration covers selected generator families and seed sets. Deduplicate candidates when reporting distinct scalar coverage.

Saved report claims 27.5 billion seeds and zero funded-index hits, with planted-index detection tests. Historical record, not rerun here.

Sources: [weak_entropy_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/weak_entropy_cuda_sweep.md)

## M199 — Bloom plus sorted funded-address index

A Bloom filter rapidly rejects most nonmembers; positive candidates then undergo exact lookup in a sorted hash160 index.

build_loyce_index.py constructs the index and GPU code performs membership checks. Bloom positives alone are not hits; the source index's date and skipped address types limit conclusions.

$$
\mathrm{hit}(h)=\mathrm{Bloom}(h)\land\mathrm{ExactLookup}(h)
$$

Every Bloom positive needs exact confirmation. With a independent hash functions, N indexed entries and m filter bits, the ideal false-positive rate is approximately (1-exp(-aN/m))^a.

Probabilistic prefilter backed by exact lookup; index date and supported address types bound conclusions.

Sources: [build_loyce_index.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/build_loyce_index.py); [weak_entropy_cuda_sweep.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/weak_entropy_cuda_sweep.md)

## M200 — Weak-RNG repository-source triage

Search wallet source for weak RNG calls and correlate findings with known disclosures and affected versions.

Curated repository scans record references and matching lines. A weak RNG in tests, an old dependency or a non-keygen path is not automatic evidence that current wallet keys are vulnerable.

$$
\mathcal{F}=\{(\mathrm{repo},\mathrm{version},\mathrm{callsite},\mathrm{dataflow})\}
$$

A source finding matters when weak outputs flow into production key entropy. A text match alone does not establish that dataflow.

Pattern hits and disclosures locate candidate implementations; historical/current refs and dependency bugs must be distinguished.

Sources: [weak_entropy_repos.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/weak_entropy_repos.md); [weak_entropy_unverified.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/weak_entropy_unverified.md)

## M201 — Recoverable-hit rederivation/address-type audit

Recompute the complete derivation and exact address type before accepting a scanner's proposed recovery.

verify_scan_hits.py rejects candidates whose derivation or P2PKH/P2SH/witness interpretation does not match. It corrects the earlier tendency to label raw index associations as recovered wallets.

$$
\mathrm{Accept}=\mathbf{1}\{\mathrm{Address}_{\mathrm{type}}(\mathrm{Derive}(s,p))=A_*\}
$$

Recompute seed/path derivation and the exact address type before accepting a hit. Index associations or Bloom positives alone fail this criterion.

Recompute candidate addresses and reject type mismatches before reporting a recovery; prior raw hits were not all valid.

Sources: [verify_scan_hits.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/verify_scan_hits.py); [Weak-Entropy-Research.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Weak-Entropy-Research.md)

## M202 — Digital-root puzzle-index association

Reduce a scalar's decimal digits repeatedly and compare the result with a puzzle-index rule.

The creative-theory report counts observed matches and compares with controls. A small digital-root match imposes at most a weak residue condition, not the scalar's full value.

$$
\mathrm{dr}(k)=1+((k-1)\;\mathrm{mod}\;9),\quad k>0
$$

The decimal digital root is essentially a modulo-nine condition. A matching puzzle-index rule constrains only this small residue class.

One of thirteen archived creative theories; report marks it nonsignificant, not a recovered-key method.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M203 — Public-key x-coordinate steganography

Compare selected low bits or XOR patterns of k and the public x-coordinate for signs of intentional embedded information.

The report summarizes bit statistics against random keys. Public multiplication is nonlinear; apparent low-bit similarity must predict unseen scalars before it can guide recovery.

$$
T_b(k)=\big(k\mathbin{\oplus}x(kG)\big)\;\mathrm{mod}\;2^b
$$

This is an example low-bit XOR statistic for testing scalar/public-x associations. Use matched random keys; no inverse map is supplied by the statistic.

Compare key/public-coordinate low-bit relations with random controls; no convincing result recorded.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M204 — Zeckendorf/Fibonacci sparsity

Represent integers as sums of nonadjacent Fibonacci numbers and measure how sparse that representation is.

The code compares known-key weights with random-key weights. Changing numeral systems can change visible sparsity without reducing the number of possible keys.

$$
k=\sum_j\epsilon_jF_j,\quad\epsilon_j\in\{0,1\},\quad\epsilon_j\epsilon_{j+1}=0
$$

Zeckendorf uses the conventional Fibonacci list 1,2,3,5,... and forbids adjacent terms. Weight counts must be compared with the same encoding on random keys.

Compare Fibonacci representation weights with random keys; no significant anomaly reported.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M205 — Low-discrepancy / Halton-like tier placement

Normalize key positions to [0,1) and measure gaps or star discrepancy against structured low-discrepancy schedules.

The creative report compares its discrepancy statistic with random controls. Evenly spread finite observations do not establish a deterministic next-key schedule.

$$
D_m^*=\sup_{0\leq u\leq1}\left\lvert\frac{1}{m}\sum_i\mathbf{1}\{u_i<u\}-u\right\rvert
$$

Star discrepancy measures spread of normalized tier positions u_i. Low discrepancy in a finite sample does not determine the next scalar.

Compare normalized-position discrepancy; no significant deterministic schedule established.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M206 — Benford leading digits of roots

Compare first decimal digits of root values with a Benford-type reference distribution.

The report computes frequency/test summaries for known roots and controls. Agreement or disagreement is a distribution diagnostic, not enough information to determine unknown remainder digits.

$$
\Pr(D=d)=\log_{10}(1+1/d),\quad d=1,\ldots,9
$$

This is the Benford reference for a leading decimal digit. Finite root ranges need a matched reference; the formula is not automatically their correct null.

Root first-digit distribution compared with controls; no convincing signal reported.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M207 — Taxicab sums of two cubes

Search whether a scalar is a sum of two integer cubes, potentially exposing a special generator family.

The creative report counts representations on disclosed keys and random controls. A special representation would still need independent evidence that the target was generated by that family.

$$
k=a^3+b^3
$$

Test whether disclosed scalars have integer two-cube representations in the declared range. Representation counts need matched controls and a justified target-generation premise.

Search special cube-sum representations of known keys; no transferable high-index key relation.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M208 — Polynomial in puzzle number

Fit a low-degree function of puzzle number and forecast later key positions or values.

The creative theory uses leave-one-out error versus controls; separate exact continuation tests verify concrete candidates. A polynomial fitting all known points has no automatic predictive authority.

$$
\widehat k_N=\sum_{j=0}^{d}a_jN^j
$$

A polynomial in index N is a hypothesized predictor. Its fitted degree, target scale and evaluation split determine what can be inferred.

Leave-one-out prediction compared with random keys; fitting known data does not determine the next scalar.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M209 — Consecutive bit-Jaccard similarity

View set-bit positions as sets and compute intersection divided by union for consecutive puzzle keys.

The report compares mean Jaccard overlap with random tier-matched keys. Similarity caused by bit widths must not be mistaken for inherited secret bits.

$$
J(A,B)=\frac{\lvert A\cap B\rvert}{\lvert A\cup B\rvert}
$$

A and B are sets of occupied bit positions in consecutive keys. Tier lengths and fixed leading bits affect the null overlap.

Bit-set overlap compared with random controls; no significant inheritance relation reported.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M210 — Mersenne-adjacent margin hypothesis

Measure whether keys lie unusually close to powers of two or all-ones Mersenne-style boundaries.

The creative test compares normalized margins with uniform controls. Small margins would identify a candidate region only under a validated generator prior.

$$
\delta(k)=\frac{\min(k-L,U-k)}{U-L+1}
$$

This normalized distance to tier endpoints is one margin diagnostic. Other power-of-two or all-ones boundary families must be declared separately.

Distances to power-of-two boundaries compared with random ranges.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M211 — Shared CRT residue / digital modular biases

Count small-modulus residues and ask whether a common congruence distinguishes disclosed keys from random intervals.

The report examines frequencies such as residues modulo three. Several weak residue preferences can arise by chance; they do not justify applying an unvalidated CRT restriction to the target.

$$
\chi^2=\sum_{r=0}^{m-1}\frac{(O_r-E_r)^2}{E_r}
$$

Compare residue counts with the correct tier-induced expected counts E_r. Trying many moduli requires accounting for that selection before imposing CRT restrictions.

Small-modulus residue frequencies examined; exploratory bias is not proof of a target constraint.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M212 — Collatz stopping-time association

Map each key through the Collatz iteration and compare stopping-time statistics.

The creative report evaluates known and random keys under the same rule. The transformed statistic is not shown to be invertible from a target address or predictive of its scalar.

$$
C(x)=x/2\ \mathrm{if\ even};\quad C(x)=3x+1\ \mathrm{if\ odd}
$$

Iterate to the stated stopping condition or cap and compare stopping times against matched controls. No general termination assumption is needed for a capped experiment.

Compare stopping statistics with random-key controls; no predictive result reported.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M213 — Brainwallet/BIP39 phrase schedule

Hash or derive keys from a fixed catalog of phrases/mnemonics and apply the puzzle's interval mask.

The creative family checks whether a phrase schedule reproduces significant known tiers. Tiny-tier coincidences are separated from evidence that one phrase generates later unknown keys.

$$
\widehat k_N=\mathrm{Mask}_N(\mathrm{Derive}(\mathrm{phrase},p_N))
$$

A phrase catalog and path schedule p_N define a finite candidate family. Tiny-tier coincidences do not establish a rule for later indices.

Catalog phrase-derived keys and masked tiers tested; archived creative report records no nontrivial hits.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M214 — Solve-date scalar encoding

Encode dates in scalars or compare normalized scalar positions with date-related numbers.

The report counts date-pattern matches and errors over known solve records. Solve date can reflect search effort rather than generation, so correlation would require independent validation.

$$
u_N=\frac{k_N-2^{N-1}}{2^{N-1}},\quad\widehat u_N=f(\mathrm{date}_N)
$$

Date encodings propose normalized tier positions or literal integers. Solve dates are observations after generation and can introduce misleading correlations.

Test date patterns in keys; no significant association recorded.

Sources: [creative_theories.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/creative_theories.md)

## M215 — UniMath-inspired arithmetic identities

Re-express arithmetic facts such as Euclidean division and reconstruction as executable exact assertions on known data.

unimath_corpora.py mirrors named mathematical ideas in Python. Passing these checks validates that implementation and corpus, not a machine-checked Agda proof or an unknown-key extractor.

$$
a=bq+r,\quad0\leq r<b,\quad b>0
$$

Euclidean division and exact reconstruction are executable arithmetic checks. Passing them is not a formal proof assistant verification of a key-extraction theorem.

Exact division, reconstruction, congruence and remainder assertions on known keys; arithmetic checks are not an Agda proof or prediction.

Sources: [unimath_corpora.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/unimath_corpora.py); [unimath_corpora.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/unimath_corpora.md)

## M216 — Residue/Legendre/coefficient distribution controls

Compare coefficient, residue, Legendre-symbol and remainder distributions with matched random samples.

unimath_insights.py produces statistical summaries and controls. It tests distributional hypotheses rather than deriving new bits directly from the target public point.

$$
\left(\frac{a}{p}\right)\equiv a^{(p-1)/2}\pmod p
$$

For odd prime p and a not divisible by p, Euler's criterion encodes the Legendre sign. Compare such symbols, residues and coefficients with matched controls.

Random controls and KS/chi-square-style summaries distinguish transformation artifacts from candidate key bias.

Sources: [unimath_insights.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/unimath_insights.py)

## M217 — DP hashing/birthday/URAND jump probes

Measure hash-table collisions, birthday behavior and candidate jump tables to improve practical walk mechanics.

Bitsavers-inspired probes model open addressing and first-collision counts, then compare URAND-derived jumps. These are solver engineering experiments, not secret-generator observations.

$$
\Pr(\mathrm{collision})\approx1-\exp\!\left(-\frac{t(t-1)}{2M}\right)
$$

This birthday approximation assumes t independent uniform draws into M buckets. It calibrates storage/jump engineering, not target-scalar prediction.

Bitsavers-inspired hash-table, collision and jump-distribution experiments assess solver mechanics.

Sources: [bitsavers_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bitsavers_methods.py); [bitsavers_methods_backtest.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/bitsavers_methods_backtest.md)

## M218 — Regression SVD/subset/interval arithmetic variants

Refit numerical predictors using alternative regression subsets/SVD and propagate rounding intervals through formulas.

The historical methods module compares fit stability, numerical bounds and selected regressions. It can diagnose approximation error but cannot manufacture predictive information absent from the data.

$$
X=U\Sigma V^{\mathsf{T}},\quad\widehat\beta=X^+y
$$

SVD and the pseudoinverse estimate regression parameters; near-zero singular values reveal instability. Numerical stabilization does not create new predictive data.

Historical numerical-method variants audit R2 fits and rounding; not new information about the target.

Sources: [bitsavers_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/bitsavers_methods.py)

## M219 — MOV and finite-field index-calculus applicability

MOV reduces certain elliptic-curve logs to finite fields when the embedding degree is suitably small; index calculus has domain-specific requirements.

The registry estimates/checks applicability for secp256k1 and records why named structural attacks do not straightforwardly apply. It is not an executed transfer solving the target log.

$$
e=\min\{j\geq1:n\mid p^j-1\}
$$

e is the embedding degree of an order-n subgroup over the base field of size p. MOV applicability depends on tractable e and the target finite-field log cost.

Registry checks distinguish attacks requiring unsuitable curve structure from applicable interval methods.

Sources: [oreilly_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/oreilly_methods.py)

## M220 — DDL preprocessing tradeoff bounds

Restricted discrete-log methods trade preprocessing, memory and online work under stated target/setup assumptions.

The JoC module evaluates heuristic DDL bounds and synthetic scenarios. Estimated online savings must include required preprocessing and oracles before being compared with an actual puzzle search.

$$
T_{\mathrm{total}}(q)=T_{\mathrm{pre}}+qT_{\mathrm{online}}
$$

Preprocessing tradeoffs must include memory, setup and the number q of targets. An online cost estimate alone is not a complete recovery bound.

Analysis estimates restricted discrete-log tradeoffs under additional setup assumptions; no blind puzzle recovery demonstrated.

Sources: [joc_methods.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/joc_methods.py)

## M221 — Finite modular difference triangles

Repeatedly subtract neighboring residues modulo m; finite rows shrink by one entry at each level.

The experiment follows declared polynomial/exponential residue families through their full finite triangles. Reaching zero on supplied samples does not determine an unknown continuation without a recurrence assumption.

$$
D_i^{(t+1)}=D_{i+1}^{(t)}-D_i^{(t)}\pmod m
$$

Ordinary finite difference rows shorten by one entry per level. Zero rows are conditional on the supplied sequence and do not fix arbitrary continuations.

Exact finite-row experiments track polynomial/exponential residues through all levels; they do not reconstruct an unknown puzzle key.

Sources: [REPORT.md](/home/arialmohan/scratch/modular-difference-levels/REPORT.md)

## M222 — Cyclic difference orbit classification

Wrap the difference operator cyclically so row length stays fixed, then detect exact zero or repeated states in a finite state graph.

The saved study enumerates all starting rows within its declared small configurations and classifies their orbits. This is an exhaustive finite dynamics result, not cryptographic inversion.

$$
(Dx)_i=x_{i+1}-x_i\pmod m,\quad i\;\mathrm{mod}\;\ell
$$

Cyclic differences preserve row length ell. The finite state space has m^ell rows, so every orbit eventually repeats; exhaustive results apply to the declared sizes.

Exhaustive finite study classified 19,617 starting rows over 35 configurations into zero/cycles.

Sources: [REPORT.md](/home/arialmohan/scratch/modular-difference-levels/REPORT.md)

## M223 — Signed quotient hierarchy with common-factor removal

Keep signed integer differences and divide a row by m whenever every entry shares that factor before taking the next difference.

The quotient experiment records divisions and exact normalized states. Removing common factors exposes structure but can still leave growing values or unresolved trajectories.

$$
Q_m(x)=x/m^{v_m(x)},\quad v_m(x)=\max\{e:m^e\mid x_i\ \mathrm{for\ all}\ i\}
$$

For a nonzero integer row, remove the largest common power of m. Combine normalization with signed differences in the exact order specified by the experiment; handle the all-zero row separately.

Remove factors of the full modulus before continuing signed differences; zero, cycle and capped outcomes remain separate.

Sources: [QUOTIENT_REPORT.md](/home/arialmohan/scratch/modular-difference-levels/QUOTIENT_REPORT.md)

## M224 — 256-level quotient continuation

Extend the same bounded quotient experiment to more levels without changing the starting rows or normalization rule.

The 256-level survey compares outcomes with the earlier 128-level cap. Capped rows remain unresolved; lack of termination by the cap is not proof of infinite nontermination.

$$
x_{t+1}=F(x_t),\quad0\leq t<256
$$

F is the declared quotient/difference update. Reaching the iteration cap gives a finite unresolved trajectory, not proof of nontermination.

Saved survey records 163 zero, 600 cycles and 18,854 unresolved rows; no new resolutions after the earlier cap.

Sources: [QUOTIENT_REPORT_256.md](/home/arialmohan/scratch/modular-difference-levels/QUOTIENT_REPORT_256.md)

## M225 — All-value magnitude/growth tracking

Track magnitudes, signs, divisibility and growth of every entry across every difference level, including after an earlier event.

The all-values run records more than 23 million observations and reports extreme bit lengths. It measures behavior of those exact finite trajectories, not secret-key information gained.

$$
B_t=\max_i\left\lceil\log_2(\lvert x_i^{(t)}\rvert+1)\right\rceil
$$

Track maximum magnitude bits along with signs and divisibility for every finite row. Statistics describe those trajectories only.

More than 23 million entry observations distinguish growth from termination; unresolved finite caps are not nontermination proofs.

Sources: [ALL_VALUES_REPORT_256.md](/home/arialmohan/scratch/modular-difference-levels/ALL_VALUES_REPORT_256.md)

## M226 — Inverse-difference kernel/anchor tests

Group all starting rows that produce the same observed difference row. Additional anchors can select among these inverse candidates.

inverse_capability.py exhaustively counts compatible inputs in small finite systems. If several remain, the transformed row alone has lost information and cannot uniquely reconstruct the original.

$$
\mathcal{F}_y=\{x:Dx=y\},\quad D(x+c\mathbf{1})=Dx
$$

Differences erase constant offsets. Additional anchors can reduce an inverse fiber; uniqueness must be checked under the declared domain and modulus.

Enumerate compatible starting rows; anchors can resolve lost constants, but the residual hierarchy supplies no missing observations.

Sources: [INVERSE_CAPABILITY_REPORT.md](/home/arialmohan/scratch/modular-difference-levels/INVERSE_CAPABILITY_REPORT.md)

## M227 — Deterministic index, byte and bit evolution

Define reversible or simple deterministic maps from an index into bitstrings, including increments and fixed byte/bit changes.

The unified framework executes registered sequence maps on artificial states. It generates controlled trajectories rather than learning the unknown puzzle creator's generation rule.

$$
x_{t+1}=F_t(x_t),\quad x_0=x_{\mathrm{seed}}
$$

A specified deterministic evolution generates controlled artificial trajectories. It does not infer an unknown real-world generator from its output hash.

Unified framework includes index mapping, linear increments, byte/bit steps and monotonic traversal; code is not an unknown-key predictor.

Sources: [unified_keyspace_framework_algorithm.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/frameworks/unified_keyspace_framework_algorithm.py)

## M228 — Masking, rotation and coupled sequences

Apply masks, rotate bit positions or couple two evolving states according to an explicit deterministic rule.

Registered transforms create particular orbits; some masks are lossy. Comparing their shapes cannot establish that a real target key belongs to one of those orbits.

$$
x'=\mathrm{rot}_b(x\mathbin{\oplus}M,r)
$$

This fixed XOR-mask/rotation example is reversible on b-bit words. AND masks are generally lossy; coupled-state transforms need their full joint update.

Unified framework includes mask application, dual-sequence coupling, mask rotation and structured 256-step schedules.

Sources: [unified_keyspace_framework_algorithm.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/frameworks/unified_keyspace_framework_algorithm.py)

## M229 — First/second-difference and drift schedulers

Measure first/second differences and choose the next transformation based on drift or entropy summaries.

The framework's schedulers switch among existing maps using their configured rules. Adaptation optimizes trajectory diagnostics; it is not rewarded by an independently discovered target-key relation.

$$
\Delta x_t=x_{t+1}-x_t,\quad\Delta^2x_t=\Delta x_{t+1}-\Delta x_t
$$

Drift schedulers choose subsequent transformations from these summaries. Arithmetic must specify whether differences are ordinary signed or modular.

Analyze trajectory differences or switch transformations using entropy thresholds; diagnostic evolution is not key recovery.

Sources: [unified_keyspace_framework_algorithm.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/frameworks/unified_keyspace_framework_algorithm.py)

## M230 — Entropy, cycles, compression and spectral diagnostics

Compute bit entropy, compression, cycles, nearest-neighbor spacings and spectral summaries, then compare with random trajectories.

Classical arrays and statistics produce these measurements. Quantum-chaos terminology denotes analogy/diagnostics, not a quantum computation or an inverse map from address hashes to private scalars.

$$
h(p)=-p\log_2p-(1-p)\log_2(1-p)
$$

Binary marginal entropy h uses observed bit frequency p and 0 log 0=0. It is one diagnostic, distinct from joint entropy, compressibility, cycles and spectral summaries.

Compare deterministic trajectories with uniform controls, including cycle tests, spacings and spectral summaries; no quantum execution implied.

Sources: [unified_keyspace_framework_algorithm.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/research/frameworks/unified_keyspace_framework_algorithm.py); [revelation_discovery.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/output/revelation_discovery.md)

## M231 — Four-dimensional key/public/address visualization

Place scalar, public-point and address-hash objects into shared visualization coordinates and connect their derivation edges.

keyspace_4d.py supports raw/ring-style layouts. Normalized coordinates can illustrate hashing's loss of visible geometry without revealing an exploitable inverse relationship.

$$
k\longmapsto(k,kG,\mathrm{ser}(kG),\mathrm{HASH160}(\mathrm{ser}(kG)))
$$

A visualization embeds these distinct derived objects into chosen display coordinates. Spatial proximity in that display is not a cryptographic inverse relation.

Display scalar-to-point-to-hash relationships in alternate layouts; no invertible address-to-scalar map is established.

Sources: [keyspace_4d.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/kangaroo_solver/keyspace_4d.py)

## M232 — Classical BSGS multiplicative-order finder

BSGS finds an exponent r with a^r=1 modulo N by matching stored small powers against larger steps.

Classical Python/native order routines operate on bounded integer examples. In the factoring reduction they replace the quantum order-finding oracle; no QFT is executed.

$$
a^{im+j}\equiv1\pmod N,\quad m\approx\sqrt{R}
$$

BSGS matches small powers with inverse giant steps to seek a positive order within bound R; require gcd(a,N)=1 and reduce a found multiple to the actual order.

Exact small-integer order traces and backend comparisons; stands in for an order oracle, not a quantum device.

Sources: [RUN_REPORT_2026-09-09.md](/home/arialmohan/workspace/research/shor-quantum-research/RUN_REPORT_2026-09-09.md)

## M233 — Brent cycle-detection order finder

Brent's cycle detector follows repeated multiplication modulo N while using a low-memory schedule to detect a return period.

The implementation measures this classical order finder against shared small inputs. Its runtime grows with the period and should not be mistaken for Shor's quantum complexity.

$$
x_{t+1}=ax_t\pmod N,\quad x_0=1
$$

For a coprime to N, this multiplication orbit has period ord_N(a). Brent's schedule detects its cycle using small memory and classical iteration.

Classical linear-period comparison backend; measured on bounded small semiprimes.

Sources: [FACTORING_RUN_REPORT_2026-10-10.md](/home/arialmohan/workspace/research/shor-quantum-research/FACTORING_RUN_REPORT_2026-10-10.md)

## M234 — Kangaroo multiplicative-order finder

Search successively larger exponent intervals with collision walks to locate a multiple/order relation.

The classical kangaroo order backend is benchmarked separately from elliptic-curve kangaroo. Matching the name does not mean these factoring experiments recovered Bitcoin private keys.

$$
a^t\equiv a^{s}\pmod N\quad\Longrightarrow\quad\mathrm{ord}_N(a)\mid(t-s)
$$

A nontrivial collision gives an order multiple. Interval walks must find a nonzero exponent difference and then verify/reduce that multiple.

Expanding exponent-interval method compared with BSGS and Brent; not a secp256k1 scalar recovery.

Sources: [FACTORING_RUN_REPORT_2026-10-10.md](/home/arialmohan/workspace/research/shor-quantum-research/FACTORING_RUN_REPORT_2026-10-10.md)

## M235 — Pollard-rho factoring fast path

Pollard rho searches for a nontrivial common divisor through repeated modular iteration and cycle-related gcds.

The high-level factor command can take this shortcut before order finding. Its reported factorization of 3233 is correctly labeled rho, not evidence of quantum or even BSGS execution on that path.

$$
x_{t+1}=f(x_t)\pmod N,\quad d=\gcd(\lvert x-y\rvert,N)
$$

Pollard rho seeks 1<d<N using suitably separated iterates x,y. This classical factoring path is distinct from quantum order finding.

Canonical factor command reports its shortcut explicitly; factoring 3233 must not be relabeled as a quantum Shor run.

Sources: [RUN_REPORT_2026-09-09.md](/home/arialmohan/workspace/research/shor-quantum-research/RUN_REPORT_2026-09-09.md)

## M236 — Python/GMP/Rust controlled order benchmarks

Hold modulus, base and repetition schedule fixed while replacing the order-finding arithmetic backend.

The saved matrix records per-backend times and verifies identical orders. This isolates local implementation constants; differences across operand sizes are not a clean universal scaling-law estimate.

$$
S_b=\frac{t_{\mathrm{reference}}}{t_b},\quad r_b=r_{\mathrm{reference}}
$$

Compare backend times on identical modulus/base/order tasks while checking returned orders. Report operand sizes and repetition schedule.

Shared modulus/base backend matrix records finite speedups; source/runtime differences are pinned in historical manifests.

Sources: [BACKEND_MATRIX_2026-09-10.md](/home/arialmohan/workspace/research/shor-quantum-research/BACKEND_MATRIX_2026-09-10.md)

## M237 — Adaptive Shor simulation trial budgets

Measure trial success, compute a confidence-aware required budget and adjust the number of repetitions to meet a target.

The factoring loop changes trial counts and ramps a bounded test size. The feedback improves a classical experimental procedure, not the underlying cryptographic problem's entropy.

$$
B\geq\left\lceil\frac{\log(1-\tau)}{\log(1-p)}\right\rceil
$$

Under independent trials with fixed success probability 0<p<1, B trials achieve success probability at least tau. An estimated p requires uncertainty and model calibration.

Empirical/analysis/improvement loop adjusts trial counts with Wilson-bound and runtime metrics.

Sources: [FACTORING_RUN_REPORT_2026-10-10.md](/home/arialmohan/workspace/research/shor-quantum-research/FACTORING_RUN_REPORT_2026-10-10.md); [loop.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/shor_sim/loop.py)

## M238 — UCB/EWMA/early-stop method selection

An upper-confidence policy explores backend choices while EWMA smooths noisy measurements and early stopping limits unnecessary trials.

Archive modules describe/use these policy choices within simulation loops. Better simulated reward can reflect assumptions in the model and needs real execution validation before any cryptanalytic interpretation.

$$
U_i=\overline{r}_i+c\sqrt{\frac{\log t}{n_i}},\quad\mu_t=\alpha r_t+(1-\alpha)\mu_{t-1}
$$

UCB scores balance exploration and reward; EWMA smooths observations. Handle untried arms explicitly; the reward's meaning depends on the experiment.

Archive describes adaptive backend policy and smoothing; simulator optimization is not target-scale quantum cryptanalysis.

Sources: [Shor-Simulation.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Shor-Simulation.md)

## M239 — Semiprime-per-puzzle circuit/manifest analogy

Construct a deterministic semiprime challenge from puzzle data to illustrate a comparable input size for factoring-resource calculations.

Circuit/manifest commands prepare that separate factoring task. A factor of the constructed integer is not mathematically shown to disclose the original elliptic-curve scalar.

$$
N=pq,\quad\gcd(a^{r/2}\pm1,N)
$$

The factoring reduction uses an even multiplicative order r with nontrivial gcd outcomes. Factoring a semiprime constructed from puzzle data does not thereby yield the elliptic-curve scalar.

Factoring challenges derived from puzzle data are resource-scale analogies, not reductions recovering puzzle scalars.

Sources: [Shor-Simulation.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Shor-Simulation.md)

## M240 — secp256k1 quantum ECDLP resource mode

The ECDLP mode combines real small-range BSGS with a probability-and-time oracle model beyond configured exact limits.

In shor_sim/ecdsa.py, exact branches call the BSGS routine; larger Shor/hybrid trials draw success from rng.random() and return formula-based elapsed time. Even the small kangaroo-labeled profile calls BSGS in its exact branch.

$$
X=\mathbf{1}\{U<p_{\mathrm{model}}\},\quad U\sim\mathrm{Unif}[0,1)
$$

This describes the simulator's success draw beyond its exact small-range branch. A model draw is not an executed quantum computation or recovered target scalar.

Models the relevant discrete-log task separately from integer factoring; no executed target-scale quantum circuit is established.

Sources: [ecdsa.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/shor_sim/ecdsa.py)

## M241 — 520-logical-qubit resource sensitivity model

Estimate logical resources under a simplified model and vary physical error/architecture assumptions to see their effect.

The standalone audit identifies omitted reversible-arithmetic workspace and other architecture costs. A 520-qubit headline is a sensitivity-model output, not a complete executable Bitcoin-breaking circuit.

$$
Q_{\mathrm{logical}}=Q_{\mathrm{data}}+Q_{\mathrm{workspace}}+Q_{\mathrm{ancilla}}
$$

A complete logical-qubit budget must state which registers are included and whether lifetimes overlap. A sensitivity headline can omit load-bearing reversible-arithmetic workspace.

Standalone audit excludes required reversible workspace and full architecture; headline counts are not a complete Bitcoin-breaking machine.

Sources: [AUDIT.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/papers/standalone_520_qubit/AUDIT.md)

## M242 — Surface-code/platform timing estimates

Map logical operation counts to physical qubits and runtime using code distance, gate/cycle assumptions and platform parameters.

quantum.py calculates resource estimates for chosen profiles. The outputs are model-dependent arithmetic, not measured throughput on an available quantum computer.

$$
t_{\mathrm{wall}}\approx D_{\mathrm{logical}}\,\tau_{\mathrm{logical}},\quad Q_{\mathrm{physical}}=Q_{\mathrm{logical}}\,\eta(d)
$$

Logical depth, logical cycle time and code-distance overhead eta(d) determine resource-model estimates; scheduling and architecture assumptions control their accuracy.

Compare physical errors, distances and cycle times for several platforms; estimates depend on explicit architecture assumptions.

Sources: [quantum.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/shor_sim/quantum.py); [Shor-Simulation.md](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/wiki/Shor-Simulation.md)

## M243 — Wolfram/mask sensitivity extensions

Feed alternative masks, assumptions or external analytical outputs into the resource/sensitivity model and compare derived estimates.

The standalone Wolfram-named modules implement follow-up model calculations. They do not construct or execute a target-sized quantum state evolution that reveals a puzzle key.

$$
R(\theta+\delta\theta)-R(\theta)
$$

A finite sensitivity change in assumptions theta measures how the resource model R responds. It is a comparison of modeled outputs, not quantum state evolution.

Standalone modules explore model sensitivity and follow-up calculations, not recovered puzzle keys.

Sources: [wolfram_masks.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/papers/standalone_520_qubit/shor_sim/wolfram_masks.py); [wolfram_mix.py](/home/arialmohan/workspace/projects/distinguished-kangaroo-main/papers/standalone_520_qubit/shor_sim/wolfram_mix.py)

## M244 — Train/holdout adaptive-trial study

Freeze a trial-budget policy on one stream, then evaluate it on additional held-out random streams to check whether tuning generalizes.

The latest factoring report records its bounded train/holdout trials and limitations. Repeated success on small semiprimes validates that experiment, not quantum-scale secp256k1 recovery.

$$
\widehat p_{\mathrm{test}}=\frac{1}{m}\sum_{i=1}^{m}\mathbf{1}\{\mathrm{success}_i\mid\theta_{\mathrm{frozen}}\}
$$

Freeze the trial policy after training, then evaluate on independent holdout streams. Small-instance experimental success does not establish target-scale quantum recovery.

Latest factoring report includes additional controlled trial streams; conclusions remain limited to classical simulation.

Sources: [FACTORING_RUN_REPORT_2026-10-10.md](/home/arialmohan/workspace/research/shor-quantum-research/FACTORING_RUN_REPORT_2026-10-10.md)
