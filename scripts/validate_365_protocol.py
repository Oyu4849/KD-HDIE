"""Validate a canonical daily CSV against the 2025 365-day protocol."""
from __future__ import annotations
import argparse,csv,json,sys
from datetime import date,timedelta
from pathlib import Path

def main():
 p=argparse.ArgumentParser(); p.add_argument('csv_file'); p.add_argument('--date-column',default='date'); a=p.parse_args()
 rows=list(csv.DictReader(Path(a.csv_file).open(encoding='utf-8')))
 dates=[]; errors=[]
 for i,r in enumerate(rows,1):
  try: dates.append(date.fromisoformat(r[a.date_column][:10]))
  except Exception: errors.append(f'row {i}: invalid date')
 expected=[date(2025,1,1)+timedelta(days=i) for i in range(365)]
 ds=set(dates)
 report={'rows':len(rows),'unique_dates':len(ds),'duplicates':len(dates)-len(ds),'missing_dates':[d.isoformat() for d in expected if d not in ds],'out_of_period':[d.isoformat() for d in ds if d not in set(expected)],'invalid_date_rows':errors}
 report['pass']=report['rows']==365 and report['unique_dates']==365 and not report['missing_dates'] and not report['out_of_period'] and not errors
 print(json.dumps(report,ensure_ascii=False,indent=2)); sys.exit(0 if report['pass'] else 2)
if __name__=='__main__': main()
