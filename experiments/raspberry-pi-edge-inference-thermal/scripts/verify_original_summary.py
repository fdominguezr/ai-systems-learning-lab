#!/usr/bin/env python3
"""Read-only verification of any original telemetry CSV against its summary JSON.
Usage: python verify_original_summary.py path/to/telemetry.csv path/to/summary.json
No network or writes; prints evidence status, does not publish original data.
"""
from pathlib import Path
import csv,hashlib,json,sys
if len(sys.argv)!=3:raise SystemExit('Usage: verify_original_summary.py telemetry.csv summary.json')
csv_path=Path(sys.argv[1]);sum_path=Path(sys.argv[2]);s=json.loads(sum_path.read_text(encoding='utf-8'))
actual=hashlib.sha256(csv_path.read_bytes()).hexdigest()
expected=s.get('telemetry_sha256','')
with csv_path.open(encoding='utf-8-sig',newline='') as f:
 r=csv.DictReader(f);rows=sum(1 for _ in r)
needed=int(s['observed_samples'])
print('SHA256', 'PASS' if actual==expected else 'FAIL', 'actual='+actual, 'declared='+expected)
print('SAMPLES','PASS' if rows==needed else 'FAIL', 'rows='+str(rows),'declared='+str(needed))
if actual!=expected or rows!=needed:raise SystemExit(1)
