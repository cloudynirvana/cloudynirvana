# Kelechi Emeka Ogbonna

**Bioinformatics and computational biology.** B.Sc. Biotechnology, Nile University of Nigeria (2022); pursuing an M.Sc. in Bioinformatics.

I write tested Python tools for biological data and models, and I try to be precise about what each result is: a measurement, a simulation, or a hypothesis. Lately I also build simulations of decision-making and control for spaceflight.

📄 **[CV (PDF)](cv/Kelechi_Ogbonna_CV.pdf)**

## Featured work

### [Adaptive Convergence](https://github.com/cloudynirvana/adaptive-convergence): when should a civilisation stop converging on its best plan?
Agent-based simulation of long-horizon R&D strategy across procedurally generated technology graphs with hidden dead ends. Committing to the best option while abandoning projects on statistical evidence of overrun gave **+15.8% capability** over the best convergent baseline (95% CI 13.0–18.9%, 400 held-out worlds), and extra exploration made things worse. Includes a replication of March (1991).
`Python` `NumPy/SciPy` `agent-based modelling` `statistics`

### [Rocket Lander RL](https://github.com/cloudynirvana/rocket-lander-rl): reward shaping, reward hacking and robustness
PPO agents trained to land a rocket under four reward designs and five seeds, evaluated on the unshaped reward. Reproduces a hover reward hack, fixes it with potential-based shaping, and stress-tests agents against a hand-written control law under wind and gravity dispersions.
`Python` `PyTorch` `Stable-Baselines3` `Gymnasium`

### [qslite](https://github.com/cloudynirvana/qslite): viral quasispecies from sequencing reads
Aligns reads with minimap2, counts alleles at every position, measures within-host diversity (Shannon entropy, nucleotide diversity), calls minor variants with a binomial error model and FDR control, measures linkage between variant sites from spanning reads, and exports the population as a GFA variation graph.
On the HIV test dataset from V-pipe and ShoRAH, it **recovers all 64 SNVs that ShoRAH reports**. Includes tests on a synthetic two-haplotype population and CI.
`Python` `pysam` `minimap2` `SciPy` `GFA`

### [Project Confluence](https://github.com/cloudynirvana/project-confluence): dynamical models of cancer metabolism
An ODE framework for metabolic reprogramming across cancer types, with identifiability analysis and adaptive-control experiments. Fitting to real CCLE metabolomics data (928 cell lines) raised the number of identifiable parameters from 7 to 15 of 17. About 190 Python modules and 315 automated tests run in GitHub Actions. All results are in-silico; none are validated on patients.
`Python` `NumPy/SciPy` `ODEs` `pytest` `FastAPI`

### [TNBC Metabolic Strain Model](https://github.com/cloudynirvana/TNBC-Metabolic-Strain-MOD): ATP and ROS dynamics in triple-negative breast cancer
A compact ODE model with stability and bifurcation analysis and parallel parameter sweeps, packaged as a reusable module with Colab notebooks.
`Python` `Jupyter` `dynamical systems`

## Skills, with where to see them

| Area | Evidence |
| --- | --- |
| Sequence data analysis | qslite: alignment, pileups, variant calling, linkage |
| Graphs | qslite (GFA variation graphs); Confluence (Forman-Ricci curvature on interaction networks) |
| Software practice | pytest suites and GitHub Actions in qslite and Confluence; packaged, installable code |
| Mathematical modelling | ODEs, identifiability, bifurcation analysis (Confluence, TNBC) |
| Wet lab | B.Sc. project: plant-extract silver nanoparticles and in vitro enzyme (α-amylase) assays |

## Other work

Shorter exploratory and theoretical write-ups (mostly cancer-modelling thought experiments, all in-silico) are indexed in one place: **[research-theses-hub](https://github.com/cloudynirvana/research-theses-hub)**. They are idea sketches, not peer-reviewed results.

## Contact

kelechiogbonna300@gmail.com · Open to internships, graduate roles and doctoral positions in computational modelling, computational biology and space life sciences.
