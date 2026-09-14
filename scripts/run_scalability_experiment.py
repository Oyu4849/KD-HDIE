"""Run the same KD-HDIE daily protocol at 30/90/180/365-day prefixes.

No synthetic data are generated. Each prefix is fetched from the same two
real sources and validated before execution. Results are written as one JSON.
"""
from __future__ import annotations
import argparse, json, time, sys
from datetime import date, timedelta
from pathlib import Path
PROJECT_ROOT=Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path: sys.path.insert(0,str(PROJECT_ROOT))
from core.bootstrap import bootstrap
from core.framework import KDHDIEFramework

SIZES=(30,90,180,365)

def end_for_days(start, days):
    return (date.fromisoformat(start)+timedelta(days=days-1)).isoformat()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--start-date',default='2025-01-01')
    p.add_argument('--latitude',type=float,default=45.0)
    p.add_argument('--longitude',type=float,default=59.0)
    p.add_argument('--output',default='reports/scalability_2025.json')
    args=p.parse_args(); bootstrap(); fw=KDHDIEFramework(); rows=[]
    for days in SIZES:
        end=end_for_days(args.start_date,days)
        sources=[
          {'source_system':'OPENMETEO','connection_parameters':{'latitude':args.latitude,'longitude':args.longitude,'start_date':args.start_date,'end_date':end,'historical':True}},
          {'source_system':'NASA','connection_parameters':{'latitude':args.latitude,'longitude':args.longitude,'start':args.start_date.replace('-',''),'end':end.replace('-',''),'parameters':['T2M','PRECTOTCORR','RH2M','WS2M'],'temporal':'DAILY'}}]
        t=time.perf_counter()
        result=fw.execute_multi_source(sources=sources,workflow='DAILY')
        elapsed=time.perf_counter()-t
        d=result.to_dict()
        if not d.get('success'):
            raise RuntimeError(f"Scalability run failed for {days} days")
        stats=d.get('statistics',{}) or d.get('metadata',{}) or {}
        source_stats=stats.get('source_statistics',{}) or {}
        for source_name in ('OPENMETEO','NASA'):
            observed=(source_stats.get(source_name,{}) or {}).get('output_records')
            if observed != days:
                raise RuntimeError(f"{source_name}: expected {days} records, got {observed}")
        rows.append({'days':days,'start_date':args.start_date,'end_date':end,'success':d.get('success'),'runtime_seconds':round(elapsed,6),'input_records':stats.get('input_records'),'fused_records':stats.get('fused_records'),'fusion_groups':stats.get('fusion_groups'),'conflicts':stats.get('conflicts',stats.get('conflict_count')),'conflicts_resolved':stats.get('conflicts_resolved')})
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps({'protocol':'KD-HDIE-365D-2025-scalability-v1','sizes':list(SIZES),'results':rows},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
