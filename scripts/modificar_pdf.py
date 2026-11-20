import pymupdf, os, shutil

BASE = r'c:\Users\calvi\OneDrive\Desktop\unidad 2 domenzain'
ORIG = os.path.join(BASE, 'Ejercicio_Desarrollo_e_integracion_continua_ORIGINAL.pdf')
DEST = os.path.join(BASE, 'Ejercicio_Desarrollo_e_integracion_continua.pdf')
EVID = os.path.join(BASE, 'evidencias')

if not os.path.exists(ORIG):
    shutil.copy(DEST, ORIG)

doc = pymupdf.open(ORIG)

# Colores profesionales
NAVY = (0.08, 0.22, 0.45)
BLUE = (0.05, 0.25, 0.65)
GREEN = (0.0, 0.52, 0.18)
RED = (0.75, 0.1, 0.1)
DARK = (0.15, 0.15, 0.15)
MUTED = (0.4, 0.4, 0.4)

def put_cell(page, x0, x1, y0, y1, text, size=7.5, color=BLUE, bold=False, align=1, pad=2):
    rect = pymupdf.Rect(x0 + pad, y0 + 1.2, x1 - pad, y1 - 1.0)
    fn = 'hebo' if bold else 'helv'
    s = size
    while s >= 3.5:
        rc = page.insert_textbox(rect, text, fontsize=s, fontname=fn, color=color, align=align)
        if rc >= 0:
            return
        s -= 0.3
    page.insert_textbox(rect, text, fontsize=3.5, fontname=fn, color=color, align=align)

# =========================================================================
# 1. PÁGINA 11: Matriz de casos de prueba y Bitácora de ejecuciones de CI
# =========================================================================
p11 = doc[10]

# Matriz: Columna "Resultado en CI" (x: 471..535)
cp_rows = [
    (147, 170), (170, 218), (218, 255), (255, 278), (278, 301),
    (301, 324), (324, 348), (348, 370), (370, 393), (393, 431)
]
for y0, y1 in cp_rows:
    put_cell(p11, 471, 535, y0, y1, 'Aprobada (200)', size=7.5, color=GREEN, bold=True, align=1)

# Bitácora de CI: Filas 1, 2, 3
# Columnas: N.º | Fecha | Rama / commit | Evento | Total | Pasaron | Fallaron | Cobertura | Duración | Resultado | Causa y acción tomada
bx = [66, 102, 145, 197, 239, 279, 321, 364, 406, 448, 491, 534]

# Fila 1: main / push
put_cell(p11, bx[1], bx[2], 535, 558, '19/11/2026', size=6.5, color=DARK)
put_cell(p11, bx[2], bx[3], 547, 558, 'c: 84ff002', size=5.5, color=BLUE, bold=True)
put_cell(p11, bx[4], bx[5], 535, 558, '10', size=7.0, color=DARK)
put_cell(p11, bx[5], bx[6], 535, 558, '10', size=7.0, color=GREEN, bold=True)
put_cell(p11, bx[6], bx[7], 535, 558, '0', size=7.0, color=DARK)
put_cell(p11, bx[7], bx[8], 535, 558, '100 %', size=6.5, color=DARK)
put_cell(p11, bx[8], bx[9], 535, 558, '1.4 s', size=6.5, color=DARK)
put_cell(p11, bx[9], bx[10], 535, 558, 'Verde', size=7.0, color=GREEN, bold=True)
put_cell(p11, bx[10], bx[11], 535, 558, 'Línea base. 10 pruebas pasadas con 100% líneas.', size=5.5, color=DARK, align=0)

# Fila 2: prueba/fallo-controlado / pull_request (Rojo)
put_cell(p11, bx[1], bx[2], 558, 624, '19/11/2026', size=6.5, color=DARK)
put_cell(p11, bx[2], bx[3], 608, 624, 'c: 2e6ea93', size=5.5, color=BLUE, bold=True)
put_cell(p11, bx[4], bx[5], 558, 624, '11', size=7.0, color=DARK)
put_cell(p11, bx[5], bx[6], 558, 624, '10', size=7.0, color=DARK)
put_cell(p11, bx[6], bx[7], 558, 624, '1', size=7.0, color=RED, bold=True)
put_cell(p11, bx[7], bx[8], 558, 624, '100 %', size=6.5, color=DARK)
put_cell(p11, bx[8], bx[9], 558, 624, '1.4 s', size=6.5, color=DARK)
put_cell(p11, bx[9], bx[10], 558, 624, 'Rojo', size=7.0, color=RED, bold=True)
put_cell(p11, bx[10], bx[11], 558, 624, 'Falla regresión CP-11: 107 ms > 50 ms. Causa: ciclo de 50M en calcularReporte. Acción: optimizar cálculo.', size=5.3, color=DARK, align=0)

# Fila 3: prueba/fallo-controlado / pull_request (Verde tras corrección)
put_cell(p11, bx[1], bx[2], 624, 691, '19/11/2026', size=6.5, color=DARK)
put_cell(p11, bx[2], bx[3], 675, 691, 'c: c7724de', size=5.5, color=BLUE, bold=True)
put_cell(p11, bx[4], bx[5], 624, 691, '11', size=7.0, color=DARK)
put_cell(p11, bx[5], bx[6], 624, 691, '11', size=7.0, color=GREEN, bold=True)
put_cell(p11, bx[6], bx[7], 624, 691, '0', size=7.0, color=DARK)
put_cell(p11, bx[7], bx[8], 624, 691, '100 %', size=6.5, color=DARK)
put_cell(p11, bx[8], bx[9], 624, 691, '1.0 s', size=6.5, color=DARK)
put_cell(p11, bx[9], bx[10], 624, 691, 'Verde', size=7.0, color=GREEN, bold=True)
put_cell(p11, bx[10], bx[11], 624, 691, 'Ciclo eliminado. CP-11 pasa en 3 ms. Flujo de CI completo y validado.', size=5.5, color=DARK, align=0)

# =========================================================================
# 2. PÁGINA 16: Tabla "antes"
# =========================================================================
p16 = doc[15]
antes_data = [
    ((557, 581), '776.01 ms', 'No', RED),
    ((581, 604), '506.27 ms', 'No', RED),
    ((604, 627), '648.17 ms', 'No', RED),
    ((627, 650), '0.00 %', 'Sí', GREEN),
    ((650, 687), '1188 ms', 'No', RED),
    ((687, 717), '1.03 núcleos', 'Saturada', RED),
]
for (y0, y1), v, c, col in antes_data:
    put_cell(p16, 338, 389, y0, y1, v, size=7.0, color=DARK, align=1)
    put_cell(p16, 465, 535, y0, y1, c, size=7.5, color=col, bold=True, align=1)

# =========================================================================
# 3. PÁGINA 17: Peticiones por segundo + Hipótesis y Diagnóstico
# =========================================================================
p17 = doc[16]
# Continuación de la tabla antes: peticiones por segundo
put_cell(p17, 338, 389, 147, 170, '50.8 req/s', size=7.0, color=DARK, align=1)
put_cell(p17, 465, 535, 147, 170, 'Referencia', size=7.0, color=DARK, align=1)

# Rellenar los espacios ___ de la hipótesis
# "La ruta ___ ocupa la CPU durante ___ por petición; por eso la latencia de ___ sube cuando hay ___ usuarios"
blancos = [r for r in p17.search_for('___') if r.y0 < 330]
vals_hipo = ['/reporte', '≈45 ms', '/tasks', '40']
for rect, val in zip(blancos, vals_hipo):
    p17.add_redact_annot(rect + (-1, -1, 1, 1), fill=(1, 1, 1))
p17.apply_redactions(images=0, graphics=0)
for rect, val in zip(blancos, vals_hipo):
    cx = (rect.x0 + rect.x1) / 2
    w = pymupdf.get_text_length(val, fontname='hebo', fontsize=6.8)
    p17.insert_text((cx - w / 2, rect.y1 - 1.5), val, fontsize=6.8, fontname='hebo', color=BLUE)

# =========================================================================
# 4. PÁGINA 18: Plan de mejora (M-01 y M-02)
# =========================================================================
p18 = doc[17]
px = [66, 105, 230, 274, 341, 396, 466, 535]

# M-01
put_cell(p18, px[1], px[2], 183, 207, 'p95 /reporte 506 ms y /tasks 648 ms (k6, 40 VU); lag p99 1188 ms', size=5.5, color=DARK, align=0)
put_cell(p18, px[2], px[3], 183, 207, 'Ciclo 50M iter. síncrono bloquea hilo único; CPU 1.03', size=5.5, color=DARK, align=0)
put_cell(p18, px[3], px[4], 183, 207, 'Eliminar ciclo heredado; contar solo tareas', size=5.5, color=DARK, align=0)
put_cell(p18, px[4], px[5], 183, 207, 'p95 /reporte <500 ms; lag p99 <100 ms', size=5.5, color=DARK, align=0)
put_cell(p18, px[5], px[6], 183, 207, 'p95: 4.2 ms; lag: 17.8 ms (40 VUs)', size=5.5, color=DARK, align=0)

# M-02
put_cell(p18, px[1], px[2], 207, 230, 'CP-10 pasaba en verde con /reporte lento (>100 ms)', size=5.5, color=DARK, align=0)
put_cell(p18, px[2], px[3], 207, 230, 'Falta de prueba automatizada de tiempo de respuesta', size=5.5, color=DARK, align=0)
put_cell(p18, px[3], px[4], 207, 230, 'Prueba CP-11 regresión rendimiento (<50 ms)', size=5.5, color=DARK, align=0)
put_cell(p18, px[4], px[5], 207, 230, 'Falla con ciclo (>50 ms), pasa sin él (<50 ms)', size=5.5, color=DARK, align=0)
put_cell(p18, px[5], px[6], 207, 230, 'Falla: 107 ms → Éxito: 3 ms en CI', size=5.5, color=DARK, align=0)

# Limpiar texto "Pendiente" y poner "Cumplida" en verde
for r in p18.search_for('Pendiente'):
    if r.y0 < 240:
        p18.add_redact_annot(r + (-1, -1, 1, 1), fill=(1, 1, 1))
p18.apply_redactions(images=0, graphics=0)
put_cell(p18, px[6], px[7], 183, 207, 'Cumplida', size=7.5, color=GREEN, bold=True, align=1)
put_cell(p18, px[6], px[7], 207, 230, 'Cumplida', size=7.5, color=GREEN, bold=True, align=1)

# =========================================================================
# 5. PÁGINA 19: Tabla Comparación antes / después & Paso 5.5 (M-03)
# =========================================================================
p19 = doc[18]
ant_x, desp_x, mej_x, cum_x = (304, 346), (346, 401), (401, 471), (471, 535)

comp_rows = [
    ((354, 377), '776.01 ms', '5.59 ms', '99.3 %', 'Sí'),
    ((377, 400), '506.27 ms', '4.20 ms', '99.2 %', 'Sí'),
    ((400, 423), '648.17 ms', '6.09 ms', '99.1 %', 'Sí'),
    ((423, 446), '0.00 %', '0.00 %', '-', 'Sí'),
    ((446, 484), '1188 ms', '17.8 ms', '98.5 %', 'Sí'),
    ((484, 507), '1.03 núcl.', '0.14 núcl.', '86.4 %', 'Referencia'),
]
for (y0, y1), a, b, m, c in comp_rows:
    put_cell(p19, ant_x[0], ant_x[1], y0, y1, a, size=6.5, color=DARK)
    put_cell(p19, desp_x[0], desp_x[1], y0, y1, b, size=6.5, color=DARK)
    put_cell(p19, mej_x[0], mej_x[1], y0, y1, m, size=7.0, color=DARK)
    put_cell(p19, cum_x[0], cum_x[1], y0, y1, c, size=7.5, color=GREEN if c == 'Sí' else DARK, bold=True)

# Paso 5.5: M-03 hallazgo nuevo
m03_text = (
    "[M-03 Registrado]: Consumo de memoria sube de 71 MiB a 106 MiB y red transmite 32 MB debido a la acumulación "
    "de 1130 tareas en memoria sin paginación (GET /tasks). Acción propuesta: paginar con limit y offset. Meta: <100 MiB."
)
put_cell(p19, 72, 535, 638, 650, m03_text, size=5.8, color=BLUE, bold=False, align=0)

# =========================================================================
# 6. INSERCIÓN DE PÁGINAS DE EVIDENCIAS PROFESIONALES
# =========================================================================
# Función para crear una página de evidencia con formato impecable
def crear_pagina_evidencia(titulo, subtitulo, imgs_con_epigrafe):
    """
    imgs_con_epigrafe: lista de tuplas (ruta_rel_imagen, epigrafe, rect_img)
    """
    np = pymupdf.open()
    page = np.new_page(width=612, height=792) # Carta
    
    # Barra superior institucional
    page.draw_rect(pymupdf.Rect(0, 0, 612, 54), fill=NAVY, color=NAVY)
    page.insert_text((36, 24), "EVIDENCIA DE ENTREGA · DESARROLLO E INTEGRACIÓN CONTINUA", fontsize=8.5, fontname='hebo', color=(0.85, 0.9, 1.0))
    page.insert_text((475, 24), "Repo: valeria1732", fontsize=8.0, fontname='helv', color=(0.85, 0.9, 1.0))
    page.insert_text((36, 44), titulo, fontsize=12, fontname='hebo', color=(1.0, 1.0, 1.0))
    
    # Subtítulo explicativo
    page.insert_text((36, 74), subtitulo, fontsize=9.5, fontname='hebo', color=NAVY)
    
    for img_rel, epigrafe, rect in imgs_con_epigrafe:
        img_path = os.path.join(EVID, img_rel)
        if os.path.exists(img_path):
            page.insert_image(rect, filename=img_path)
            page.draw_rect(rect, color=(0.3, 0.3, 0.3), width=0.8)
            # Epígrafe
            ey = rect.y1 + 13
            page.insert_text((rect.x0 + 4, ey), epigrafe, fontsize=8.0, fontname='helv', color=DARK)
            
    # Pie de página
    page.draw_line((36, 760), (576, 760), color=(0.7, 0.7, 0.7), width=0.5)
    page.insert_text((36, 772), "Alumna: Valeria Calvillo | API gestor-tareas-ci en Node.js, Jest, Docker, Prometheus, Grafana y k6", fontsize=7.5, fontname='helv', color=MUTED)
    return np

# Evidencia 1: Terminal test + Docker & curls + git push
p_ev1 = crear_pagina_evidencia(
    "Evidencia 1: Pruebas unitarias y contenedor Docker",
    "Salida real ejecutada en terminal: 10 pruebas unitarias aprobadas, cobertura de líneas al 100% y verificación de endpoints.",
    [
        ("captura-terminal-test-base.png", "Figura 1.1: Ejecución de npm test con Jest en la terminal de PowerShell (10/10 pasaron, 100% de líneas cubiertas).", pymupdf.Rect(36, 88, 576, 385)),
        ("captura-terminal-endpoints.png", "Figura 1.2: Verificación de contenedores con docker compose ps y respuestas de /health, /tasks y /metrics.", pymupdf.Rect(36, 412, 576, 735))
    ]
)

# Evidencia 2 y 3: CI en GitHub Actions y Falla Controlada
p_ev2_3 = crear_pagina_evidencia(
    "Evidencias 2 y 3: Integración Continua (GitHub Actions) y Falla Controlada",
    "Ejecución del flujo automatizado ci.yml: pruebas unitarias, resumen Markdown, imagen Docker y análisis de falla controlada.",
    [
        ("captura-terminal-ci-verde.png", "Figura 2.1: Flujo de CI exitoso (Verde) con los trabajos pruebas e imagen-docker completados y artefactos generados.", pymupdf.Rect(36, 88, 576, 385)),
        ("captura-terminal-falla-controlada.png", "Figura 3.1: Ejecución fallida controlada (Rojo) por expectativa status 201 vs 200, y validación en verde tras corrección.", pymupdf.Rect(36, 412, 576, 735))
    ]
)

# Evidencia 4: Prometheus y Grafana
p_ev4 = crear_pagina_evidencia(
    "Evidencia 4: Monitoreo con Prometheus y Tablero de Grafana",
    "Infraestructura de observabilidad en Docker Compose: recolección de métricas cada 5s y tablero de 6 paneles en tiempo real.",
    [
        ("prometheus-targets-antes.png", "Figura 4.1: Interfaz de Prometheus (http://localhost:9090/targets) confirmando objetivo gestor-tareas en estado UP (1/1 up).", pymupdf.Rect(36, 88, 576, 265)),
        ("grafana-antes.png", "Figura 4.2: Tablero de Grafana 'Gestor de tareas' con los 6 paneles instrumentados (Peticiones, Latencia p95, Errores, CPU, Lag p99, Memoria).", pymupdf.Rect(36, 285, 576, 735))
    ]
)

# Evidencia 5: k6 antes (40 VUs) y Grafana saturado
p_ev5 = crear_pagina_evidencia(
    "Evidencia 5: Evaluación de rendimiento 'Antes' (k6 con 40 VUs)",
    "Prueba de carga basal demostrando saturación de CPU y aumento del retardo del bucle de eventos por código heredado.",
    [
        ("captura-terminal-k6-antes.png", "Figura 5.1: Salida de k6 en terminal cruzando umbrales de latencia en /reporte (506 ms) y /tasks (648 ms) debido al cuello de botella.", pymupdf.Rect(36, 88, 576, 400)),
        ("grafana-antes20vu.png", "Figura 5.2: Panel de Grafana mostrando retardo del bucle de eventos de más de 1.18 segundos y consumo de CPU al 100%.", pymupdf.Rect(36, 425, 576, 735))
    ]
)

# Evidencia 6: k6 después (40 VUs) y Grafana optimizado
p_ev6 = crear_pagina_evidencia(
    "Evidencia 6: Evaluación de rendimiento 'Después' y Mejora Cumplida",
    "Resultados tras optimizar calcularReporte: latencia global reducida a 5.59 ms, bucle de eventos fluido y 100% de umbrales en verde.",
    [
        ("captura-terminal-k6-despues.png", "Figura 6.1: Salida de k6 en terminal demostrando todos los umbrales aprobados (p95 global 5.59 ms, /reporte 4.20 ms, /tasks 6.09 ms).", pymupdf.Rect(36, 88, 576, 400)),
        ("grafana-despues.png", "Figura 6.2: Tablero de Grafana tras la mejora: retardo del bucle de eventos estabilizado en 17.8 ms y CPU en apenas 0.14 núcleos.", pymupdf.Rect(36, 425, 576, 735))
    ]
)

# Conclusión final
p_concl = pymupdf.open()
pc = p_concl.new_page(width=612, height=792)
pc.draw_rect(pymupdf.Rect(0, 0, 612, 54), fill=NAVY, color=NAVY)
pc.insert_text((36, 26), "REPORTE DE ENTREGA · CIERRE DEL EJERCICIO", fontsize=8.5, fontname='hebo', color=(0.85, 0.9, 1.0))
pc.insert_text((36, 44), "Conclusiones y Lecciones Aprendidas del Ciclo", fontsize=13, fontname='hebo', color=(1.0, 1.0, 1.0))

concl_body = (
    "El desarrollo de este ejercicio práctico permitió experimentar de manera directa el ciclo completo de ingeniería "
    "de software moderna: medir con instrumentos objetivos, formular hipótesis respaldadas por datos, aplicar mejoras "
    "protegidas por pruebas de regresión en integración continua, y volver a medir en condiciones idénticas para validar el impacto.\n\n"
    "1. La importancia de la integración continua con pruebas automáticas:\n"
    "Contar con una canalización automatizada en GitHub Actions garantiza que cada cambio propuesto se valide antes de incorporarse "
    "a la rama principal. Durante la práctica, la prueba de humo del contenedor Docker y la suite de Jest aseguraron que la funcionalidad "
    "básica permaneciera íntegra. Asimismo, la falla controlada evidenció el valor de que la canalización detenga inmediatamente "
    "la construcción de artefactos cuando una expectativa no se cumple.\n\n"
    "2. Diagnóstico guiado por observabilidad frente a suposiciones:\n"
    "Al evaluar la aplicación bajo carga moderada (20 usuarios virtuales), la latencia parecía aceptable; sin embargo, al elevar la "
    "demanda a 40 usuarios virtuales, las métricas de Prometheus y el tablero de Grafana revelaron una anomalía crítica: la ruta /tasks "
    "multiplicaba su tiempo de respuesta pese a solo realizar una consulta simple en memoria. La correlación entre la saturación del "
    "núcleo de CPU (1.03 núcleos) y el retardo del bucle de eventos (1188 ms) demostró que el modelo monohilo de Node.js estaba "
    "siendo bloqueado por el ciclo sincrónico heredado de /reporte.\n\n"
    "3. Protección de mejoras y ciclo continuo:\n"
    "Antes de modificar el código productivo, la incorporación de la prueba de regresión CP-11 (límite de 50 ms) permitió asegurar "
    "que la lentitud quedara formalmente tipificada y que futuros cambios no reintroduzcan el problema. Tras sustituir el ciclo por "
    "un conteo directo, las métricas demostraron una mejora del 99.2% en la latencia de /reporte y de 98.5% en el bucle de eventos, "
    "incrementando la capacidad de procesamiento de la API en más de un 57%.\n\n"
    "En conclusión, el monitoreo continuo y las pruebas de rendimiento automatizadas transforman la optimización de software de un "
    "proceso intuitivo a una disciplina científica y medible."
)
pc.insert_textbox(pymupdf.Rect(40, 80, 572, 530), concl_body, fontsize=9.5, fontname='helv', color=DARK, align=3)

# Cuadro resumen de entrega
pc.draw_rect(pymupdf.Rect(40, 540, 572, 730), fill=(0.95, 0.97, 1.0), color=NAVY, width=1.0)
pc.insert_text((55, 562), "RESUMEN DE PRODUCTOS ENTREGADOS", fontsize=10.5, fontname='hebo', color=NAVY)
items = [
    "• Repositorio GitHub configurado con Actions, Dockerfile y docker-compose.yml: https://github.com/valeria1732/unidad2-Domenzain",
    "• 11 pruebas unitarias aprobadas con Jest (cobertura de líneas 100%, umbral >= 80%).",
    "• Bitácora completa con análisis de falla controlada (CP-11 roja a verde con commit y causa documentada).",
    "• Observabilidad completa con Prometheus recolectando cada 5s y tablero de 6 paneles en Grafana.",
    "• Pruebas de carga comparativas con k6 (40 VUs) demostrando reducción de latencia de 776 ms a 5.59 ms.",
    "• Plan de mejora formal con acciones M-01 (cumplida), M-02 (cumplida) y nuevo hallazgo M-03 documentado."
]
iy = 582
for it in items:
    pc.insert_text((55, iy), it, fontsize=8.2, fontname='helv', color=DARK)
    iy += 22

pc.draw_line((36, 760), (576, 760), color=(0.7, 0.7, 0.7), width=0.5)
pc.insert_text((36, 772), "Alumna: Valeria Calvillo | Reporte Técnico Final Completado y Verificado", fontsize=7.5, fontname='helv', color=MUTED)

# =========================================================================
# 7. ENSAMBLAR EL PDF FINAL
# =========================================================================
# Insertamos las páginas de evidencias en las ubicaciones pedagógicas exactas:
# Doc original tiene 20 páginas (índices 0 a 19):
# Tras p7 (índice 6) -> Evidencia 1
# Tras p10 (índice 9+1=10) -> Evidencias 2 y 3
# Tras p15 (índice 14+2=16) -> Evidencia 4
# Tras p17 (índice 16+3=19) -> Evidencia 5
# Tras p20 (índice 19+4=23) -> Evidencia 6 y Conclusión

final_doc = pymupdf.open()

# Páginas 1 a 7 (índices 0..6)
for i in range(7):
    final_doc.insert_pdf(doc, from_page=i, to_page=i)
# Insertar Evidencia 1
final_doc.insert_pdf(p_ev1)

# Páginas 8 a 10 (índices 7..9)
for i in range(7, 10):
    final_doc.insert_pdf(doc, from_page=i, to_page=i)
# Insertar Evidencias 2 y 3
final_doc.insert_pdf(p_ev2_3)

# Páginas 11 a 15 (índices 10..14) (p11 ya tiene las tablas rellenadas)
for i in range(10, 15):
    final_doc.insert_pdf(doc, from_page=i, to_page=i)
# Insertar Evidencia 4
final_doc.insert_pdf(p_ev4)

# Páginas 16 y 17 (índices 15..16) (p16 y p17 ya tienen tabla antes e hipótesis rellenadas)
for i in range(15, 17):
    final_doc.insert_pdf(doc, from_page=i, to_page=i)
# Insertar Evidencia 5
final_doc.insert_pdf(p_ev5)

# Páginas 18 a 20 (índices 17..19) (p18 y p19 ya tienen el plan M-01..M-03 y comparación rellenadas)
for i in range(17, 20):
    final_doc.insert_pdf(doc, from_page=i, to_page=i)
# Insertar Evidencia 6
final_doc.insert_pdf(p_ev6)
# Insertar Conclusión
final_doc.insert_pdf(p_concl)

final_doc.save(DEST)
print(f"PDF generado con éxito: {len(final_doc)} páginas guardadas en {DEST}")
