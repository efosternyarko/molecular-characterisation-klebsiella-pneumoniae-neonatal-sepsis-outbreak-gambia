# Appendix Figure — Comparative Genomic Organisation of the Chromosomal AMR Locus

**Caption:** Comparative genomic organisation of the chromosomal antimicrobial resistance
locus in *K. pneumoniae* ST39 strains 38833B1 and 38277B1. Gene cluster comparison
generated with clinker (Gilchrist & Chooi, *Bioinformatics* 2021).

The interactive HTML output is provided as a supplementary file:
`clinker_tn3_replacement_v2.html`

---

## Tool

**clinker** — automatic generation of gene cluster comparison figures  
- GitHub: https://github.com/gamcil/clinker  
- Citation: Gilchrist CLM & Chooi YH. *Bioinformatics* 37(16):2473–2475 (2021).
  https://doi.org/10.1093/bioinformatics/btab007

---

## Inputs

Two GenBank (`.gbk`) files, each containing the chromosomal AMR locus region of
interest extracted from the respective ST39 assembly:

| File | Isolate | Description |
|------|---------|-------------|
| `38277B1_locus.gbk` | 38277B1 | Chromosomal AMR locus — Tn3-containing ancestor |
| `38833B1_locus.gbk` | 38833B1 | Chromosomal AMR locus — 11.2 kb resistance island replacement |

These were extracted from the complete hybrid assemblies (Illumina + ONT) of each
isolate. The locus boundaries were defined by flanking conserved chromosomal genes.

---

## Generating the input GenBank files

Extract the region of interest from a complete assembly using any of the following:

```bash
# Option A — using Biopython (if you know the coordinates)
python3 - <<'EOF'
from Bio import SeqIO
record = SeqIO.read("38277B1_assembly.gbk", "genbank")
locus = record[START:END]   # replace START/END with coordinates
locus.id = "38277B1_locus"
SeqIO.write(locus, "38277B1_locus.gbk", "genbank")
EOF

# Option B — using seqkit (coordinate-based extraction then re-annotate with Prokka)
seqkit subseq -r START:END 38277B1_assembly.fasta > 38277B1_locus.fasta
prokka --outdir 38277B1_locus_prokka --prefix 38277B1_locus 38277B1_locus.fasta
```

---

## Running clinker

```bash
# Install
pip install clinker

# Run comparison (produces interactive HTML)
clinker 38277B1_locus.gbk 38833B1_locus.gbk \
    --output clinker_tn3_replacement.html \
    --identity 0.3

# Open in a browser
open clinker_tn3_replacement.html
```

Key parameters used in this study:
- `--identity 0.3` — minimum amino acid identity to draw links between genes (30%)
- Default settings for all other parameters

---

## Notes

- The comparison shows the replacement of a Tn3 family transposon in 38277B1 with
  an 11.2 kb resistance island (containing *bla*CTX-M-15 and additional resistance
  genes) in 38833B1.
- Gene labels and colours were adjusted interactively in the clinker HTML interface
  before export to PDF/SVG for the final figure.
- The complete assemblies for 38277B1 and 38833B1 are deposited at NCBI under the
  BioProject associated with this study.

---

## Contact

Ebenezer Foster-Nyarko — ebenezer.foster-nyarko2@lshtm.ac.uk
