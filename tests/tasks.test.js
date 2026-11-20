const request = require('supertest');
const app = require('../src/app');

beforeEach(() => app.locals.reiniciar());

describe('Salud y mÃ©tricas', () => {
  test('GET /health responde ok', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ status: 'ok' });
  });

  test('GET /metrics expone mÃ©tricas de Prometheus', async () => {
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

  test('POST /tasks sin tÃ­tulo devuelve 400', async () => {
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
  test('GET /reporte responde en menos de 50 ms (regresión de rendimiento)', async () => {
    const inicio = process.hrtime.bigint();
    const res = await request(app).get('/reporte');
    const ms = Number(process.hrtime.bigint() - inicio) / 1e6;
    expect(res.status).toBe(200);
    expect(ms).toBeLessThan(50);
  });
});
