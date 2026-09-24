# Figure 3 — Study Flow Diagram

Figure 3 is a study design and sample flow diagram showing the progression from
the original outbreak case population through isolate availability, sequencing,
quality control, species confirmation, and identification of the ST39 outbreak
clone.

## How it was made

Recreated (22-Sep-2026, in response to peer review) as a reproducible
**Python/matplotlib** script: `fig03_flow_diagram.py`. The original figure was
built manually in Adobe Illustrator and was not reproducible from source; this
script replaces it.

## Why it changed

Two reviewer comments on the original figure:
1. Reviewer 1 asked for a flow diagram linking the original outbreak
   population (case-level counts from the previously published outbreak
   report, ref. 26) through to isolate-level and genomic outcomes, including
   ST39 case numbers and fatalities — the original figure started at "isolates
   retrieved from frozen stocks" and stopped at "K. pneumoniae genomes passing
   QC," never reaching case-level or outcome data.
2. Reviewer 2 flagged an internal contradiction in the original figure text:
   "ONT sequencing with MinION on R10 flowcells on PromethION" — MinION and
   PromethION are different instruments, and only PromethION was used (Methods
   already states this correctly). The recreated figure omits instrument-level
   sequencing detail entirely (it's unambiguous in Methods) rather than risk
   restating it incorrectly.

## Description

The diagram traces, top to bottom, with exclusion counts branching to the
side at each attrition step:
- Original outbreak cases (76 cases, 57 neonates; ref. 26)
- Isolates retrieved from frozen storage (158; Table 1)
- Isolates revived for DNA extraction & sequencing (148)
- WGS data passing quality control (126)
- Species split: K. pneumoniae sensu stricto (90) vs. other species (36:
  K. quasipneumoniae, K. variicola, K. quasivariicola, K. africana, E. coli)
- Within K. pneumoniae: 2023–2024 clinical + environmental (50) vs. historical
  2012–2022 (40, ST39 not detected)
- ST39-KL62 outbreak clone (29 clinical cases + 3 environmental IV-fluid
  isolates; 28/29 clinical isolates in a single transmission cluster)
- Outcomes (16 deaths among 29 cases, 55% case fatality)

All counts are sourced from Table 1 and the Results text of the main
manuscript (current as of the 18-Sep-2026 revision) — see the script's
docstring and inline comments for the exact provenance of each number.

## Source file

`fig03_flow_diagram.py` (Python, matplotlib). Outputs `fig03_flow_diagram.pdf`
and `fig03_flow_diagram.svg`. No external data file required — all counts are
hardcoded from the manuscript (this figure has no underlying per-isolate
dataset the way the other figures do).
