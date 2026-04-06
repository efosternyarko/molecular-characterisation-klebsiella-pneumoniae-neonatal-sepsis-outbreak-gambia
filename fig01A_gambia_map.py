#!/usr/bin/env python3
"""
Figure 1A — Map of The Gambia highlighting study sites (Bansang, Basse, Banjul)

Paper: Foster-Nyarko E et al. Microbial Genomics (2025). MGEN-S-26-00245.

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

# --- Region colours ---
unique_regions = gambia_map["NAME_1"].unique()
cmap = plt.cm.get_cmap("tab20", len(unique_regions))
region_colors = {region: cmap(i) for i, region in enumerate(unique_regions)}

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 8))

# Regions
for region in unique_regions:
    region_data = gambia_map[gambia_map["NAME_1"] == region]
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

# Region legend (outside right)
region_patches = [mpatches.Patch(color=region_colors[r], label=r) for r in unique_regions]
leg1 = ax.legend(handles=region_patches, title="Regions",
                 loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
ax.add_artist(leg1)

# Town legend (inside)
town_handles = [Line2D([0], [0], marker="o", linestyle="",
                       markerfacecolor=town_colors[t], markeredgecolor="black",
                       markersize=9, label=t) for t in town_colors]
ax.legend(handles=town_handles, title="Towns", loc="upper left", frameon=True)

ax.set_aspect("equal")
ax.set_axis_off()

plt.tight_layout()
plt.savefig(output_pdf_path, format="pdf", bbox_inches="tight")
print(f"Saved: {output_pdf_path}")
plt.show()
