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

Lee `references/governance-contract.md` para la estructura completa y ejemplos.

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

Perfiles disponibles en `references/profiles/`:
- `data-aws.md` — Ingeniería de datos en AWS
- `api-rest.md` — APIs REST con OWASP
- `webapp-react.md` — Aplicaciones web React
- `infra-k8s.md` — Infraestructura Kubernetes

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
características del proyecto. Lee `references/architecture-catalog.md` para el catálogo
completo con reglas de selección.

Resumen rápido:
- **Hexagonal** → lógica de dominio compleja, 3+ integraciones, testing prioritario
- **Event-driven** → procesamiento asíncrono, múltiples consumidores
- **Layered** → CRUD simple, equipo pequeño, MVP
- **Medallion** → data products con etapas de transformación
- **Serverless** → carga variable, optimización de costos

## Seguridad: OWASP y más allá

GCDD trata seguridad como governance de primera clase. Lee `references/security-policies.md`
para las reglas completas de OWASP API Top 10, Web Top 10, y políticas de escaneo.

Principio central: el Builder genera código que ya sigue el `builder_constraint` de cada
categoría OWASP. No se genera y después se escanea — se genera conforme desde el inicio.

## Implementación

Lee `references/implementation-guide.md` para guías específicas por plataforma:
- Claude Code / Claude Skills
- Kiro (AWS IDE)
- Cursor / VS Code
- GitHub Copilot

## Comenzar un proyecto con GCDD

Cuando el usuario quiera iniciar un proyecto con GCDD:

1. Genera `governance-contract.yaml` usando la plantilla en `templates/governance-contract.yaml`
   Pregunta al usuario sobre su dominio, naming, seguridad, arquitectura preferida
2. Crea la constitución del proyecto (CLAUDE.md, .cursorrules, etc.)
3. Genera los validadores iniciales (naming.py, security.py)
4. Define los roles necesarios (mínimo: Specifier + Builder + Steward)
5. Configura las capas de enforcement
