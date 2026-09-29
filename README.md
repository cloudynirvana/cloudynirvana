# Kelechi Emeka Ogbonna

**Computational biologist** · systems biology and nonlinear dynamics · cancer metabolism modelling

GitHub: [github.com/cloudynirvana](https://github.com/cloudynirvana) · Contact via GitHub

> **Status note:** my research is in-silico. Nothing here is a cure, a therapy, a medical device or clinical decision support. Model outputs are hypotheses under stated assumptions and need wet-lab and clinical validation.

---

## Profile

Computational biologist with a biotechnology background. I build and test mathematical models of cancer cell metabolism, and I publish the code and the limits of each model openly. I am working toward clinical training so that computational hypotheses can be tested against real biology and patient need.

## Education

- **M.Sc. Biotechnology**, Ahmadu Bello University, Zaria. *In progress (started 2024).* Focus: systems biology and nonlinear dynamics.
- **B.Sc. Biotechnology**, Nile University of Nigeria, 2018 to 2022. Second Class Upper. Research: green synthesis of silver nanoparticles.
- **Medicine and Surgery**, University of Uyo. *Applying (Direct Entry); admission not yet confirmed.*

## Research projects

### Project Confluence (`project-confluence`)
Open-source computational oncology framework for modelling how tumour metabolism shifts with disease progression.
- Uses public CCLE metabolomics data (225 metabolites, 928 cell lines).
- Reports structural identifiability rising from 7/17 to 15/17 parameters with six real metabolomics channels *(as stated in the repository README; independent re-run pending)*.
- In simulated stress tests, 1 of 200 uncertain scenarios (0.5%) showed resistant takeover. These scenarios are simulated, not clinical.
- Includes tests (pytest), packaging (`pyproject.toml`), a disclaimer, and an MIT licence.

### TNBC Metabolic Strain model (`TNBC-Metabolic-Strain-MOD`)
Three-variable ODE model (ATP, ROS, glucose) of triple-negative breast cancer cells (MDA-MB-231), runnable in Google Colab.
- Reports a glucose-threshold metric (`G_mix`) shifting from 0.238 to 0.245 under the modelled treatment arm. This is a model output, not a cell measurement.
- **In progress:** an added GPX4-clearance term as an in-silico hypothesis. Under an assumed, unfitted clearance parameter, the model predicts a ROS runaway threshold near 58% GPX4 inhibition (checked numerically). Known limits: single-cell, 30-minute timescale; no lipid-peroxidation species; no resistance; the parameter is unestimated. Published work reports GPX4-inhibitor-resistant TNBC lines, so resistance must be part of any interpretation.
- **Validation path:** public dependency data (DepMap), then wet-lab tests (viability, lipid peroxidation, ferrostatin-1 rescue), with predictions recorded before experiments.

### Research thesis series (`research-theses-hub`)
An index of 50+ numbered computational thesis-proposal repositories. Each is an in-silico proposal with an explicit research-only disclaimer. Some numbers are duplicated or deprecated; the hub tracks canonical versions.

### `saem-mcp`
Research prototype for a model-context-protocol tool. Not for clinical use.

## Skills

- **Modelling:** ODE systems, nonlinear dynamics, structural identifiability, parameter sensitivity, threshold and bifurcation analysis.
- **Data:** cancer cell-line metabolomics and dependency data (CCLE, DepMap); exploratory statistics.
- **Software:** Python (SciPy, pandas), Jupyter and Colab, pytest, reproducible packaging, Git and GitHub.
- **Research practice:** stating assumptions and limits, labelling unverified claims, defining falsification tests before experiments.

## Working principles

- Every claim is labelled by evidence level; unverified items are marked as such.
- Disclaimers and limitations ship with the code.
- Results are hypotheses until validated in cells, animals and patients.

## Goals

- Test the GPX4 x TNBC hypothesis against public dependency data, then with a wet-lab partner.
- Complete the M.Sc. and pursue medical training to connect computational work to clinical need.
- Publish reproducible, peer-reviewable work.
