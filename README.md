# Kelechi Emeka Ogbonna

**Biotechnologist and self-taught engineer. I build computer models of the body, of disease and of rockets.**

M.Sc. Medical Biochemistry (in progress), University of Uyo · B.Sc. Biotechnology, Nile University of Nigeria (2022) · Founder, Wakanda Series (Kelechi Wagen Services), Akwa Ibom State, Nigeria · ORCID [0009-0006-0065-8226](https://orcid.org/0009-0006-0065-8226)

📄 **[Full CV (PDF)](cv/Kelechi_Ogbonna_CV.pdf)** · ✉️ keonix200@gmail.com · [X @Kelechi_Wagen_s](https://x.com/Kelechi_Wagen_s)

I write software that simulates how living things and machines behave, and I try to be precise about what each result is: a lab measurement, a computer model, or an idea. My work covers three areas that I see as one path: keeping people healthy, understanding disease, and getting Africa to space.

## Health and biology

### Freezing blood for long space trips (CRYO-RESTORE, M.Sc. project)
My M.Sc. proposal freezes human red blood cells in five ways and measures the damage after thawing. Before the lab work, I built four computer models: damage over time, freezing-agent flow through the cell, energy recovery after thawing, and a search over 1,368 protocols. The models point to the wash step that removes the freezing agent as the step that bursts cells. These are model predictions, still to be tested in the lab.

### [Will the same medicine work in orbit?](https://github.com/cloudynirvana/space-medicine)
Combined 7 NASA spaceflight studies of mouse livers from NASA's open science data (OSDR/GeneLab). The drug-processing gene *Cyp3a11* rose about 30% in 6 of the 7 missions, which suggests some antibiotics, such as clarithromycin, may clear faster in space. Mouse gene data only.
`Python` `meta-analysis` `NASA OSDR`

### Can a laptop spot drugs that might stop the heart?
Machine-learning models on 13,445 molecules predict blockade of the hERG heart channel. Random forest ROC-AUC 0.91 on a random split, falling to 0.85 on new chemical scaffolds. I also wrote a nearest-neighbour similarity check that predicts this gap before training.
`RDKit` `scikit-learn` `PyTorch` `Therapeutics Data Commons`

### [Project Confluence](https://github.com/cloudynirvana/project-confluence): how cancer cells use energy
A mathematical model of cancer metabolism (about 190 Python modules, 300+ automated tests) fitted to metabolomics from 928 cancer cell lines (CCLE). My later audit found that one snapshot of data pins down only 4 of 17 parameters, and time-course data would pin down 15. That correction is published. All results are computer simulation, none validated on patients.
`Python` `ODE models` `pytest`

### El Niño Risk Watch for Nigeria
A public dashboard for all 36 states and the FCT that refreshed every 6 hours from five free satellite and weather feeds, to warn people before dangerous heat.

### [Silver nanoparticles from pawpaw leaves](https://github.com/cloudynirvana/thesis-bsc-carica-papaya-agnp) (B.Sc. wet-lab project, 2022)
Made silver nanoparticles from papaya leaf extract and tested them against two diabetes-related enzymes. In 2026 I re-analysed my own data honestly: the plain extract did better than the nanoparticles, and the standard drug beat both.

## Space and engineering

All engine and rocket work below is computer design and simulation. Nothing has been printed, built or fired yet.

- **W-2750 rocket engine and T01 test chamber.** My own full-flow methane and oxygen engine (about 2.75 MN), sized with Cantera chemistry, every part generated in code (PicoGK) and stress-checked with CalculiX. The stress checks found three failures that hand sums missed; all parts now pass. A calibrated metal-printing simulation (7.8% error on a second NIST alloy) produced a print-ready file for a small cooled copper test chamber.
- **Wakanda-3 reusable rocket.** Full-size FreeCAD model. A real-geometry check showed the engines could not steer in a 4.2 m body, so the design moved to 5.5 m.
- **WK-1 "Ngao" spacecraft chip.** A radiation-tolerant motor-control chip taken to a clean layout on the open SkyWater 130 nm process: 1,036 random bit-flips, zero wrong outputs.
- **Test-stand electronics** in KiCad with ESP32 firmware that passes 4 of 4 safety cases in simulation.
- **Wakanda 009**, a 600 mm reusable model rocket checked in 2,000 simulated flights (RocketPy, cross-checked in OpenRocket).

## AI and data

### [Rocket Lander RL](https://github.com/cloudynirvana/rocket-lander-rl): teaching an AI to land a rocket
The trained agent lands on the pad 499 times out of 500, against 399 for a hand-written controller. A badly designed reward made it hover forever instead of landing; fixing the reward brought landings back to 98%.
`PyTorch` `Stable-Baselines3` `Gymnasium`

### Three NASA data projects
Kepler exoplanet finder (neural network, ROC-AUC 0.97), Mars terrain mapping from rover images (AI4Mars, mean IoU 0.81) and spacecraft telemetry fault detection (SMAP/MSL).

### More space software
- [mars-impact-scheduler](https://github.com/cloudynirvana/mars-impact-scheduler): 6,770 Earth to Mars transfers from JPL Horizons data, matching JPL to 0.007 degrees.
- [lunar-south-pole](https://github.com/cloudynirvana/lunar-south-pole): sunlight at the Moon's south pole from NASA LOLA height maps over an 18.6-year cycle.
- [adaptive-convergence](https://github.com/cloudynirvana/adaptive-convergence): when should a space programme quit a plan? The best strategy in 400 simulated worlds made 16% more progress.

## Research writing

16 open papers with DOIs on Zenodo (2026, not peer reviewed), each with its code and checked references. Full list on [ORCID](https://orcid.org/0009-0006-0065-8226).

| Area | Papers |
| --- | --- |
| Health and biology | [Food, tumour metabolism and gut bacteria](https://doi.org/10.5281/zenodo.23834525) · [AI-assisted cervical cancer care planning](https://doi.org/10.5281/zenodo.23210715) · [Brain activity in mouse, crow and macaque](https://doi.org/10.5281/zenodo.23912194) |
| Climate, health and energy | [El Niño heat-risk dashboard](https://doi.org/10.5281/zenodo.23834519) · [Gas flaring in the Niger Delta](https://doi.org/10.5281/zenodo.23844593) · [Biogas from Nigerian waste](https://doi.org/10.5281/zenodo.23834537) · [Bio-derived rocket fuels](https://doi.org/10.5281/zenodo.23844408) |
| Method | [Five reproducibility checks for students](https://doi.org/10.5281/zenodo.23844790) |
| Space | [Reusable rockets for Nigeria](https://doi.org/10.5281/zenodo.23834516) · [Satellites worth building](https://doi.org/10.5281/zenodo.23834521) · [Lunar south pole landing](https://doi.org/10.5281/zenodo.23834523) · [Deorbiting the ISS](https://doi.org/10.5281/zenodo.23834529) · [One rocket family for Africa](https://doi.org/10.5281/zenodo.23834531) · [Interstellar probes](https://doi.org/10.5281/zenodo.23834533) · [Negative energy and warp drives](https://doi.org/10.5281/zenodo.23834535) · [Jet engines from first principles](https://doi.org/10.5281/zenodo.23844950) |

Shorter exploratory write-ups (mostly cancer-modelling thought experiments, all computer simulation) are indexed at [research-theses-hub](https://github.com/cloudynirvana/research-theses-hub). They are idea sketches, not peer-reviewed results.

## Certifications

- **Anthropic:** AI Fluency · Claude 101 · Model Context Protocol Foundations
- **Hugging Face:** Fundamentals of Agents (2026)
- **Google:** Project Management Certificate (Coursera)
- **IELTS Academic:** 7.5 overall (CEFR C1), May 2024

## Experience

- **Founder**, Wakanda Series (Kelechi Wagen Services), Akwa Ibom, Oct 2026 to now. Briefs for the Akwa Ibom State space agency (ASTAL), which agreed to support the programme.
- **NYSC Educator**, Etinan College of Health and Technology. Taught biology, medical laboratory science and PCR.
- **Research Intern**, Arubah Medical Diagnostic Services. Blood collection, malaria and Widal tests.
- **Research Intern**, National Biotechnology Development Agency (NABDA), Abuja.
- **Managing Director**, Uloma Shopping Mall. Six staff, sales, stock and finances.

## Contact

keonix200@gmail.com · Open to research and engineering roles, internships and graduate study where biology, health and space meet.
