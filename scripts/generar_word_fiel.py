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

# ----------------- Márgenes y Configuración Carta -----------------
for sec in doc.sections:
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11.0)
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.8)
    sec.right_margin = Inches(0.8)
    
    # Encabezado
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("Ejercicio práctico: Desarrollo e integración continua · Valeria Calvillo")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(120, 120, 120)
    
    # Pie de página
    fp = sec.footer.paragraphs[0]
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
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(19)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_STEEL
    return p

def add_h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_DARK
    return p

def add_p(text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3.5)
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

def add_bullet(text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2.5)
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
    r.font.color.rgb = COLOR_DARK
    return p

def add_code_block(code_text, filename=""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.9)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F6F8FA")
    set_cell_margins(cell, top=70, bottom=70, left=130, right=130)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="16" w:space="0" w:color="0969DA"/>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_after = Pt(0)
    cp.paragraph_format.line_spacing = 1.05
    if filename:
        rf = cp.add_run(f"// {filename}\n")
        rf.font.name = "Consolas"
        rf.font.size = Pt(8.5)
        rf.font.bold = True
        rf.font.color.rgb = COLOR_STEEL
        
    rc = cp.add_run(code_text.strip())
    rc.font.name = "Consolas"
    rc.font.size = Pt(8.5)
    rc.font.color.rgb = RGBColor(36, 41, 47)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

def add_callout(text, title="Importante"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.9)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=80, bottom=80, left=130, right=130)
    
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
    cp.paragraph_format.space_after = Pt(0)
    rt = cp.add_run(f"{title}: ")
    rt.font.name = "Calibri"
    rt.font.size = Pt(9.5)
    rt.font.bold = True
    rt.font.color.rgb = COLOR_NAVY
    
    rc = cp.add_run(text)
    rc.font.name = "Calibri"
    rc.font.size = Pt(9.5)
    rc.font.color.rgb = COLOR_DARK
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

def add_image_box(filename, caption):
    img_path = os.path.join(EVID, filename)
    if not os.path.exists(img_path):
        img_path = os.path.join(BASE, filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(5)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.6))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(6)
        run_cap = p_cap.add_run(f"Evidencia: {caption}")
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(8.5)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(90, 90, 90)

def style_table(tbl, col_widths, headers, data, align_cols=None):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    # Encabezado
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = Inches(col_widths[i])
        set_cell_background(hdr_cells[i], "1F4E79")
        set_cell_margins(hdr_cells[i], top=70, bottom=70, left=70, right=70)
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
            set_cell_margins(row_cells[c_idx], top=55, bottom=55, left=65, right=65)
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
                
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

# =========================================================================
# CONTENIDO VERBATIM CON FORMATO DEL DOCUMENTO ORIGINAL
# =========================================================================

# Encabezado / Título oficial
add_title("Ejercicio práctico: Desarrollo e integración continua")

p_meta = doc.add_paragraph()
p_meta.paragraph_format.space_after = Pt(8)
r_meta = p_meta.add_run("Alumna: Valeria Calvillo | Repositorio: https://github.com/valeria1732/unidad2-Domenzain | Fecha: 19 de noviembre de 2026")
r_meta.font.name = "Calibri"
r_meta.font.size = Pt(9.5)
r_meta.font.italic = True
r_meta.font.color.rgb = COLOR_STEEL

add_h1("Objetivo")
add_p("Realizar un ejercicio práctico que incluya seguimiento de pruebas, uso de CI con GitHub y herramientas de monitoreo de aplicaciones, y relacionar los planes de mejora con los resultados de la evaluación del rendimiento.")

add_h1("Resultados esperados")
add_bullet("Un repositorio en GitHub con pruebas automatizadas que se ejecutan en cada push y pull request.")
add_bullet("Una bitácora de seguimiento de pruebas con al menos una ejecución fallida analizada y corregida.")
add_bullet("Una API instrumentada y monitoreada con Prometheus y visualizada en Grafana.")
add_bullet("Una evaluación de rendimiento con k6, con métricas antes y después de una mejora.")
add_bullet("Un plan de mejora donde cada acción cita la métrica que la justifica y la meta que debe cumplir.")

add_h1("Cómo trabajar este documento")
add_p("Cada parte termina con una lista Verifica antes de continuar. Si algún punto no se cumple, no avances: la parte siguiente depende de él. Las evidencias marcadas como Evidencia se capturan en pantalla y se integran al reporte final.")

add_h1("Visión general del ejercicio")
add_p("El ejercicio es un ciclo: un cambio se prueba automáticamente en GitHub, se ejecuta y se mide en tu equipo, y lo que se mide alimenta el plan de mejora que origina el siguiente cambio.")
add_p("ciclo del ejercicio · 6 etapas, con regreso al primer paso\nLa fila superior ocurre en GitHub y la inferior en tu equipo; el plan de mejora (resaltado) es el punto donde se decide qué cambiar y vuelve al primer paso.", italic=True)

add_h1("Estructura final del repositorio")
add_code_block(
"""gestor-tareas-ci/ 
├── .github/workflows/ci.yml 
├── k6/carga.js 
├── monitoring/ 
│   ├── prometheus.yml 
│   └── grafana/provisioning/datasources/prometheus.yml 
├── scripts/resumen-pruebas.js 
├── src/ 
│   ├── app.js 
│   └── server.js 
├── tests/tasks.test.js 
├── .dockerignore 
├── .gitignore 
├── Dockerfile 
├── docker-compose.yml 
├── package.json 
└── package-lock.json"""
)

# =========================================================================
# PARTE 1
# =========================================================================
add_h1("Parte 1. Proyecto base, pruebas y contenedor")
add_p("Al terminar esta parte tendrás en GitHub una API con 10 pruebas automáticas y una imagen Docker que se construye y responde en el puerto 3000.")

add_h2("Paso 1.1 Crear el repositorio")
add_p("1. En GitHub crea un repositorio llamado gestor-tareas-ci (sin README ni .gitignore).")
add_p("2. Clónalo y crea la estructura de carpetas:")
add_code_block(
"""git clone https://github.com/valeria1732/unidad2-Domenzain.git gestor-tareas-ci
cd gestor-tareas-ci 
mkdir -p src tests scripts k6 monitoring/grafana/provisioning/datasources .github/workflows"""
)

add_h2("Paso 1.2 Crear la aplicación")
add_p("Crea los siguientes archivos con el contenido indicado. La API administra tareas en memoria, expone /health, /metrics (para Prometheus) y un endpoint /reporte que usarás más adelante en la evaluación de rendimiento.")

add_code_block(
"""{ 
  "name": "gestor-tareas", 
  "version": "1.0.0", 
  "description": "API de tareas para el ejercicio de CI y monitoreo", 
  "main": "src/server.js", 
  "scripts": { 
    "start": "node src/server.js", 
    "test": "jest --ci --coverage" 
  }, 
  "dependencies": { 
    "express": "^4.21.2", 
    "prom-client": "^15.1.3" 
  }, 
  "devDependencies": { 
    "jest": "^29.7.0", 
    "supertest": "^7.0.0" 
  }, 
  "jest": { 
    "testEnvironment": "node", 
    "coverageReporters": ["text", "json-summary", "lcov"], 
    "coverageThreshold": { 
      "global": { "lines": 80 } 
    } 
  } 
}""",
filename="package.json"
)

add_code_block(
"""const express = require('express'); 
const client = require('prom-client'); 
 
const app = express(); 
app.use(express.json()); 
 
// ---------- Métricas (Prometheus) ---------- 
client.collectDefaultMetrics(); 
 
const duracionHttp = new client.Histogram({ 
  name: 'http_request_duration_seconds', 
  help: 'Duración de las peticiones HTTP en segundos', 
  labelNames: ['method', 'route', 'status_code'], 
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5] 
}); 
 
app.use((req, res, next) => { 
  const fin = duracionHttp.startTimer(); 
  res.on('finish', () => { 
    const ruta = req.route ? req.baseUrl + req.route.path : 'sin_ruta'; 
    fin({ method: req.method, route: ruta, status_code: res.statusCode }); 
  }); 
  next(); 
}); 
 
// ---------- Datos en memoria ---------- 
let tareas = []; 
let siguienteId = 1; 
app.locals.reiniciar = () => { 
  tareas = []; 
  siguienteId = 1; 
}; 
 
// ---------- Rutas ---------- 
app.get('/health', (req, res) => res.json({ status: 'ok' })); 
 
app.get('/tasks', (req, res) => res.json(tareas)); 
 
app.post('/tasks', (req, res) => { 
  const { title } = req.body || {}; 
  if (typeof title !== 'string' || !title.trim()) { 
    return res.status(400).json({ error: 'title es obligatorio' }); 
  } 
  const tarea = { id: siguienteId++, title: title.trim(), done: false }; 
  tareas.push(tarea); 
  res.status(201).json(tarea); 
}); 
 
app.put('/tasks/:id/done', (req, res) => { 
  const tarea = tareas.find((t) => t.id === Number(req.params.id)); 
  if (!tarea) return res.status(404).json({ error: 'Tarea no encontrada' }); 
  tarea.done = true; 
  res.json(tarea); 
}); 
 
app.delete('/tasks/:id', (req, res) => { 
  const i = tareas.findIndex((t) => t.id === Number(req.params.id)); 
  if (i === -1) return res.status(404).json({ error: 'Tarea no encontrada' }); 
  tareas.splice(i, 1); 
  res.status(204).end(); 
}); 
 
// Versión 1 del reporte (código heredado). 
function calcularReporte() { 
  // Cálculo "de validación" heredado que recorre un ciclo muy largo. 
  let acumulado = 0; 
  for (let i = 0; i < 50000000; i++) { 
    acumulado += i % 7; 
  } 
  const total = tareas.length; 
  const hechas = tareas.filter((t) => t.done).length; 
  return { total, hechas, pendientes: total - hechas, valido: acumulado >= 0 }; 
} 
 
app.get('/reporte', (req, res) => res.json(calcularReporte())); 
 
app.get('/metrics', async (req, res) => { 
  res.set('Content-Type', client.register.contentType); 
  res.end(await client.register.metrics()); 
}); 
 
module.exports = app;""",
filename="src/app.js"
)

add_code_block(
"""const app = require('./app'); 
 
const PUERTO = process.env.PORT || 3000; 
app.listen(PUERTO, () => console.log(`API escuchando en el puerto ${PUERTO}`));""",
filename="src/server.js"
)

add_callout(
    "Importante: no modifiques todavía la función calcularReporte. Es código heredado y su comportamiento "
    "se analizará con métricas en las partes 3 a 5; el objetivo es que el problema aparezca en los datos, no por leer el código."
)

add_h2("Paso 1.3 Crear las pruebas automáticas")
add_code_block(
"""const request = require('supertest'); 
const app = require('../src/app'); 
 
beforeEach(() => app.locals.reiniciar()); 
 
describe('Salud y métricas', () => { 
  test('GET /health responde ok', async () => { 
    const res = await request(app).get('/health'); 
    expect(res.status).toBe(200); 
    expect(res.body).toEqual({ status: 'ok' }); 
  }); 
 
  test('GET /metrics expone métricas de Prometheus', async () => { 
    await request(app).get('/health'); 
    const res = await request(app).get('/metrics'); 
    expect(res.status).toBe(200); 
    expect(res.text).toContain('http_request_duration_seconds'); 
  }); 
}); 
 
describe('Tareas', () => { 
  test('POST /tasks crea una tarea', async () => { 
    const res = await request(app).post('/tasks').send({ title: 'Estudiar CI' }); 
    expect(res.status).toBe(201); 
    expect(res.body).toMatchObject({ id: 1, title: 'Estudiar CI', done: false }); 
  }); 
 
  test('POST /tasks sin título devuelve 400', async () => { 
    const res = await request(app).post('/tasks').send({}); 
    expect(res.status).toBe(400); 
  }); 
 
  test('GET /tasks lista las tareas creadas', async () => { 
    await request(app).post('/tasks').send({ title: 'A' }); 
    const res = await request(app).get('/tasks'); 
    expect(res.body).toHaveLength(1); 
  }); 
 
  test('PUT /tasks/:id/done marca la tarea como hecha', async () => { 
    await request(app).post('/tasks').send({ title: 'A' }); 
    const res = await request(app).put('/tasks/1/done'); 
    expect(res.status).toBe(200); 
    expect(res.body.done).toBe(true); 
  }); 
 
  test('PUT /tasks/:id/done con id inexistente devuelve 404', async () => { 
    const res = await request(app).put('/tasks/99/done'); 
    expect(res.status).toBe(404); 
  }); 
 
  test('DELETE /tasks/:id elimina la tarea', async () => { 
    await request(app).post('/tasks').send({ title: 'A' }); 
    const res = await request(app).delete('/tasks/1'); 
    expect(res.status).toBe(204); 
    const lista = await request(app).get('/tasks'); 
    expect(lista.body).toHaveLength(0); 
  }); 
 
  test('DELETE /tasks/:id con id inexistente devuelve 404', async () => { 
    const res = await request(app).delete('/tasks/99'); 
    expect(res.status).toBe(404); 
  }); 
}); 
 
describe('Reporte', () => { 
  test('GET /reporte cuenta tareas totales, hechas y pendientes', async () => { 
    await request(app).post('/tasks').send({ title: 'A' }); 
    await request(app).post('/tasks').send({ title: 'B' }); 
    await request(app).put('/tasks/1/done'); 
    const res = await request(app).get('/reporte'); 
    expect(res.status).toBe(200); 
    expect(res.body).toMatchObject({ total: 2, hechas: 1, pendientes: 1 }); 
  }); 
});""",
filename="tests/tasks.test.js"
)

add_code_block(
"""node_modules/ 
coverage/ 
test-results.json""",
filename=".gitignore"
)

add_h2("Paso 1.4 Instalar dependencias y ejecutar las pruebas con Docker")
add_p("No necesitas Node en tu equipo: se usa un contenedor temporal que monta la carpeta del proyecto.")
add_code_block(
"""docker run --rm -v "$(pwd)":/app -w /app node:22-alpine npm install 
docker run --rm -v "$(pwd)":/app -w /app node:22-alpine npm test"""
)
add_p("Resultado esperado: Tests: 10 passed y una tabla de cobertura con líneas por encima de 80 %.")

add_h2("Paso 1.5 Empaquetar en una imagen Docker")
add_code_block(
"""FROM node:22-alpine 
WORKDIR /app 
COPY package*.json ./ 
RUN npm ci --omit=dev 
COPY src ./src 
ENV NODE_ENV=production 
EXPOSE 3000 
USER node 
CMD ["node", "src/server.js"]""",
filename="Dockerfile"
)

add_code_block(
"""node_modules 
coverage 
test-results.json 
.git""",
filename=".dockerignore"
)

add_p("Construye la imagen, ejecuta el contenedor y prueba los endpoints:")
add_code_block(
"""docker build -t gestor-tareas:local . 
docker run --rm -d --name api -p 3000:3000 gestor-tareas:local 
curl http://localhost:3000/health 
curl -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{"title":"Mi primera tarea"}' 
curl http://localhost:3000/tasks 
curl http://localhost:3000/metrics | head -n 20 
docker stop api"""
)

add_h2("Paso 1.6 Primer commit")
add_code_block(
"""git add . 
git commit -m "feat: API de tareas con pruebas y Dockerfile" 
git branch -M main 
git push -u origin main"""
)

add_h3("Verifica antes de continuar")
add_bullet("npm test en contenedor muestra 10 pruebas aprobadas y cobertura de líneas ≥ 80 %.")
add_bullet("La imagen gestor-tareas:local se construye sin errores.")
add_bullet("/health responde {\"status\":\"ok\"} y /metrics incluye http_request_duration_seconds.")
add_bullet("package-lock.json está en el repositorio de GitHub.")

add_callout(
    "Evidencia 1: captura de la salida de las pruebas con la cobertura y de la respuesta de /metrics.",
    title="Evidencia 1"
)
add_image_box("captura-terminal-test-base.png", "Salida de npm test con 10/10 pruebas aprobadas y 100% de cobertura de líneas.")
add_image_box("captura-terminal-endpoints.png", "Contenedores activos con docker compose ps y validación de endpoints (/health, /tasks, /metrics).")
add_image_box("push.png", "Salida del comando git push -u origin main confirmando la publicación en GitHub.")

# =========================================================================
# PARTE 2
# =========================================================================
add_h1("Parte 2. Integración continua con GitHub Actions y seguimiento de pruebas")
add_p("Al terminar esta parte, cada push a main y cada pull request ejecutará las pruebas, publicará un resumen de resultados y construirá y probará la imagen Docker; además tendrás una bitácora con una falla analizada.")

add_h2("Paso 2.1 Script de resumen de pruebas")
add_code_block(
"""// Genera un resumen en Markdown a partir de los resultados de Jest. 
const fs = require('fs'); 
 
function leer(ruta) { 
  try { 
    return JSON.parse(fs.readFileSync(ruta, 'utf8')); 
  } catch { 
    return null; 
  } 
} 
 
const r = leer('test-results.json'); 
if (!r) { 
  console.log('## Resumen de pruebas\\n\\nNo se generó test-results.json.'); 
  process.exit(0); 
} 
const c = leer('coverage/coverage-summary.json'); 
const cobertura = c ? `${c.total.lines.pct}%` : 'n/d'; 
 
console.log('## Resumen de pruebas\\n'); 
console.log('| Total | Pasaron | Fallaron | Cobertura de líneas |'); 
console.log('|---|---|---|---|'); 
console.log(`| ${r.numTotalTests} | ${r.numPassedTests} | ${r.numFailedTests} | ${cobertura} |`); 
 
const fallidas = r.testResults 
  .flatMap((f) => f.assertionResults) 
  .filter((t) => t.status === 'failed'); 
if (fallidas.length > 0) { 
  console.log('\\n### Pruebas fallidas\\n'); 
  fallidas.forEach((t) => console.log(`- ${t.fullName}`)); 
}""",
filename="scripts/resumen-pruebas.js"
)

add_h2("Paso 2.2 Flujo de trabajo de CI")
add_code_block(
"""name: CI 
 
on: 
  push: 
    branches: [main] 
  pull_request: 
    branches: [main] 
 
jobs: 
  pruebas: 
    runs-on: ubuntu-latest 
    steps: 
      - uses: actions/checkout@v4 
 
      - uses: actions/setup-node@v4 
        with: 
          node-version: 22 
          cache: npm 
 
      - name: Instalar dependencias 
        run: npm ci 
 
      - name: Ejecutar pruebas con cobertura 
        run: npm test -- --json --outputFile=test-results.json 
 
      - name: Resumen en el panel de la ejecución 
        if: always() 
        run: node scripts/resumen-pruebas.js >> "$GITHUB_STEP_SUMMARY" 
 
      - name: Guardar reportes de pruebas 
        if: always() 
        uses: actions/upload-artifact@v4 
        with: 
          name: reportes-pruebas 
          path: | 
            test-results.json 
            coverage/ 
 
  imagen-docker: 
    needs: pruebas 
    runs-on: ubuntu-latest 
    steps: 
      - uses: actions/checkout@v4 
 
      - name: Construir imagen 
        run: docker build -t gestor-tareas:${{ github.sha }} . 
 
      - name: Prueba de humo del contenedor 
        run: | 
          docker run -d --name api -p 3000:3000 gestor-tareas:${{ github.sha }} 
          for i in $(seq 1 15); do curl -sf http://localhost:3000/health && break || sleep 1; done 
          curl -sf http://localhost:3000/health 
          curl -sf http://localhost:3000/metrics | head -n 5 
 
      - name: Mostrar bitácora del contenedor si algo falló 
        if: failure() 
        run: docker logs api""",
filename=".github/workflows/ci.yml"
)

add_h2("Paso 2.3 Primera ejecución")
add_code_block(
"""git add . 
git commit -m "ci: flujo de trabajo con pruebas, resumen y construcción de imagen" 
git push"""
)
add_p("1. En GitHub abre la pestaña Actions y entra a la ejecución más reciente.\n2. Revisa que los dos trabajos (pruebas e imagen-docker) tengan palomita verde.\n3. En la página de la ejecución baja hasta Summary: ahí aparece la tabla de resumen y, más abajo, el artefacto reportes-pruebas.")

add_callout(
    "Evidencia 2: captura de la ejecución en verde con la tabla de resumen visible.",
    title="Evidencia 2"
)
add_image_box("captura-terminal-ci-verde.png", "Ejecución de CI completada con éxito en GitHub Actions (ambos trabajos aprobados con resumen).")

add_h2("Paso 2.4 Provocar una falla controlada y darle seguimiento")
add_p("Un flujo de CI se entiende mejor cuando se ve fallar. Harás una falla a propósito en una rama y la pasarás por un pull request.")
add_code_block(
"""git checkout -b prueba/fallo-controlado 
# En tests/tasks.test.js se cambia expect(res.status).toBe(200) por 201 en /health
git commit -am "test: falla controlada para practicar seguimiento" 
git push -u origin prueba/fallo-controlado"""
)
add_p("Esperar a que la ejecución termine en rojo. Entrar a Details, localizar la prueba que falló. Verificar que el trabajo imagen-docker fue omitido. Corregir volviendo a toBe(200), hacer commit y push para ponerlo en verde.")

add_callout(
    "Evidencia 3: captura de la ejecución en rojo con el detalle de la prueba fallida y otra de la ejecución corregida en verde.",
    title="Evidencia 3"
)
add_image_box("captura-terminal-falla-controlada.png", "Detalle de la prueba fallida en rojo por discrepancia de status code 201 vs 200 y restauración a verde.")

add_h2("Paso 2.5 Proteger la rama principal (recomendado)")
add_p("En Settings → Rules → Rulesets crear una regla para main que exija pull request y que el chequeo de pruebas pase antes de hacer merge.")

add_h2("Paso 2.6 Bitácora de seguimiento de pruebas")
add_p("Matriz de casos de prueba (ya relacionada con las pruebas del proyecto; agrega la columna de resultado según CI):")

matriz_headers = ["ID", "Endpoint", "Escenario", "Resultado esperado", "Resultado en CI"]
matriz_widths = [0.8, 1.4, 1.8, 1.7, 1.2]
matriz_data = [
    ["CP-01", "GET /health", "Consulta de salud", "200 y {\"status\":\"ok\"}", "Aprobada (200)"],
    ["CP-02", "GET /metrics", "Consulta de métricas", "200 y contiene http_request_duration_seconds", "Aprobada (200)"],
    ["CP-03", "POST /tasks", "Título válido", "201 y tarea con id 1 y done falso", "Aprobada (200)"],
    ["CP-04", "POST /tasks", "Sin título", "400", "Aprobada (200)"],
    ["CP-05", "GET /tasks", "Con una tarea creada", "Lista de 1 elemento", "Aprobada (200)"],
    ["CP-06", "PUT /tasks/:id/done", "Tarea existente", "200 y done verdadero", "Aprobada (200)"],
    ["CP-07", "PUT /tasks/:id/done", "Id inexistente", "404", "Aprobada (200)"],
    ["CP-08", "DELETE /tasks/:id", "Tarea existente", "204 y lista vacía", "Aprobada (200)"],
    ["CP-09", "DELETE /tasks/:id", "Id inexistente", "404", "Aprobada (200)"],
    ["CP-10", "GET /reporte", "2 tareas, 1 hecha", "total 2, hechas 1, pendientes 1", "Aprobada (200)"]
]
tbl_m = doc.add_table(rows=len(matriz_data) + 1, cols=5)
style_table(tbl_m, matriz_widths, matriz_headers, matriz_data, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER})

add_p("Bitácora de ejecuciones de CI (mínimo 3 filas: primera ejecución verde, falla controlada y corrección):")
bit_headers = ["N.º", "Fecha", "Rama / commit", "Evento", "Total", "Pasaron", "Fallaron", "Cobertura", "Duración", "Resultado", "Causa y acción tomada"]
bit_widths = [0.4, 0.8, 1.1, 0.8, 0.4, 0.4, 0.4, 0.5, 0.5, 0.6, 1.6]
bit_data = [
    ["1", "19/11/2026", "main / 84ff002", "push", "10", "10", "0", "100 %", "1.4 s", "Verde", "Línea base del proyecto. 10/10 pruebas pasadas con 100% de cobertura."],
    ["2", "19/11/2026", "prueba/fallo-controlado / 2e6ea93", "pull_request", "11", "10", "1", "100 %", "1.4 s", "Rojo", "Falla controlada CP-11: 107 ms > 50 ms. Causa: ciclo de 50M en calcularReporte. Acción: optimizar cálculo."],
    ["3", "19/11/2026", "prueba/fallo-controlado / c7724de", "pull_request", "11", "11", "0", "100 %", "1.0 s", "Verde", "Ciclo eliminado de calcularReporte. CP-11 pasa en 3 ms. Flujo de CI completo y validado."]
]
tbl_b = doc.add_table(rows=len(bit_data) + 1, cols=11)
style_table(tbl_b, bit_widths, bit_headers, bit_data, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER, 5: WD_ALIGN_PARAGRAPH.CENTER, 6: WD_ALIGN_PARAGRAPH.CENTER, 7: WD_ALIGN_PARAGRAPH.CENTER, 8: WD_ALIGN_PARAGRAPH.CENTER, 9: WD_ALIGN_PARAGRAPH.CENTER})

add_h3("Verifica antes de continuar")
add_bullet("Existe al menos una ejecución verde y una roja en la pestaña Actions.")
add_bullet("La ejecución roja no construyó la imagen Docker (el trabajo imagen-docker aparece omitido).")
add_bullet("La bitácora tiene al menos 3 ejecuciones con datos reales y la causa de la falla explicada con tus palabras.")
add_bullet("main contiene el código corregido (la prueba de /health espera 200).")

# =========================================================================
# PARTE 3
# =========================================================================
add_h1("Parte 3. Monitoreo con Prometheus y Grafana")
add_p("Al terminar esta parte tendrás la API, Prometheus y Grafana corriendo juntos con Docker Compose, un tablero con seis paneles y objetivos de rendimiento escritos con números.")

add_h2("Paso 3.1 Archivos de configuración")
add_code_block(
"""services: 
  api: 
    build: . 
    ports: 
      - "3000:3000" 
 
  prometheus: 
    image: prom/prometheus:latest 
    ports: 
      - "9090:9090" 
    volumes: 
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro 
    depends_on: 
      - api 
 
  grafana: 
    image: grafana/grafana:latest 
    ports: 
      - "3001:3000" 
    environment: 
      GF_SECURITY_ADMIN_USER: admin 
      GF_SECURITY_ADMIN_PASSWORD: admin 
    volumes: 
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro 
      - grafana-data:/var/lib/grafana 
    depends_on: 
      - prometheus 
 
  k6: 
    image: grafana/k6:latest 
    profiles: ["carga"] 
    volumes: 
      - ./k6:/scripts:ro 
    environment: 
      BASE_URL: http://api:3000 
    command: run /scripts/carga.js 
    depends_on: 
      - api 
 
volumes: 
  grafana-data:""",
filename="docker-compose.yml"
)

add_code_block(
"""global: 
  scrape_interval: 5s 
 
scrape_configs: 
  - job_name: gestor-tareas 
    metrics_path: /metrics 
    static_configs: 
      - targets: ['api:3000']""",
filename="monitoring/prometheus.yml"
)

add_code_block(
"""apiVersion: 1 
datasources: 
  - name: Prometheus 
    type: prometheus 
    access: proxy 
    url: http://prometheus:9090 
    isDefault: true""",
filename="monitoring/grafana/provisioning/datasources/prometheus.yml"
)

add_h2("Paso 3.2 Levantar el entorno")
add_code_block(
"""docker compose up -d --build 
docker compose ps"""
)

add_h2("Paso 3.3 Confirmar que Prometheus recolecta métricas")
add_p("1. Abre http://localhost:9090/targets: el objetivo gestor-tareas debe estar en estado UP.\n2. En http://localhost:9090/graph ejecuta la consulta up; debe devolver el valor 1.\n3. Genera tráfico de prueba con curl y consulta http_request_duration_seconds_count.")

add_h2("Paso 3.4 Crear el tablero en Grafana")
add_p("Entra a http://localhost:3001 con admin/admin. Crea el tablero 'Gestor de tareas' con los 6 paneles:")

pan_headers = ["Panel", "Consulta (PromQL)", "Unidad", "Qué te dice"]
pan_widths = [1.5, 2.7, 0.9, 1.8]
pan_data = [
    ["Peticiones por segundo", "sum by (route) (rate(http_request_duration_seconds_count[1m]))", "req/s", "Cuánta carga recibe cada ruta"],
    ["Latencia p95 por ruta", "histogram_quantile(0.95, sum by (le, route) (rate(http_request_duration_seconds_bucket[1m])))", "segundos", "El tiempo que supera el 5 % de las peticiones más lentas"],
    ["Errores 5xx por segundo", "sum(rate(http_request_duration_seconds_count{status_code=~\"5..\"}[1m])) or vector(0)", "req/s", "Fallas del servidor"],
    ["Uso de CPU del proceso", "rate(process_cpu_seconds_total[1m])", "núcleos (1 = 100 %)", "Si la aplicación está saturando el procesador"],
    ["Retardo del bucle de eventos (p99)", "nodejs_eventloop_lag_p99_seconds", "segundos", "Cuánto se atrasa Node.js para atender trabajo pendiente"],
    ["Memoria residente", "process_resident_memory_bytes", "bytes", "Consumo de memoria del proceso"]
]
tbl_pan = doc.add_table(rows=len(pan_data) + 1, cols=4)
style_table(tbl_pan, pan_widths, pan_headers, pan_data)

add_h2("Paso 3.5 Definir los objetivos de rendimiento")
add_p("Para poder decir que algo “está lento” hace falta un número contra el cual comparar:")

obj_headers = ["Indicador", "Objetivo", "Dónde se mide"]
obj_widths = [2.4, 2.2, 2.3]
obj_data = [
    ["Latencia p95 global", "Menor a 500 ms", "k6 y panel de latencia p95"],
    ["Tasa de errores", "Menor a 1 %", "k6 y panel de errores 5xx"],
    ["Retardo del bucle de eventos (p99)", "Menor a 100 ms", "Panel de retardo del bucle de eventos"]
]
tbl_o = doc.add_table(rows=len(obj_data) + 1, cols=3)
style_table(tbl_o, obj_widths, obj_headers, obj_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER})

add_h3("Verifica antes de continuar")
add_bullet("docker compose ps muestra api, prometheus y grafana en ejecución.")
add_bullet("El objetivo gestor-tareas aparece en UP en Prometheus.")
add_bullet("El tablero de Grafana tiene los 6 paneles y los de peticiones y latencia muestran datos.")
add_bullet("Los objetivos de rendimiento están escritos en tu reporte.")

add_callout(
    "Evidencia 4: captura de http://localhost:9090/targets con el objetivo en UP y captura del tablero de Grafana con datos.",
    title="Evidencia 4"
)
add_image_box("prometheus-targets-antes.png", "Objetivo gestor-tareas en estado UP (1/1 up) en Prometheus Targets.")
add_image_box("grafana-antes.png", "Tablero de Grafana 'Gestor de tareas' con 6 paneles activos en tiempo real.")

# =========================================================================
# PARTE 4
# =========================================================================
add_h1("Parte 4. Evaluación de rendimiento con k6")
add_p("Al terminar esta parte tendrás una medición base (“antes”) de la API bajo carga, con datos de k6 y de Grafana, y una hipótesis sobre el cuello de botella respaldada por esas métricas.")

add_h2("Paso 4.1 Script de carga")
add_code_block(
"""import http from 'k6/http'; 
import { check, sleep } from 'k6'; 
 
export const options = { 
  stages: [ 
    { duration: '15s', target: 10 }, 
    { duration: '30s', target: 40 }, // Elevado a 40 VUs para evidenciar saturación
    { duration: '15s', target: 0 }, 
  ], 
  thresholds: { 
    http_req_failed: ['rate<0.01'], 
    http_req_duration: ['p(95)<500'], 
    'http_req_duration{name:listar}': ['p(95)<500'], 
    'http_req_duration{name:reporte}': ['p(95)<500'], 
  }, 
}; 
 
const BASE = __ENV.BASE_URL || 'http://localhost:3000'; 
 
export default function () { 
  const crear = http.post( 
    `${BASE}/tasks`, 
    JSON.stringify({ title: 'Tarea de carga' }), 
    { headers: { 'Content-Type': 'application/json' }, tags: { name: 'crear' } } 
  ); 
  check(crear, { 'crear devuelve 201': (r) => r.status === 201 }); 
 
  const lista = http.get(`${BASE}/tasks`, { tags: { name: 'listar' } }); 
  check(lista, { 'listar devuelve 200': (r) => r.status === 200 }); 
 
  const reporte = http.get(`${BASE}/reporte`, { tags: { name: 'reporte' } }); 
  check(reporte, { 'reporte devuelve 200': (r) => r.status === 200 }); 
 
  sleep(1); 
}""",
filename="k6/carga.js"
)

add_h2("Paso 4.2 Ejecutar la medición base")
add_code_block(
"""docker compose up -d --build 
docker compose restart api 
sleep 10 
docker compose run --rm k6"""
)

add_h2("Paso 4.3 Registrar la medición “antes”")
add_p("Toma los valores de k6 y, en Grafana, los picos observados durante la prueba:")

antes_headers = ["Indicador", "Objetivo", "Valor medido (antes)", "Fuente", "¿Cumple?"]
antes_widths = [2.2, 1.3, 1.3, 1.2, 0.9]
antes_data = [
    ["Latencia p95 global", "< 500 ms", "776.01 ms", "k6", "No"],
    ["Latencia p95 de /reporte", "< 500 ms", "506.27 ms", "k6 y Grafana", "No"],
    ["Latencia p95 de /tasks (listar)", "< 500 ms", "648.17 ms", "k6 y Grafana", "No"],
    ["Tasa de errores", "< 1 %", "0.00 %", "k6", "Sí"],
    ["Retardo del bucle de eventos p99 (pico)", "< 100 ms", "1188 ms", "Grafana", "No"],
    ["Uso de CPU del proceso (pico)", "Referencia: cercano a 1 núcleo indica saturación", "1.03 núcleos", "Grafana", "Saturada"],
    ["Peticiones por segundo (pico)", "Referencia", "50.8 req/s", "Grafana", "Referencia"]
]
tbl_a = doc.add_table(rows=len(antes_data) + 1, cols=5)
style_table(tbl_a, antes_widths, antes_headers, antes_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER})

add_h2("Paso 4.4 Diagnóstico guiado con las métricas")
add_p("Responde cada pregunta con evidencia (valores y capturas), no con suposiciones:")
add_p("1. ¿Qué ruta tiene la latencia p95 más alta? ¿Alguna otra ruta se ve afectada aunque no debería ser lenta?", bold_prefix="1. ")
add_p("Respuesta: En k6, /tasks (listar) registró 648.17 ms y /reporte 506.27 ms. La ruta /tasks resulta gravemente afectada pese a solo devolver un arreglo en memoria, debido a la saturación global del bucle de eventos.")

add_p("2. ¿La CPU del proceso se acerca a 1 núcleo durante la carga?", bold_prefix="2. ")
add_p("Respuesta: Sí, alcanzó 1.03 núcleos en Grafana (100% de ocupación del procesador).")

add_p("3. ¿Qué pasa con el retardo del bucle de eventos? Node.js atiende todas las peticiones en un solo hilo: si una ruta ocupa la CPU durante mucho tiempo, las demás esperan.", bold_prefix="3. ")
add_p("Respuesta: El retardo p99 escaló hasta 1188 ms (casi 1.2 segundos), lo cual excede por casi 12 veces el objetivo tolerado (100 ms).")

add_p("4. Con lo anterior, escribe una hipótesis:", bold_prefix="4. Hipótesis redactada: ")
add_callout(
    "«La ruta /reporte ocupa la CPU durante ≈45 ms por petición; por eso la latencia de /tasks sube cuando hay 40 usuarios.»",
    title="Hipótesis"
)

add_p("5. Solo ahora abre src/app.js, localiza el código de la ruta que identificaste y explica qué parte provoca el comportamiento.", bold_prefix="5. Explicación del código: ")
add_p("Respuesta: En src/app.js, la función calcularReporte() ejecuta un ciclo for síncrono de 50,000,000 de iteraciones (acumulado += i % 7). Al ser código puramente síncrono en Node.js, bloquea el hilo de ejecución e impide procesar cualquier otra solicitud.")

add_h3("Verifica antes de continuar")
add_bullet("Tienes la tabla “antes” completa con valores reales y la columna ¿Cumple? contestada.")
add_bullet("Identificaste una ruta como causa principal y la respaldas con al menos dos métricas distintas.")
add_bullet("Escribiste tu hipótesis antes de modificar cualquier código.")

add_callout(
    "Evidencia 5: captura del resumen de k6 con los umbrales y captura del tablero de Grafana durante la carga.",
    title="Evidencia 5"
)
add_image_box("captura-terminal-k6-antes.png", "Resumen terminal de k6 cruzando los umbrales p(95) de latencia bajo carga de 40 VUs.")
add_image_box("grafana-antes20vu.png", "Tablero de Grafana durante la saturación de CPU y retardo de event loop de 1.18 s.")

# =========================================================================
# PARTE 5
# =========================================================================
add_h1("Parte 5. Plan de mejora ligado a los resultados")
add_p("Al terminar esta parte tendrás un plan de mejora donde cada acción cita la métrica que la originó, una mejora aplicada mediante pull request con CI y una medición “después” que dice si la meta se cumplió.")

add_h2("Paso 5.1 Redactar el plan de mejora")
plan_headers = ["ID", "Hallazgo y evidencia (valor “antes”)", "Causa", "Acción de mejora", "Meta medible", "Resultado (después)", "Estado"]
plan_widths = [0.5, 1.3, 1.2, 1.2, 1.1, 1.0, 0.6]
plan_data = [
    [
        "M-01",
        "p95 /reporte 506 ms y /tasks 648 ms (k6, 40 VU); lag p99 1188 ms",
        "Ciclo de 50M iteraciones síncrono que bloquea el hilo; CPU en 1.03",
        "Eliminar el ciclo heredado; solo contar las tareas (versión 2)",
        "p95 /reporte < 500 ms y lag p99 < 100 ms",
        "p95: 4.2 ms; lag: 17.8 ms",
        "Cumplida"
    ],
    [
        "M-02",
        "CP-10 pasaba en verde con /reporte lento (> 100 ms)",
        "Falta de prueba automatizada de tiempo de respuesta",
        "Prueba CP-11 de regresión de rendimiento (< 50 ms)",
        "Falla con ciclo (> 50 ms) y pasa sin él (< 50 ms)",
        "107 ms → 3 ms",
        "Cumplida"
    ]
]
tbl_p = doc.add_table(rows=len(plan_data) + 1, cols=7)
style_table(tbl_p, plan_widths, plan_headers, plan_data, align_cols={0: WD_ALIGN_PARAGRAPH.CENTER, 6: WD_ALIGN_PARAGRAPH.CENTER})

add_h2("Paso 5.2 Proteger la mejora con una prueba antes de corregir")
add_p("Trabaja en una rama nueva y escribe primero la prueba que exige el comportamiento deseado:")
add_code_block(
"""git checkout main 
git pull 
git checkout -b mejora/reporte-rapido""",
filename="Terminal"
)
add_p("En tests/tasks.test.js, dentro del bloque describe('Reporte', ...), agrega esta prueba:")
add_code_block(
"""  test('GET /reporte responde en menos de 50 ms (regresión de rendimiento)', async () => { 
    const inicio = process.hrtime.bigint(); 
    const res = await request(app).get('/reporte'); 
    const ms = Number(process.hrtime.bigint() - inicio) / 1e6; 
    expect(res.status).toBe(200); 
    expect(ms).toBeLessThan(50); 
  });""",
filename="tests/tasks.test.js"
)
add_code_block(
"""git commit -am "test: prueba de regresión de rendimiento para /reporte" 
git push -u origin mejora/reporte-rapido"""
)

add_h2("Paso 5.3 Aplicar la mejora")
add_p("Usa tu diagnóstico de la Parte 4 para corregir calcularReporte en src/app.js. La acción esperada para M-01 es eliminar el trabajo innecesario de la función:")
add_code_block(
"""// Versión 2 del reporte: solo cuenta las tareas, sin el ciclo heredado. 
function calcularReporte() { 
  const total = tareas.length; 
  const hechas = tareas.filter((t) => t.done).length; 
  return { total, hechas, pendientes: total - hechas }; 
}""",
filename="src/app.js"
)
add_code_block(
"""git commit -am "perf: elimina el ciclo innecesario de calcularReporte" 
git push"""
)

add_h2("Paso 5.4 Medir “después” y comparar")
add_p("Repite la medición con las mismas condiciones que la Parte 4 (mismo script, mismos usuarios, API reiniciada):")
add_code_block(
"""docker compose up -d --build 
docker compose restart api 
sleep 10 
docker compose run --rm k6"""
)

add_p("Completa la comparación con los valores de la tabla “antes” de la Parte 4 y los nuevos de k6 y Grafana:")
comp_headers = ["Indicador", "Objetivo", "Antes", "Después", "Mejora (%)", "¿Cumple ahora?"]
comp_widths = [2.2, 1.3, 1.1, 1.1, 1.1, 0.9]
comp_data = [
    ["Latencia p95 global", "< 500 ms", "776.01 ms", "5.59 ms", "99.3 %", "Sí"],
    ["Latencia p95 de /reporte", "< 500 ms", "506.27 ms", "4.20 ms", "99.2 %", "Sí"],
    ["Latencia p95 de /tasks (listar)", "< 500 ms", "648.17 ms", "6.09 ms", "99.1 %", "Sí"],
    ["Tasa de errores", "< 1 %", "0.00 %", "0.00 %", "-", "Sí"],
    ["Retardo del bucle de eventos p99 (pico)", "< 100 ms", "1188 ms", "17.8 ms", "98.5 %", "Sí"],
    ["Uso de CPU del proceso (pico)", "Referencia", "1.03 núcleos", "0.14 núcleos", "86.4 %", "Referencia"]
]
tbl_c = doc.add_table(rows=len(comp_data) + 1, cols=6)
style_table(tbl_c, comp_widths, comp_headers, comp_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER, 5: WD_ALIGN_PARAGRAPH.CENTER})

add_h2("Paso 5.5 Abrir el siguiente ciclo")
add_p("Observa el tablero de Grafana con la API ya mejorada y detecta un hallazgo nuevo. Regístralo como M-03 con su evidencia, su causa probable y una acción propuesta:")
add_callout(
    "[M-03 Registrado]: Consumo de memoria sube de 71 MiB a 106 MiB y la red transmite 32 MB debido a la acumulación "
    "de 1130 tareas en memoria sin paginación (GET /tasks devuelve todo el arreglo). Acción propuesta: paginar mediante "
    "parámetros limit y offset. Meta: memoria residente < 100 MiB y carga de red < 100 KB por petición.",
    title="Hallazgo M-03 (Siguiente Ciclo)"
)

add_h3("Verifica antes de terminar")
add_bullet("Cada fila del plan cita un valor medido y una meta con número.")
add_bullet("La ejecución roja de la prueba de regresión y la verde posterior aparecen en tu bitácora.")
add_bullet("La tabla antes/después está completa y mide lo mismo con las mismas condiciones.")
add_bullet("M-03 describe un hallazgo nuevo con evidencia de Grafana o k6.")

add_callout(
    "Evidencia 6: captura del resumen de k6 “después” y del tablero de Grafana con la mejora visible.",
    title="Evidencia 6"
)
add_image_box("captura-terminal-k6-despues.png", "Resumen terminal de k6 'Después' con 100% de umbrales aprobados y p95 global en 5.59 ms.")
add_image_box("grafana-despues.png", "Tablero de Grafana tras la optimización: CPU en 0.14 núcleos y retardo del bucle de eventos en 17.8 ms.")

# =========================================================================
# ENTREGABLES Y RÚBRICA
# =========================================================================
add_h1("Entregables y evaluación")
add_p("Se entregan dos productos: el repositorio de GitHub y un reporte en PDF con las evidencias y los análisis.")
add_h2("Qué se entrega")
add_bullet("1. Repositorio en GitHub con el historial de commits, el pull request de la falla controlada y el de la mejora, y las ejecuciones visibles en la pestaña Actions: https://github.com/valeria1732/unidad2-Domenzain")
add_bullet("2. Reporte en PDF con: portada; Evidencias 1 a 6; matriz de casos de prueba y bitácora de ejecuciones; objetivos de rendimiento; tablas “antes” y “después”; plan de mejora con M-01, M-02 y M-03; y una conclusión de máximo una cuartilla sobre lo aprendido del ciclo medir, mejorar y volver a medir.")
add_p("Al terminar, limpia el entorno local con docker compose down -v.")

add_h2("Rúbrica de evaluación")
rub_headers = ["Criterio", "Puntos", "Qué se revisa"]
rub_widths = [2.0, 0.8, 4.1]
rub_data = [
    ["Repositorio y pruebas automatizadas (Parte 1)", "1.0", "Proyecto completo, 10 pruebas aprobadas, cobertura de líneas ≥ 80 %, imagen Docker funcional"],
    ["Integración continua con GitHub Actions (Parte 2)", "2.0", "Flujo de trabajo operando en push y pull request, resumen de pruebas, artefactos y construcción de imagen con prueba de humo"],
    ["Seguimiento de pruebas (Parte 2)", "1.5", "Matriz de casos completa y bitácora con al menos una falla analizada: causa, acción y evidencia"],
    ["Monitoreo de la aplicación (Parte 3)", "1.5", "Prometheus recolectando, tablero con 6 paneles con datos y objetivos de rendimiento escritos antes de medir"],
    ["Evaluación de rendimiento (Parte 4)", "1.5", "Medición “antes” completa, diagnóstico apoyado en al menos dos métricas e hipótesis previa a modificar el código"],
    ["Plan de mejora relacionado con los resultados (Parte 5)", "2.0", "Cada acción cita un hallazgo medido, una causa, una meta con número y su resultado “después” en las mismas condiciones; hallazgo nuevo M-03"],
    ["Presentación del reporte", "0.5", "Capturas legibles, evidencias identificadas y redacción propia"],
    ["Total", "10", "Evaluación integral de desarrollo, CI, observabilidad y mejora de rendimiento."]
]
tbl_r = doc.add_table(rows=len(rub_data) + 1, cols=3)
style_table(tbl_r, rub_widths, rub_headers, rub_data, align_cols={1: WD_ALIGN_PARAGRAPH.CENTER})

# =========================================================================
# CONCLUSIÓN FINAL
# =========================================================================
add_h1("Conclusión del Ciclo Medir, Mejorar y Volver a Medir")
add_p(
    "La realización de este ejercicio práctico demostró que la optimización del rendimiento en sistemas de software debe "
    "regirse por el método científico y no por la intuición. Al evaluar la API de tareas en una fase temprana con 20 usuarios "
    "virtuales, las métricas tradicionales de latencia promedio sugerían que el comportamiento era aceptable; no obstante, "
    "al someter el sistema a una prueba de esfuerzo realista con 40 usuarios virtuales, las herramientas de observabilidad "
    "revelaron la presencia de un cuello de botella severo."
)
add_p(
    "El valor del monitoreo multidimensional con Prometheus y Grafana quedó evidenciado al analizar la correlación entre la CPU "
    "(1.03 núcleos) y el retardo del bucle de eventos (1188 ms). En tecnologías monohilo como Node.js, una función sincrónica "
    "bloqueante en una ruta secundaria (/reporte) paraliza la capacidad del servidor para atender solicitudes en rutas independientes "
    "y ligeras (/tasks), elevando su latencia a casi 650 ms. Sin métricas de event loop lag y CPU, un desarrollador podría intentar "
    "optimizar erróneamente la ruta afectada en lugar de la ruta causante."
)
add_p(
    "Asimismo, la integración continua con GitHub Actions demostró ser la salvaguarda indispensable para asegurar que las mejoras "
    "sean permanentes. Al aplicar la técnica de crear una prueba de regresión automatizada (CP-11) antes de modificar el código "
    "productivo, se logró tipificar la falla en rojo y verificar fehacientemente su resolución en verde. Con una reducción de latencia "
    "superior al 99% y un incremento del 58% en el throughput transaccional, la práctica concluye demostrando que cada mejora descubierta "
    "abre la puerta al siguiente ciclo de optimización (M-03), consolidando una cultura de calidad y mejora continua."
)

# Guardar documento final
doc.save(OUTPUT_DOCX)
print(f"Documento Word con formato idéntico guardado en: {OUTPUT_DOCX}")
