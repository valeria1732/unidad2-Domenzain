# unidad2-Domenzain

API de tareas (`gestor-tareas`) para el ejercicio de desarrollo e integración continua: pruebas con Jest, CI con GitHub Actions, monitoreo con Prometheus/Grafana y carga con k6.

## Comandos

```bash
npm install && npm test                 # pruebas + cobertura
docker compose up -d --build            # api :3000, prometheus :9090, grafana :3001 (admin/admin)
docker compose restart api && docker compose run --rm k6   # prueba de carga
docker compose down -v                  # limpiar
```
