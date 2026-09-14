"""Compute reproducible baseline and scalability comparisons from canonical 365-day data.

No observations are generated. The script only uses an existing validated CSV.
It compares two simple baselines against source-pair agreement and produces CSV/JSON.
"""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
import pandas as pd

SOURCE_PAIRS = {
    "temperature": ("om_temperature", "nasa_temperature"),
    "precipitation": ("om_precipitation", "nasa_precipitation"),
    "wind_speed": ("om_wind_speed", "nasa_wind_speed"),
}

def rel_diff(a, b, eps=1e-9):
    den = max(abs(a), abs(b), eps)
    return abs(a-b) / den

def evaluate(df, threshold=0.05):
    rows=[]
    for name,(a,b) in SOURCE_PAIRS.items():
        x=pd.to_numeric(df[a], errors='coerce'); y=pd.to_numeric(df[b], errors='coerce')
        valid=x.notna() & y.notna()
        if not valid.any():
            rows.append({"attribute":name,"paired_days":0,"conflicts":None,"conflict_rate":None,"priority_mae":None,"mean_agreement":None})
            continue
        xv=x[valid]; yv=y[valid]
        conflicts=((xv-yv).abs()/pd.concat([xv.abs(),yv.abs()],axis=1).max(axis=1).clip(lower=1e-9) > threshold)
        priority_mae=(xv-yv).abs().mean()
        agreement=1-conflicts.mean()
        rows.append({"attribute":name,"paired_days":int(valid.sum()),"conflicts":int(conflicts.sum()),"conflict_rate":float(conflicts.mean()),"priority_mae":float(priority_mae),"mean_agreement":float(agreement)})
    return pd.DataFrame(rows)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--csv',required=True); p.add_argument('--output-dir',default='reports/comparison'); p.add_argument('--threshold',type=float,default=.05); args=p.parse_args()
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.csv)
    required=['date']+[c for pair in SOURCE_PAIRS.values() for c in pair]
    missing=[c for c in required if c not in df.columns]
    if missing: raise ValueError('Missing columns: '+', '.join(missing))
    dates=pd.to_datetime(df.date,errors='coerce').dropna().dt.strftime('%Y-%m-%d')
    if len(df)!=365 or dates.nunique()!=365 or dates.duplicated().any():
        raise ValueError('Input is not a validated 365-day dataset.')
    started=time.perf_counter(); result=evaluate(df,args.threshold); elapsed=time.perf_counter()-started
    result.to_csv(out/'baseline_comparison.csv',index=False)
    payload={'protocol':'KD-HDIE-365D-2025-comparison-v1','threshold_relative':args.threshold,'days':365,'methods':['direct_merge','source_priority','KD-HDIE'],'note':'Baseline metrics are computed from observed paired source values; KD-HDIE metrics must be taken from the actual KD-HDIE run, not inferred here.','elapsed_seconds':elapsed,'attributes':result.to_dict(orient='records')}
    (out/'comparison_manifest.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(payload,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
