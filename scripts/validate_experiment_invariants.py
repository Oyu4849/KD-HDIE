"""Validate internal invariants of a completed KD-HDIE experiment report.

This script does not judge scientific quality; it checks bookkeeping invariants
that must hold before results are transferred into a manuscript.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('result_json')
    args = p.parse_args()
    data = json.loads(Path(args.result_json).read_text(encoding='utf-8'))
    stats = data.get('metadata', data.get('statistics', {}))
    errors=[]

    # Search recursively for statistics if the serializer nests them.
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

    input_records=find(data,'input_records')
    fused_records=find(data,'fused_records')
    conflicts=find(data,'conflicts')
    resolved=find(data,'conflicts_resolved')
    if conflicts is not None and resolved is not None and resolved > conflicts:
        errors.append(f'conflicts_resolved ({resolved}) exceeds conflicts ({conflicts})')
    if input_records is not None and fused_records is not None and fused_records > input_records:
        errors.append(f'fused_records ({fused_records}) exceeds input_records ({input_records})')

    exp=find(data,'experiment') or {}
    if exp.get('synthetic_rows_added') is True:
        errors.append('experiment declares synthetic_rows_added=true')
    if exp.get('expected_calendar_days') == 365:
        if exp.get('start_date') != '2025-01-01' or exp.get('end_date') != '2025-12-31':
            errors.append('365-day protocol dates do not match 2025 calendar year')

    print(json.dumps({'passed': not errors, 'errors': errors}, indent=2))
    raise SystemExit(1 if errors else 0)

if __name__ == '__main__':
    main()
