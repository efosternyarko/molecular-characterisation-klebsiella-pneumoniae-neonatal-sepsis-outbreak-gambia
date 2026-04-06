#!/usr/bin/env python3
"""
Figure 2 — Clustered antimicrobial resistance heatmap (clinical and environmental isolates)

Paper: Foster-Nyarko E et al. medRxiv (2026). https://doi.org/10.64898/2026.03.03.26347025.

Produces a hierarchically clustered heatmap of AMR phenotype data for all
K. pneumoniae isolates, with row colour bars distinguishing clinical vs
environmental samples and IV-fluid vs other environmental sources.
ST39 isolates are labelled with "(ST39)" in their sample IDs.

Requirements:
    pip install pandas numpy seaborn matplotlib

Data (place in data/ directory):
    kpn_clinical_AMR.csv    — Clinical isolate AMR data
    kpn_environmental_AMR.csv — Environmental isolate AMR data

    Both CSVs must have:
        - sample_id      : isolate identifier
        - status         : e.g. "ST39", "Non-ST39" (used to label ST39 isolates)
        - source_type    : (environmental file only) e.g. "IV bag", "water", etc.
        - Antibiotic columns: values are R / I / S (or Resistant/Susceptible/Intermediate)

    Amoxicillin-clavulanate and ampicillin columns are excluded automatically.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['font.family'] = 'Helvetica'
plt.rcParams['font.size'] = 12

# ---------- Paths ----------
clin_path = Path("data/kpn_clinical_AMR.csv")
env_path  = Path("data/kpn_environmental_AMR.csv")
out_pdf   = Path("fig02_resistance_heatmap.pdf")
out_svg   = Path("fig02_resistance_heatmap.svg")


# ---------- Helpers ----------
def clean_abx_names(cols):
    out = []
    for v in cols:
        v2 = re.sub(r"[^A-Za-z0-9+/_-]", "_", str(v))
        v2 = re.sub(r"__+", "_", v2).strip("_")
        out.append(v2)
    return out


def format_antibiotic_name(name):
    name = name.replace('_', '-')
    if 'trimethoprim' in name.lower() and 'sulfa' in name.lower():
        return 'Trimethoprim-sulfamethoxazole'
    return name.title()


def is_amoxclav(name):
    return bool(re.search(r"amoxi|co-?amoxi|amoxicillin.*/?clav|amox.*clav|amclav", name, flags=re.I))


def is_ampicillin(name):
    return bool(re.search(r"^ampicillin$", name, flags=re.I))


def map_ast(series, treat_I_as=0.0):
    s = series.astype(str).str.strip().str.lower()
    s = s.replace({"": np.nan, "na": np.nan, "n/a": np.nan, "nan": np.nan,
                   "-": np.nan, "not tested": np.nan})
    s = s.replace({"r": "1", "resistant": "1",
                   "s": "0", "susceptible": "0",
                   "i": str(treat_I_as), "intermediate": str(treat_I_as)})
    return pd.to_numeric(s, errors="coerce")


# ---------- Load ----------
clin = pd.read_csv(clin_path)
env  = pd.read_csv(env_path)

# Keep original sample IDs
clin['sample_id'] = clin['sample_id'].astype(str).str.strip()
env['sample_id']  = env['sample_id'].astype(str).str.strip()

# Label ST39 isolates in the display ID
if 'status' in clin.columns:
    clin['sample_id_display'] = clin.apply(
        lambda row: f"{row['sample_id']} (ST39)" if 'ST39' in str(row['status']).upper()
        else row['sample_id'], axis=1)
else:
    clin['sample_id_display'] = clin['sample_id']

if 'status' in env.columns:
    env['sample_id_display'] = env.apply(
        lambda row: f"{row['sample_id']} (ST39)" if 'ST39' in str(row['status']).upper()
        else row['sample_id'], axis=1)
else:
    env['sample_id_display'] = env['sample_id']

# ---------- Identify columns ----------
metadata_cols_clin = ['sample_id', 'sample_id_display']
if 'status' in clin.columns:
    metadata_cols_clin.append('status')
if 'Status' in clin.columns:
    metadata_cols_clin.append('Status')

metadata_cols_env = ['sample_id', 'sample_id_display', 'status', 'source_type']

ast_cols_clin = [c for c in clin.columns if c not in metadata_cols_clin]
ast_cols_env  = [c for c in env.columns  if c not in metadata_cols_env]

# Rename AST columns (normalise special characters)
clin_ren = clin.copy()
env_ren  = env.copy()
clin_ren = clin_ren.rename(columns=dict(zip(ast_cols_clin, clean_abx_names(ast_cols_clin))))
env_ren  = env_ren.rename(columns=dict(zip(ast_cols_env, clean_abx_names(ast_cols_env))))

ast_cols_clin = [c for c in clin_ren.columns if c not in metadata_cols_clin]
ast_cols_env  = [c for c in env_ren.columns  if c not in metadata_cols_env]

# Exclude amoxicillin-clavulanate and ampicillin
ast_cols_clin = [c for c in ast_cols_clin if not is_amoxclav(c) and not is_ampicillin(c)]
ast_cols_env  = [c for c in ast_cols_env  if not is_amoxclav(c) and not is_ampicillin(c)]

all_abx = sorted(set(ast_cols_clin) | set(ast_cols_env))

# ---------- Build long format ----------
long_clin = (clin_ren[['sample_id_display'] + ast_cols_clin]
             .melt(id_vars=['sample_id_display'], var_name="Antibiotic", value_name="Call")
             .assign(Value=lambda d: map_ast(d["Call"]),
                     SampleType="Clinical",
                     EnvSubtype=np.nan)
             .rename(columns={'sample_id_display': "Sample"})
             )[["Sample", "Antibiotic", "Value", "SampleType", "EnvSubtype"]]

long_env = (env_ren[['sample_id_display', 'source_type'] + ast_cols_env]
            .melt(id_vars=['sample_id_display', 'source_type'], var_name="Antibiotic", value_name="Call")
            .assign(Value=lambda d: map_ast(d["Call"]),
                    SampleType="Environmental")
            .assign(EnvSubtype=lambda d: np.where(
                d['source_type'].str.contains(r"iv|bag", case=False, na=False), "IV", "Other"))
            .rename(columns={'sample_id_display': "Sample"})
            )[["Sample", "Antibiotic", "Value", "SampleType", "EnvSubtype"]]

long_all = pd.concat([long_clin, long_env], ignore_index=True)
long_all = long_all[long_all["Antibiotic"].isin(all_abx)]
long_all["Antibiotic"] = long_all["Antibiotic"].apply(format_antibiotic_name)

# ---------- Pivot to wide matrix ----------
mat = long_all.pivot_table(index="Sample", columns="Antibiotic", values="Value", aggfunc="first")

# ---------- Row annotations ----------
ann = (long_all[["Sample", "SampleType", "EnvSubtype"]]
       .drop_duplicates()
       .set_index("Sample")
       .reindex(mat.index))

cont_colors = {
    "Clinical": "#377EB8",
    "Environmental": "#F7B237"
}
envsub_colors = {
    "IV fluids": "#D66518",
    "Other": "#CCCCCC",
    "Not applicable": "#89D5F4"
}

cmap_heatmap = LinearSegmentedColormap.from_list("res_map", ["white", "#d73027"])

row_colors = pd.DataFrame({
    "Sample type": ann["SampleType"].map(cont_colors),
    "Env source":  ann["EnvSubtype"].map(
        lambda x: envsub_colors.get(
            "IV fluids" if x == "IV" else ("Other" if pd.notna(x) else "Not applicable")))
}, index=mat.index)

# ---------- Clustermap ----------
n_samples = len(mat)
height = max(12, n_samples * 0.4)

g = sns.clustermap(
    data=mat,
    cmap=cmap_heatmap,
    row_cluster=True,
    col_cluster=True,
    linewidths=0.0,
    figsize=(14, height),
    row_colors=row_colors,
    vmin=0, vmax=1,
    yticklabels=True,
    cbar_pos=None
)

if hasattr(g, 'ax_cbar') and g.ax_cbar is not None:
    g.ax_cbar.set_visible(False)

g.ax_heatmap.set_xlabel('Antibiotic', fontsize=14)
g.ax_heatmap.set_ylabel('Sample', fontsize=14)
g.ax_heatmap.tick_params(axis='y', labelsize=12)
g.ax_heatmap.tick_params(axis='x', labelsize=12)
plt.setp(g.ax_heatmap.get_xticklabels(), rotation=45, ha='right', fontsize=12)
plt.setp(g.ax_heatmap.get_yticklabels(), fontsize=12)

# Sample type legend
handles_sample = [plt.Line2D([0], [0], marker='s', color='w',
                              markerfacecolor=c, markersize=12, label=k)
                  for k, c in cont_colors.items()]
legend1 = g.ax_row_dendrogram.legend(handles=handles_sample,
                                      title="Sample type",
                                      loc="lower left", bbox_to_anchor=(0.05, -0.20),
                                      fontsize=12, title_fontsize=12, frameon=True)

# Environmental source legend
handles_env = [plt.Line2D([0], [0], marker='s', color='w',
                           markerfacecolor=c, markersize=12, label=k)
               for k, c in envsub_colors.items()]
g.ax_row_dendrogram.legend(handles=handles_env,
                            title="Env source",
                            loc="lower left", bbox_to_anchor=(0.05, -0.10),
                            fontsize=12, title_fontsize=12, frameon=True)
g.ax_row_dendrogram.add_artist(legend1)

# Resistance key
g.ax_heatmap.text(1.00, 1.05, "Red = Resistant\nWhite = Susceptible",
                  transform=g.ax_heatmap.transAxes,
                  fontsize=12, verticalalignment='top', horizontalalignment='left',
                  bbox=dict(boxstyle='round', facecolor='white',
                            edgecolor='black', linewidth=1))

plt.tight_layout()
g.savefig(out_pdf, dpi=300, bbox_inches="tight")
g.savefig(out_svg, dpi=300, bbox_inches="tight")
print(f"Saved: {out_pdf}\n       {out_svg}")
