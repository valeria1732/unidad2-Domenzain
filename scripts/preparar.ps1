$ErrorActionPreference = 'Continue'
New-Item -ItemType Directory -Force evidencias | Out-Null
docker compose up -d 2>&1 | Out-Null
Start-Sleep 15
$ds = (curl.exe -s -u admin:admin http://localhost:3001/api/datasources | ConvertFrom-Json)[0].uid
(Get-Content scripts\dashboard.json -Raw).Replace('"PROM"', '"' + $ds + '"') | Set-Content -Encoding utf8 evidencias\dash.tmp
curl.exe -s -u admin:admin -X POST -H "Content-Type: application/json" --data-binary "@evidencias/dash.tmp" http://localhost:3001/api/dashboards/db
Remove-Item evidencias\dash.tmp
docker compose ps | Out-File -Encoding utf8 evidencias\01-compose-ps.txt
$o = @()
$o += '$ curl http://localhost:3000/health'
$o += (curl.exe -s http://localhost:3000/health)
$o += ''
$o += '$ curl -X POST http://localhost:3000/tasks -d {"title":"Mi primera tarea"}'
$o += (curl.exe -s -X POST http://localhost:3000/tasks -H "Content-Type: application/json" -d '{\"title\":\"Mi primera tarea\"}')
$o += ''
$o += '$ curl http://localhost:3000/tasks'
$o += (curl.exe -s http://localhost:3000/tasks)
$o += ''
$o += '$ curl http://localhost:3000/metrics | head -n 20'
$o += (curl.exe -s http://localhost:3000/metrics | Select-Object -First 20)
$o | Out-File -Encoding utf8 evidencias\02-curl.txt
Get-Content evidencias\01-compose-ps.txt, evidencias\02-curl.txt
