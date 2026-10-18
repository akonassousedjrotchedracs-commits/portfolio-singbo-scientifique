#!/usr/bin/env python3
"""Rebuild the public Benin child-survival table and SVG from the bundled UNICEF series."""
import csv, html, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/"data/benin_unicef_under5_mortality_1990_2024.csv"
out=ROOT/"results/under5_mortality_benin.svg"
with source.open(encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
if len(rows)!=35 or [int(r["year"]) for r in rows]!=list(range(1990,2025)): raise SystemExit("Unexpected year coverage")
vals=[float(r["u5mr_deaths_per_1000_live_births"]) for r in rows]
W,H=1100,560; x0,y0,pw,ph=95,100,930,360
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 560" role="img" aria-labelledby="t d">','<title id="t">Mortalité des moins de cinq ans au Bénin, estimations UN IGME</title>','<desc id="d">Série annuelle UNICEF Data de 1990 à 2024, en décès pour 1 000 naissances vivantes.</desc>','<rect width="100%" height="100%" fill="#fff"/>','<text x="55" y="48" font-family="Arial" font-size="25" fill="#153b52">Bénin · mortalité des moins de cinq ans</text>','<text x="55" y="75" font-family="Arial" font-size="15" fill="#59686e">Estimations UN IGME · décès pour 1 000 naissances vivantes · 1990–2024</text>']
for tick in (0,50,100,150,200):
 y=y0+ph-(tick/200)*ph; svg += [f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+pw}" y2="{y:.1f}" stroke="#d7e1e4"/>',f'<text x="{x0-12}" y="{y+5:.1f}" text-anchor="end" font-family="Arial" font-size="13" fill="#59686e">{tick}</text>']
pts=[]
for i,v in enumerate(vals):
 x=x0+i*pw/(len(vals)-1); y=y0+ph-v/200*ph; pts.append(f"{x:.1f},{y:.1f}")
svg += [f'<polyline points="{" ".join(pts)}" fill="none" stroke="#087e8b" stroke-width="4" stroke-linejoin="round"/>']
for i in (0,10,20,30,34):
 x=x0+i*pw/(len(vals)-1); y=y0+ph-vals[i]/200*ph; svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#153b52"/><text x="{x:.1f}" y="{y-12:.1f}" text-anchor="middle" font-family="Arial" font-size="13" fill="#153b52">{vals[i]:.1f}</text><text x="{x:.1f}" y="{y0+ph+25}" text-anchor="middle" font-family="Arial" font-size="13" fill="#59686e">{rows[i]["year"]}</text>')
svg += [f'<text x="{x0+pw/2}" y="{y0+ph+65}" text-anchor="middle" font-family="Arial" font-size="14" fill="#59686e">Année</text>','<text x="55" y="530" font-family="Arial" font-size="12" fill="#59686e">Source : UNICEF Data, profil Bénin (série UN IGME). Valeurs estimées; non observées directement.</text>','</svg>']
out.parent.mkdir(parents=True,exist_ok=True); out.write_text("\n".join(svg)+"\n",encoding="utf-8")
print(f"Generated {out.name} from {len(rows)} real, modelled annual estimates.")
