// Genera reporte.html a partir de las evidencias reales guardadas en /evidencias.
const fs = require('fs');
const path = require('path');
const ev = (f) => path.join(__dirname, '..', 'evidencias', f);
const leer = (f) =>
  fs.readFileSync(ev(f), 'utf8')
    .replace(/^\uFEFF/, '')
    .replace(/Ã©/g, 'é').replace(/Ã³/g, 'ó').replace(/Ã­/g, 'í').replace(/Ã±/g, 'ñ').replace(/Ã¡/g, 'á').replace(/Ãº/g, 'ú')
    .replace(/\r/g, '');
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function term(titulo, cmd, texto) {
  return `<div class="term"><div class="bar"><i></i><i></i><i></i><span>${esc(titulo)}</span></div><pre>${
    cmd ? `<span class="p">PS ...\\unidad 2 domenzain&gt;</span> <span class="c">${esc(cmd)}</span>\n` : ''}${esc(texto.trimEnd())}</pre></div>`;
}
function resumenK6(f) {
  const t = leer(f);
  const i = t.indexOf('█ THRESHOLDS');
  const j = t.indexOf('running (1m');
  const cuerpo = t.slice(i, j).replace(/\n{3,}/g, '\n\n');
  const fin = t.slice(j).split('\n').filter((l) => l.trim()).slice(0, 2).join('\n');
  return cuerpo.trimEnd() + '\n\n' + fin;
}
function resumenTests(f) {
  const t = leer(f).split('\n');
  const i = t.findIndex((l) => /^(PASS|FAIL)/.test(l));
  return t.slice(i).join('\n');
}
const fig = (src, cap) => `<figure><img src="evidencias/${src}"><figcaption>${cap}</figcaption></figure>`;
const pend = (t) => `<div class="pend">${t}</div>`;
const J = (f) => JSON.parse(leer(f));
const A = J('picos-antes.json'), D = J('picos-despues.json'), A20 = J('picos-antes20vu.json');

const html = `<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>Reporte - Desarrollo e integración continua</title>
<style>
@page{size:Letter;margin:18mm 16mm}
body{font-family:Segoe UI,Arial,sans-serif;color:#222;font-size:12.5px;line-height:1.5}
h1{color:#1f3d6e;border-bottom:3px solid #2b5797;padding-bottom:5px}
h2{color:#2b5797;margin-top:26px;border-bottom:1px solid #c5d3e8;padding-bottom:3px;break-after:avoid}
h3{color:#1f3d6e;break-after:avoid}
.portada{height:230mm;display:flex;flex-direction:column;justify-content:center;text-align:center;break-after:page}
.portada h1{border:none;font-size:30px}
.nuevo{break-before:page}
.term{background:#1e1e1e;border-radius:6px;margin:10px 0;break-inside:avoid-page;overflow:hidden}
.term .bar{background:#333;padding:5px 10px;color:#ccc;font-size:11px}
.term .bar i{display:inline-block;width:9px;height:9px;border-radius:50%;background:#e55;margin-right:5px}
.term .bar i:nth-child(2){background:#eb3}.term .bar i:nth-child(3){background:#4c4;margin-right:12px}
.term pre{margin:0;padding:10px 12px;color:#d4d4d4;font:10.5px/1.35 Consolas,monospace;white-space:pre-wrap}
.p{color:#6cf}.c{color:#dcdcaa}
figure{margin:10px 0;break-inside:avoid}figure img{width:100%;border:1px solid #888;border-radius:4px}
figcaption{font-size:11px;color:#555;text-align:center}
table{border-collapse:collapse;width:100%;font-size:11.5px;margin:8px 0;break-inside:avoid}
td,th{border:1px solid #999;padding:4px 6px;vertical-align:top}th{background:#e3ebf7}
.ok{color:#0a7a2f;font-weight:600}.no{color:#b00020;font-weight:600}
.pend{background:#fff4cc;border-left:4px solid #e0a800;padding:8px 10px;margin:10px 0;break-inside:avoid}
.box{border:2px dashed #999;padding:40px 10px;text-align:center;color:#777;margin:10px 0;break-inside:avoid}
code{background:#eef;padding:1px 4px;border-radius:3px}
</style></head><body>

<div class="portada">
<p>Unidad 2 · Desarrollo e integración continua</p>
<h1>Ejercicio práctico:<br>Integración continua, monitoreo y evaluación de rendimiento</h1>
<p><b>Proyecto:</b> gestor-tareas-ci (API de tareas en Node.js/Express)</p>
<p><b>Repositorio:</b> https://github.com/valeria1732/unidad2-Domenzain</p>
<p><b>Alumna:</b> Valeria Calvillo</p>
<p><b>Fecha:</b> 19 de noviembre de 2026</p>
</div>

<h2 style="margin-top:0">Contenido</h2>
<ol>
<li>Objetivo y entorno</li>
<li>Parte 1. Proyecto base, pruebas y contenedor (Evidencia 1)</li>
<li>Parte 2. Integración continua y seguimiento de pruebas (Evidencias 2 y 3)</li>
<li>Parte 3. Monitoreo con Prometheus y Grafana (Evidencia 4)</li>
<li>Parte 4. Evaluación de rendimiento con k6, medición "antes" (Evidencia 5)</li>
<li>Parte 5. Plan de mejora, medición "después" y comparación (Evidencia 6)</li>
<li>Conclusión</li>
</ol>
${pend('<b>Estado de las evidencias.</b> Las evidencias de las Partes 1, 3, 4 y 5 son salidas reales ejecutadas en el equipo (Docker Desktop, Jest, Prometheus, Grafana y k6); las capturas de terminal se presentan como bloques con el texto exacto de cada comando. Las evidencias de GitHub Actions (2 y 3) requieren la sesión de GitHub y aparecen marcadas con un recuadro para pegar la captura.')}

<h2>1. Objetivo y entorno</h2>
<p>Realizar un ciclo completo de <b>medir, mejorar y volver a medir</b>: una API se prueba automáticamente con GitHub Actions, se ejecuta y se monitorea localmente con Prometheus y Grafana, se somete a carga con k6 y los resultados alimentan un plan de mejora con metas numéricas.</p>
<table><tr><th>Componente</th><th>Detalle</th></tr>
<tr><td>Sistema</td><td>Windows, Docker Desktop (motor Linux), Docker ${'29.7.2'}</td></tr>
<tr><td>Aplicación</td><td>Node.js 22 (imagen <code>node:22-alpine</code>), Express 4, prom-client 15</td></tr>
<tr><td>Pruebas</td><td>Jest 29 + Supertest 7 (umbral de cobertura de líneas 80 %)</td></tr>
<tr><td>Monitoreo</td><td>Prometheus (scrape cada 5 s) y Grafana, puertos 9090 y 3001</td></tr>
<tr><td>Carga</td><td>k6 en contenedor, perfil <code>carga</code> de docker compose</td></tr>
</table>

<h2 class="nuevo">2. Parte 1. Proyecto base, pruebas y contenedor</h2>
<h3>Evidencia 1. Pruebas con cobertura</h3>
${term('npm test (rama mejora/reporte-rapido)', 'npm test', leer('test-verde.txt') && resumenTests('test-verde.txt').replace('11 passed, 11 total', '11 passed, 11 total'))}
<p>Nota: la salida mostrada corresponde a la rama de mejora, con 11 pruebas (las 10 originales más la prueba de regresión de rendimiento de la Parte 5). En <code>main</code> el proyecto base tuvo 10 pruebas aprobadas con cobertura de líneas del 100 % (umbral ≥ 80 %).</p>

<h3>Servicios en ejecución y respuesta de los endpoints</h3>
${term('docker compose ps', 'docker compose ps', leer('01-compose-ps.txt'))}
${term('Prueba de endpoints', '', leer('02-curl.txt'))}
<p>El endpoint <code>/health</code> responde <code>{"status":"ok"}</code> y <code>/metrics</code> expone las métricas de Prometheus, entre ellas <code>http_request_duration_seconds</code> (definida en <code>src/app.js</code>) y las métricas por defecto del proceso.</p>

<h3>Publicación en GitHub</h3>
${fig('../push.jpg', 'Salida de <code>git push -u origin main</code>: la rama main quedó publicada en el repositorio.')}

<h2 class="nuevo">3. Parte 2. Integración continua y seguimiento de pruebas</h2>
<p>El flujo <code>.github/workflows/ci.yml</code> corre en cada <code>push</code> y <code>pull_request</code> hacia main. Tiene dos trabajos: <b>pruebas</b> (npm ci, Jest con cobertura, resumen en el panel de la ejecución y artefacto <code>reportes-pruebas</code>) e <b>imagen-docker</b> (construye la imagen y hace una prueba de humo; depende de <code>pruebas</code> con <code>needs</code>, por lo que se omite si las pruebas fallan).</p>
<h3>Evidencia 2. Ejecución en verde con tabla de resumen</h3>
<div class="box">Pegar aquí la captura de la pestaña Actions con la ejecución en verde y la tabla de resumen.</div>
<h3>Evidencia 3. Falla controlada y corrección</h3>
<div class="box">Pegar aquí la captura de la ejecución en rojo (detalle de la prueba fallida) y de la ejecución corregida en verde.</div>

<h3>Matriz de casos de prueba</h3>
<table><tr><th>ID</th><th>Endpoint</th><th>Escenario</th><th>Resultado esperado</th><th>Resultado local (Jest)</th><th>Resultado en CI</th></tr>
<tr><td>CP-01</td><td>GET /health</td><td>Consulta de salud</td><td>200 y {"status":"ok"}</td><td class="ok">Pasó</td><td>(completar con Actions)</td></tr>
<tr><td>CP-02</td><td>GET /metrics</td><td>Consulta de métricas</td><td>200 y contiene http_request_duration_seconds</td><td class="ok">Pasó</td><td></td></tr>
<tr><td>CP-03</td><td>POST /tasks</td><td>Título válido</td><td>201, id 1, done falso</td><td class="ok">Pasó</td><td></td></tr>
<tr><td>CP-04</td><td>POST /tasks</td><td>Sin título</td><td>400</td><td class="ok">Pasó</td><td></td></tr>
<tr><td>CP-05</td><td>GET /tasks</td><td>Con una tarea creada</td><td>Lista de 1 elemento</td><td class="ok">Pasó</td><td></td></tr>
<tr><td>CP-06</td><td>PUT /tasks/:id/done</td><td>Tarea existente</td><td>200 y done verdadero</td><td class="ok">Pasó</td><td></td></tr>
<tr><td>CP-07</td><td>PUT /tasks/:id/done</td><td>Id inexistente</td><td>404</td><td class="ok">Pasó</td><td></td></tr>
<tr><td>CP-08</td><td>DELETE /tasks/:id</td><td>Tarea existente</td><td>204 y lista vacía</td><td class="ok">Pasó</td><td></td></tr>
<tr><td>CP-09</td><td>DELETE /tasks/:id</td><td>Id inexistente</td><td>404</td><td class="ok">Pasó</td><td></td></tr>
<tr><td>CP-10</td><td>GET /reporte</td><td>2 tareas, 1 hecha</td><td>total 2, hechas 1, pendientes 1</td><td class="ok">Pasó</td><td></td></tr>
<tr><td>CP-11</td><td>GET /reporte</td><td>Regresión de rendimiento</td><td>Responde en &lt; 50 ms</td><td><span class="no">Falló</span> (107 ms) → <span class="ok">Pasó</span> (3 ms) tras la mejora</td><td></td></tr>
</table>

<h3>Bitácora de ejecuciones</h3>
<p>Las ejecuciones locales siguientes son reales. Las de GitHub Actions deben completarse con los datos de la pestaña Actions (fecha, duración y resultado) después de abrir los pull requests.</p>
<table><tr><th>N.º</th><th>Fecha</th><th>Rama / commit</th><th>Evento</th><th>Total</th><th>Pasaron</th><th>Fallaron</th><th>Cobertura</th><th>Resultado</th><th>Causa y acción</th></tr>
<tr><td>1</td><td>19/11/2026</td><td>main (local)</td><td>npm test</td><td>10</td><td>10</td><td>0</td><td>100 %</td><td class="ok">Verde</td><td>Línea base del proyecto.</td></tr>
<tr><td>2</td><td>19/11/2026</td><td>mejora/reporte-rapido · 2e6ea93 (local)</td><td>npm test</td><td>11</td><td>10</td><td>1</td><td>100 %</td><td class="no">Rojo</td><td>CP-11: esperado &lt; 50 ms, recibido 107.45 ms (línea 79 de tests/tasks.test.js). Causa: el ciclo heredado de 50 millones de iteraciones en <code>calcularReporte</code>. Acción: eliminar el ciclo.</td></tr>
<tr><td>3</td><td>19/11/2026</td><td>mejora/reporte-rapido · c7724de (local)</td><td>npm test</td><td>11</td><td>11</td><td>0</td><td>100 %</td><td class="ok">Verde</td><td>Corrección aplicada; CP-11 responde en 3 ms.</td></tr>
<tr><td>4–6</td><td></td><td>(Actions)</td><td>push / pull_request</td><td></td><td></td><td></td><td></td><td></td><td>Completar con las ejecuciones de GitHub Actions.</td></tr>
</table>
<h3>Análisis de la falla (con mis palabras)</h3>
<p>La prueba de regresión midió el tiempo de respuesta de <code>/reporte</code> y obtuvo 107.45 ms contra un límite de 50 ms, por lo que Jest marcó la aserción <code>expect(ms).toBeLessThan(50)</code> como fallida. La causa no estaba en la lógica del reporte, sino en el trabajo extra que hacía la función antes de contar las tareas. La acción fue quitar ese trabajo; después de eso la misma prueba pasó con 3 ms.</p>
${term('Prueba en rojo (rama mejora/reporte-rapido)', 'npm test', resumenTests('test-rojo.txt'))}

<h2 class="nuevo">4. Parte 3. Monitoreo con Prometheus y Grafana</h2>
<h3>Objetivos de rendimiento (definidos antes de medir)</h3>
<table><tr><th>Indicador</th><th>Objetivo</th><th>Dónde se mide</th></tr>
<tr><td>Latencia p95 global</td><td>&lt; 500 ms</td><td>k6 y panel de latencia p95</td></tr>
<tr><td>Tasa de errores</td><td>&lt; 1 %</td><td>k6 y panel de errores 5xx</td></tr>
<tr><td>Retardo del bucle de eventos (p99)</td><td>&lt; 100 ms</td><td>Panel de retardo del bucle de eventos</td></tr></table>
<h3>Evidencia 4. Prometheus recolectando</h3>
${fig('prometheus-targets-antes.png', 'http://localhost:9090/targets: el objetivo <b>gestor-tareas</b> (api:3000) está en estado <b>UP</b> (1 / 1 up).')}
<h3>Tablero de Grafana "Gestor de tareas" (6 paneles)</h3>
<table><tr><th>Panel</th><th>Consulta PromQL</th><th>Unidad</th></tr>
<tr><td>Peticiones por segundo</td><td><code>sum by (route) (rate(http_request_duration_seconds_count[1m]))</code></td><td>req/s</td></tr>
<tr><td>Latencia p95 por ruta</td><td><code>histogram_quantile(0.95, sum by (le, route) (rate(http_request_duration_seconds_bucket[1m])))</code></td><td>s</td></tr>
<tr><td>Errores 5xx por segundo</td><td><code>sum(rate(http_request_duration_seconds_count{status_code=~"5.."}[1m])) or vector(0)</code></td><td>req/s</td></tr>
<tr><td>Uso de CPU del proceso</td><td><code>rate(process_cpu_seconds_total[1m])</code></td><td>núcleos</td></tr>
<tr><td>Retardo del bucle de eventos (p99)</td><td><code>nodejs_eventloop_lag_p99_seconds</code></td><td>s</td></tr>
<tr><td>Memoria residente</td><td><code>process_resident_memory_bytes</code></td><td>bytes</td></tr></table>
<p>El tablero se creó mediante la API de Grafana a partir de <code>scripts/dashboard.json</code>, incluido en el repositorio.</p>

<h2 class="nuevo">5. Parte 4. Evaluación de rendimiento, medición "antes"</h2>
<p><b>Procedimiento.</b> Siempre desde el mismo estado: API reiniciada, espera de 10 s y <code>docker compose run --rm k6</code>. Flujo por usuario: crear tarea, listar tareas y pedir el reporte, con 1 s de pausa.</p>
<h3>Primera corrida: 20 usuarios virtuales (script original)</h3>
${term('k6 · 20 VUs', 'docker compose run --rm k6', resumenK6('k6-antes20vu.txt'))}
<p>Con 20 usuarios virtuales todos los umbrales de latencia de k6 se cumplieron (p95 global 75.92 ms), pero el retardo del bucle de eventos p99 ya alcanzó <b>116.7 ms</b>, por encima del objetivo de 100 ms. Como el documento indica, cuando el p95 ya cumple el objetivo se sube el segundo tramo de 20 a 40 usuarios y se repite la medición. <b>Cambio documentado:</b> <code>{ duration: '30s', target: 20 }</code> pasó a <code>{ duration: '30s', target: 40 }</code> en <code>k6/carga.js</code>.</p>
${fig('grafana-antes20vu.png', 'Grafana durante la corrida de 20 usuarios virtuales.')}

<h3 class="nuevo">Evidencia 5. Medición "antes" con 40 usuarios virtuales</h3>
${term('k6 · 40 VUs (antes de la mejora)', 'docker compose run --rm k6', resumenK6('k6-antes.txt'))}
${fig('grafana-antes.png', 'Tablero de Grafana durante la carga "antes" (40 VUs): el retardo del bucle de eventos llega a más de 1 s y la CPU a cerca de 1 núcleo.')}

<h3>Tabla "antes"</h3>
<table><tr><th>Indicador</th><th>Objetivo</th><th>Valor medido (antes)</th><th>Fuente</th><th>¿Cumple?</th></tr>
<tr><td>Latencia p95 global</td><td>&lt; 500 ms</td><td>776.01 ms</td><td>k6</td><td class="no">No</td></tr>
<tr><td>Latencia p95 de /reporte</td><td>&lt; 500 ms</td><td>506.27 ms</td><td>k6</td><td class="no">No</td></tr>
<tr><td>Latencia p95 de /tasks (listar)</td><td>&lt; 500 ms</td><td>648.17 ms</td><td>k6</td><td class="no">No</td></tr>
<tr><td>Tasa de errores</td><td>&lt; 1 %</td><td>0.00 %</td><td>k6</td><td class="ok">Sí</td></tr>
<tr><td>Retardo del bucle de eventos p99 (pico)</td><td>&lt; 100 ms</td><td>${(A.lag_p99 * 1000).toFixed(0)} ms</td><td>Grafana / Prometheus</td><td class="no">No</td></tr>
<tr><td>Uso de CPU del proceso (pico)</td><td>Cercano a 1 núcleo = saturación</td><td>${A.cpu.toFixed(2)} núcleos</td><td>Grafana / Prometheus</td><td>Saturada</td></tr>
<tr><td>Peticiones por segundo (pico)</td><td>Referencia</td><td>${A.rps.toFixed(1)} req/s</td><td>Grafana / Prometheus</td><td>—</td></tr></table>
<p><i>Nota:</i> los p95 de Grafana se calculan con <code>histogram_quantile</code> sobre los buckets del histograma de la API, por lo que se miden dentro del servidor; k6 mide desde el cliente e incluye la espera en cola.</p>

<h3>Diagnóstico guiado</h3>
<ol>
<li><b>¿Qué ruta tiene la latencia p95 más alta?</b> En k6, <code>/tasks</code> (listar) con 648.17 ms y <code>/reporte</code> con 506.27 ms. Es llamativo que <code>/tasks</code>, que solo devuelve un arreglo, sea tan lenta: es una ruta afectada aunque no debería serlo. Con 20 usuarios <code>/tasks</code> tenía un p95 de solo 2.47 ms, mientras <code>/reporte</code> ya tenía 98.58 ms.</li>
<li><b>¿La CPU se acerca a 1 núcleo?</b> Sí: pico de ${A.cpu.toFixed(2)} núcleos (0.88 con 20 usuarios).</li>
<li><b>¿Qué pasa con el retardo del bucle de eventos?</b> Pasó de ${(A20.lag_p99 * 1000).toFixed(0)} ms con 20 usuarios a <b>${(A.lag_p99 * 1000).toFixed(0)} ms</b> con 40, es decir, unas 12 veces el objetivo de 100 ms.</li>
<li><b>Hipótesis (escrita antes de modificar el código):</b> “La ruta <b>/reporte</b> ocupa la CPU durante unos <b>45 ms</b> por petición (su latencia mínima en k6 es de 44.31 ms incluso casi sin carga); por eso la latencia de <b>/tasks</b> sube cuando hay <b>40</b> usuarios, ya que Node.js atiende todo en un solo hilo y las demás peticiones esperan.”</li>
<li><b>Revisión del código.</b> En <code>src/app.js</code>, la función <code>calcularReporte</code> recorre un ciclo de 50 000 000 de iteraciones (<code>acumulado += i % 7</code>) en cada petición, antes de contar las tareas. Ese ciclo es síncrono: bloquea el hilo único de Node.js, y el único dato que produce (<code>valido</code>) no depende de las tareas.</li>
</ol>
<p><b>Dos métricas que respaldan la causa:</b> (1) el retardo del bucle de eventos de ${(A.lag_p99 * 1000).toFixed(0)} ms y (2) la CPU en ${A.cpu.toFixed(2)} núcleos, además de la latencia en k6 que contagia a <code>/tasks</code>. Una observación adicional: en Prometheus el p95 de <code>/tasks</code> medido dentro del servidor es de apenas ${(A.p95_tasks * 1000).toFixed(1)} ms, porque el tiempo que pasó esperando el bucle bloqueado ocurre antes de que el servidor empiece a cronometrar; de ahí la diferencia con los 648 ms de k6.</p>

<h2 class="nuevo">6. Parte 5. Plan de mejora ligado a los resultados</h2>
<h3>Plan de mejora</h3>
<table><tr><th>ID</th><th>Hallazgo y evidencia (valor "antes")</th><th>Causa</th><th>Acción de mejora</th><th>Meta medible</th><th>Resultado (después)</th><th>Estado</th></tr>
<tr><td>M-01</td><td>p95 de /reporte = 506.27 ms y de /tasks = 648.17 ms con 40 VUs (k6); retardo del bucle de eventos p99 = ${(A.lag_p99 * 1000).toFixed(0)} ms (Grafana)</td><td>Ciclo de 50 M de iteraciones síncrono en <code>calcularReporte</code> que bloquea el hilo único; CPU en ${A.cpu.toFixed(2)} núcleos</td><td>Eliminar el ciclo; contar solo las tareas (versión 2)</td><td>p95 de /reporte &lt; 500 ms (k6, 40 VUs), p95 global &lt; 500 ms y retardo p99 &lt; 100 ms (Grafana)</td><td>p95 /reporte = 4.2 ms; p95 global = 5.59 ms; retardo p99 = ${(D.lag_p99 * 1000).toFixed(1)} ms</td><td class="ok">Cumplida</td></tr>
<tr><td>M-02</td><td>El problema no se detectó en las pruebas funcionales: CP-10 pasó en verde aunque /reporte tardaba más de 100 ms</td><td>Ninguna prueba automática exigía un tiempo máximo de respuesta</td><td>Prueba de regresión de rendimiento (CP-11) que se ejecuta en cada CI</td><td>CP-11 falla con el código heredado (&gt; 50 ms) y pasa tras la mejora (&lt; 50 ms)</td><td>Rojo: 107.45 ms → Verde: 3 ms (local; confirmar en Actions)</td><td class="ok">Cumplida</td></tr>
<tr><td>M-03</td><td>Con la API ya mejorada, la memoria residente sube de 71 MiB a 106 MiB durante la carga (Grafana) y k6 recibe 32 MB frente a 13 MB antes (1130 tareas acumuladas)</td><td>Las tareas viven en memoria sin límite y <code>GET /tasks</code> devuelve la lista completa, que crece con cada iteración</td><td>Propuesta (no implementada): paginar <code>GET /tasks</code> y limitar el tamaño de la lista</td><td>Memoria residente &lt; 100 MiB y respuesta de /tasks &lt; 100 KB con 40 VUs durante 1 minuto</td><td>No aplica: propuesta para el siguiente ciclo</td><td>Pendiente</td></tr></table>

<h3>Paso 5.2. Prueba de regresión antes de corregir</h3>
<p>Se creó la rama <code>mejora/reporte-rapido</code> y se agregó la prueba CP-11. Con el código heredado falló, como se esperaba (ver bitácora, ejecución 2):</p>
${term('Prueba en rojo', 'npm test', resumenTests('test-rojo.txt').split('\n').filter((l) => /×|√|Expected|Received|Tests:|FAIL|PASS|Reporte/.test(l)).join('\n'))}
<h3>Paso 5.3. Mejora aplicada</h3>
<table><tr><th>Versión 1 (heredada)</th><th>Versión 2 (mejora)</th></tr><tr><td><pre style="white-space:pre-wrap;font-size:10.5px">function calcularReporte() {
  let acumulado = 0;
  for (let i = 0; i &lt; 50000000; i++) {
    acumulado += i % 7;
  }
  const total = tareas.length;
  const hechas = tareas.filter((t) =&gt; t.done).length;
  return { total, hechas, pendientes: total - hechas,
           valido: acumulado &gt;= 0 };
}</pre></td><td><pre style="white-space:pre-wrap;font-size:10.5px">function calcularReporte() {
  const total = tareas.length;
  const hechas = tareas.filter((t) =&gt; t.done).length;
  return { total, hechas, pendientes: total - hechas };
}</pre></td></tr></table>
${term('Prueba en verde tras la mejora', 'npm test', resumenTests('test-verde.txt'))}

<h3 class="nuevo">Evidencia 6. Medición "después" (mismas condiciones: 40 VUs, API reiniciada)</h3>
${term('k6 · 40 VUs (después de la mejora)', 'docker compose run --rm k6', resumenK6('k6-despues.txt'))}
${fig('grafana-despues.png', 'Tablero de Grafana durante la carga "después": retardo del bucle de eventos máximo de unos 18 ms y CPU alrededor de 0.1 núcleos.')}

<h3>Comparación antes / después</h3>
<table><tr><th>Indicador</th><th>Objetivo</th><th>Antes</th><th>Después</th><th>Mejora</th><th>¿Cumple ahora?</th></tr>
<tr><td>Latencia p95 global</td><td>&lt; 500 ms</td><td>776.01 ms</td><td>5.59 ms</td><td>99.3 %</td><td class="ok">Sí</td></tr>
<tr><td>Latencia p95 de /reporte</td><td>&lt; 500 ms</td><td>506.27 ms</td><td>4.20 ms</td><td>99.2 %</td><td class="ok">Sí</td></tr>
<tr><td>Latencia p95 de /tasks (listar)</td><td>&lt; 500 ms</td><td>648.17 ms</td><td>6.09 ms</td><td>99.1 %</td><td class="ok">Sí</td></tr>
<tr><td>Tasa de errores</td><td>&lt; 1 %</td><td>0.00 %</td><td>0.00 %</td><td>—</td><td class="ok">Sí</td></tr>
<tr><td>Retardo del bucle de eventos p99 (pico)</td><td>&lt; 100 ms</td><td>${(A.lag_p99 * 1000).toFixed(0)} ms</td><td>${(D.lag_p99 * 1000).toFixed(1)} ms</td><td>${((1 - D.lag_p99 / A.lag_p99) * 100).toFixed(1)} %</td><td class="ok">Sí</td></tr>
<tr><td>Uso de CPU del proceso (pico)</td><td>Referencia</td><td>${A.cpu.toFixed(2)} núcleos</td><td>${D.cpu.toFixed(2)} núcleos</td><td>${((1 - D.cpu / A.cpu) * 100).toFixed(1)} %</td><td>—</td></tr>
<tr><td>Peticiones por segundo (pico)</td><td>Referencia</td><td>${A.rps.toFixed(1)}</td><td>${D.rps.toFixed(1)}</td><td>+${((D.rps / A.rps - 1) * 100).toFixed(0)} %</td><td>—</td></tr></table>
<p>Con la misma carga (40 usuarios virtuales), k6 completó 3390 peticiones frente a 2154 antes, sin cruzar ningún umbral. Las metas de M-01 y M-02 se cumplieron.</p>

<h3>Paso 5.5. Siguiente ciclo: M-03</h3>
<p>Observando el tablero con la API mejorada (gráfica "Memoria residente"), la memoria sube de unos 71 MiB a unos 106 MiB a lo largo de la prueba, y el volumen recibido por k6 aumentó de 13 MB a 32 MB. Cada usuario virtual crea una tarea en cada iteración y <code>GET /tasks</code> devuelve todas, por lo que la respuesta crece con el tiempo. Esto no es un problema a esta escala, pero con una lista creciente y sin límite acabaría afectando memoria y latencia. Por eso se registra como M-03, con una acción propuesta (paginación) y una meta numérica, sin implementarla.</p>

<h2>7. Conclusión (borrador, para reescribir con tus palabras)</h2>
<p>El ejercicio mostró que medir antes de modificar evita corregir a ciegas. Con 20 usuarios virtuales la API parecía cumplir el objetivo de latencia, y fue al subir la carga a 40 cuando los datos revelaron el problema: la latencia de <code>/tasks</code> subía aunque esa ruta no hace trabajo pesado. La clave fue cruzar métricas distintas: el retardo del bucle de eventos (más de 1 s) y la CPU cerca de un núcleo explicaron por qué una ruta lenta afectaba a las demás en un entorno de un solo hilo.</p>
<p>La integración continua aportó la parte preventiva: la prueba de regresión de rendimiento falló con el código heredado y pasó con la mejora, de modo que el problema no puede volver sin que alguien lo note. Al volver a medir en las mismas condiciones, todas las metas se cumplieron y el siguiente cuello de botella (la memoria y el tamaño de la respuesta de <code>/tasks</code>) quedó registrado como M-03. Lo aprendido es que medir, mejorar y volver a medir es un ciclo continuo: cada mejora deja ver el siguiente hallazgo.</p>

<h2>Anexo. Repositorio</h2>
<table><tr><th>Commit</th><th>Descripción</th></tr>
<tr><td>84ff002</td><td>feat: API de tareas con pruebas y Dockerfile</td></tr>
<tr><td>fbbcd2f</td><td>docs: reporte parcial con evidencia de pruebas</td></tr>
<tr><td>128e4fa</td><td>perf: tablero Grafana, scripts de medición y carga a 40 VUs</td></tr>
<tr><td>2e6ea93</td><td>test: prueba de regresión de rendimiento para /reporte (rama mejora/reporte-rapido, en rojo)</td></tr>
<tr><td>1aad6fe, c7724de</td><td>perf: elimina el ciclo innecesario de calcularReporte (en verde)</td></tr></table>
</body></html>`;
fs.writeFileSync(path.join(__dirname, '..', 'reporte.html'), html);
console.log('ok', html.length);
