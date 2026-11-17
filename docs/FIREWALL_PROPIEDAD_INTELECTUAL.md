# Firewall transversal de propiedad intelectual e integridad

**Versión:** 1.0  
**Estado:** contrato y arquitectura propuestos; prototipo local en Gabinete; no desplegado.  
**Alcance:** repositorios y artefactos autorizados del ecosistema de trabajo.

## 1. Propósito

Proteger código fuente, archivos Python, reglas operativas, contratos, prompts, documentación privada, datos de casos y artefactos de investigación contra lectura, copia, exportación o modificación no autorizada. Esta política es transversal; cada repositorio conserva la autoridad sobre sus activos y declara su propio inventario y restricciones.

## 2. Capas de defensa

1. **Inventario y clasificación:** PUBLIC, INTERNAL, PROPRIETARY, RESTRICTED, SECRET; propietario, rutas, acciones permitidas y hashes de referencia.
2. **Identidad y autorización:** principal autenticado, autorización explícita, recurso, acción y destino. Denegar por defecto ante identidad o política ausente.
3. **Integridad:** manifiestos SHA-256 independientes del canal de escritura; comparar antes/después de operaciones sensibles. Hash detecta cambios, no prueba quién los hizo.
4. **Guardianes existentes:** mantienen sus controles de intención, autoridad, alcance, capacidad, seguridad, concurrencia, evidencia, calidad, recuperación y continuidad.
5. **Revisión 9+1:** nueve evaluaciones primarias y un décimo revisor adversarial independiente. El décimo puede elevar a cuarentena aunque las nueve ramas estén limpias; no puede anular una denegación de política.
6. **Ross Boost:** peso adicional a una señal adversarial respaldada por evidencia trazable; nunca convierte una sospecha en hecho.
7. **Respuesta acotada:** ALLOW, QUARANTINE, BLOCK. La cuarentena afecta la operación, identidad o recurso sospechoso; no destruye ni altera evidencia.
8. **Auditoría y recuperación:** eventos append-only, backups separados, revisión de sesiones/tokens y restauración verificada.

## 3. Correcciones al algoritmo de partida

- Las matrices aleatorias no representan actividad real de un atacante. La detección debe consumir eventos observables de repositorio, identidad, permisos, integridad, descargas y destinos.
- Semillas distintas no garantizan independencia. La décima revisión necesita separación de proceso, datos/criterios y credenciales.
- Monte Carlo sólo es válido con distribuciones empíricas y eventos etiquetados; no inventar probabilidades desde números uniformes.
- El score es un índice heurístico, no probabilidad calibrada hasta validación con incidentes etiquetados.
- El boost sólo pondera señales adversariales con evidencia; no reemplaza autenticación ni autorización.
- El factor ±0.5 se interpreta como banda de sensibilidad determinista sobre el delta configurable, nunca como ruido aleatorio en una decisión de seguridad.
- El rango 0.05–0.90 es un límite numérico de presentación, no una afirmación sobre la probabilidad real.
- No ocultar activaciones del registro del propietario/auditor. La vista externa puede ser mínima; la auditoría autorizada conserva motivos completos.

## 4. Límites de autoridad

El firewall no concede permisos, no elude autenticación y no modifica automáticamente roles, secretos, ramas protegidas, credenciales o archivos. Cambios de permisos, rotación, borrado, force-push, publicación externa y restauraciones destructivas requieren el procedimiento y autorización propios. Un score bajo nunca puede convertir una acción prohibida en permitida.

La implementación debe integrarse con controles reales del proveedor: protección de ramas, mínimo privilegio, PR/revisión/checks, 2FA, secret scanning y auditoría. Un script local no reemplaza esos controles.

## 5. Adaptadores por proyecto

- orquestador-central: política transversal, autoridad e inventario; no almacenar secretos.
- motor-u6-storage: adapter inicialmente de solo lectura; sus canónicos, reglas y datos siguen bajo su contrato local. No exportar restricciones U6 al contrato común.
- capcot-capsulas-imaginantes: separar material público, interno y restringido; proteger cola y preproducción no publicada.
- red-teaming-safety-u6: proteger planes, casos adversariales y hallazgos; separar datos de prueba de credenciales.
- agente-cero-costo: sandbox por defecto y secretos fuera del repositorio.
- Gabinete: implementación neutral, adaptadores y pruebas sintéticas; no copiar activos privados de los proyectos.

La clasificación anterior es propuesta; no constituye auditoría de permisos ni confirma rutas o accesos reales.

## 6. Estados de incidente

OBSERVED → SUSPECTED → QUARANTINED → CONFIRMED → RECOVERING → CLOSED.

No marcar CONFIRMED por una puntuación. Cada transición conserva fuente, tiempo, actor, recurso, acción y evidencia. Un falso positivo debe poder revertirse sin pérdida de datos.

## 7. Despliegue por etapas

1. Inventario/clasificación sin cambiar permisos.
2. Modo observación con fuentes de eventos identificadas.
3. Pruebas de integridad en archivos de prueba.
4. Cuarentena simulada y ejercicios de recuperación.
5. Piloto de enforcement en un único repositorio, tras revisión del propietario.
6. Adaptadores por repositorio con mínimo privilegio.

Criterios de salida: falsos positivos medidos, denegaciones probadas, recuperación demostrada, auditoría íntegra, permisos mínimos y aprobación del propietario. Unit tests sintéticos no equivalen a despliegue.

## 8. Prototipo y evidencia

El prototipo neutral está en el scaffold local de gabinete-de-herramientas, bajo tools/security-firewall/, con pruebas sintéticas. En la sesión actual pasaron 7/7 pruebas unitarias. No está conectado a eventos reales, GitHub, Dropbox, Notion, runners ni filesystem de producción. No está aplicando enforcement.