# Publication excerpt

This report is a comprehensive inventory of research into Bitcoin puzzle-solving methods. It brings together years of experiments, source-code reviews, mathematical analysis, computational tests, and retrospective audits into one structured reference.

The report examines how different approaches work, what inputs they require, what was actually implemented, and what conclusions the evidence supports. It covers direct verification, interval searches, bounded discrete-log techniques, scalar decompositions, CTheory, generator hypotheses, entropy analysis, ECDSA signatures, statistical prediction, GPU implementations, and quantum-resource simulations.

A central purpose of the inventory is to distinguish genuine computational progress from attractive but unverified claims. Some methods are fully practical under the right conditions. Others are useful only as conditional tools, while many proposed shortcuts fail to demonstrate reliable prediction or meaningful reduction of the unknown search space.

The report also preserves corrections and negative results. These include implementation limitations, calibration leakage, incomplete search-cost accounting, and cases where a mathematical reformulation was mistaken for a reduction in cryptographic difficulty.

This is a historical and technical evidence archive. It does not claim recovery of Puzzle #71 or any other unsolved private key, and it does not disclose credentials or methods for attacking ordinary wallets.

Full report and supporting materials:  
https://github.com/escache/bitcoin-puzzle-methods
