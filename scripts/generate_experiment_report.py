"""Generate reproducible reporting tables from a KD-HDIE experiment JSON."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('result_json')
    p.add_argument('--out-dir', default='reports/generated')
    a=p.parse_args()
    src=Path(a.result_json); data=json.loads(src.read_text(encoding='utf-8'))
    out=Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    stats=data.get('metadata',{}) or data.get('statistics',{}) or {}
    # Framework results commonly expose statistics at top level or under metadata.
    if not stats:
        stats=data.get('result',{}).get('metadata',{}) or data.get('result',{}).get('statistics',{})
    rows=[]
    keys=['input_records','fused_records','fusion_groups','checked_groups','duplicate_groups','conflicts','unit_conflicts','value_conflicts','conflicts_resolved','attributes_selected','completeness','validity','quality','semantic_coverage','matching_accuracy','reliability_mean','reliability_min','reliability_max','execution_time_seconds','execution_wall_time_seconds']
    for k in keys:
        if k in stats: rows.append((k,stats[k]))
        elif k in data: rows.append((k,data[k]))
    with (out/'metrics.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['metric','value']); w.writerows(rows)
    exp=data.get('experiment',{})
    md=['# KD-HDIE experiment results','',f"Result file: `{src.name}`",'']
    for k,v in exp.items(): md.append(f'- **{k}:** {v}')
    md += ['', '## Metrics', '', '| Metric | Value |','|---|---:|']
    for k,v in rows: md.append(f'| {k} | {v} |')
    (out/'results_summary.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps({'metrics_csv':str(out/'metrics.csv'),'summary_md':str(out/'results_summary.md'),'metrics_count':len(rows)},indent=2))
if __name__=='__main__': main()
