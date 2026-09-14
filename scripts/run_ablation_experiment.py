"""Run A1-A4 ablation variants on the same two real daily sources.

A0 direct merge remains a deterministic baseline computed separately from the
validated canonical CSV. No variant fabricates observations.
"""
from __future__ import annotations
import argparse, json, time, sys
from pathlib import Path
PROJECT_ROOT=Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path: sys.path.insert(0,str(PROJECT_ROOT))
from core.bootstrap import bootstrap
from core.framework import KDHDIEFramework

def main():
    p=argparse.ArgumentParser(); p.add_argument('--start-date',default='2025-01-01'); p.add_argument('--end-date',default='2025-12-31'); p.add_argument('--latitude',type=float,default=45.0); p.add_argument('--longitude',type=float,default=59.0); p.add_argument('--output',default='reports/ablation_2025.json'); args=p.parse_args()
    bootstrap(); fw=KDHDIEFramework(); rows=[]
    sources=[{'source_system':'OPENMETEO','connection_parameters':{'latitude':args.latitude,'longitude':args.longitude,'start_date':args.start_date,'end_date':args.end_date,'historical':True}}, {'source_system':'NASA','connection_parameters':{'latitude':args.latitude,'longitude':args.longitude,'start':args.start_date.replace('-',''),'end':args.end_date.replace('-',''),'parameters':['T2M','PRECTOTCORR','RH2M','WS2M'],'temporal':'DAILY'}}]
    for variant in ('ABLATION_A1','ABLATION_A2','ABLATION_A3','ABLATION_A4'):
        t=time.perf_counter(); result=fw.execute_multi_source(sources=sources,workflow=variant); elapsed=time.perf_counter()-t; d=result.to_dict(); stats=d.get('statistics',{}) or d.get('metadata',{}) or {}; rows.append({'variant':variant,'success':d.get('success'),'runtime_seconds':round(elapsed,6),'statistics':stats})
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps({'protocol':'KD-HDIE-365D-2025-ablation-v1','variants':['A0','A1','A2','A3','A4'],'results':rows},ensure_ascii=False,indent=2,default=str),encoding='utf-8'); print(out)
if __name__=='__main__': main()
