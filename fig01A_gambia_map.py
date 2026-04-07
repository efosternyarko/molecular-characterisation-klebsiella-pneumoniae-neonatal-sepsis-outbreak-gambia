#!/usr/bin/env python3
"""
Figure 1A — Map of The Gambia highlighting study sites (Bansang, Basse, Banjul)

Paper: Foster-Nyarko E et al. medRxiv (2026). https://doi.org/10.64898/2026.03.03.26347025.

Requirements:
    pip install pandas geopandas matplotlib shapely

Data:
    gadm41_GMB_1.shp — Gambia administrative shapefile (level 1 = regions)
    Download from https://gadm.org/download_country.html (Gambia, level 1)
    Place the .shp (and associated .dbf, .prj, .shx) files in ../data/
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# --- Paths ---
gambia_shapefile_path = "data/gadm41_GMB_1.shp"
output_pdf_path = "fig01A_gambia_map.pdf"

# --- Load map ---
gambia_map = gpd.read_file(gambia_shapefile_path)

# --- Study sites ---
town_data = {
    "Town":      ["Basse",    "Bansang",  "Banjul"],
    "Latitude":  [13.3096,    13.4333,    13.4549],
    "Longitude": [-14.2136,  -14.6461,   -16.5790],
}
town_colors = {"Basse": "orange", "Bansang": "purple", "Banjul": "red"}

df_towns = pd.DataFrame(town_data)
geometry = [Point(xy) for xy in zip(df_towns["Longitude"], df_towns["Latitude"])]
gdf_towns = gpd.GeoDataFrame(df_towns, geometry=geometry, crs="EPSG:4326")

# --- Region name mapping (shapefile → display name) ---
region_rename = {
    "Banjul":           "Greater Banjul",
    "Maccarthy Island": "Central River",
}
gambia_map["display_name"] = gambia_map["NAME_1"].map(
    lambda x: region_rename.get(x, x)
)

# Display order for legend
region_order = ["Greater Banjul", "Lower River", "Central River",
                "North Bank", "Upper River", "Western"]

unique_regions = region_order  # use ordered display names
cmap = plt.cm.get_cmap("tab20", len(unique_regions))
region_colors = {region: cmap(i) for i, region in enumerate(unique_regions)}

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 8))

# Regions
for region in unique_regions:
    region_data = gambia_map[gambia_map["display_name"] == region]
    region_data.plot(ax=ax, color=region_colors[region], edgecolor="black", linewidth=0.6)

# Town points
for _, row in gdf_towns.iterrows():
    ax.scatter(row.geometry.x, row.geometry.y,
               s=110, color=town_colors[row["Town"]], edgecolor="black", zorder=5)

# Town labels
for _, row in gdf_towns.iterrows():
    ax.annotate(row["Town"],
                xy=(row.geometry.x, row.geometry.y),
                xytext=(4, 4), textcoords="offset points",
                fontsize=12, color="black",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, pad=1.5))

# Region legend — placed inside the figure on the right using figure coordinates
# so it is never clipped regardless of bbox settings.
region_patches = [mpatches.Patch(color=region_colors[r], label=r) for r in unique_regions]
leg1 = fig.legend(handles=region_patches, title="Regions",
                  loc="center right",
                  bbox_to_anchor=(0.98, 0.5),
                  bbox_transform=fig.transFigure,
                  frameon=True, framealpha=0.85, edgecolor="grey",
                  fontsize=10, title_fontsize=11,
                  handlelength=1.2, handleheight=1.2)

# Town legend — lower left, inside axes
town_handles = [Line2D([0], [0], marker="o", linestyle="",
                       markerfacecolor=town_colors[t], markeredgecolor="black",
                       markersize=9, label=t) for t in town_colors]
ax.legend(handles=town_handles, title="Study sites", loc="upper left",
          bbox_to_anchor=(-0.13, 1.05),
          frameon=True, fontsize=10, title_fontsize=11)

ax.set_aspect("equal")
ax.set_axis_off()

# Reserve right margin for region legend, then save
fig.subplots_adjust(right=0.78)
plt.savefig(output_pdf_path, format="pdf", bbox_inches="tight")
print(f"Saved: {output_pdf_path}")
plt.show()
