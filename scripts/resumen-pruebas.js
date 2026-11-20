// Genera un resumen en Markdown a partir de los resultados de Jest.
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
  console.log('## Resumen de pruebas\n\nNo se generó test-results.json.');
  process.exit(0);
}
const c = leer('coverage/coverage-summary.json');
const cobertura = c ? `${c.total.lines.pct}%` : 'n/d';

console.log('## Resumen de pruebas\n');
console.log('| Total | Pasaron | Fallaron | Cobertura de líneas |');
console.log('|---|---|---|---|');
console.log(`| ${r.numTotalTests} | ${r.numPassedTests} | ${r.numFailedTests} | ${cobertura} |`);

const fallidas = r.testResults
  .flatMap((f) => f.assertionResults)
  .filter((t) => t.status === 'failed');
if (fallidas.length > 0) {
  console.log('\n### Pruebas fallidas\n');
  fallidas.forEach((t) => console.log(`- ${t.fullName}`));
}
