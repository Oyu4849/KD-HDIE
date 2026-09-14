"""Reproducible baseline comparison from an already validated canonical CSV.

This script is intentionally offline: it does not fabricate observations and
never claims that a baseline is a ground truth. It compares two deterministic
baselines on the same input CSV used for the KD-HDIE experiment.
"""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
import pandas as pd

DATE_CANDIDATES=("date","timestamp","time")

def find_date_col(df):
    for c in DATE_CANDIDATES:
        if c in df.columns: return c
    raise ValueError("No date/timestamp column found")

def numeric_cols(df, date_col):
    return [c for c in df.columns if c != date_col and pd.api.types.is_numeric_dtype(df[c])]

def direct_merge(df, date_col):
    # Baseline metric: retain all source observations; duplicate timestamps are
    # not reconciled. This is deliberately a weak interoperability baseline.
    out=df.copy(); dup=int(out[date_col].duplicated().sum())
    return {"rows":int(len(out)),"duplicate_timestamps":dup,"missing_cells":int(out.isna().sum().sum())}

def source_priority(df, date_col):
    # Deterministic first-observation-per-date rule. Column-level source
    # priority is represented by input column order; no quality reasoning.
    out=df.drop_duplicates(subset=[date_col], keep="first")
    return {"rows":int(len(out)),"duplicate_timestamps":int(len(df)-len(out)),"missing_cells":int(out.isna().sum().sum())}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--csv",required=True); p.add_argument("--output",default="reports/baseline_comparison_2025.json")
    a=p.parse_args(); path=Path(a.csv); df=pd.read_csv(path)
    dc=find_date_col(df); df[dc]=pd.to_datetime(df[dc],errors="coerce")
    if df[dc].isna().any(): raise ValueError("Input contains invalid dates")
    cols=numeric_cols(df,dc)
    if not cols: raise ValueError("No numeric observation columns found")
    expected_start=pd.Timestamp('2025-01-01'); expected_end=pd.Timestamp('2025-12-31')
    if df[dc].nunique()!=365 or df[dc].min()!=expected_start or df[dc].max()!=expected_end:
        raise ValueError("Baseline input must contain exactly 365 unique dates from 2025-01-01 through 2025-12-31")
    t=time.perf_counter(); dm=direct_merge(df,dc); dm["runtime_seconds"]=round(time.perf_counter()-t,6)
    t=time.perf_counter(); sp=source_priority(df,dc); sp["runtime_seconds"]=round(time.perf_counter()-t,6)
    result={"protocol":"KD-HDIE-365D-baselines-v1","input_file":str(path.resolve()),"rows":int(len(df)),"unique_dates":int(df[dc].nunique()),"date_column":dc,"numeric_columns":cols,"baselines":{"direct_merge":dm,"source_priority":sp}}
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8"); print(out)
if __name__=="__main__": main()
