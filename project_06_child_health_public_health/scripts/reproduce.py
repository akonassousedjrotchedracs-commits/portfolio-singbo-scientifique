#!/usr/bin/env python3
"""Rebuild descriptive summaries and SVG from the bundled public-data snapshot."""
import csv,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COUNTRIES=['Benin','Togo','Ghana',"Cote d'Ivoire",'Nigeria']
COLORS=['#087e8b','#d07627','#3a6ea5','#7e5aa6','#52854c']
def main():
 data=[]
 with (ROOT/'data/under5_mortality_public.csv').open(newline='',encoding='utf-8-sig') as f:
  for x in csv.DictReader(f):data.append({'country':x['country'],'year':int(x['year']),'rate':float(x['under5_mortality_per_1000'].replace(',','.'))})
 out=[]
 for c in COUNTRIES:
  xs=[x for x in data if x['country']==c];first=next(x for x in xs if x['year']==1990);last=max(xs,key=lambda z:z['year'])
  out.append({'country':c,'first_year':first['year'],'rate_1990':first['rate'],'latest_year':last['year'],'latest_rate':last['rate'],'absolute_change_per_1000':round(last['rate']-first['rate'],1),'relative_decline_percent':round(100*(first['rate']-last['rate'])/first['rate'],1)})
 with (ROOT/'results/selected_years_summary.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
 years=sorted({x['year'] for x in data});lo,hi=min(years),max(years);x0,y0,pw,ph=88,100,820,340;top=200
 svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 530" role="img" aria-labelledby="t d"><title id="t">Under-five mortality estimates</title><desc id="d">UN IGME modelled estimates per 1000 live births in five West African countries, 1990 to 2024.</desc><rect width="100%" height="100%" fill="#fff"/><text x="45" y="43" font-family="Arial" font-size="23" font-weight="bold" fill="#153b52">Child survival - modelled estimates</text><text x="45" y="69" font-family="Arial" font-size="13" fill="#59686e">Deaths before age five per 1,000 live births - WDI / UN IGME</text>']
 for t in [0,50,100,150,200]:
  y=y0+ph*(top-t)/top;svg += [f'<line x1="{x0}" y1="{y}" x2="{x0+pw}" y2="{y}" stroke="#d7e1e4"/>',f'<text x="{x0-10}" y="{y+4}" text-anchor="end" font-family="Arial" font-size="11" fill="#59686e">{t}</text>']
 for yr in [1990,2000,2010,2020,2024]:
  x=x0+pw*(yr-lo)/(hi-lo);svg += [f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0+ph}" stroke="#eef2f3"/>',f'<text x="{x}" y="{y0+ph+22}" text-anchor="middle" font-family="Arial" font-size="11" fill="#59686e">{yr}</text>']
 for j,c in enumerate(COUNTRIES):
  xs=sorted((x for x in data if x['country']==c),key=lambda z:z['year']);pts=' '.join(f"{x0+pw*(z['year']-lo)/(hi-lo):.1f},{y0+ph*(top-z['rate'])/top:.1f}" for z in xs)
  svg.append(f'<polyline points="{pts}" fill="none" stroke="{COLORS[j]}" stroke-width="3"/>');lx=660+(j%2)*150;ly=113+(j//2)*24
  svg += [f'<line x1="{lx}" y1="{ly}" x2="{lx+20}" y2="{ly}" stroke="{COLORS[j]}" stroke-width="4"/>',f'<text x="{lx+26}" y="{ly+4}" font-family="Arial" font-size="12" fill="#153b52">{html.escape(c)}</text>']
 svg += ['<text x="490" y="500" text-anchor="middle" font-family="Arial" font-size="13" fill="#59686e">Year</text>','<text x="20" y="280" transform="rotate(-90 20 280)" text-anchor="middle" font-family="Arial" font-size="13" fill="#59686e">Per 1,000 live births</text>','</svg>']
 (ROOT/'results/under5_mortality_trends.svg').write_text('\n'.join(svg),encoding='utf-8')
 print(f'Built summaries for {len(data)} annual country estimates.')
if __name__=='__main__':main()
