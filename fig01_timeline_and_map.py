#!/usr/bin/env python3
"""
Figure 1 — Outbreak timeline (A) and map of study sites (B)

Paper: Foster-Nyarko E et al. medRxiv (2026). https://doi.org/10.64898/2026.03.03.26347025.

Panel A: monthly K. pneumoniae sepsis cases (stacked by whole-genome sequencing result) with deaths,
annotated with the outbreak investigation and environmental sampling events.
Panel B: map of The Gambia showing Bansang, Basse and Banjul.

Requirements:
    pip install pandas geopandas matplotlib shapely

Data (in data/):
    fig01_epi_curve.csv             — monthly case and death totals (outbreak report epidemic curve)
    fig01_clinical_kpn_isolates.csv — WGS-confirmed clinical K. pneumoniae isolates (Supplementary File 1)
    gadm41_GMB_1.shp (+ .dbf/.prj/.shx) — Gambia level-1 boundaries, https://gadm.org/download_country.html
"""

import calendar

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from matplotlib.lines import Line2D
from shapely.geometry import Point

plt.rcParams["font.family"] = "DejaVu Sans"

out_pdf = "fig01_timeline_and_map.pdf"

# ---------- Data ----------
epi = pd.read_csv("data/fig01_epi_curve.csv", comment="#")
iso = pd.read_csv("data/fig01_clinical_kpn_isolates.csv")
iso["month"] = iso.apply(lambda r: f"{int(r.year)}-{int(r.month):02d}", axis=1)
wgs = (iso.assign(st39=iso["st"].eq("ST39"))
          .groupby("month")["st39"].agg(st39="sum", total="count"))
epi = epi.join(wgs, on="month").fillna({"st39": 0, "total": 0})
epi["other_kp"] = epi["total"] - epi["st39"]
epi["no_wgs"] = epi["cases"] - epi["total"]
assert (epi["no_wgs"] >= 0).all(), "more WGS-confirmed isolates than cases in a month"

months = pd.PeriodIndex(epi["month"], freq="M")
x = list(range(len(epi)))


def date_x(year, month, day):
    """x position of a calendar date (bars are centred on integer month indices)."""
    i = list(months).index(pd.Period(f"{year}-{month:02d}", freq="M"))
    return i - 0.5 + (day - 0.5) / calendar.monthrange(year, month)[1]


# ---------- Colours ----------
C_ST39, C_OTHER, C_NOWGS = "#2E8C8C", "#9EC7E8", "#C9CCD1"
C_DEATH, C_SAMPLING, C_WATER = "#C0392B", "#F0A93B", "#BBD7EE"

# ---------- Figure ----------
fig = plt.figure(figsize=(16.4, 15.07))
axA = fig.add_axes([0.045, 0.39, 0.93, 0.53])
axB = fig.add_axes([0.03, 0.0, 0.94, 0.34])

# Panel A: stacked bars + deaths
axA.bar(x, epi["st39"], width=0.8, color=C_ST39, label="ST39-confirmed (WGS)", zorder=2)
axA.bar(x, epi["other_kp"], width=0.8, bottom=epi["st39"], color=C_OTHER,
        label="WGS-confirmed K. pneumoniae, other ST", zorder=2)
axA.bar(x, epi["no_wgs"], width=0.8, bottom=epi["st39"] + epi["other_kp"], color=C_NOWGS,
        label="No WGS-confirmed K. pneumoniae isolate", zorder=2)
axA.plot(x, epi["deaths"], color=C_DEATH, lw=1.8, marker="D", ms=6, label="Deaths", zorder=3)

axA.set_ylim(-9.6, 16)
axA.set_xlim(-0.8, len(x) + 0.9)
axA.set_yticks(range(0, 13, 2))
axA.tick_params(axis="y", labelsize=15)
axA.set_ylabel("Number of cases", fontsize=18, fontweight="bold")
axA.yaxis.set_label_coords(-0.035, 0.62)
axA.spines["bottom"].set_position(("data", 0))
for s in ("top", "right"):
    axA.spines[s].set_visible(False)
axA.set_xticks(x)
axA.set_xticklabels([calendar.month_abbr[m.month] for m in months])
axA.tick_params(axis="x", labelsize=17, length=0, pad=6)
for y in range(2, 13, 2):
    axA.axhline(y, color="#EEEEEE", lw=0.8, zorder=0)

handles = dict(zip(*axA.get_legend_handles_labels()[::-1]))
order = ["Deaths", "ST39-confirmed (WGS)",                                          # column 1
         "WGS-confirmed K. pneumoniae, other ST", "No WGS-confirmed K. pneumoniae isolate"]  # column 2
axA.legend([handles[k] for k in order], order, ncol=2, fontsize=14, frameon=False,
           loc="lower left", bbox_to_anchor=(0.03, 0.985), columnspacing=2.5, handlelength=1.8)
fig.text(0.985, 0.985, "*indicates Kpn belonging to the ST39 cluster", ha="right", va="top",
         fontsize=13, style="italic")
fig.text(0.005, 0.998, "A.", fontsize=22, fontweight="bold", va="top")


def event(xc, target, title, body=None, colour="white", body_lines=0):
    """Dated event box below the axis, with an arrow to the event date and an optional details box."""
    axA.annotate(title, xy=(target, 0), xytext=(xc, -2.55), textcoords="data",
                 ha="center", va="center", fontsize=11.5,
                 bbox=dict(boxstyle="round,pad=0.35", fc=colour, ec="black", lw=1.1),
                 arrowprops=dict(arrowstyle="-|>", color="black", lw=1.1, shrinkA=0, shrinkB=2))
    if body:
        axA.text(xc, -3.9, body, ha="center", va="top", fontsize=10.5, linespacing=1.25,
                 bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="black", lw=0.9))


event(5.5, date_x(2023, 7, 31), "31 July\nInitial investigation meeting",
      "Multiple Infection\nprevention & control\nhazards identified in\nlabour and neonatal wards")
event(8.6, date_x(2023, 10, 9), "9 October\nWard sampling",
      "14/48 Kpn positive\n\nLabour ward:\n• sinks/sink surfaces\n• baby beds\n• weighing scale\n\n"
      "Neonatal ward:\n• sinks/sink surfaces\n• baby beds\n• intravenous fluids*", colour=C_SAMPLING)
event(11.0, date_x(2023, 12, 6), "6 December\nWard sampling",
      "8/56 Kpn positive\n\nLabour ward:\n• sinks/sink surfaces\n• hand soap\n\n"
      "Neonatal ward:\n• sinks/sink surfaces\n• cots\n• intravenous fluids*", colour=C_SAMPLING)
event(13.0, date_x(2024, 1, 5), "5 January\nWard sampling",
      "2/55 Kpn positive\n\nLabour ward:\n• sinks/sink surfaces\n\nNeonatal ward:\n• sinks/sink surfaces",
      colour=C_SAMPLING)
event(15.0, date_x(2024, 3, 10), "10 March\nWard sampling", "0/55 Kpn positive", colour=C_SAMPLING)

# Water-source sampling (above the bars)
nov = date_x(2023, 11, 9)
axA.annotate("9 November\nWater source sampling\n(hospital water tanks and\nreservoirs tested)\nNo Kpn grown",
             xy=(nov, epi.loc[10, "cases"] + 0.4), xytext=(10.0, 15.7), ha="center", va="center",
             fontsize=11.5, bbox=dict(boxstyle="round,pad=0.4", fc=C_WATER, ec="black", lw=1.1),
             arrowprops=dict(arrowstyle="-|>", color="black", lw=1.1, shrinkA=0, shrinkB=0))

# ---------- Panel B: map ----------
gmap = gpd.read_file("data/gadm41_GMB_1.shp")
gmap["display_name"] = gmap["NAME_1"].replace({"Banjul": "Greater Banjul", "Maccarthy Island": "Central River"})
region_order = ["Greater Banjul", "Lower River", "Central River", "North Bank", "Upper River", "Western"]
cmap = plt.colormaps["tab20"].resampled(len(region_order))
region_colors = {r: cmap(i) for i, r in enumerate(region_order)}
for r in region_order:
    gmap[gmap["display_name"] == r].plot(ax=axB, color=region_colors[r], edgecolor="black", linewidth=0.6)

towns = pd.DataFrame({"Town": ["Basse", "Bansang", "Banjul"],
                      "lat": [13.3096, 13.4333, 13.4549], "lon": [-14.2136, -14.6461, -16.5790]})
town_colors = {"Basse": "orange", "Bansang": "purple", "Banjul": "red"}
towns = gpd.GeoDataFrame(towns, geometry=[Point(xy) for xy in zip(towns.lon, towns.lat)], crs="EPSG:4326")
for _, t in towns.iterrows():
    axB.scatter(t.geometry.x, t.geometry.y, s=130, color=town_colors[t.Town], edgecolor="black", zorder=5)
    axB.annotate(t.Town, xy=(t.geometry.x, t.geometry.y), xytext=(5, 5), textcoords="offset points",
                 fontsize=15, bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, pad=1.5))
axB.set_aspect("equal")
axB.set_axis_off()
axB.legend(handles=[Line2D([0], [0], marker="o", ls="", markerfacecolor=town_colors[t],
                           markeredgecolor="black", markersize=10, label=t) for t in town_colors],
           title="Study sites", loc="upper left", fontsize=14, title_fontsize=15, frameon=True)
fig.legend(handles=[mpatches.Patch(color=region_colors[r], label=r) for r in region_order],
           title="Regions", loc="lower center", bbox_to_anchor=(0.62, 0.0), ncol=3, fontsize=14,
           title_fontsize=15, frameon=True)
fig.text(0.03, 0.365, "B.", fontsize=22, fontweight="bold", va="top")

fig.savefig(out_pdf, bbox_inches="tight")
print(f"Saved: {out_pdf}")
