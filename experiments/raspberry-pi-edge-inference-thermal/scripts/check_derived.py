#!/usr/bin/env python3
"""Recreate the published, deliberately non-interpolated summary plots.
Requirements: Python 3.10+, matplotlib, numpy, Pillow. No original logs or network access.
Input dataset: ../data/resumen_sesiones.csv (source-derived, no model attribution).
For exact scripts of the source acquisition, refer to the private laboratory.
"""
import csv
from pathlib import Path
P=Path(__file__).resolve().parents[1]
with (P/'data/resumen_sesiones.csv').open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==3 and [int(r['observadas']) for r in rows]==[239,2699,303]
print('Datos derivados presentes; gráficos regenerables mediante plot_public_figures.py. La serie temporal completa requiere los CSV originales verificados.')
