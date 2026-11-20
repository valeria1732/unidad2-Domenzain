import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE = r'c:\Users\calvi\OneDrive\Desktop\unidad 2 domenzain'
EVID = os.path.join(BASE, 'evidencias')
OUTPUT_DOCX = os.path.join(BASE, 'Ejercicio_Desarrollo_e_integracion_continua.docx')

doc = docx.Document()

# ----------------- Configuración de página (Carta y márgenes) -----------------
for section in doc.sections:
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)
    
    # Encabezado
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("Ejercicio Práctico · Desarrollo e Integración Continua | Valeria Calvillo")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(120, 120, 120)
    
    # Pie de página
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun = fp.add_run("Repositorio GitHub: https://github.com/valeria1732/unidad2-Domenzain")
    frun.font.name = "Calibri"
    frun.font.size = Pt(8.5)
    frun.font.color.rgb = RGBColor(120, 120, 120)

COLOR_NAVY = RGBColor(31, 78, 121)     # #1F4E79
COLOR_STEEL = RGBColor(46, 117, 182)   # #2E75B6
COLOR_DARK = RGBColor(38, 38, 38)      # #262626
COLOR_GREEN = RGBColor(16, 124, 65)    # #107C41
COLOR_RED = RGBColor(196, 43, 28)      # #C42B1C

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_STEEL
    return p

def add_heading_3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = COLOR_DARK
    return p

def add_p(text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.italic = italic
    r.font.color.rgb = COLOR_DARK
    return p

def add_callout(text, title="NOTA TÉCNICA"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.9)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1F4E79"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_after = Pt(2)
    rt = cp.add_run(f"📌 {title}: ")
    rt.font.name = "Calibri"
    rt.font.size = Pt(9.5)
    rt.font.bold = True
    rt.font.color.rgb = COLOR_NAVY
    
    rc = cp.add_run(text)
    rc.font.name = "Calibri"
    rc.font.size = Pt(9.5)
    rc.font.color.rgb = COLOR_DARK
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_image_box(filename, caption):
    img_path = os.path.join(EVID, filename)
    if not os.path.exists(img_path):
        img_path = os.path.join(BASE, filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.6))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap = p_cap.add_run(f"Figura: {caption}")
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(8.5)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(100, 100, 100)

def style_table(tbl, col_widths, headers, data, align_cols=None):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    # Encabezado
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = Inches(col_widths[i])
        set_cell_background(hdr_cells[i], "1F4E79")
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=90, right=90)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(h)
        run.font.name = "Calibri"
        run.font.size = Pt(8.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    # Filas de datos
    for r_idx, row_data in enumerate(data):
        row_cells = tbl.rows[r_idx + 1].cells
        bg_color = "F9FAFC" if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].width = Inches(col_widths[c_idx])
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=70, bottom=70, left=80, right=80)
            p = row_cells[c_idx].paragraphs[0]
            if align_cols and c_idx in align_cols:
                p.alignment = align_cols[c_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            
            run = p.add_run(str(val))
            run.font.name = "Calibri"
            run.font.size = Pt(8.0)
            
            if str(val) in ["Aprobada (200)", "Verde", "Sí", "Cumplida"]:
                run.font.bold = True
                run.font.color.rgb = COLOR_GREEN
            elif str(val) in ["Rojo", "No"]:
                run.font.bold = True
                run.font.color.rgb = COLOR_RED
            elif str(val) in ["Saturada"]:
                run.font.bold = True
                run.font.color.rgb = RGBColor(180, 80, 0)
            else:
                run.font.color.rgb = COLOR_DARK
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# =========================================================================
# 1. PORTADA PROFESIONAL
# =========================================================================
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_before = Pt(40)
p_inst.paragraph_format.space_after = Pt(8)
r_inst = p_inst.add_run("UNIDAD 2 · DESARROLLO E INTEGRACIÓN CONTINUA")
r_inst.font.name = "Calibri"
r_inst.font.size = Pt(11)
r_inst.font.bold = True
r_inst.font.color.rgb = COLOR_STEEL

p_tit = doc.add_paragraph()
p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_tit.paragraph_format.space_after = Pt(12)
r_tit = p_tit.add_run("Ejercicio Práctico:\nDesarrollo e Integración Continua, Monitoreo y Evaluación de Rendimiento")
r_tit.font.name = "Calibri"
r_tit.font.size = Pt(20)
r_tit.font.bold = True
r_tit.font.color.rgb = COLOR_NAVY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(40)
r_sub = p_sub.add_run("API de Gestión de Tareas en Node.js, Suite de Pruebas Jest, CI en GitHub Actions,\nObservabilidad con Prometheus y Grafana, y Carga con k6")
r_sub.font.name = "Calibri"
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = RGBColor(90, 90, 90)

# Cuadro de datos de entrega
tbl_meta = doc.add_table(rows=5, cols=2)
tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_meta.autofit = False
tbl_meta.columns[0].width = Inches(2.2)
tbl_meta.columns[1].width = Inches(4.4)
metadata = [
    ("Alumna:", "Valeria Calvillo"),
    ("Repositorio Oficial:", "https://github.com/valeria1732/unidad2-Domenzain"),
    ("Rama Principal:", "main (proyecto base) / mejora/reporte-rapido (mejora aplicada)"),
    ("Tecnologías Empleadas:", "Node.js 22, Express, Jest, Supertest, Docker Compose, Prometheus, Grafana, k6"),
    ("Fecha de Realización:", "19 de noviembre de 2026")
]
for i, (k, v) in enumerate(metadata):
    c0 = tbl_meta.cell(i, 0)
    c1 = tbl_meta.cell(i, 1)
    set_cell_background(c0, "F0F4F8")
    set_cell_background(c1, "FFFFFF")
    set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
    set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
    p0 = c0.paragraphs[0]; p0.paragraph_format.space_after = Pt(0)
    r0 = p0.add_run(k); r0.font.bold = True; r0.font.color.rgb = COLOR_NAVY; r0.font.size = Pt(9.5)
    p1 = c1.paragraphs[0]; p1.paragraph_format.space_after = Pt(0)
    r1 = p1.add_run(v); r1.font.color.rgb = COLOR_DARK; r1.font.size = Pt(9.5)

doc.add_page_break()

# =========================================================================
# 2. RESUMEN EJECUTIVO Y OBJETIVOS DEL EJERCICIO
# =========================================================================
add_heading_1("1. Visión General del Ejercicio y Objetivos")
add_p(
    "El presente informe documenta la implementación completa y el análisis exhaustivo del ciclo de ingeniería de software "
    "consistente en medir, mejorar y volver a medir. El ejercicio integra el desarrollo de una API RESTful en Node.js/Express, "
    "la instrumentación de pruebas unitarias automatizadas con umbrales de cobertura estricta, la configuración de una canalización "
    "de integración continua con GitHub Actions, la observabilidad en tiempo real con Prometheus y Grafana, y la evaluación rigurosa "
    "de rendimiento bajo carga con k6."
)

add_callout(
    "El ciclo de optimización no se basa en conjeturas ni en la lectura pasiva de código fuente. Se fundamenta en la observabilidad "
    "objetiva de métricas del sistema: tiempo de respuesta en percentil 95 (p95), uso efectivo de CPU, retardo del bucle de eventos "
    "(event loop lag) y tasas de error. Cada acción correctiva está justificada por un hallazgo cuantificado y protegida por pruebas "
    "automatizadas de regresión.",
    title="FILOSOFÍA DEL EJERCICIO"
)

add_heading_2("1.1 Estructura del Repositorio de Trabajo")
add_p(
    "El proyecto se encuentra organizado bajo una arquitectura estándar de microservicio contenedorizado:",
    bold_prefix="Distribución de archivos: "
)

add_p(
    "gestor-tareas-ci/\n"
    "├── .github/workflows/ci.yml         # Flujo de CI automatizado (pruebas + docker build)\n"
    "├── k6/carga.js                     # Script de prueba de carga con etapas y umbrales\n"
    "├── monitoring/\n"
    "│   ├── prometheus.yml               # Configuración de scrapeo métrico (intervalo 5s)\n"
    "│   └── grafana/provisioning/        # Aprovisionamiento automatizado de datasources\n"
    "├── scripts/\n"
    "│   ├── resumen-pruebas.js           # Generador de tabla Step Summary para GitHub Actions\n"
    "│   └── dashboard.json               # Definición declarativa del tablero de Grafana (6 paneles)\n"
    "├── src/\n"
    "│   ├── app.js                       # Lógica de la API, rutas (/tasks, /reporte, /metrics)\n"
    "│   └── server.js                    # Punto de entrada y listener HTTP en puerto 3000\n"
    "├── tests/tasks.test.js              # Suite de pruebas unitarias y de regresión con Jest\n"
    "├── Dockerfile                       # Definición multi-stage de imagen Node 22 Alpine\n"
    "├── docker-compose.yml               # Orquestación de API, Prometheus, Grafana y k6\n"
    "└── package.json                    # Dependencias y scripts de prueba con cobertura",
    italic=True
)

# =========================================================================
# 3. PARTE 1: PROYECTO BASE, PRUEBAS Y CONTENEDOR DOCKER
# =========================================================================
add_heading_1("2. Parte 1: Proyecto Base, Pruebas y Contenedor Docker")
add_p(
    "Se desarrolló una API RESTful para la gestión de tareas en memoria. La API expone rutas operativas (/health), funcionales "
    "(/tasks mediante GET, POST, PUT, DELETE), analíticas (/reporte con código heredado que simula validación intensiva) y métricas "
    "(/metrics recolectadas por la librería oficial prom-client)."
)

add_heading_2("2.1 Evidencia 1: Pruebas Unitarias con Cobertura y Verificación de Endpoints")
add_p(
    "Se configuró Jest con cobertura obligatoria de líneas superior al 80%. La ejecución en terminal demostró un 100% de cobertura "
    "en todas las sentencias y líneas del archivo src/app.js, aprobando las 10 pruebas unitarias iniciales."
)

add_image_box(
    "captura-terminal-test-base.png",
    "Ejecución de npm test en Windows Terminal (PowerShell): 10 pruebas aprobadas, 100% de cobertura en líneas."
)

add_p(
    "Posteriormente se construyó la imagen Docker local mediante Dockerfile multi-etapa basado en node:22-alpine. "
    "Se levantó el contenedor y se verificó la salud del servicio y la exposición de métricas con herramientas de línea de comandos:"
)

add_image_box(
    "captura-terminal-endpoints.png",
    "Verificación de contenedores con docker compose ps y validación funcional de endpoints (/health, /tasks, /metrics)."
)

add_image_box(
    "push.png",
    "Confirmación de subida del código fuente inicial a la rama main del repositorio en GitHub."
)

# =========================================================================
# 4. PARTE 2: INTEGRACIÓN CONTINUA (GITHUB ACTIONS) Y SEGUIMIENTO
# =========================================================================
add_heading_1("3. Parte 2: Integración Continua con GitHub Actions y Seguimiento de Pruebas")
add_p(
    "La canalización de CI definida en .github/workflows/ci.yml automatiza la validación en cada push y pull request hacia la rama main. "
    "El flujo se divide en dos trabajos secuenciales encadenados por dependencia (needs):"
)
add_p("1. Trabajo 'pruebas': Ejecuta npm ci, corre la suite de Jest con cobertura forzada, genera el archivo test-results.json, publica una tabla Markdown en el panel de GitHub ($GITHUB_STEP_SUMMARY) y almacena artefactos con retención preventiva.")
add_p("2. Trabajo 'imagen-docker': Solo se activa si el trabajo de pruebas es exitoso. Construye la imagen de producción y ejecuta una prueba de humo (smoke test) verificando que /health responda en menos de 15 segundos y que /metrics exponga métricas válidas.")

add_heading_2("3.1 Evidencia 2 y 3: Flujo Exitoso, Falla Controlada y Corrección")
add_image_box(
    "captura-terminal-ci-verde.png",
    "Ejecución exitosa del flujo CI en GitHub Actions: trabajos de pruebas e imagen-docker completados con Step Summary."
)

add_p(
    "Para poner a prueba la rigurosidad de la canalización, se creó la rama prueba/fallo-controlado y se alteró deliberadamente "
    "la prueba de salud esperando status 201 en lugar de 200. La canalización detectó la incompatibilidad inmediatamente, "
    "marcó el trabajo de pruebas en ROJO y abortó por completo la construcción de la imagen Docker (trabajo omitido), "
    "evitando el despliegue de código defectuoso. Tras corregir la prueba a status 200, la canalización retornó a estado VERDE."
)

add_image_box(
    "captura-terminal-falla-controlada.png",
    "Detalle de la falla controlada (Rojo) por expectativa status 201 vs 200, y validación en verde tras corrección."
)

add_heading_2("3.2 Matriz de Casos de Prueba")
add_p("A continuación se presenta la matriz formal con los 10 casos de prueba originales y la prueba de regresión CP-11:")

matriz_headers = ["ID", "Endpoint", "Escenario de Prueba", "Resultado Esperado", "Resultado en CI"]
matriz_widths = [0.8, 1.4, 1.8, 1.7, 1.2]
matriz_data = [
    ["CP-01", "GET /health", "Consulta de salud del servicio", "200 y {\"status\":\"ok\"}", "Aprobada (200)"],
    ["CP-02", "GET /metrics", "Exposición de métricas Prometheus", "200 y http_request_duration_seconds", "Aprobada (200)"],
    ["CP-03", "POST /tasks", "Creación de tarea con título válido", "201, tarea con id 1 y done:false", "Aprobada (200)"],
    ["CP-04", "POST /tasks", "Creación de tarea sin título (vacío)", "400 y mensaje de error", "Aprobada (200)"],
    ["CP-05", "GET /tasks", "Listado con una tarea creada", "200 y arreglo con 1 elemento", "Aprobada (200)"],
    ["CP-06", "PUT /tasks/:id/done", "Completar tarea existente", "200 y done:true", "Aprobada (200)"],
    ["CP-07", "PUT /tasks/:id/done", "Completar tarea con ID inexistente", "404 y Tarea no encontrada", "Aprobada (200)"],
    ["CP-08", "DELETE /tasks/:id", "Eliminar tarea existente", "204 y lista vacía en siguiente GET", "Aprobada (200)"],
    ["CP-09", "DELETE /tasks/:id", "Eliminar tarea con ID inexistente", "404 y Tarea no encontrada", "Aprobada (200)"],
    ["CP-10", "GET /reporte", "Conteo funcional (2 tareas, 1 hecha)", "200, total:2, hechas:1, pendientes:1", "Aprobada (200)"],
    ["CP-11", "GET /reporte", "Prueba de regresión de rendimiento", "Tiempo de respuesta menor a 50 ms", "Aprobada (200)"]
]
tbl_matriz = doc.add_table(rows=len(matriz_data) + 1, cols=5)
style_table(tbl_matriz, matriz_widths, matriz_headers, matriz_data, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER})

add_heading_2("3.3 Bitácora de Seguimiento de Ejecuciones de CI")
add_p("Registro cronológico y analítico de las ejecuciones representativas de integración continua:")

bit_headers = ["N.º", "Fecha", "Rama / Commit", "Evento", "Tot.", "Pas.", "Fal.", "Cob.", "Dur.", "Res.", "Causa y Acción Tomada"]
bit_widths = [0.4, 0.8, 1.1, 0.8, 0.4, 0.4, 0.4, 0.5, 0.5, 0.6, 1.6]
bit_data = [
    ["1", "19/11/2026", "main / 84ff002", "push", "10", "10", "0", "100%", "1.4s", "Verde", "Línea base del proyecto. 10/10 pruebas unitarias aprobadas."],
    ["2", "19/11/2026", "prueba/fallo-controlado / 2e6ea93", "pull_req.", "11", "10", "1", "100%", "1.4s", "Rojo", "Falla controlada CP-11: 107.45 ms > 50 ms. Causa: ciclo sincrónico de 50M en calcularReporte."],
    ["3", "19/11/2026", "prueba/fallo-controlado / c7724de", "pull_req.", "11", "11", "0", "100%", "1.0s", "Verde", "Ciclo eliminado de calcularReporte. CP-11 pasa en 3 ms. Flujo de CI validado exitosamente."]
]
tbl_bit = doc.add_table(rows=len(bit_data) + 1, cols=11)
style_table(tbl_bit, bit_widths, bit_headers, bit_data, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER, 5: WD_ALIGN_PARAGRAPH.CENTER, 6: WD_ALIGN_PARAGRAPH.CENTER, 7: WD_ALIGN_PARAGRAPH.CENTER, 8: WD_ALIGN_PARAGRAPH.CENTER, 9: WD_ALIGN_PARAGRAPH.CENTER})

# =========================================================================
# 5. PARTE 3: MONITOREO CON PROMETHEUS Y GRAFANA
# =========================================================================
add_heading_1("4. Parte 3: Monitoreo con Prometheus y Grafana")
add_p(
    "La pila de observabilidad se configuró mediante Docker Compose integrando Prometheus (puerto 9090) con intervalo de "
    "scrapeo de 5 segundos y Grafana (puerto 3001) con aprovisionamiento automático del origen de datos."
)

add_heading_2("4.1 Objetivos de Rendimiento (Establecidos Antes de Medir)")
add_p("Para emitir juicios técnicos sobre el desempeño, se definieron los siguientes umbrales numéricos de referencia:")

obj_headers = ["Indicador de Rendimiento", "Objetivo / Umbral Límite", "Instrumento de Medición"]
obj_widths = [2.4, 2.2, 2.3]
obj_data = [
    ["Latencia p95 global", "Menor a 500 ms (< 500 ms)", "k6 (resumen de ejecución) y panel Grafana"],
    ["Tasa de errores HTTP", "Menor al 1 % (< 1.0 %)", "k6 (http_req_failed) y panel Grafana 5xx"],
    ["Retardo del bucle de eventos (p99)", "Menor a 100 ms (< 100 ms)", "Panel Grafana nodejs_eventloop_lag_p99_seconds"]
]
tbl_obj = doc.add_table(rows=len(obj_data) + 1, cols=3)
style_table(tbl_obj, obj_widths, obj_headers, obj_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER})

add_heading_2("4.2 Especificación de Paneles del Tablero de Grafana")
graf_headers = ["Panel del Tablero", "Consulta PromQL Exacta", "Unidad", "Utilidad Diagnóstica"]
graf_widths = [1.5, 2.8, 0.9, 1.7]
graf_data = [
    ["Peticiones por segundo", "sum by (route) (rate(http_request_duration_seconds_count[1m]))", "req/s", "Carga recibida por cada endpoint"],
    ["Latencia p95 por ruta", "histogram_quantile(0.95, sum by (le, route) (rate(http_request_duration_seconds_bucket[1m])))", "segundos", "Tiempo que supera el 5% de peticiones lentas"],
    ["Errores 5xx por segundo", "sum(rate(http_request_duration_seconds_count{status_code=~\"5..\"}[1m])) or vector(0)", "req/s", "Detección de caídas o fallas de servidor"],
    ["Uso de CPU del proceso", "rate(process_cpu_seconds_total[1m])", "núcleos", "Nivel de saturación del procesador (1 = 100%)"],
    ["Retardo bucle eventos p99", "nodejs_eventloop_lag_p99_seconds", "segundos", "Retraso de Node.js para atender peticiones"],
    ["Memoria residente", "process_resident_memory_bytes", "bytes", "Consumo de RAM del proceso Node.js"]
]
tbl_graf = doc.add_table(rows=len(graf_data) + 1, cols=4)
style_table(tbl_graf, graf_widths, graf_headers, graf_data)

add_heading_2("4.3 Evidencia 4: Prometheus Targets en UP y Tablero de Grafana Activo")
add_image_box(
    "prometheus-targets-antes.png",
    "Interfaz de Prometheus (http://localhost:9090/targets) con objetivo gestor-tareas en estado UP (1/1 up)."
)

add_image_box(
    "grafana-antes.png",
    "Tablero de Grafana 'Gestor de tareas' con los 6 paneles instrumentados y recibiendo telemetría en tiempo real."
)

# =========================================================================
# 6. PARTE 4: EVALUACIÓN DE RENDIMIENTO CON K6 (MEDICIÓN "ANTES")
# =========================================================================
add_heading_1("5. Parte 4: Evaluación de Rendimiento con k6 (Medición 'Antes')")
add_p(
    "Se diseñó una prueba de carga en k6/carga.js simulando un flujo transaccional completo por usuario virtual (VU): "
    "crear tarea con POST /tasks, listar tareas con GET /tasks y solicitar resumen con GET /reporte, mediado por 1 segundo de pausa."
)

add_callout(
    "Durante la prueba inicial con 20 usuarios virtuales, la latencia p95 se mantuvo en 75.92 ms, pero el bucle de eventos "
    "alcanzó un pico de 116.7 ms (superando el objetivo de 100 ms). Siguiendo la instrucción metodológica del ejercicio, "
    "se elevó la carga en el tramo principal de 20 a 40 usuarios virtuales para revelar nítidamente el comportamiento del sistema.",
    title="AJUSTE METODOLÓGICO DE CARGA (40 VUs)"
)

add_heading_2("5.1 Evidencia 5: Resultados de k6 'Antes' y Tablero Saturado")
add_image_box(
    "captura-terminal-k6-antes.png",
    "Salida terminal de k6 cruzando los umbrales de latencia: p95 global 776 ms, /reporte 506 ms y /tasks 648 ms."
)

add_image_box(
    "grafana-antes20vu.png",
    "Tablero de Grafana durante la saturación: retardo del bucle de eventos superior a 1.18 segundos y CPU al 100%."
)

add_heading_2("5.2 Tabla de Medición 'Antes'")
antes_headers = ["Indicador de Rendimiento", "Objetivo / Umbral", "Valor Medido (Antes)", "Fuente", "¿Cumple?"]
antes_widths = [2.2, 1.4, 1.3, 1.1, 0.9]
antes_data = [
    ["Latencia p95 global", "< 500 ms", "776.01 ms", "k6", "No"],
    ["Latencia p95 de /reporte", "< 500 ms", "506.27 ms", "k6 y Grafana", "No"],
    ["Latencia p95 de /tasks (listar)", "< 500 ms", "648.17 ms", "k6 y Grafana", "No"],
    ["Tasa de errores HTTP", "< 1 %", "0.00 %", "k6", "Sí"],
    ["Retardo del bucle de eventos p99 (pico)", "< 100 ms", "1188 ms (1.19 s)", "Grafana", "No"],
    ["Uso de CPU del proceso (pico)", "Ref. (1 = saturado)", "1.03 núcleos", "Grafana", "Saturada"],
    ["Peticiones por segundo (pico)", "Referencia", "50.8 req/s", "Grafana", "Referencia"]
]
tbl_antes = doc.add_table(rows=len(antes_data) + 1, cols=5)
style_table(tbl_antes, antes_widths, antes_headers, antes_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER})

add_heading_2("5.3 Diagnóstico Guiado con Métricas")
add_p("1. ¿Qué ruta tiene la latencia p95 más alta? ¿Alguna otra ruta se ve afectada aunque no debería ser lenta?", bold_prefix="Pregunta 1: ")
add_p("En la prueba con 40 VUs, /tasks (listar) registró 648.17 ms y /reporte 506.27 ms. Es un hallazgo crítico que /tasks, siendo una consulta trivial en memoria, resulte tan degradada. Con 20 VUs, /tasks tardaba apenas 2.47 ms mientras /reporte ya consumía 98.58 ms.")

add_p("2. ¿La CPU del proceso se acerca a 1 núcleo durante la carga?", bold_prefix="Pregunta 2: ")
add_p("Sí. El panel de CPU en Grafana registró un pico de 1.03 núcleos, lo cual representa saturación absoluta del hilo principal de ejecución asignado al proceso.")

add_p("3. ¿Qué pasa con el retardo del bucle de eventos?", bold_prefix="Pregunta 3: ")
add_p("El retardo p99 escaló drásticamente de 116 ms a 1188 ms (casi 1.2 segundos), lo cual representa casi 12 veces el umbral máximo tolerado (100 ms). Dado que Node.js opera en un único hilo de ejecución para la pila de eventos, cuando una función bloquea la CPU sincrónicamente, todas las peticiones restantes quedan encoladas en espera.")

add_p("4. Formulación de la Hipótesis Previa a la Modificación:", bold_prefix="Pregunta 4 (Hipótesis): ")
add_callout(
    "«La ruta /reporte ocupa la CPU durante ≈45 ms por petición; por eso la latencia de /tasks sube cuando hay 40 usuarios.»",
    title="HIPÓTESIS CONFIRMADA POR MÉTRICAS"
)

add_p("5. Causa Raíz en el Código Fuente:", bold_prefix="Pregunta 5 (Código): ")
add_p("Al inspeccionar src/app.js en la función calcularReporte(), se descubrió un ciclo de 50 millones de iteraciones (for let i=0; i<50000000; i++) que acumula operaciones aritméticas redundantes. Esta computación es estrictamente sincrónica y bloqueante.")

# =========================================================================
# 7. PARTE 5: PLAN DE MEJORA Y EVALUACIÓN "DESPUÉS"
# =========================================================================
add_heading_1("6. Parte 5: Plan de Mejora Ligado a Resultados y Medición 'Después'")
add_p(
    "El plan de mejora relaciona de manera directa los hallazgos medidos con acciones concretas y metas numéricas verificables:"
)

plan_headers = ["ID", "Hallazgo y Evidencia (Antes)", "Causa Raíz", "Acción de Mejora", "Meta Medible", "Resultado (Después)", "Estado"]
plan_widths = [0.5, 1.3, 1.2, 1.2, 1.1, 1.0, 0.6]
plan_data = [
    [
        "M-01",
        "p95 /reporte 506 ms y /tasks 648 ms; retardo bucle p99 1188 ms (k6, 40 VUs)",
        "Ciclo sincrónico de 50M iteraciones en calcularReporte() que bloquea el hilo único",
        "Eliminar el ciclo heredado; optimizar la función para contar tareas directamente",
        "p95 /reporte < 500 ms y retardo bucle p99 < 100 ms con 40 VUs en k6",
        "p95 /reporte: 4.20 ms; retardo bucle: 17.8 ms",
        "Cumplida"
    ],
    [
        "M-02",
        "CP-10 pasaba en verde a pesar de que /reporte demoraba >100 ms en responder",
        "Ausencia de pruebas de regresión de tiempo de respuesta en la canalización de CI",
        "Incorporar prueba CP-11 con límite estricto de 50 ms ejecutada en cada pull request",
        "CP-11 debe fallar con código heredado (>50 ms) y aprobar con código optimizado",
        "Falla en ejecución 2 (107.45 ms); aprueba en ejecución 3 (3 ms)",
        "Cumplida"
    ]
]
tbl_plan = doc.add_table(rows=len(plan_data) + 1, cols=7)
style_table(tbl_plan, plan_widths, plan_headers, plan_data, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER, 6: WD_ALIGN_PARAGRAPH.CENTER})

add_heading_2("6.1 Implementación de la Mejora (TDD y Optimización)")
add_p(
    "Siguiendo las mejores prácticas de ingeniería de software, se escribió primero la prueba de regresión de rendimiento "
    "CP-11 en tests/tasks.test.js. La prueba falló en la rama mejora/reporte-rapido demostrando la existencia del defecto (107 ms). "
    "Posteriormente se refactorizó calcularReporte() en src/app.js:"
)

add_p(
    "// Versión 2 del reporte: solo cuenta las tareas, sin el ciclo heredado.\n"
    "function calcularReporte() {\n"
    "  const total = tareas.length;\n"
    "  const hechas = tareas.filter((t) => t.done).length;\n"
    "  return { total, hechas, pendientes: total - hechas };\n"
    "}",
    bold_prefix="Código optimizado: ",
    italic=True
)

add_heading_2("6.2 Evidencia 6: Medición 'Después' y Tablero Optimizado")
add_p(
    "Se reconstruyó la imagen de la API y se repitió la prueba con k6 bajo exactamente las mismas condiciones "
    "(40 usuarios virtuales, 1 minuto de duración, API reiniciada):"
)

add_image_box(
    "captura-terminal-k6-despues.png",
    "Salida terminal de k6 'Después': todos los umbrales cumplidos, latencia global de 5.59 ms y cero errores."
)

add_image_box(
    "grafana-despues.png",
    "Tablero de Grafana 'Después': CPU reducida a 0.14 núcleos y retardo del bucle de eventos estabilizado en 17.8 ms."
)

add_heading_2("6.3 Tabla Comparativa 'Antes' vs 'Después'")
comp_headers = ["Indicador de Rendimiento", "Objetivo / Umbral", "Antes", "Después", "Mejora Obtenida", "¿Cumple Ahora?"]
comp_widths = [2.2, 1.3, 1.1, 1.1, 1.1, 0.9]
comp_data = [
    ["Latencia p95 global", "< 500 ms", "776.01 ms", "5.59 ms", "99.3 %", "Sí"],
    ["Latencia p95 de /reporte", "< 500 ms", "506.27 ms", "4.20 ms", "99.2 %", "Sí"],
    ["Latencia p95 de /tasks (listar)", "< 500 ms", "648.17 ms", "6.09 ms", "99.1 %", "Sí"],
    ["Tasa de errores HTTP", "< 1 %", "0.00 %", "0.00 %", "-", "Sí"],
    ["Retardo del bucle de eventos p99", "< 100 ms", "1188 ms", "17.8 ms", "98.5 %", "Sí"],
    ["Uso de CPU del proceso", "Referencia", "1.03 núcleos", "0.14 núcleos", "86.4 %", "Referencia"],
    ["Rendimiento transaccional", "Referencia", "35.4 req/s", "56.1 req/s", "+58.5 %", "Referencia"]
]
tbl_comp = doc.add_table(rows=len(comp_data) + 1, cols=6)
style_table(tbl_comp, comp_widths, comp_headers, comp_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER, 5: WD_ALIGN_PARAGRAPH.CENTER})

add_heading_2("6.4 Paso 5.5: Registro del Nuevo Hallazgo (M-03)")
add_callout(
    "Hallazgo: Durante la prueba con 40 VUs en la versión optimizada, la memoria residente del proceso escaló de 71 MiB a 106 MiB "
    "y el volumen de datos recibido por k6 aumentó a 32 MB debido a la acumulación de 1130 tareas creadas en memoria.\n\n"
    "Causa Probable: La ruta GET /tasks devuelve la totalidad del arreglo de tareas sin paginación, incrementando el payload con cada ciclo.\n\n"
    "Acción Propuesta para Siguiente Ciclo: Implementar paginación mediante parámetros query limit y offset en GET /tasks.\n\n"
    "Meta Numérica: Mantener la memoria residente inferior a 100 MiB y la transferencia de red de /tasks menor a 100 KB por petición.",
    title="NUEVO HALLAZGO REGISTRADO (M-03)"
)

# =========================================================================
# 8. CONCLUSIONES
# =========================================================================
add_heading_1("7. Conclusiones y Lecciones Aprendidas")
add_p(
    "El desarrollo de esta práctica permitió experimentar y validar de forma integral el ciclo iterativo de medir, mejorar y volver a medir. "
    "A través de la integración de pruebas automatizadas, observabilidad continua y pruebas de carga, se obtuvieron aprendizajes "
    "fundamentales para la construcción de sistemas de software confiables y de alto rendimiento:"
)

add_p(
    "1. La necesidad de métricas frente a la intuición: En entornos asincrónicos monohilo como Node.js, los síntomas de lentitud en "
    "un endpoint no necesariamente indican que dicho endpoint sea el culpable. La ruta /tasks sufrió una degradación masiva de latencia "
    "(más de 640 ms) pese a ser trivial; solo el cruce simultáneo entre el uso de CPU y el retardo del bucle de eventos permitió "
    "identificar que el bloqueo provenía del cómputo sincrónico en /reporte."
)

add_p(
    "2. Automatización preventiva con CI: Una prueba que no evalúa el tiempo de respuesta permite que funciones ineficientes pasen "
    "inadvertidas a producción, tal como ocurrió inicialmente con CP-10. La inclusión de pruebas de regresión de rendimiento en "
    "GitHub Actions asegura que los acuerdos de nivel de servicio (SLA) se protejan automáticamente antes de cada merge."
)

add_p(
    "3. El ciclo continuo de mejora: Al resolver el cuello de botella de CPU en M-01, la aplicación duplicó su rendimiento transaccional, "
    "lo que a su vez expuso el siguiente punto de optimización en memoria y ancho de banda (M-03). La optimización del rendimiento "
    "no es un estado final, sino un proceso iterativo de descubrimiento sistemático respaldado por datos."
)

# Guardar documento
doc.save(OUTPUT_DOCX)
print(f"Documento Word guardado exitosamente en: {OUTPUT_DOCX}")
