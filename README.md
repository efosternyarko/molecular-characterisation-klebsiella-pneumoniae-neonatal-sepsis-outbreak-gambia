# Molecular characterisation of a *Klebsiella pneumoniae* neonatal sepsis outbreak in a rural Gambian hospital

This repository contains the analysis scripts used to generate the figures in:

> Foster-Nyarko E, *et al.* **Molecular characterisation of a *Klebsiella pneumoniae* neonatal sepsis outbreak in a rural Gambian hospital: a retrospective genomic epidemiology investigation.** *medRxiv* (2026). https://doi.org/10.64898/2026.03.03.26347025

---

## Repository Structure

```
code/
├── README.md                          # This file
├── data/
│   └── README.md                      # Data sources and access instructions
├── fig01A_gambia_map.py               # Figure 1A — Map of The Gambia
├── fig02_resistance_heatmap.py        # Figure 2 — AMR heatmap (clinical + environmental)
├── fig03_flow_diagram.md              # Figure 3 — Study flow diagram (Illustrator)
├── fig04_epi_curve.qmd                # Figure 4 — Epidemiological curves
├── fig05_kpn_phylotree_annotated.qmd  # Figure 5 — All-Kp phylogenetic tree + metadata
├── fig06_st39_global_clones.qmd       # Figure 6 — Global ST39 clone distribution + AMR
├── figS1_ward_contamination.md        # Figure S1 — Ward contamination sources (Illustrator)
├── figS2_transmission_clusters.md     # Figure S2 — Transmission cluster analysis (note)
├── figS3_st39_plasmid.qmd             # Figure S3 — ST39 multi-panel with plasmid coverage
└── figAppendix_clinker_amr_locus.md   # Appendix — Chromosomal AMR locus comparison (clinker)
```

---

## Figures Summary

| Figure | Description | Script | Language |
|--------|-------------|--------|----------|
| Fig 1A | Map of The Gambia showing study sites | `fig01A_gambia_map.py` | Python |
| Fig 1B | Timeline of outbreak investigation | Assembled in Illustrator | — |
| Fig 2  | Clustered AMR heatmap (clinical + environmental isolates) | `fig02_resistance_heatmap.py` | Python |
| Fig 3  | Study flow diagram | Assembled in Illustrator | — |
| Fig 4  | Epidemiological curves — 3 panels (Kp clinical, Kp environmental, other species) | `fig04_epi_curve.qmd` | R (Quarto) |
| Fig 5  | *K. pneumoniae* phylogeny annotated with ST, K-locus, virulence, and AMR | `fig05_kpn_phylotree_annotated.qmd` | R (Quarto) |
| Fig 6  | Global ST39 clone distribution and AMR by continent | `fig06_st39_global_clones.qmd` | R (Quarto) |
| Fig S1 | Sources of bacterial contamination in labour and neonatal wards | `figS1_ward_contamination.md` | Assembled in Illustrator |
| Fig S2 | Transmission cluster plots (*Kp* and *Kqp*) | `figS2_transmission_clusters.md` | R (see note) |
| Fig S3 | ST39 multi-panel: tree + AMR + metadata + plasmid + timeline | `figS3_st39_plasmid.qmd` | R (Quarto) |
| Appendix | Comparative genomic organisation of chromosomal AMR locus (38277B1 vs 38833B1) | `figAppendix_clinker_amr_locus.md` | clinker |

> **Note on Fig 5:** The submitted figure was post-processed in Adobe Illustrator.
> The script reproduces the base R output. Asterisk labels for environmental isolates
> are coded in the script; final legend layout was adjusted manually.

---

## Requirements

### Python (Figs 1A, 2)

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

### R / Quarto (Figs 4, 5, 6, S3)

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
- **Pathogenwatch global *K. pneumoniae* ST39 collection** — https://pathogen.watch/collection/81f6uz2riu07-updatedst39globalcollection6nov25
- **Phylogenetic tree** — IQ-TREE2 maximum likelihood tree of ST39 isolates (`st39_cluster.treefile`). Included in `data/`.
- **Transmission cluster assignments** — output of genomic cluster analysis (`clusters_data_final.csv`). Included in `data/`.
- **Plasmid coverage data** — BWA-MEM alignment of ST39 assemblies against pNS39_A reference plasmid (`pNS39_A_alignment_coverage_summary.tsv`). Included in `data/`.
- **Chromosomal AMR locus GenBank files** — extracted from complete hybrid assemblies of 38277B1 and 38833B1 (`38277B1_locus.gbk`, `38833B1_locus.gbk`). Included in `data/`.

---

## Usage

### Python scripts

Run from the `code/` directory:
```bash
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

Ebenezer Foster-Nyarko — MRC Unit The Gambia at LSHTM  
ebenezer.foster-nyarko2@lshtm.ac.uk
