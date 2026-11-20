import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 10 },
    { duration: '30s', target: 20 },
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
}
