#!/usr/bin/env python3
"""
Figure S1 — Chromosomal blaCTX-M-15 mobile element replacement

Paper: Foster-Nyarko E et al. medRxiv (2026). https://doi.org/10.64898/2026.03.03.26347025.

Schematic diagram comparing the chromosomal region flanking the resistance locus
in a reference ST39 strain (38833B1, Tn3 composite transposon with catA1) vs
the outbreak ST39 strain (38277B1, 11.2 kb mosaic resistance island with
blaCTX-M-15 and aac(3)-IId).

This figure does not require external data files — all genomic coordinates
and annotations are hard-coded based on manual inspection of the assembly
comparison (Clinker / BLAST alignment).

Requirements:
    pip install matplotlib numpy
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

plt.style.use('seaborn-v0_8-paper')
fig, ax = plt.subplots(figsize=(16, 9))

# ---- Layout positions ----
y_38833 = 7.5   # Reference strain (top)
y_38277 = 3.0   # Outbreak strain (bottom)

flank_width = 2
gap_38833   = 16    # ~35 kb Tn3 transposon
gap_38277   = 5.5   # 11.2 kb resistance island

# ---- Colours ----
color_flank      = '#A8DADC'  # Light blue  — conserved flanks
color_tn3        = '#F4A261'  # Orange      — Tn3 transposon
color_resistance = '#E63946'  # Red         — new resistance island
color_is         = '#457B9D'  # Dark blue   — IS elements
color_cat        = '#FFB703'  # Amber       — catA1 (old resistance)
color_ctx        = '#C1121F'  # Dark red    — CTX-M-15 (new resistance)

# ============================================================
# 38833B1 — Reference strain (top)
# ============================================================

# Upstream flank
ax.add_patch(FancyBboxPatch((1, y_38833 - 0.35), flank_width, 0.7,
    boxstyle="round,pad=0.05", edgecolor='black', facecolor=color_flank, linewidth=2.5))
ax.text(2, y_38833 + 0.9, 'Upstream\nFlank', ha='center', va='bottom', fontsize=10, weight='bold')
ax.text(2, y_38833, '100% ID', ha='center', va='center', fontsize=8, style='italic')

# 35 kb Tn3 composite transposon
ax.add_patch(FancyBboxPatch((3.3, y_38833 - 0.45), gap_38833, 0.9,
    boxstyle="round,pad=0.05", edgecolor='black', facecolor=color_tn3, linewidth=2.5))

# Tn3 transposases (left)
ax.add_patch(Rectangle((3.5, y_38833 - 0.35), 2.5, 0.7,
    edgecolor='black', facecolor='#E76F51', linewidth=1.5))
ax.text(4.75, y_38833, 'Tn3\ntransposases', ha='center', va='center', fontsize=8, weight='bold', color='white')

# catA1 (chloramphenicol resistance)
ax.add_patch(Rectangle((6.2, y_38833 - 0.4), 1.8, 0.8,
    edgecolor='black', facecolor=color_cat, linewidth=2.5))
ax.text(7.1, y_38833, 'catA1', ha='center', va='center', fontsize=10, weight='bold')
ax.text(7.1, y_38833 - 0.75, '(Chloramphenicol\nResistance)', ha='center', va='top', fontsize=7, style='italic')

# TnAs3-like elements
ax.add_patch(Rectangle((8.2, y_38833 - 0.35), 3.0, 0.7,
    edgecolor='black', facecolor='#E76F51', linewidth=1.5))
ax.text(9.7, y_38833, 'TnAs3-like\nelements', ha='center', va='center', fontsize=8, weight='bold', color='white')

# More Tn3 machinery
ax.add_patch(Rectangle((11.4, y_38833 - 0.35), 3.5, 0.7,
    edgecolor='black', facecolor='#E76F51', linewidth=1.5))
ax.text(13.15, y_38833, 'Tn3 family\ntransposon\nmachinery', ha='center', va='center', fontsize=8, weight='bold', color='white')

ax.text(11.3, y_38833 + 1.3, '~35 kb Tn3 Composite Transposon',
    ha='center', va='bottom', fontsize=12, weight='bold', color='#E76F51')
ax.text(11.3, y_38833 + 1.0, 'Obsolete resistance (chloramphenicol)',
    ha='center', va='bottom', fontsize=10, style='italic', color='#994400')

# Downstream flank
ax.add_patch(FancyBboxPatch((19.5, y_38833 - 0.35), flank_width, 0.7,
    boxstyle="round,pad=0.05", edgecolor='black', facecolor=color_flank, linewidth=2.5))
ax.text(20.5, y_38833 + 0.9, 'Downstream\nFlank', ha='center', va='bottom', fontsize=10, weight='bold')
ax.text(20.5, y_38833, '99.76% ID', ha='center', va='center', fontsize=8, style='italic')

# Strain label
ax.text(-0.2, y_38833, '38833B1\n(Reference)\nST39-B', ha='right', va='center',
    fontsize=12, weight='bold',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=1.5))

# Size bracket
ax.annotate('', xy=(3.3, y_38833 - 1.4), xytext=(19.5, y_38833 - 1.4),
    arrowprops=dict(arrowstyle='<->', color='black', lw=2))
ax.text(11.4, y_38833 - 1.75, '~35 kb', ha='center', fontsize=11, weight='bold')

# ============================================================
# 38277B1 — Outbreak strain (bottom)
# ============================================================

# Upstream flank
ax.add_patch(FancyBboxPatch((1, y_38277 - 0.35), flank_width, 0.7,
    boxstyle="round,pad=0.05", edgecolor='black', facecolor=color_flank, linewidth=2.5))

# 11.2 kb resistance island
ax.add_patch(FancyBboxPatch((3.3, y_38277 - 0.55), gap_38277, 1.1,
    boxstyle="round,pad=0.05", edgecolor='black', facecolor=color_resistance, linewidth=3))

# Novel IS (left)
ax.add_patch(Rectangle((3.4, y_38277 - 0.45), 0.7, 0.9,
    edgecolor='black', facecolor=color_is, linewidth=1.5))
ax.text(3.75, y_38277 - 1.0, 'Novel\nIS', ha='center', va='top', fontsize=8, weight='bold')

# Tn2 remnant
ax.add_patch(Rectangle((4.2, y_38277 - 0.4), 0.6, 0.8,
    edgecolor='black', facecolor='#780000', linewidth=1.5))
ax.text(4.5, y_38277, 'Tn2', ha='center', va='center', fontsize=7, color='white', weight='bold')
ax.text(4.5, y_38277 - 1.0, '(promoter\nsource)', ha='center', va='top', fontsize=6, style='italic')

# aac(3)-IId (aminoglycoside resistance)
ax.add_patch(Rectangle((4.9, y_38277 - 0.35), 0.9, 0.7,
    edgecolor='black', facecolor='#C1121F', linewidth=1.5))
ax.text(5.35, y_38277, 'aac(3)-IId', ha='center', va='center', fontsize=8, color='white', weight='bold')
ax.text(5.35, y_38277 - 1.0, '(Gentamicin)', ha='center', va='top', fontsize=7, style='italic')

# Intergenic regulatory region
ax.add_patch(Rectangle((5.9, y_38277 - 0.25), 1.1, 0.5,
    edgecolor='gray', facecolor='#FFE5E5', linewidth=1, linestyle='--'))
ax.text(6.45, y_38277, 'Reg.', ha='center', va='center', fontsize=6)

# blaCTX-M-15 (ESBL)
ax.add_patch(Rectangle((7.1, y_38277 - 0.4), 1.0, 0.8,
    edgecolor='black', facecolor=color_ctx, linewidth=2))
ax.text(7.6, y_38277, 'blaCTX-M-15', ha='center', va='center', fontsize=9, color='white', weight='bold')
ax.text(7.6, y_38277 - 1.0, '(Cefotaxime)', ha='center', va='top', fontsize=7, style='italic')

# ISKpn14
ax.add_patch(Rectangle((8.2, y_38277 - 0.45), 0.7, 0.9,
    edgecolor='black', facecolor=color_is, linewidth=1.5))
ax.text(8.55, y_38277 - 1.0, 'ISKpn14', ha='center', va='top', fontsize=8, weight='bold')
ax.text(8.55, y_38277 - 1.3, '(9 bp TSD)', ha='center', va='top', fontsize=6, style='italic')

ax.text(6.05, y_38277 + 1.4, '11.2 kb Mosaic Resistance Island',
    ha='center', va='bottom', fontsize=12, weight='bold', color='darkred')
ax.text(6.05, y_38277 + 1.1, 'Modern frontline antibiotic resistance',
    ha='center', va='bottom', fontsize=10, style='italic', color='#990000')
ax.text(6.05, y_38277 + 0.85, '(Cefotaxime + Gentamicin = WHO-recommended therapy)',
    ha='center', va='bottom', fontsize=9, color='#660000')

# Downstream flank
ax.add_patch(FancyBboxPatch((9.0, y_38277 - 0.35), flank_width, 0.7,
    boxstyle="round,pad=0.05", edgecolor='black', facecolor=color_flank, linewidth=2.5))

# Strain label
ax.text(-0.2, y_38277, '38277B1\n(Outbreak)\nST39-B', ha='right', va='center',
    fontsize=12, weight='bold', color='darkred',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFE5E5', edgecolor='darkred', linewidth=1.5))

# Size bracket
ax.annotate('', xy=(3.3, y_38277 - 2.0), xytext=(9.0, y_38277 - 2.0),
    arrowprops=dict(arrowstyle='<->', color='darkred', lw=2))
ax.text(6.15, y_38277 - 2.35, '11.2 kb', ha='center', fontsize=11, weight='bold', color='darkred')

# ============================================================
# Connecting dashed lines (conserved flanks)
# ============================================================
ax.plot([2, 2],   [y_38833 - 0.5, y_38277 + 0.5], 'k--', linewidth=1.5, alpha=0.6)
ax.plot([20.5, 10], [y_38833 - 0.5, y_38277 + 0.5], 'k--', linewidth=1.5, alpha=0.6)

# ============================================================
# Central annotation — resistance upgrade event
# ============================================================
ax.add_patch(FancyBboxPatch((11.5, 4.8), 6, 1.3,
    boxstyle="round,pad=0.3", edgecolor='black', facecolor='#FFF3CD', linewidth=3))
ax.text(14.5, 5.8, 'ANTIMICROBIAL RESISTANCE', ha='center', va='center', fontsize=13, weight='bold')
ax.text(14.5, 5.45, 'UPGRADE EVENT', ha='center', va='center', fontsize=13, weight='bold')
ax.text(14.5, 5.1, 'Mobile Element Replacement', ha='center', va='center', fontsize=10, style='italic', color='#666666')

ax.add_patch(FancyArrowPatch((11.3, y_38833 - 0.8), (7.6, y_38277 + 0.9),
    arrowstyle='->', mutation_scale=40, linewidth=4, color='#E63946', alpha=0.7,
    connectionstyle="arc3,rad=0.3"))

ax.add_patch(FancyBboxPatch((18.2, 4.8), 5, 1.3,
    boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white', linewidth=2))
ax.text(20.7, 5.75, 'Net Change:', ha='center', va='center', fontsize=11, weight='bold')
ax.text(20.7, 5.45, '−34,988 bp', ha='center', va='center', fontsize=11, color='blue')
ax.text(20.7, 5.15, '(35 kb → 11.2 kb)', ha='center', va='center', fontsize=9, style='italic')

ax.text(14.5, 4.3, 'LOST: catA1 (duplicate copy)', ha='center', va='center',
    fontsize=10, weight='bold', color='#994400',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFE5CC', edgecolor='#994400', linewidth=1.5))
ax.text(14.5, 3.8, 'GAINED: blaCTX-M-15 + aac(3)-IId', ha='center', va='center',
    fontsize=10, weight='bold', color='darkred',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFE5E5', edgecolor='darkred', linewidth=1.5))
ax.text(14.5, 3.2, '↓ Adaptive Evolution ↓', ha='center', va='center',
    fontsize=11, style='italic', weight='bold', color='#666666')
ax.text(14.5, 2.7, 'Obsolete → Modern Antibiotics', ha='center', va='center',
    fontsize=10, style='italic', color='#666666')
ax.text(14.5, 2.4, 'Chloramphenicol → Cephalosporins + Aminoglycosides', ha='center', va='center',
    fontsize=9, color='#666666')

# Key features box
features_text = (
    "Key Features:\n"
    "• Recombination hotspot (MGE exchange site)\n"
    "• No fitness cost (MGE → MGE, no housekeeping genes lost)\n"
    "• Genomic streamlining (23.8 kb reduction)\n"
    "• Duplicate catA1 eliminated (ancestral copy retained in integron)\n"
    "• Response to antibiotic selection pressure"
)
ax.text(1.5, 1.2, features_text, ha='left', va='top', fontsize=9, family='monospace',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#F0F8FF', edgecolor='gray', linewidth=1.5))

# ============================================================
# Legend
# ============================================================
legend_elements = [
    mpatches.Patch(facecolor=color_flank,      edgecolor='black', label='Conserved Chromosomal Flanks (99.76–100% ID)'),
    mpatches.Patch(facecolor=color_tn3,        edgecolor='black', label='Tn3 Composite Transposon (replaced)'),
    mpatches.Patch(facecolor=color_cat,        edgecolor='black', label='catA1 — Chloramphenicol Resistance (obsolete)'),
    mpatches.Patch(facecolor=color_resistance, edgecolor='black', label='Mosaic Resistance Island (acquired)'),
    mpatches.Patch(facecolor=color_ctx,        edgecolor='black', label='blaCTX-M-15 — ESBL (modern, frontline)'),
    mpatches.Patch(facecolor=color_is,         edgecolor='black', label='IS Elements (insertion sequences)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
          framealpha=0.95, title='Legend', title_fontsize=10)

# ============================================================
# Formatting and save
# ============================================================
ax.set_xlim(-1.5, 24)
ax.set_ylim(1, 9.5)
ax.axis('off')
plt.title(
    'Antimicrobial Resistance Upgrade Through Mobile Element Replacement\n'
    'K. pneumoniae ST39 Outbreak Clone vs Reference Strain',
    fontsize=15, weight='bold', pad=20)

plt.tight_layout()
plt.savefig('figS1_chromosomal_blactxm.pdf', bbox_inches='tight')
plt.savefig('figS1_chromosomal_blactxm.png', dpi=300, bbox_inches='tight')
print("Saved: figS1_chromosomal_blactxm.pdf and .png")
plt.show()
