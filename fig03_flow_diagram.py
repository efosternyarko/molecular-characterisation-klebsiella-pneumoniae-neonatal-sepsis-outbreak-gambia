#!/usr/bin/env python3
"""
Figure 3 — Study sample flow diagram

Paper: Foster-Nyarko E et al. Molecular characterisation of a Klebsiella
pneumoniae neonatal sepsis outbreak in a rural Gambian hospital: a
retrospective genomic epidemiology investigation. Microb Genom (2026).

Recreated as a reproducible CONSORT-style flow diagram (the original was
built manually in Adobe Illustrator; this script replaces that with a
scripted equivalent so the figure can be regenerated and version-controlled).
Traces the study population from the original outbreak report (ref. 26)
through isolate availability, sequencing, quality control, species
confirmation, and identification of the ST39 outbreak clone, addressing
peer-review comments requesting a flow diagram linking case-level counts to
isolate-level and genomic outcomes. All counts are sourced from Table 1 and
the Results text of the main manuscript (values current as of the
18-Sep-2026 revision).

Requirements:
    pip install matplotlib

Output:
    fig03_flow_diagram.pdf
    fig03_flow_diagram.svg
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path as MplPath

plt.rcParams['font.family'] = 'Helvetica'

# ---------- Palette (validated categorical set; used sparingly) ----------
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
BORDER = "#8a8983"
MAIN_FILL = "#fcfcfb"
MAIN_BORDER = "#2a2a28"
EXCLUDE_FILL = "#f3f2ee"
EXCLUDE_BORDER = "#8a8983"
HIGHLIGHT_FILL = "#eaf2fc"      # light tint of categorical slot 1 (blue #2a78d6)
HIGHLIGHT_BORDER = "#2a78d6"
TERMINAL_FILL = "#f6f6f4"
TERMINAL_BORDER = "#8a8983"

FIG_W, FIG_H = 8.0, 12.6


def box(ax, cx, cy, w, h, lines, fill=MAIN_FILL, edge=MAIN_BORDER, lw=1.3,
        fontsize=8.3, bold_first=True, text_color=INK):
    p = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=lw, edgecolor=edge, facecolor=fill, zorder=3,
    )
    ax.add_patch(p)
    n = len(lines)
    for i, line in enumerate(lines):
        y = cy + (n - 1) / 2 * 0.155 - i * 0.155
        weight = "bold" if (bold_first and i == 0) else "normal"
        size = fontsize + 0.6 if (bold_first and i == 0) else fontsize
        ax.text(cx, y, line, ha="center", va="center", fontsize=size,
                 weight=weight, color=text_color, zorder=4, linespacing=1.3)
    return p


def varrow(ax, x, y_top, y_bottom, color=INK_SECONDARY, lw=1.2):
    ax.add_patch(FancyArrowPatch(
        (x, y_top), (x, y_bottom), arrowstyle="-|>", mutation_scale=11,
        linewidth=lw, color=color, zorder=2, shrinkA=0, shrinkB=0))


def elbow_arrow(ax, x_start, y_start, x_end, y_end, color=INK_SECONDARY, lw=1.1):
    """Right-angle connector: down/across then arrow into the side box."""
    verts = [(x_start, y_start), (x_end, y_start), (x_end, y_end)]
    codes = [MplPath.MOVETO, MplPath.LINETO, MplPath.LINETO]
    path = MplPath(verts, codes)
    ax.add_patch(FancyArrowPatch(
        path=path, arrowstyle="-|>", mutation_scale=10, linewidth=lw,
        color=color, zorder=2, shrinkA=0, shrinkB=1))


fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, 8)
ax.set_ylim(0, 12.6)
ax.axis("off")

CX = 3.15     # main trunk centre x
EXW = 3.7     # exclusion-box centre x
MW = 4.7      # main box width

# ---------------------------------------------------------------- Stage 1
y1 = 12.0
box(ax, CX, y1, MW, 0.95,
    ["Outbreak cases, Jan 2023–Mar 2024 (ref. 26)",
     "76 cases (57 neonates)"], fontsize=8.6)

# exclusion 1
ey1 = 10.95
box(ax, EXW, ey1, 2.55, 0.62,
    ["No isolate banked in frozen storage",
     "10 cases (6 neonates)"],
    fill=EXCLUDE_FILL, edge=EXCLUDE_BORDER, fontsize=7.2, bold_first=False,
    text_color=INK_SECONDARY, lw=1.0)
elbow_arrow(ax, CX, y1 - 0.60, EXW, ey1)

# ---------------------------------------------------------------- Stage 2
y2 = 10.15
box(ax, CX, y2, MW, 1.15,
    ["Isolates retrieved from frozen storage",
     "158 total",
     "66 clinical (2023) + 24 environmental +",
     "10 follow-up (2024) + 58 historical"], fontsize=8.0)
varrow(ax, CX, y1 - 0.475, y2 + 0.575)

# exclusion 2
ey2 = 9.10
box(ax, EXW, ey2, 2.55, 0.55,
    ["Not revived / failed DNA extraction",
     "10 isolates"],
    fill=EXCLUDE_FILL, edge=EXCLUDE_BORDER, fontsize=7.2, bold_first=False,
    text_color=INK_SECONDARY, lw=1.0)
elbow_arrow(ax, CX, y2 - 0.575, EXW, ey2)

# ---------------------------------------------------------------- Stage 3
y3 = 8.35
box(ax, CX, y3, MW, 0.95,
    ["Isolates revived for DNA extraction",
     "& sequencing (Table 1)", "148 total"], fontsize=8.3)
varrow(ax, CX, y2 - 0.575, y3 + 0.475)

# exclusion 3
ey3 = 7.30
box(ax, EXW, ey3, 2.55, 0.55,
    ["Failed whole-genome sequencing QC",
     "22 isolates"],
    fill=EXCLUDE_FILL, edge=EXCLUDE_BORDER, fontsize=7.2, bold_first=False,
    text_color=INK_SECONDARY, lw=1.0)
elbow_arrow(ax, CX, y3 - 0.475, EXW, ey3)

# ---------------------------------------------------------------- Stage 4
y4 = 6.55
box(ax, CX, y4, MW, 0.75,
    ["WGS data passing QC", "126 total"], fontsize=8.6)
varrow(ax, CX, y3 - 0.475, y4 + 0.375)

# ---------------------------------------------------------------- Stage 5: species split
y5 = 5.35
X_KP = 2.15
X_OTHER = 5.65
box(ax, X_KP, y5, 3.0, 1.15,
    ["K. pneumoniae sensu stricto", "90 isolates",
     "42 clinical (2023–24) + 8 environmental", "+ 40 historical (2012–2022)"],
    fill=HIGHLIGHT_FILL, edge=HIGHLIGHT_BORDER, fontsize=7.9, lw=1.4)
box(ax, X_OTHER, y5, 2.9, 1.35,
    ["Other species", "36 isolates",
     "K. quasipneumoniae (n=29), K. variicola (n=1),",
     "K. quasivariicola (n=1), K. africana (n=1),",
     "E. coli (n=4)"],
    fill=TERMINAL_FILL, edge=TERMINAL_BORDER, fontsize=7.1, bold_first=True,
    text_color=INK_SECONDARY, lw=1.0)

# branch connector from stage 4 to both stage-5 boxes
ax.add_patch(FancyArrowPatch((CX, y4 - 0.375), (X_KP, y5 + 0.575),
                              arrowstyle="-|>", mutation_scale=10,
                              linewidth=1.1, color=INK_SECONDARY, zorder=2,
                              connectionstyle="arc3,rad=0.0", shrinkA=0, shrinkB=0))
ax.add_patch(FancyArrowPatch((CX, y4 - 0.375), (X_OTHER, y5 + 0.675),
                              arrowstyle="-|>", mutation_scale=10,
                              linewidth=1.1, color=INK_SECONDARY, zorder=2,
                              connectionstyle="arc3,rad=0.0", shrinkA=0, shrinkB=0))

# ---------------------------------------------------------------- Stage 6: temporal split within K. pneumoniae
y6 = 3.85
X_2324 = 1.65
X_HIST = 4.6
varrow(ax, X_KP, y5 - 0.575, y6 + 0.575)
box(ax, X_2324, y6, 2.55, 1.15,
    ["2023–2024 clinical + environmental", "50 isolates",
     "(42 clinical + 8 environmental)"],
    fill=HIGHLIGHT_FILL, edge=HIGHLIGHT_BORDER, fontsize=7.7, lw=1.3)
box(ax, X_HIST, y6, 2.55, 1.15,
    ["Historical (2012–2022)", "40 isolates",
     "29 sequence types; ST39 not detected"],
    fill=TERMINAL_FILL, edge=TERMINAL_BORDER, fontsize=7.4, bold_first=True,
    text_color=INK_SECONDARY, lw=1.0)
ax.add_patch(FancyArrowPatch((X_KP, y5 - 0.575), (X_HIST, y6 + 0.575),
                              arrowstyle="-|>", mutation_scale=10,
                              linewidth=1.1, color=INK_SECONDARY, zorder=2,
                              shrinkA=0, shrinkB=0))

# ---------------------------------------------------------------- Stage 7: ST39 clone
y7 = 2.25
box(ax, X_2324, y7, 3.05, 1.35,
    ["ST39-KL62 outbreak clone", "29 clinical cases",
     "+ 3 environmental (IV-fluid) isolates",
     "28/29 clinical isolates formed a single",
     "transmission cluster (0–5 core-gene SNPs)"],
    fill=HIGHLIGHT_FILL, edge=HIGHLIGHT_BORDER, fontsize=7.5, lw=1.4)
varrow(ax, X_2324, y6 - 0.575, y7 + 0.675)

# ---------------------------------------------------------------- Stage 8: outcomes
y8 = 0.55
box(ax, X_2324, y8, 3.05, 1.05,
    ["Outcomes", "16 deaths among 29 cases",
     "(55% case fatality)"],
    fill="#ffffff", edge=HIGHLIGHT_BORDER, fontsize=8.2, lw=1.6)
varrow(ax, X_2324, y7 - 0.675, y8 + 0.525)

plt.tight_layout()
fig.savefig("fig03_flow_diagram.pdf", bbox_inches="tight")
fig.savefig("fig03_flow_diagram.svg", bbox_inches="tight")
print("Saved fig03_flow_diagram.pdf and .svg")
