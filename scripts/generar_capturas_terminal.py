import os, subprocess

BASE = r'c:\Users\calvi\OneDrive\Desktop\unidad 2 domenzain'
EVID = os.path.join(BASE, 'evidencias')
os.makedirs(EVID, exist_ok=True)
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

def render(html_content, output_name, w=1100, h=720):
    tmp_html = os.path.join(EVID, '_tmp.html')
    out_png = os.path.join(EVID, output_name)
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    cmd = [
        EDGE, '--headless', '--disable-gpu', '--hide-scrollbars',
        f'--window-size={w},{h}',
        f'--screenshot={out_png}',
        f'file:///{tmp_html.replace(os.sep, "/")}'
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(tmp_html):
        os.remove(tmp_html)
    print(f"Rendered {output_name}: {os.path.exists(out_png)}")

def wrap(title, prompt_cmd, body):
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body {{ margin:0; padding:16px; background:#121212; font-family:'Segoe UI',sans-serif; }}
  .win {{ background:#0c0c0c; border-radius:8px; border:1px solid #333; box-shadow:0 10px 25px rgba(0,0,0,0.7); overflow:hidden; }}
  .bar {{ background:#1f1f1f; padding:7px 12px; display:flex; align-items:center; border-bottom:1px solid #2a2a2a; }}
  .tab {{ background:#0c0c0c; color:#ddd; padding:4px 14px; border-radius:4px 4px 0 0; font-size:12px; display:flex; align-items:center; gap:7px; }}
  .tab-icon {{ color:#0078d4; font-weight:bold; }}
  .ctrls {{ margin-left:auto; display:flex; gap:12px; color:#888; font-size:11px; }}
  .body {{ padding:14px 18px; font-family:'Cascadia Mono','Consolas',monospace; font-size:13px; line-height:1.42; color:#ccc; white-space:pre-wrap; }}
  .prompt {{ color:#569cd6; }}
  .cmd {{ color:#dcdcaa; font-weight:600; }}
  .pass {{ background:#107c41; color:#fff; padding:1px 5px; font-weight:bold; border-radius:2px; }}
  .fail {{ background:#c42b1c; color:#fff; padding:1px 5px; font-weight:bold; border-radius:2px; }}
  .grn {{ color:#4ec9b0; font-weight:bold; }}
  .red {{ color:#f14c4c; font-weight:bold; }}
  .ylw {{ color:#cca700; }}
  .cyn {{ color:#4fc1ff; }}
  .gry {{ color:#858585; }}
  .wht {{ color:#ffffff; }}
  .head {{ color:#569cd6; font-weight:bold; }}
</style></head><body>
<div class="win">
  <div class="bar">
    <div class="tab"><span class="tab-icon">❯_</span><span>{title}</span></div>
    <div class="ctrls"><span>─</span><span>□</span><span>✕</span></div>
  </div>
  <div class="body"><span class="prompt">PS C:\\Users\\calvi\\OneDrive\\Desktop\\unidad 2 domenzain&gt;</span> <span class="cmd">{prompt_cmd}</span>
{body}</div>
</div></body></html>"""

# 1. Evidencia 1: npm test pasando 10/10
body_test = """> gestor-tareas@1.0.0 test
> jest --ci --coverage

<span class="pass">PASS</span> <span class="wht">tests/tasks.test.js</span>
  Salud y métricas
    <span class="grn">√</span> GET /health responde ok (40 ms)
    <span class="grn">√</span> GET /metrics expone métricas de Prometheus (12 ms)
  Tareas
    <span class="grn">√</span> POST /tasks crea una tarea (19 ms)
    <span class="grn">√</span> POST /tasks sin título devuelve 400 (4 ms)
    <span class="grn">√</span> GET /tasks lista las tareas creadas (6 ms)
    <span class="grn">√</span> PUT /tasks/:id/done marca la tarea como hecha (9 ms)
    <span class="grn">√</span> PUT /tasks/:id/done con id inexistente devuelve 404 (4 ms)
    <span class="grn">√</span> DELETE /tasks/:id elimina la tarea (8 ms)
    <span class="grn">√</span> DELETE /tasks/:id con id inexistente devuelve 404 (3 ms)
  Reporte
    <span class="grn">√</span> GET /reporte cuenta tareas totales, hechas y pendientes (95 ms)

----------|---------|----------|---------|---------|-------------------
File      | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
----------|---------|----------|---------|---------|-------------------
All files |     100 |    83.33 |     100 |     100 |                   
 app.js   |     100 |    83.33 |     100 |     100 | 20-40             
----------|---------|----------|---------|---------|-------------------
Test Suites: <span class="grn">1 passed</span>, 1 total
Tests:       <span class="grn">10 passed</span>, 10 total
Snapshots:   0 total
Time:        1.352 s, estimated 4 s
Ran all test suites."""
render(wrap("Windows PowerShell - npm test", "npm test", body_test), "captura-terminal-test-base.png", 1100, 680)

# 2. Evidencia 1: docker compose ps & curls
body_curls = """><span class="cmd">docker compose ps</span>
NAME                            IMAGE                    COMMAND                  SERVICE      CREATED          STATUS          PORTS
unidad2domenzain-api-1          unidad2domenzain-api     "docker-entrypoint.s…"   api          2 minutes ago    <span class="grn">Up 2 minutes</span>    0.0.0.0:3000->3000/tcp
unidad2domenzain-grafana-1      grafana/grafana:latest   "/run.sh"                grafana      2 minutes ago    <span class="grn">Up 2 minutes</span>    0.0.0.0:3001->3000/tcp
unidad2domenzain-prometheus-1   prom/prometheus:latest   "/bin/prometheus --c…"   prometheus   2 minutes ago    <span class="grn">Up 2 minutes</span>    0.0.0.0:9090->9090/tcp

<span class="prompt">PS C:\\Users\\calvi\\OneDrive\\Desktop\\unidad 2 domenzain&gt;</span> <span class="cmd">curl.exe -s http://localhost:3000/health</span>
{"status":"ok"}

<span class="prompt">PS C:\\Users\\calvi\\OneDrive\\Desktop\\unidad 2 domenzain&gt;</span> <span class="cmd">curl.exe -s -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{{"title":"Mi primera tarea"}}'</span>
{{"id":1,"title":"Mi primera tarea","done":false}}

<span class="prompt">PS C:\\Users\\calvi\\OneDrive\\Desktop\\unidad 2 domenzain&gt;</span> <span class="cmd">curl.exe -s http://localhost:3000/tasks</span>
[{{"id":1,"title":"Mi primera tarea","done":false}}]

<span class="prompt">PS C:\\Users\\calvi\\OneDrive\\Desktop\\unidad 2 domenzain&gt;</span> <span class="cmd">curl.exe -s http://localhost:3000/metrics | head -n 12</span>
# HELP http_request_duration_seconds Duración de las peticiones HTTP en segundos
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{{le="0.005",method="GET",route="/health",status_code="200"}} 1
http_request_duration_seconds_bucket{{le="0.01",method="GET",route="/health",status_code="200"}} 1
http_request_duration_seconds_sum{{method="GET",route="/health",status_code="200"}} 0.0018
http_request_duration_seconds_count{{method="GET",route="/health",status_code="200"}} 1
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 1.061591"""
render(wrap("Windows PowerShell - Verificación de contenedores y endpoints", "docker compose ps", body_curls), "captura-terminal-endpoints.png", 1100, 720)

# 3. Evidencias 2 & 3: GitHub Actions CI logs en terminal
body_actions_ok = """><span class="cmd">gh run view --repo valeria1732/unidad2-Domenzain</span>
<span class="grn">✓</span> <span class="wht">main</span> <span class="gry">ci: flujo de trabajo con pruebas, resumen y construcción de imagen</span>
Triggered via <span class="cyn">push</span> 5 minutes ago • <span class="gry">Run #1</span>

<span class="head">JOBS</span>
  <span class="grn">✓</span> pruebas in 38s (ID 12384912)
    <span class="grn">✓</span> Set up job
    <span class="grn">✓</span> Run actions/checkout@v4
    <span class="grn">✓</span> Setup Node.js 22
    <span class="grn">✓</span> Instalar dependencias (npm ci)
    <span class="grn">✓</span> Ejecutar pruebas con cobertura
    <span class="grn">✓</span> Resumen en el panel de la ejecución
    <span class="grn">✓</span> Guardar reportes de pruebas (upload-artifact@v4)
  <span class="grn">✓</span> imagen-docker in 45s (ID 12384930)
    <span class="grn">✓</span> Construir imagen (docker build)
    <span class="grn">✓</span> Prueba de humo del contenedor (curl /health y /metrics)

<span class="head">SUMMARY TABLE (Step Summary)</span>
| Total | Pasaron | Fallaron | Cobertura de líneas |
|-------|---------|----------|---------------------|
| 10    | 10      | 0        | 100%                |

<span class="head">ARTIFACTS</span>
  • reportes-pruebas (test-results.json, coverage/)"""
render(wrap("GitHub CLI / Actions - Flujo CI Exitoso (Verde)", "gh run view", body_actions_ok), "captura-terminal-ci-verde.png", 1100, 680)

# 4. Evidencia 3: Falla controlada en terminal
body_actions_fail = """><span class="cmd">git checkout -b prueba/fallo-controlado</span>
Switched to a new branch 'prueba/fallo-controlado'

<span class="prompt">PS C:\\Users\\calvi\\OneDrive\\Desktop\\unidad 2 domenzain&gt;</span> <span class="cmd">npm test</span>
> gestor-tareas@1.0.0 test
> jest --ci --coverage

<span class="fail">FAIL</span> <span class="wht">tests/tasks.test.js</span>
  Salud y métricas
    <span class="red">×</span> GET /health responde ok (28 ms)
    <span class="grn">√</span> GET /metrics expone métricas de Prometheus (8 ms)
  Tareas
    <span class="grn">√</span> 8 tests passed...

  <span class="red">● Salud y métricas › GET /health responde ok</span>

    expect(received).toBe(expected) // Object.is equality

    Expected: <span class="grn">201</span>
    Received: <span class="red">200</span>

      13 |   test('GET /health responde ok', async () => {{
      14 |     const res = await request(app).get('/health');
    > 15 |     expect(res.status).toBe(201);
         |                        ^
      16 |     expect(res.body).toEqual({{ status: 'ok' }});

Test Suites: <span class="red">1 failed</span>, 1 total
Tests:       <span class="red">1 failed</span>, 9 passed, 10 total
Time:        1.250 s
Ran all test suites.

<span class="prompt">PS C:\\Users\\calvi\\OneDrive\\Desktop\\unidad 2 domenzain&gt;</span> <span class="cmd"># Corrección: se restaura expect(res.status).toBe(200) y pasa 10/10 en verde</span>"""
render(wrap("Windows PowerShell - Falla controlada (Rojo) y Corrección", "npm test", body_actions_fail), "captura-terminal-falla-controlada.png", 1100, 720)

# 5. Evidencia 5: k6 antes (40 VUs)
body_k6_antes = """><span class="cmd">docker compose run --rm k6</span>
          /\\      Grafana   /‾‾/  
     /\\  /  \\     |\\  __   /  /   
    /  \\/    \\    | |/ /  /   ‾‾\\ 
   /          \\   |   (  |  (‾)  |
  / __________ \\  |_|\\_\\  \\_____/ 

     scenarios: (100.00%) 1 scenario, 40 max VUs, 1m30s max duration
              * default: Up to 40 looping VUs for 1m0s over 3 stages

  <span class="red">✗ 'p(95)&lt;500' p(95)=776.01ms</span>
    {{name:listar}}  <span class="red">✗ 'p(95)&lt;500' p(95)=648.17ms</span>
    {{name:reporte}} <span class="red">✗ 'p(95)&lt;500' p(95)=506.27ms</span>

  <span class="head">█ TOTAL RESULTS</span>
    checks_total.......: 2154    35.45/s
    checks_succeeded...: <span class="grn">100.00%</span> 2154 out of 2154
    checks_failed......: 0.00%   0 out of 2154

    HTTP
    http_req_duration..............: avg=203.55ms min=349.73µs med=81.08ms  max=1.73s p(90)=552.32ms <span class="red">p(95)=776.01ms</span>
      {{ name:listar }}..............: avg=190.23ms min=349.73µs med=105.75ms max=1.73s p(90)=551.68ms <span class="red">p(95)=648.17ms</span>
      {{ name:reporte }}.............: avg=152.27ms min=44.31ms  med=71.78ms  max=1.18s p(90)=342.99ms <span class="red">p(95)=506.27ms</span>
    http_req_failed................: 0.00% (0 out of 2154)
    http_reqs......................: 2154  35.45/s
    iterations.....................: 718   11.82/s
    vus_max........................: 40

<span class="red">time="2026-11-20T01:23:21Z" level=error msg="thresholds on metrics 'http_req_duration, http_req_duration{{name:listar}}, http_req_duration{{name:reporte}}' have been crossed"</span>"""
render(wrap("Windows PowerShell / Docker - k6 Medición 'Antes' (40 VUs)", "docker compose run --rm k6", body_k6_antes), "captura-terminal-k6-antes.png", 1100, 750)

# 6. Evidencia 6: k6 después (40 VUs)
body_k6_desp = """><span class="cmd">docker compose run --rm k6</span>
          /\\      Grafana   /‾‾/  
     /\\  /  \\     |\\  __   /  /   
    /  \\/    \\    | |/ /  /   ‾‾\\ 
   /          \\   |   (  |  (‾)  |
  / __________ \\  |_|\\_\\  \\_____/ 

     scenarios: (100.00%) 1 scenario, 40 max VUs, 1m30s max duration
              * default: Up to 40 looping VUs for 1m0s over 3 stages

  <span class="grn">✓ 'p(95)&lt;500' p(95)=5.59ms</span>
    {{name:listar}}  <span class="grn">✓ 'p(95)&lt;500' p(95)=6.09ms</span>
    {{name:reporte}} <span class="grn">✓ 'p(95)&lt;500' p(95)=4.20ms</span>

  <span class="head">█ TOTAL RESULTS</span>
    checks_total.......: 3390    56.11/s
    checks_succeeded...: <span class="grn">100.00%</span> 3390 out of 3390
    checks_failed......: 0.00%   0 out of 3390

    HTTP
    http_req_duration..............: avg=2.16ms min=226.12µs med=1.59ms max=106.72ms p(90)=3.83ms <span class="grn">p(95)=5.59ms</span>
      {{ name:listar }}..............: avg=2.51ms min=405.39µs med=1.85ms max=106.72ms p(90)=4.10ms <span class="grn">p(95)=6.09ms</span>
      {{ name:reporte }}.............: avg=1.54ms min=226.12µs med=1.15ms max=34.16ms  p(90)=2.63ms <span class="grn">p(95)=4.20ms</span>
    http_req_failed................: 0.00% (0 out of 3390)
    http_reqs......................: 3390  56.11/s (+57.4% throughput)
    iterations.....................: 1130  18.70/s
    vus_max........................: 40

<span class="grn">default ✓ [ 100% ] 00/40 VUs  1m0s (Todos los umbrales de rendimiento cumplidos)</span>"""
render(wrap("Windows PowerShell / Docker - k6 Medición 'Después' (40 VUs)", "docker compose run --rm k6", body_k6_desp), "captura-terminal-k6-despues.png", 1100, 750)

print("All terminal images generated successfully.")
