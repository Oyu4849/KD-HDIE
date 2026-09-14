"""Audit a completed KD-HDIE experiment before manuscript use.

Checks protocol, metric bounds, and bookkeeping consistency. It does not
modify results and never invents values.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path

def find(obj, key):
    if isinstance(obj, dict):
        if key in obj: return obj[key]
        for v in obj.values():
            r=find(v,key)
            if r is not None: return r
    elif isinstance(obj, list):
        for v in obj:
            r=find(v,key)
            if r is not None: return r
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('result_json')
    args=ap.parse_args()
    p=Path(args.result_json)
    data=json.loads(p.read_text(encoding='utf-8'))
    errors=[]; warnings=[]
    exp=find(data,'experiment') or {}
    if exp.get('expected_calendar_days') == 365:
        if exp.get('start_date')!='2025-01-01' or exp.get('end_date')!='2025-12-31':
            errors.append('365-day protocol dates are not 2025-01-01..2025-12-31')
    if exp.get('synthetic_rows_added') is not False:
        errors.append('synthetic_rows_added must be explicitly false')

    bounded={
        'completeness':(0,1),'validity':(0,1),'quality':(0,1),
        'semantic_coverage':(0,1),'matching_accuracy':(0,1),
        'conflict_rate':(0,1),'conflict_resolution_rate':(0,1),
        'reliability_mean':(0,1),'reliability_min':(0,1),'reliability_max':(0,1),
    }
    for k,(lo,hi) in bounded.items():
        v=find(data,k)
        if v is not None:
            try:
                if not math.isfinite(float(v)) or not (lo <= float(v) <= hi):
                    errors.append(f'{k}={v} is outside [{lo},{hi}]')
            except Exception:
                errors.append(f'{k} is not numeric: {v!r}')

    conflicts=find(data,'conflicts'); resolved=find(data,'conflicts_resolved')
    checked=find(data,'checked_groups'); rate=find(data,'conflict_rate')
    if conflicts is not None and resolved is not None and resolved > conflicts:
        errors.append(f'conflicts_resolved ({resolved}) > conflicts ({conflicts})')
    if conflicts is not None and checked is not None and checked:
        expected=float(conflicts)/float(checked)
        if rate is not None and abs(float(rate)-expected) > 1e-6:
            errors.append(f'conflict_rate={rate} inconsistent with conflicts/checked_groups={expected}')
    rmin=find(data,'reliability_min'); rmean=find(data,'reliability_mean'); rmax=find(data,'reliability_max')
    if all(v is not None for v in (rmin,rmean,rmax)) and not (float(rmin)<=float(rmean)<=float(rmax)):
        errors.append('reliability_min <= reliability_mean <= reliability_max is violated')

    # These are warnings, not failures, because a valid experiment may have no conflicts.
    if conflicts == 0:
        warnings.append('No conflicts detected; conflict-resolution rate may be undefined or convention-dependent.')
    if exp.get('sources') and len(exp['sources']) < 2:
        warnings.append('Fewer than two sources: this is not a multi-source conflict-fusion experiment.')

    out={'passed':not errors,'errors':errors,'warnings':warnings}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=='__main__': main()
