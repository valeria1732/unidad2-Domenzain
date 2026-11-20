import pymupdf, shutil, os, re
BASE = r'c:\Users\calvi\OneDrive\Desktop\unidad 2 domenzain'
ORIG = os.path.join(BASE, 'Ejercicio_Desarrollo_e_integracion_continua_ORIGINAL.pdf')
DEST = os.path.join(BASE, 'Ejercicio_Desarrollo_e_integracion_continua.pdf')
if not os.path.exists(ORIG):
    shutil.copy(DEST, ORIG)

d = pymupdf.open(ORIG)
BLUE = (0.05, 0.2, 0.65)
GREEN = (0.0, 0.5, 0.15)
RED = (0.75, 0.1, 0.1)

def put(page, x0, x1, y0, y1, text, size=7.5, color=BLUE, bold=False, align=0, pad=2):
    """Escribe texto dentro de una celda; reduce la fuente si no cabe."""
    rect = pymupdf.Rect(x0 + pad, y0 + 1.5, x1 - pad, y1 - 1)
    fn = 'hebo' if bold else 'helv'
    s = size
    while s > 3.5:
        rc = page.insert_textbox(rect, text, fontsize=s, fontname=fn, color=color, align=align)
        if rc >= 0:
            return
        # no cabe: no se dibujó nada con rc<0 en PyMuPDF; reducir y reintentar
        s -= 0.4
    page.insert_textbox(rect, text, fontsize=3.6, fontname=fn, color=color, align=align)

# ---------- Página 11: matriz de casos (columna Resultado en CI) ----------
p = d[10]
filas = [(147,170),(170,218),(218,255),(255,278),(278,301),(301,324),(324,348),(348,370),(370,393),(393,431)]
for (y0, y1) in filas:
    put(p, 471, 535, y0, y1, 'Pasó (Jest)', size=8, color=GREEN, bold=True)
# bitácora: columnas x
bx = [66,102,145,197,239,279,321,364,406,448,491,534]
def cell(row_y, col, text, **k):
    put(p, bx[col], bx[col+1], row_y[0], row_y[1], text, **k)
r1, r2, r3 = (535,558), (558,624), (624,691)
datos = {
  r1: ['19/11/26', None, None, '10', '10', '0', '100 %', '1.4 s', 'Verde', 'Línea base 84ff002'],
  r2: ['19/11/26', None, None, '11', '10', '1', '100 %', '1.4 s', 'Rojo', '2e6ea93 CP-11: 107 ms >50. Ver Anexo'],
  r3: ['19/11/26', None, None, '11', '11', '0', '100 %', '1.0 s', 'Verde', 'c7724de Ciclo quitado. CP-11: 3 ms'],
}
for ry, vals in datos.items():
    for i, v in enumerate(vals):
        if v is None: continue
        col = i + 1
        color = GREEN if v == 'Verde' else RED if v == 'Rojo' else BLUE
        put(p, bx[col], bx[col+1], ry[0], ry[1], v, size=6.5, color=color, bold=(v in ('Verde','Rojo')))
# commit bajo la rama prefijada




# ---------- Página 16: tabla "antes" ----------
p = d[15]
vals_x = (338, 389); cum_x = (465, 535)
antes = [
  ((557,581), '776.01 ms', 'No', RED),
  ((581,604), '506.27 ms', 'No', RED),
  ((604,627), '648.17 ms', 'No', RED),
  ((627,650), '0.00 %', 'Sí', GREEN),
  ((650,687), '1188 ms', 'No', RED),
  ((687,717), '1.03 núcleos', 'Saturada', RED),
]
for (y0, y1), v, c, col in antes:
    put(p, vals_x[0], vals_x[1], y0, y1, v, size=7)
    put(p, cum_x[0], cum_x[1], y0, y1, c, size=8, color=col, bold=True)
# Página 17: continuación (peticiones por segundo)
p = d[16]
put(p, 338, 389, 147, 170, '50.8 req/s', size=7)
put(p, 465, 535, 147, 170, 'Referencia', size=7)
# hipótesis (sobre los espacios en blanco)
def sobre_blanco(page, rect, texto, size=8):
    cx = (rect.x0 + rect.x1) / 2
    w = pymupdf.get_text_length(texto, fontname='hebo', fontsize=size)
    page.insert_text((cx - w / 2, rect.y0 + 3.5), texto, fontsize=size, fontname='hebo', color=BLUE)
blancos = [r for r in p.search_for('___') if r.y0 < 330]
for rect, t in zip(blancos, ['/reporte', '45 ms', '/tasks', '40']):
    sobre_blanco(p, rect, t)

# ---------- Página 18: plan de mejora ----------
p = d[17]
px = [66,105,230,274,341,396,466,535]
def plan(y0, y1, textos):
    for i, t in enumerate(textos):
        put(p, px[i+1], px[i+2], y0, y1, t, size=6)
plan(183, 207, ['p95 /reporte 506 ms y /tasks 648 ms (k6, 40 VU); lag p99 1188 ms',
                'Ciclo de 50M iter. bloquea el hilo',
                'Quitar el ciclo; solo contar',
                'p95 <500 ms; lag <100 ms',
                'p95 4.2 ms; lag 17.8 ms'])
plan(207, 230, ['CP-10 pasaba con /reporte lento (>100 ms)',
                'Sin prueba de tiempo',
                'Prueba CP-11 en CI',
                'CP-11 rojo >50 ms y verde <50',
                '107 ms a 3 ms'])
# Estado: reemplazar "Pendiente"
for r in p.search_for('Pendiente'):
    if r.y0 < 240:
        p.add_redact_annot(r, fill=(1, 1, 1))
p.apply_redactions(images=0, graphics=0)
for (y0, y1) in [(183, 207), (207, 230)]:
    put(p, 466, 535, y0, y1, 'Cumplida', size=8, color=GREEN, bold=True)

# ---------- Página 19: comparación antes / después ----------
p = d[18]
cx = [236, 304, 346, 401, 471, 535]
comp = [
  ((354,377), '776.01 ms', '5.59 ms', '99.3 %', 'Sí'),
  ((377,400), '506.27 ms', '4.20 ms', '99.2 %', 'Sí'),
  ((400,423), '648.17 ms', '6.09 ms', '99.1 %', 'Sí'),
  ((423,446), '0.00 %', '0.00 %', '-', 'Sí'),
  ((446,484), '1188 ms', '17.8 ms', '98.5 %', 'Sí'),
  ((484,507), '1.03 núcleos', '0.14 núcleos', '86.3 %', 'Referencia'),
]
for (y0, y1), a, b, m, c in comp:
    put(p, 346, 401, y0, y1, a, size=7) if False else None
# columnas reales: Antes 346-401? se verifica abajo con las medidas de la imagen
ant, desp, mej, cum = (304, 346), (346, 401), (401, 471), (471, 535)
for (y0, y1), a, b, m, c in comp:
    put(p, ant[0], ant[1], y0, y1, a, size=6.5)
    put(p, desp[0], desp[1], y0, y1, b, size=6.5)
    put(p, mej[0], mej[1], y0, y1, m, size=7.5)
    put(p, cum[0], cum[1], y0, y1, c, size=8, color=GREEN if c == 'Sí' else BLUE, bold=True)

"
# ---------- Anexo: página separadora + evidencias del reporte ----------
rep = pymupdf.open(os.path.join(BASE, 'Reporte.pdf'))
sep = d.new_page(-1, width=612, height=792)
sep.insert_textbox(pymupdf.Rect(72, 150, 540, 230), 'ANEXO', fontsize=34, fontname='hebo', color=(0.12, 0.24, 0.43), align=1)
sep.insert_textbox(pymupdf.Rect(72, 205, 540, 300), 'Evidencias, análisis y plan de mejora completo', fontsize=18, fontname='helv', color=(0.12, 0.24, 0.43), align=1)
lineas = ['Evidencia 1: pruebas con cobertura, servicios y endpoints (Parte 1)',
          'Evidencias 2 y 3: GitHub Actions (pendientes de captura desde GitHub)',
          'Evidencia 4: Prometheus en UP y tablero de Grafana (Parte 3)',
          'Evidencia 5: k6 y Grafana, medición antes (Parte 4)',
          'Evidencia 6: k6 y Grafana, medición después (Parte 5)',
          'Diagnóstico, plan M-01, M-02 y M-03, comparación y conclusión']
y = 330
for l in lineas:
    sep.insert_text((120, y), l, fontsize=11, fontname='helv', color=(0.2, 0.2, 0.2)); y += 24
sep.insert_text((120, y + 20), 'Las celdas llenadas en las tablas de este documento están en azul.', fontsize=10, fontname='hebo', color=BLUE)
d.insert_pdf(rep, from_page=1)
d.save(os.path.join(BASE, '.tmpp', 'relleno.pdf'))
d.save(DEST)"
print('relleno ok')
