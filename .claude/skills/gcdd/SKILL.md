---
name: gcdd
description: >
  Governance-Constrained Driven Development (GCDD). Usa este skill cuando el usuario
  necesite construir cualquier proyecto de software con governance, compliance o estándares
  organizacionales. Aplica para data pipelines, APIs REST, aplicaciones web, apps móviles,
  infraestructura como código, microservicios o cualquier artefacto técnico que deba cumplir
  con reglas de seguridad, convenciones de nombres, patrones de arquitectura, políticas de
  escaneo o estándares corporativos. También se activa cuando el usuario menciona: governance,
  compliance, naming conventions, SCPs, OWASP, shift-left security, architecture patterns,
  governance contract, security policies, o cuando pide que el código generado cumpla con
  estándares desde el inicio. Úsalo incluso si el usuario no menciona GCDD explícitamente —
  si hay reglas organizacionales que enforcar, este skill aplica.
---

# GCDD — Governance-Constrained Driven Development

GCDD es una metodología donde el governance organizacional, las políticas de seguridad y los
estándares arquitectónicos se aplican *durante* la generación de código — no *después*.

La idea central: SDD (Spec-Driven Development) le dice a la AI *qué* construir. GCDD le dice
a la AI *qué no puede hacer*, *qué patrones debe seguir* y *qué estándares debe cumplir cada
artefacto* — antes de escribir la primera línea de código.

## Cuándo usar este skill

- El usuario quiere construir un proyecto que debe cumplir reglas organizacionales
- Hay convenciones de nombres que respetar
- Hay políticas de seguridad (SCPs, OWASP, encriptación, auth)
- Hay patrones de arquitectura que la organización requiere
- Se necesita compliance verificable antes del deployment
- El usuario quiere generar un contrato de governance para su organización
- El usuario quiere configurar roles de agentes con enforcement real

## Los 5 conceptos fundamentales

### 1. Contrato de Governance
Un artefacto YAML legible por máquina que define TODAS las reglas organizacionales. No es
documentación — es código que los validadores y herramientas consumen directamente.

Contiene: naming, security, architecture, domains, tags, environments, scanning, deployment.

Lee `references/governance-contract.md` (en el directorio del skill) para la estructura completa
y ejemplos.

### 2. Generación Constrañida
Las restricciones se codifican en las **herramientas**, no en los **prompts**. Un agente al
que le dices "no hagas X" en un prompt ignorará la instrucción ~20-30% del tiempo. Una
herramienta que rechaza la operación y retorna la alternativa correcta nunca falla.

```
Flujo SDD:  Spec → AI genera → Linter detecta violaciones → Developer corrige → Repetir
Flujo GCDD: Governance → Spec → AI genera a través de tools gobernados → Conforme por construcción
```

### 3. Perfiles de Dominio
Implementaciones concretas del contrato de governance para industrias o tecnologías específicas.
GCDD es la metodología; los perfiles son cómo se adopta.

Los perfiles se encuentran en `profiles/` en la raíz del proyecto (no en el directorio del skill).
Un perfil ✅ está completo y listo para usar. Un perfil 🚧 es un stub — úsalo como punto de partida pero completar las secciones faltantes.

**Perfiles disponibles (✅ completos):**
- `profiles/data-azure.yaml` — Ingeniería de datos en Azure (ADLS Gen2, ADF, Synapse, Databricks)
- `profiles/data-gcp.yaml` — Ingeniería de datos en GCP (BigQuery, GCS, Pub/Sub, Dataflow)
- `profiles/infra-terraform.yaml` — Infraestructura como código Terraform (multi-cloud AWS/GCP/Azure)

**Perfiles en desarrollo (🚧 stubs, contribuciones bienvenidas):**
- `profiles/data-aws.yaml` — Ingeniería de datos en AWS (S3, Glue, Step Functions)
- `profiles/api-rest.yaml` — APIs REST con OWASP API Top 10
- `profiles/webapp-react.yaml` — Aplicaciones web React
- `profiles/infra-k8s.yaml` — Infraestructura Kubernetes
- `profiles/fintech.yaml` — Fintech (PCI-DSS, cumplimiento financiero)
- `profiles/healthcare.yaml` — Salud (HIPAA, PHI)

### 4. Especialización de Agentes por Acceso a Herramientas
Cada rol tiene una whitelist de herramientas. El enforcement es por infraestructura (el
servidor MCP rechaza llamadas no autorizadas), no por prompt.

| Rol | Responsabilidad | Acceso |
|-----|----------------|--------|
| Navigator | Orienta, rutea | Solo lectura: governance, dominios |
| Specifier | Captura requerimientos | Validación de governance |
| Builder | Genera código/artefactos | Tools de generación (constrañidos) |
| Guardian | Valida seguridad | Escaneo, validadores de políticas |
| Steward | Valida governance | Naming, tags, scorecards |
| Chronicler | Documenta | Lectura de todos los artefactos |
| Orchestrator | Rutea, enforce límites | Meta-nivel |

### 5. Tres Capas de Enforcement

```
Capa 3 — ESTRUCTURAL (más fuerte)
  Las herramientas rechazan operaciones no conformes.
  El agente NO PUEDE saltarse esto.

Capa 2 — AUTORIZACIÓN DE HERRAMIENTAS
  Cada rol tiene whitelist de tools.
  El servidor MCP rechaza llamadas no autorizadas.

Capa 1 — PROMPT (más débil)
  Instrucciones y restricciones en la definición del rol.
  Útil para UX pero insuficiente como único mecanismo.
```

Las tres capas deben implementarse. Prompt solo falla ~20-30% del tiempo.

## El Flujo GCDD

```
CONTRATO DE GOVERNANCE (constrañe todo)
         │
         ▼
1. ORIENTAR — Navigator identifica dominio, perfil, reglas
         │
         ▼
2. ESPECIFICAR — Specifier captura requerimientos dentro de governance
   Arquitectura se SELECCIONA de catálogo gobernado, no se inventa
   Salida: requirements.md → design.md → tasks.md
   Gate: Aprobación humana
         │
         ▼
3. CONSTRUIR — Builder genera a través de tools gobernados
   Naming auto-aplicado, seguridad embebida, arquitectura constrañida
   Salida: Código conforme POR CONSTRUCCIÓN
         │
         ▼
4. VALIDAR — Guardian + Steward validan
   SAST, dependencias, OWASP, scorecard governance
   Salida: Reporte de compliance
         │
         ▼
5. DOCUMENTAR — Chronicler genera docs + audit trail
         │
         ▼
6. DESPLEGAR — Solo si validación pasó + certificado de compliance
```

## Niveles de Ceremonia

No todo cambio necesita el flujo completo:

**Quick** (bugs, cambios menores): Builder genera → Steward valida automáticamente. Sin gates.

**Standard** (features nuevas): Flujo completo con aprobación humana en spec.

**Enterprise** (regulado, auditoría): Flujo completo + gates adicionales + certificado de
compliance + audit trail + múltiples aprobaciones.

## Motor de Selección de Arquitectura

El agente NO inventa una arquitectura — la selecciona de un catálogo gobernado según las
características del proyecto. Lee `references/architecture-catalog.md` (en el directorio del skill)
para el catálogo completo con reglas de selección.

Resumen rápido:
- **Hexagonal** → lógica de dominio compleja, 3+ integraciones, testing prioritario
- **Event-driven** → procesamiento asíncrono, múltiples consumidores
- **Layered** → CRUD simple, equipo pequeño, MVP
- **Medallion** → data products con etapas de transformación
- **Serverless** → carga variable, optimización de costos

## Seguridad: OWASP y más allá

GCDD trata seguridad como governance de primera clase. Lee `references/security-policies.md`
(en el directorio del skill) para las reglas completas de OWASP API Top 10, Web Top 10, y
políticas de escaneo.

Principio central: el Builder genera código que ya sigue el `builder_constraint` de cada
categoría OWASP. No se genera y después se escanea — se genera conforme desde el inicio.

## Implementación

Lee `references/implementation-guide.md` para guías específicas por plataforma:
- Claude Code / Claude Skills
- Kiro (AWS IDE)
- Cursor / VS Code
- GitHub Copilot

## Protocolo de Comportamiento de Claude

Esta sección es la guía operativa. Todo lo anterior es la teoría — aquí está lo que Claude
hace en la práctica cuando este skill está activo.

### Paso 0: Detectar el contexto (siempre, al inicio de cualquier tarea)

1. Buscar `.gcdd/governance/contract.yaml` en la raíz del proyecto
2. Si existe → leerlo COMPLETO antes de generar cualquier artefacto
3. Si NO existe → ver "Modo: Proyecto Nuevo" más abajo

### Modo: Proyecto Nuevo (sin contrato de governance)

Cuando no existe `.gcdd/governance/contract.yaml`:

1. Preguntar al usuario: "Este proyecto no tiene un contrato de governance GCDD. ¿Quieres que lo configure?"
2. Detectar el dominio (preguntar si no es obvio por el código existente)
3. Recomendar el perfil ✅ completo de `profiles/` más adecuado; si ninguno aplica, usar la
   plantilla en `templates/governance-contract.yaml`
4. Crear `.gcdd/governance/contract.yaml` personalizado
5. Crear o actualizar `CLAUDE.md` en la raíz con las reglas de governance
6. Informar al usuario qué se creó y qué secciones debe revisar/personalizar

### Modo: Proyecto Existente (con contrato de governance)

En cada tarea de generación de código:

**Antes de generar:**
- Leer la sección relevante del contrato: `naming`, `security`, `architecture`
- Si es una feature nueva → confirmar con el usuario qué patrón de arquitectura aplica (seleccionar
  del catálogo, no inventar)

**Al generar cada artefacto:**
- Aplicar el `naming` pattern del contrato para cada tipo de recurso
- Incluir los `tags`/`labels` requeridos en todos los recursos
- Aplicar las `security` constraints del perfil (encriptación, auth, network)
- Si el perfil tiene `builder_constraints.always_include` → incluirlos
- Nunca generar lo que esté en `builder_constraints.never_generate`

**Al finalizar la tarea — Checklist de Compliance:**
Antes de declarar cualquier tarea completada, verificar explícitamente:
- [ ] Nombres de recursos siguen el patrón del contrato (`naming.resources`)
- [ ] Todos los recursos tienen los tags/labels requeridos (`tags.required`)
- [ ] Sin credenciales hardcodeadas (secrets, keys, tokens, passwords)
- [ ] Configuraciones de seguridad cumplen constraints del perfil
- [ ] Arquitectura sigue el patrón seleccionado
- [ ] Listar los escaneos que el usuario debe ejecutar manualmente (de `scanning.pre_commit`)

### Modo: Agente Único (Claude Code sin multi-agente)

La mayoría de usuarios usa Claude Code como agente único. En este modo, Claude asume
secuencialmente todos los roles en cada tarea:

| Momento | Rol que asume | Qué hace |
|---------|--------------|----------|
| Inicio de tarea | Navigator | Lee el contrato, identifica qué reglas aplican |
| Antes de implementar | Specifier | Confirma arquitectura si es feature nueva |
| Durante implementación | Builder | Genera código conforme por construcción |
| Al terminar | Steward | Verifica naming y tags |
| Al terminar | Guardian | Lista escaneos pendientes que el usuario debe correr |

No intentar configurar un servidor MCP ni multi-agente a menos que el usuario lo pida
explícitamente. El valor de GCDD se obtiene incluso con Claude como agente único.

---

## Comenzar un proyecto con GCDD

Cuando el usuario quiera iniciar un proyecto con GCDD:

1. **Seleccionar perfil**: Si existe un perfil ✅ completo en `profiles/` que aplique al dominio del
   usuario, úsalo directamente — ya tiene naming, seguridad y escaneo definidos. Si no existe un
   perfil completo, usa la plantilla en `templates/governance-contract.yaml` (dentro del directorio
   del skill) como punto de partida y pregunta al usuario sobre su dominio, naming y seguridad.

2. **Crear el governance-contract**: Genera `.gcdd/governance/contract.yaml` en la raíz del
   proyecto del usuario, personalizado con el perfil o plantilla del paso anterior.

3. Crea `CLAUDE.md` en la raíz del proyecto referenciando el contrato.
4. Genera los validadores iniciales (`.gcdd/validators/naming.py`, `security.py`) si el usuario los necesita.
5. Define los roles necesarios (mínimo: Specifier + Builder + Steward) solo si se requiere multi-agente.
6. Configura las capas de enforcement según la guía en `references/implementation-guide.md`.
