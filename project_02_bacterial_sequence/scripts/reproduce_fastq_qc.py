#!/usr/bin/env python3
"""Summarize per-read and per-cycle Phred+33 metrics for a tiny synthetic FASTQ."""
import argparse
import csv
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def parse(path):
    lines=path.read_text(encoding='ascii').splitlines(); rec=[]
    if len(lines)%4: raise ValueError('FASTQ must contain complete four-line records')
    for i in range(0,len(lines),4):
        h,s,p,q=lines[i:i+4]
        if not h.startswith('@') or not p.startswith('+') or not s or len(s)!=len(q): raise ValueError(f'Invalid FASTQ record at line {i+1}')
        if p[1:].strip() and p[1:].strip()!=h[1:].strip(): raise ValueError(f'FASTQ identifier mismatch at line {i+3}')
        if any(base.upper() not in 'ACGTRYSWKMBDHVN' for base in s): raise ValueError(f'Invalid DNA symbol at line {i+2}')
        if any(not 33<=ord(x)<=126 for x in q): raise ValueError('Quality chars outside Phred+33 printable range')
        rec.append((h[1:],s.upper(),[ord(x)-33 for x in q]))
    if not rec: raise ValueError('No FASTQ records')
    return rec
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',type=Path,default=ROOT/'data/DEMO_SYNTHETIC_reads.fastq');ap.add_argument('--output-dir',type=Path,default=ROOT/'results');a=ap.parse_args(); rec=parse(a.input)
    out=[]
    for name,seq,qs in rec:
        n=len(seq); gc=sum(x in 'GC' for x in seq); q20=sum(x>=20 for x in qs);q30=sum(x>=30 for x in qs)
        out.append({'read_id':name,'length_bp':n,'gc_percent':round(100*gc/n,1),'ambiguous_bases':sum(x not in 'ACGT' for x in seq),'mean_phred':round(sum(qs)/len(qs),2),'q20_bases':q20,'q20_percent':round(100*q20/n,1),'q30_bases':q30,'q30_percent':round(100*q30/n,1)})
    maxlen=max(len(s) for _,s,_ in rec); cyc=[]
    for pos in range(maxlen):
        qs=[q[pos] for _,s,q in rec if pos<len(s)];cyc.append({'cycle':pos+1,'n_bases':len(qs),'mean_phred':round(sum(qs)/len(qs),2),'q20_percent':round(100*sum(x>=20 for x in qs)/len(qs),1),'q30_percent':round(100*sum(x>=30 for x in qs)/len(qs),1)})
    a.output_dir.mkdir(parents=True,exist_ok=True)
    for name,rows in [('fastq_read_qc.csv',out),('fastq_per_cycle_qc.csv',cyc)]:
        with (a.output_dir/name).open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (a.output_dir/'fastq_qc_summary.json').write_text(json.dumps({'records':len(rec),'bases':sum(len(s) for _,s,_ in rec),'encoding':'Phred+33','status':'synthetic training fixture; not sequencer output','limitations':'No adapter detection, instrument calibration, contamination screening, or biological inference.'},indent=2)+'\n',encoding='utf-8')
    width,height=860,390; outsvg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 390" role="img" aria-labelledby="t d"><title id="t">Synthetic FASTQ Phred quality by cycle</title><desc id="d">Mean Phred scores and Q30 percentage across 20 read positions in three synthetic reads.</desc><rect width="100%" height="100%" fill="#fff"/><text x="35" y="42" font-family="Arial" font-size="22" font-weight="bold" fill="#153b52">Qualité FASTQ synthétique · Phred+33</text><text x="35" y="68" font-family="Arial" font-size="13" fill="#59686e">Moyenne Phred par cycle · trois lectures de démonstration</text>']
    x0,y0,pw,ph=58,100,750,220
    for t in [0,10,20,30,40]:
        y=y0+ph*(40-t)/40;outsvg += [f'<line x1="{x0}" y1="{y}" x2="{x0+pw}" y2="{y}" stroke="#d7e1e4"/>',f'<text x="{x0-10}" y="{y+4}" text-anchor="end" font-family="Arial" font-size="11" fill="#59686e">{t}</text>']
    pts=[]
    for r in cyc: pts.append(f"{x0+pw*(r['cycle']-1)/(maxlen-1):.1f},{y0+ph*(40-r['mean_phred'])/40:.1f}")
    outsvg += [f'<polyline points="{" ".join(pts)}" fill="none" stroke="#087e8b" stroke-width="3"/>']
    for r in cyc:
        x=x0+pw*(r['cycle']-1)/(maxlen-1);y=y0+ph*(40-r['mean_phred'])/40;outsvg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#087e8b"/>')
    outsvg += [f'<text x="{x0+pw/2}" y="358" text-anchor="middle" font-family="Arial" font-size="13" fill="#59686e">Cycle de base</text>','<text x="35" y="382" font-family="Arial" font-size="12" fill="#59686e">Q20/Q30 = fraction des bases avec score Phred ≥20/≥30; indicateurs de démonstration uniquement.</text>','</svg>']
    (a.output_dir/'fastq_quality_by_cycle.svg').write_text('\n'.join(outsvg),encoding='utf-8')
    print(f'FASTQ QC rebuilt: {len(rec)} synthetic reads, {sum(len(s) for _,s,_ in rec)} bases, {len(cyc)} cycles.')
if __name__=='__main__':main()
