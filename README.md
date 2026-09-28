# *Klebsiella pneumoniae* neonatal sepsis outbreak in a rural Gambian hospital

This repository contains the analysis scripts used to generate the figures in:

> Foster-Nyarko E, *et al.* ***Klebsiella pneumoniae* neonatal sepsis outbreak in a rural Gambian hospital: a retrospective genomic epidemiology investigation.** *medRxiv* (2026). https://doi.org/10.64898/2026.03.03.26347025

---

## Repository Structure

```
code/
├── README.md                          # This file
├── data/
│   └── README.md                      # Data sources and access instructions
├── fig01_timeline_and_map.py          # Figure 1 — Outbreak timeline (A) + map of study sites (B)
├── fig01A_gambia_map.py               # Figure 1B — Map of The Gambia (stand-alone)
├── fig02_resistance_heatmap.py        # Figure 2 — AMR heatmap (clinical + environmental)
├── fig03_flow_diagram.py               # Figure 3 — Study flow diagram
├── fig03_flow_diagram.md              # Figure 3 — notes and provenance
├── fig04_epi_curve.qmd                # Figure 4 — Epidemiological curves
├── fig05_kpn_phylotree_annotated.qmd  # Supplementary Figure 2 — All-Kp phylogenetic tree + metadata
├── fig06_st39_global_clones.qmd       # Figure 6 — Global ST39 clone distribution + AMR
├── figS1_ward_contamination.md        # Figure S1 — Ward contamination sources (Illustrator)
├── figS2_transmission_clusters.md     # Supplementary Figure 3 — Transmission cluster analysis (note)
├── figS3_st39_plasmid.qmd             # Figure 5 — ST39 multi-panel with plasmid coverage
└── figAppendix_clinker_amr_locus.md   # Appendix — Chromosomal AMR locus comparison (clinker)
```

---

## Figures Summary

Figure numbers follow the revised manuscript. Script filenames keep the numbering of the original preprint: in the revision, the former Figure 5 became Supplementary Figure 2, the former Supplementary Figure 2 became Supplementary Figure 3, and the former Supplementary Figure 3 became Figure 5.

| Figure | Description | Script | Language |
|--------|-------------|--------|----------|
| Fig 1  | Outbreak timeline (monthly cases by WGS result, deaths, investigation and sampling events) and map of study sites | `fig01_timeline_and_map.py` | Python |
| Fig 2  | Clustered AMR heatmap (clinical + environmental isolates; resistant / intermediate / susceptible, 2023 CLSI M100) | `fig02_resistance_heatmap.py` | Python |
| Fig 3  | Study flow diagram (case population → isolates → QC → species → ST39 → outcomes) | `fig03_flow_diagram.py` | Python |
| Fig 4  | Epidemiological curves — 3 panels (Kp clinical, Kp environmental, other species) | `fig04_epi_curve.qmd` | R (Quarto) |
| Fig 5  | ST39 multi-panel: tree + AMR + metadata + plasmid + timeline | `figS3_st39_plasmid.qmd` | R (Quarto) |
| Fig 6  | Global ST39 clone distribution and AMR by continent | `fig06_st39_global_clones.qmd` | R (Quarto) |
| Fig S1 | Sources of bacterial contamination in labour and neonatal wards | `figS1_ward_contamination.md` | Assembled in Illustrator |
| Fig S2 | *K. pneumoniae* phylogeny annotated with ST, K-locus, virulence, and AMR | `fig05_kpn_phylotree_annotated.qmd` | R (Quarto) |
| Fig S3 | Transmission cluster plots (*Kp* and *Kqp*) | `figS2_transmission_clusters.md` | R (see note) |
| Appendix | Comparative genomic organisation of chromosomal AMR locus (38277B1 vs 38833B1) | `figAppendix_clinker_amr_locus.md` | clinker |

---

## Requirements

### Python (Figs 1, 2, 3)

```
python >= 3.9
pandas
geopandas
matplotlib
shapely
seaborn
numpy
```

Install with:
```bash
pip install pandas geopandas matplotlib shapely seaborn numpy
```

### R / Quarto (Figs 4, 5, 6, S2)

R packages:
```r
install.packages(c(
  "tidyverse", "ggplot2", "readxl", "patchwork",
  "lubridate", "scales", "knitr", "ggnewscale",
  "RColorBrewer", "ape"
))

# Bioconductor packages (ggtree only — ggtreeExtra no longer required)
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("ggtree")
```

Quarto: https://quarto.org/docs/get-started/

### clinker (Appendix figure)

```bash
pip install clinker
```

---

## Data

All data files are described in `data/README.md`. Key inputs:

- **Supplementary data** (`FileS1_to_FileS10.xlsx`, sheet `FileS3`) — isolate metadata including ST, collection dates, and sample type. Available with the published paper.
- **Gambia administrative shapefile** — from GADM (https://gadm.org/download_country.html, country = Gambia, level 1). Free for academic use.
- **Figure 1 epidemic curve** — monthly case and death totals from the original outbreak report (`fig01_epi_curve.csv`) and WGS-confirmed clinical *K. pneumoniae* isolates (`fig01_clinical_kpn_isolates.csv`, from Supplementary File 1). Included in `data/`.
- **Pathogenwatch global *K. pneumoniae* ST39 collection** (deduplicated, 750 isolates, 22 September 2026) — https://pathogen.watch/collections/ryKcxCmfzKKegsAUkueS8P-updated-st-39-collection-deduplicated-22-september-20261703
- **Phylogenetic tree** — IQ-TREE2 maximum likelihood tree of ST39 isolates (`st39_cluster.treefile`). Included in `data/`.
- **Transmission cluster assignments** — output of genomic cluster analysis (`clusters_data_final.csv`). Included in `data/`.
- **Plasmid coverage data** — BWA-MEM alignment of ST39 assemblies against pNS39_A reference plasmid (`pNS39_A_alignment_coverage_summary.tsv`). Included in `data/`.
- **Chromosomal AMR locus GenBank files** — extracted from complete hybrid assemblies of 38277B1 and 38833B1 (`38277B1_locus.gbk`, `38833B1_locus.gbk`). Included in `data/`.

---

## Usage

### Python scripts

Run from the `code/` directory:
```bash
python fig01_timeline_and_map.py
python fig01A_gambia_map.py
python fig02_resistance_heatmap.py
```

### Quarto documents

Render from the `code/` directory:
```bash
quarto render fig04_epi_curve.qmd
quarto render fig05_kpn_phylotree_annotated.qmd
quarto render fig06_st39_global_clones.qmd
quarto render figS3_st39_plasmid.qmd
```

Or open in RStudio and use the Render button.

### clinker (Appendix)

```bash
clinker 38277B1_locus.gbk 38833B1_locus.gbk \
    --output clinker_tn3_replacement.html \
    --identity 0.3
```

See `figAppendix_clinker_amr_locus.md` for full details.

**Before running**, update the file paths in each script to point to your local copies of the data files. All paths are defined at the top of each script in a clearly marked `--- Paths ---` or `file-paths` section.

---

## Contact

Ebenezer Foster-Nyarko — LSHTM  
ebenezer.foster-nyarko2@lshtm.ac.uk
