# ARCHETYPE-SEQUENTIAL-VERIFIABLE-v1
**Identificador:** `sequential-verifiable-v1`  
**Versión:** 1.0  
**Tipo:** arquetipo de familia de trabajo; activación explícita  
**Estado:** especificación; no implica ejecución automática.

## 1. Propósito y alcance
Define una familia de trabajos que recibe una entrada estructurada X, ejecuta pasos ordenados con evidencia y produce una salida Y verificable mecánicamente. No es un arquetipo universal ni una política obligatoria para todos los repositorios.

## 2. Condiciones de pertenencia
Deben cumplirse las tres:
- **Semántica:** existen X estructurado, Y objetivo y transformación por pasos.
- **Productiva:** los pasos tienen orden, cada uno deja evidencia y dispone de verificación mecánica.
- **Actancial:** creación de X, ejecución y validación final están separadas por roles o procesos identificables. El contrato puede permitir que un mismo sistema aloje roles distintos, pero debe demostrar la separación.

## 3. Exclusiones
No aplica a conversación libre, exploración abierta, trabajo improvisado, salidas juzgadas principalmente por gusto u opinión, procesos sin orden definido o resultados que no puedan verificarse por código.

## 4. Activación explícita
Se activa solo cuando el artefacto declara una marca reconocida:
- Markdown / SKILL: frontmatter YAML con `archetype: sequential-verifiable-v1`.
- JSON: `$schema` que identifica el esquema de esta familia y `_contract: SEQUENTIAL-VERIFIABLE-v1`.
- Texto/script: `@archetype: sequential-verifiable-v1` y `@contract: SEQUENTIAL-VERIFIABLE-v1`.

Sin marca, no aplica. No activar por nombre de archivo, carpeta, contenido parecido ni inferencia.

**La marca identifica el contrato; no ejecuta nada por sí sola.** Para que produzca efecto, el runner, pipeline o validador debe reconocerla, cargar el esquema, comprobar la entrada y aplicar el flujo. Si no existe ese componente, el artefacto está marcado pero la ejecución automática sigue **NO_IMPLEMENTADA**.

## 5. Autoridad y precedencia
1. Reglas locales del proyecto para sus datos, entorno, seguridad y archivos protegidos.
2. Contrato transversal del coordinador, en lo que sea compatible.
3. Este arquetipo, solo para el artefacto marcado.
4. Configuración de una ejecución concreta, sin poder anular las capas anteriores.

El arquetipo no obliga a un proyecto a adoptarlo. El proyecto decide marcar los artefactos elegibles y documenta adaptadores o excepciones locales. Una marca no concede permisos ni altera la autoridad de los repositorios.

## 6. Contrato mínimo de X
Campos obligatorios:
- `_contract`: `SEQUENTIAL-VERIFIABLE-v1`.
- `id`, `project`, `version`: identificadores no vacíos.
- `steps`: lista ordenada no vacía. Cada paso contiene `name`, `action`, `expected`, `verify`.
- `expected_output`: tipo, ruta y mínimos de salida.

El esquema normativo está en `../schemas/sequential-verifiable-v1.schema.json`.

## 7. Design by Contract
### Precondiciones
- X existe y es JSON válido.
- X cumple el esquema y declara la marca de activación.
- Las entradas referenciadas existen y son accesibles.
- Los pasos tienen acciones permitidas, criterios esperados y verificadores disponibles.
- El ejecutor tiene permisos y límites suficientes.

### Ejecución
- Ejecutar los pasos en el orden declarado.
- Registrar entrada, salida, tiempo, estado y evidencia por paso.
- No liberar el paso siguiente hasta que la verificación del anterior pase.
- Ante fallo, detener la cadena dependiente y reportar el primer paso fallido.
- Reanudar desde el paso fallido solo si el paso es seguro para reintentar y el contrato lo permite; no reiniciar todo por defecto.

### Postcondiciones
- Y existe en la ruta declarada.
- Y satisface tipo, cantidad, longitud y criterios adicionales definidos.
- Un validador mecánico independiente del generador comprueba la salida.
- Se conserva un recibo de ejecución reproducible.

## 8. Separación de responsabilidades
- **Autor de X:** prepara la especificación de entrada.
- **Runner:** ejecuta las acciones autorizadas.
- **Verificador:** ejecuta checks deterministas y produce PASS/FAIL.
- **LLM:** puede preparar, transformar o explicar X y ayudar a diagnosticar; no declara válido Y basándose solo en su propia lectura o afirmación.
- **Auditor:** revisa evidencia y separación de funciones cuando el riesgo lo requiera.

La separación debe ser observable; no basta con asignar nombres distintos a funciones que en realidad comparten el mismo resultado no verificado.

## 9. Regla de cierre
Si falla un paso, el reporte identifica ese paso, su evidencia y las dependencias detenidas. No se repite todo por defecto. La ejecución solo se declara completa cuando el verificador final pasa.

## 10. Límites de esta versión
Esta especificación y el JSON Schema describen el contrato de entrada. No incluyen todavía un runner universal, un sistema de colas ni un motor automático de guardianes. Cada proyecto que adopte el arquetipo debe aportar o seleccionar esos componentes y demostrar su integración.
