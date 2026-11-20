param([string]$etapa = 'antes')
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
function Captura($url, $archivo, $w = 1500, $h = 1000) {
  & $edge --headless --disable-gpu --hide-scrollbars --window-size="$w,$h" --virtual-time-budget=20000 --screenshot="$PWD\evidencias\$archivo" $url 2>&1 | Out-Null
}
New-Item -ItemType Directory -Force evidencias | Out-Null

docker compose restart api 2>&1 | Out-Null
Start-Sleep 10
$ini = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() - 20000
docker compose run --rm k6 2>&1 | Out-File -Encoding utf8 "evidencias\k6-$etapa.txt"
$fin = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() + 15000
Start-Sleep 8
Captura "http://localhost:3001/d/gestor-tareas/gestor-de-tareas?orgId=1&from=$ini&to=$fin&kiosk" "grafana-$etapa.png" 1600 1300
Captura "http://localhost:9090/targets" "prometheus-targets-$etapa.png" 1400 700

# Valores pico desde Prometheus (rango de la prueba)
$s = [math]::Floor($ini / 1000); $e = [math]::Ceiling($fin / 1000)
function Pico($q) {
  $u = "http://localhost:9090/api/v1/query_range?query=" + [uri]::EscapeDataString($q) + "&start=$s&end=$e&step=2"
  $r = curl.exe -s $u | ConvertFrom-Json
  $vals = @(); foreach ($ser in $r.data.result) { foreach ($v in $ser.values) { if ($v[1] -ne 'NaN') { $vals += [double]$v[1] } } }
  if ($vals.Count) { ($vals | Measure-Object -Maximum).Maximum } else { 'n/d' }
}
$res = [ordered]@{
  p95_reporte = Pico 'histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{route="/reporte"}[30s])))'
  p95_tasks   = Pico 'histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{route="/tasks",method="GET"}[30s])))'
  lag_p99     = Pico 'nodejs_eventloop_lag_p99_seconds'
  cpu         = Pico 'rate(process_cpu_seconds_total[30s])'
  rps         = Pico 'sum(rate(http_request_duration_seconds_count[30s]))'
  mem_mb      = (Pico 'process_resident_memory_bytes') / 1MB
}
$res | ConvertTo-Json | Out-File -Encoding utf8 "evidencias\picos-$etapa.json"
Get-Content "evidencias\k6-$etapa.txt" -Tail 45
Get-Content "evidencias\picos-$etapa.json"
