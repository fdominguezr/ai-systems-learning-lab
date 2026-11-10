#!/usr/bin/env python3
"""Recreate the public summary figures from the fixed derived values and nominal model sizes.

No original telemetry is included or regenerated. Continuous temperature curves
cannot be produced without verified original CSV inputs. Requires matplotlib,
numpy. This script only draws honest aggregate/endpoint figures.
Run from any directory: python scripts/plot_public_figures.py
"""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
DEST = Path(__file__).resolve().parents[1]
FIG = DEST / 'figures'
DATA = DEST / 'data'
FIG.mkdir(parents=True,exist_ok=True)
# Data constants below are copied only from published derived summaries / stated endpoints.
models=[('LFM 350M',0.35),('Qwen3 0.6B',0.6),('MiniCPM 1B',1.0),('LFM 1.2B',1.2),('MiniCPM 2B',2.0),('LFM 2.6B',2.6)]
plt.rcParams.update({'font.size':11,'axes.titlesize':16,'figure.dpi':120,'savefig.dpi':180})
fig,ax=plt.subplots(figsize=(10,5.3)); labels=[v[0] for v in models];vals=[v[1] for v in models]
ax.barh(labels,vals);ax.invert_yaxis();ax.set_xlim(0,3.0);ax.set_xlabel('Miles de millones de parámetros (B)');ax.set_title('Modelos de IA local: tamaños nominales')
for i,v in enumerate(vals):ax.text(v+.03,i,f'{v:g} B',va='center',fontsize=10)
fig.text(.1,.025,'Tamaños comerciales aproximados. No son consumo de RAM, velocidad ni temperatura.',fontsize=9)
fig.tight_layout(rect=[0,.055,1,1]);fig.savefig(FIG/'modelos_parametros.png');plt.close(fig)
# CPU inference diagram: rectangle geometry and arrows deliberately in gaps only
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(11, 4.2))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
fig.text(.5, .91, 'Cómo se ejecuta una respuesta sin GPU dedicada', ha='center', fontsize=16)
boxes = [
  (.02, .16, 'Pregunta\ndel usuario'),
  (.25, .26, 'Modelo cuantizado\nen memoria RAM'),
  (.58, .17, 'Cálculo con\nCPU ARM'),
  (.83, .15, 'Respuesta\ngenerada'),
]
for x, width, label in boxes:
    ax.add_patch(FancyBboxPatch((x,.43),width,.22,boxstyle='round,pad=0.008,rounding_size=0.025',
        transform=ax.transAxes,facecolor='white',edgecolor='black',linewidth=1.3))
    ax.text(x+width/2,.54,label,transform=ax.transAxes,va='center',ha='center',fontsize=10)
for left,right in zip(boxes[:-1],boxes[1:]):
    xa=left[0]+left[1]+.012; xb=right[0]-.012
    assert xb>xa, 'Arrows must fit entirely between rectangles'
    ax.annotate('',xy=(xb,.54),xytext=(xa,.54),xycoords=ax.transAxes,
        arrowprops={'arrowstyle':'->','lw':1.8,'mutation_scale':15})
fig.text(.5,.15,'Cuantización = menos bits por peso · RAM, tiempo y calor siguen siendo restricciones.',ha='center',fontsize=9)
fig.savefig(FIG/'inferencia_cpu.png',bbox_inches='tight');plt.close(fig)
# coverage three different sessions, no fake thermal series.
# Legend is BELOW the axes; this avoids obscuring the longest bar on desktop or mobile.
counts=[('Baja actividad',239,239),('Primera prueba',2699,2699),('Segunda prueba',303,2759)]
fig,ax=plt.subplots(figsize=(10.6,5.4))
x=np.arange(3); obs=[a[1] for a in counts]; missing=[a[2]-a[1] for a in counts]
ax.barh(x,obs,label='Muestras observadas',height=.62)
ax.barh(x,missing,left=obs,label='Sin registro',height=.62)
ax.invert_yaxis();ax.set_yticks(x,[a[0] for a in counts]);ax.set_xlabel('Número de muestras')
ax.set_title('Cobertura de los registros térmicos')
for i,(_,o,total) in enumerate(counts):
    ax.text(total+22,i,f'{o:,}/{total:,}'.replace(',','.'),va='center',fontsize=10)
ax.set_xlim(0,3300)
fig.subplots_adjust(left=.20,right=.97,top=.86,bottom=.30)
ax.legend(loc='upper center',bbox_to_anchor=(.5,-.17),ncol=2,frameon=False)
fig.text(.5,.04,'Cadencia nominal: una lectura cada 5 s. Tres sesiones independientes.',ha='center',fontsize=9)
fig.savefig(FIG/'cobertura_registros.png');plt.close(fig)
# first thermal points; no interpolating
fig,ax=plt.subplots(figsize=(9.6,4.8));ax.scatter([0,10],[33.589,27.745],s=90,marker='o')
ax.set_xlim(-1.2,11.5);ax.set_ylim(25,36);ax.set_xticks([0,10],['Fin de la carga','~10 min después']);ax.set_ylabel('Temperatura (°C)');ax.set_title('Recuperación: dos lecturas, no una curva reconstruida');ax.grid(alpha=.25)
for x,y in [(0,33.589),(10,27.745)]:ax.annotate(f'{y:.2f} °C',(x,y),xytext=(0,12),textcoords='offset points',ha='center')
fig.text(.11,.018,'Lecturas comunicadas de la primera prueba. No se representa la trayectoria entre ambas.',fontsize=9)
fig.tight_layout(rect=[0,.05,1,1]);fig.savefig(FIG/'recuperacion_dos_puntos.png');plt.close(fig)
# second comparison observed peak types, not max by model
fig,ax=plt.subplots(figsize=(9.8,5.0));vals=[38.946,37.97,37.48]
cats=['Registro cada 5 s\nmáximo','Controles de esa fase\nmáximo','Control posterior\npuntual']
ax.scatter(list(range(3)),vals,s=190)
ax.set_xticks(list(range(3)),cats)
ax.axhline(38.5,ls='--',label='Umbral experimental 38,5 °C')
ax.set_ylim(34,40);ax.set_ylabel('Temperatura (°C)')
ax.set_title('Segunda prueba: distintos instrumentos e instantes');ax.grid(axis='y',alpha=.25)
for i,v in enumerate(vals):ax.text(i,v+.14,f'{v:.2f} °C',ha='center')
fig.subplots_adjust(left=.10,right=.95,top=.85,bottom=.36)
ax.legend(loc='upper center',bbox_to_anchor=(.5,-.31),ncol=1,frameon=False)
fig.text(.5,.025,'Puntos con distinto alcance temporal: no corresponden a tres modelos comparables.',ha='center',fontsize=9)
fig.savefig(FIG/'segunda_prueba_registros.png');plt.close(fig)
# maxima by session but show noncausal, use dot plot no model label
fig,ax=plt.subplots(figsize=(9.6,4.8));ys=[37.972,38.946];x=[0,1];ax.scatter(x,ys,s=170)
for xx,yy in zip(x,ys):ax.annotate(f'{yy:.3f} °C',(xx,yy),xytext=(0,13),textcoords='offset points',ha='center')
ax.set_xlim(-.6,1.6);ax.set_xticks([0,1],['Primera prueba\n(ventana completa)','Segunda prueba\n(adquisición parcial)']);ax.set_ylim(35,40);ax.set_ylabel('Máximo registrado (°C)');ax.set_title('Máximos por sesión, NO por modelo')
ax.grid(axis='y',alpha=.25);fig.text(.1,.02,'Cambian tareas, secuencia, cuantización, duración y estado inicial.',fontsize=9)
fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(FIG/'maximos_por_sesion.png');plt.close(fig)
# confounding conceptual diagram
fig,ax=plt.subplots(figsize=(10.3,4.4));ax.axis('off');fig.text(.5,.89,'¿Un modelo mayor puede registrar menos temperatura?',ha='center',size=16)
items=['Carga real de CPU','Cuantización /\narquitectura','Tokens y latencia','Memoria / esperas','Temperatura inicial','Ventilación / ambiente']
for j,t in enumerate(items):
   row,col=divmod(j,3);x=.04+col*.32;y=.67-row*.36
   ax.text(x+.125,y,t,transform=ax.transAxes,va='center',ha='center',bbox={'boxstyle':'round,pad=.6','edgecolor':'black','facecolor':'white'},fontsize=10)
fig.text(.5,.12,'Sin controlar estas variables, tamaño de modelo ≠ explicación causal del máximo.',ha='center',size=10)
fig.savefig(FIG/'variables_confusion.png',bbox_inches='tight');plt.close(fig)
# experiment design graphic
fig,ax=plt.subplots(figsize=(10,4));ax.axis('off');fig.text(.5,.90,'Siguiente prueba: comparar en igualdad de condiciones',ha='center',size=15)
steps=['Misma tarea','Mismo presupuesto\nde salida','Inicio térmico\ncomparable','Orden alternado\ny repeticiones','Medir ambiente\ny energía']
for i,t in enumerate(steps):
    x=.018+i*.198
    ax.text(x+.089,.49,t,ha='center',va='center',transform=ax.transAxes,bbox=dict(boxstyle='round,pad=.45',edgecolor='black',facecolor='white'),fontsize=9)
    if i<4:ax.annotate('',xy=(x+.19,.49),xytext=(x+.175,.49),xycoords='axes fraction',arrowprops={'arrowstyle':'->'})
fig.text(.5,.13,'Objetivo: comparación controlada. Aún no ejecutada.',ha='center',size=10)
fig.savefig(FIG/'protocolo_futuro.png',bbox_inches='tight');plt.close(fig)
# public minimal derived overview
rows=[{'observacion':'baja_actividad','observadas':239,'previstas':239,'temp_min_c':26.284,'temp_max_c':28.719,'max_corresponds_to':'sesion_independiente','integridad_sha_csv':'pendiente'},
 {'observacion':'primera_prueba','observadas':2699,'previstas':2699,'temp_min_c':25.310,'temp_max_c':37.972,'max_corresponds_to':'sesion_varias_cargas','integridad_sha_csv':'pendiente'},
 {'observacion':'segunda_prueba','observadas':303,'previstas':2759,'temp_min_c':26.771,'temp_max_c':38.946,'max_corresponds_to':'sesion_cobertura_parcial','integridad_sha_csv':'pendiente'}]
with open(DATA/'resumen_sesiones.csv','w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)

print("Public summary figures created; original time series not reconstructed.")
