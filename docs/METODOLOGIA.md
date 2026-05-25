# GCDD — Governance-Constrained Driven Development

> Una metodología para construir software con agentes AI donde el governance organizacional, las políticas de seguridad y los estándares arquitectónicos se aplican *durante* la generación — no *después*.

---

## El Problema

Spec-Driven Development (SDD) resolvió la primera crisis de la ingeniería asistida por AI: el intent drift. Al escribir especificaciones antes del código, los equipos dejaron de generar software "plausible pero incorrecto".

Pero SDD tiene un punto ciego: **asume que la spec es suficiente**.

En industrias reguladas, entornos enterprise y cualquier organización con estándares de seguridad, convenciones de nombres, patrones arquitectónicos o requisitos de compliance, la spec captura *qué* construir — pero no *cómo debe cumplir*. El resultado:

- Los agentes AI generan código que pasa la validación de spec pero viola políticas de seguridad
- Las convenciones de nombres se ignoran porque el LLM no las conoce
- Los patrones arquitectónicos los elige la AI basándose en datos de entrenamiento, no en estándares organizacionales
- El compliance se valida *después* de generar el código, creando ciclos de retrabajo
- Se introducen vulnerabilidades de seguridad porque la AI no conoce el modelo de amenazas de la organización

**GCDD agrega la capa que falta: un Contrato de Governance que se ubica por encima de la spec y constrañe todo lo que está debajo.**

---

## ¿Qué es GCDD?

GCDD (Governance-Constrained Driven Development) es una metodología de desarrollo de software donde:

1. **Los contratos de governance** — no solo las specs — son la fuente de verdad principal
2. **Las restricciones se aplican durante la generación**, no se validan después
3. **El conocimiento de dominio se codifica en herramientas (tools)**, no en prompts
4. **Los agentes se especializan por responsabilidad**, no son de propósito general
5. **El compliance es estructural**, no conductual

La idea central: en SDD, la spec le dice a la AI *qué* construir. En GCDD, el contrato de governance le dice a la AI *qué no puede hacer*, *qué patrones debe seguir* y *qué estándares debe cumplir cada artefacto* — antes de que la spec siquiera se escriba.

---

## Cómo se diferencia GCDD de SDD

| Aspecto | SDD (Spec-Driven) | GCDD (Governance-Constrained) |
|---------|-------------------|-------------------------------|
| Fuente de verdad | La especificación | Contrato de governance + especificación |
| Cuándo se valida compliance | Después de generar código | Durante la generación |
| Conocimiento del agente | Propósito general + instrucciones en prompt | Tools domain-specific con reglas embebidas |
| Mecanismo de enforcement | Basado en prompt ("no hagas X") | Estructural (tools rechazan operaciones inválidas) |
| Decisiones de arquitectura | Las toma la AI desde datos de entrenamiento | Restringidas por catálogo organizacional |
| Seguridad | Validada post-hoc (linters, scanners) | Shift-left: embebida en la generación |
| Naming/convenciones | Descritas en docs, esperando que la AI las siga | Enforced por validadores, el agente no puede saltarlas |
| Alcance | Desarrollo de software | Cualquier artefacto: data products, APIs, apps, infra, docs |

---

## Conceptos Fundamentales

### 1. El Contrato de Governance

Un **Contrato de Governance** es un artefacto legible por máquina que define las reglas organizacionales que todo artefacto generado debe satisfacer. A diferencia de una constitución (que es recomendación), un contrato de governance es **enforceable** — los agentes físicamente no pueden violarlo porque las herramientas que usan rechazan operaciones no conformes.

Un contrato de governance contiene:

```
governance-contract.yaml
├── naming/              # Convenciones de nombres por tipo de recurso
│   ├── patterns         # Patrones regex o templates
│   ├── prefixes         # Prefijos requeridos por dominio
│   └── separators       # Separadores permitidos (-, _, .)
├── security/            # Políticas de seguridad
│   ├── policies         # SCPs, OPAs, o reglas equivalentes
│   ├── encryption       # Requisitos de encriptación
│   ├── auth             # Estándares de autenticación
│   └── owasp            # Reglas de compliance OWASP por categoría
├── architecture/        # Patrones arquitectónicos permitidos
│   ├── patterns         # ej: hexagonal, layered, event-driven
│   ├── selection_rules  # Cuándo usar cada patrón
│   └── constraints      # Qué está prohibido
├── domains/             # Estructura de dominios de negocio
│   ├── domain_map       # Dominios y subdominios válidos
│   └── ownership        # Quién es dueño de qué
├── tags/                # Metadata/tags requeridos por recurso
├── environments/        # Ambientes permitidos y sus restricciones
└── scanning/            # Escaneos de seguridad requeridos antes del deploy
    ├── sast             # Reglas de análisis estático
    ├── dast             # Triggers de análisis dinámico
    ├── dependency       # Políticas de vulnerabilidades en dependencias
    └── container        # Reglas de escaneo de imágenes de contenedor
```

**El contrato de governance no es documentación. Es código.** Los validadores, herramientas y agentes lo consumen directamente.

### 2. Generación Constrañida

En SDD, la AI genera código y después lo validas. En GCDD, la AI genera código **a través de herramientas que ya enforzan el contrato de governance**. La diferencia:

```
Flujo SDD:
  Spec → AI genera código → Linter detecta violaciones → Developer corrige → Repetir

Flujo GCDD:
  Contrato de Governance → Spec (constrañida) → AI genera a través de tools gobernados → Código es conforme por construcción
```

Esto se logra codificando las reglas de governance en las **herramientas** que usa el agente, no en los **prompts** que lee. Un agente al que le dices "no uses encriptación S3_MANAGED" en un prompt eventualmente ignorará esa instrucción. Un agente cuya herramienta `create_bucket` rechaza `S3_MANAGED` y retorna un error con la alternativa correcta **no puede** violar la regla.

### 3. Perfiles de Dominio

Un **Perfil de Dominio** es una implementación concreta de un contrato de governance para una industria o dominio tecnológico específico. GCDD es la metodología; los perfiles de dominio son cómo las organizaciones la adoptan.

Ejemplos:

| Perfil | Dominio | Governance Clave |
|--------|---------|-----------------|
| `gcdd-data-aws` | Ingeniería de Datos en AWS | Naming S3, encriptación KMS, versiones de Glue, validación de SCPs |
| `gcdd-api-rest` | Desarrollo de APIs REST | Compliance OpenAPI, OWASP API Top 10, rate limiting, estándares de auth |
| `gcdd-webapp-react` | Aplicaciones Web | Accesibilidad (WCAG), headers CSP, políticas de dependencias |
| `gcdd-mobile-ios` | Apps iOS | Guías de App Store, privacy manifest, validación de entitlements |
| `gcdd-infra-k8s` | Infraestructura Kubernetes | Pod security policies, network policies, límites de recursos |
| `gcdd-ml-pipeline` | Pipelines ML/AI | Governance de modelos, linaje de datos, detección de sesgo |
| `gcdd-fintech` | Servicios Financieros | PCI-DSS, controles SOX, audit trails de transacciones |
| `gcdd-healthcare` | Aplicaciones de Salud | HIPAA, manejo de PHI, gestión de consentimiento |

Las organizaciones pueden componer múltiples perfiles (ej: `gcdd-api-rest` + `gcdd-fintech` para una API bancaria).

### 4. Especialización de Agentes

GCDD define **roles**, no agentes. Un agente es una implementación; un rol es un límite de responsabilidad. La metodología requiere como mínimo:

| Rol | Responsabilidad | Tiene Acceso A |
|-----|----------------|----------------|
| **Navigator** | Orienta al usuario, rutea al rol correcto | Solo lectura: contrato de governance, mapa de dominios |
| **Specifier** | Captura requerimientos, crea especificaciones | Herramientas de validación de governance |
| **Builder** | Genera código/artefactos desde specs aprobadas | Herramientas de generación domain-specific (constrañidas) |
| **Guardian** | Valida seguridad y compliance | Herramientas de escaneo de seguridad, validadores de políticas |
| **Steward** | Valida governance, naming, estándares | Validadores de nombres, validadores de tags, scorecards |
| **Chronicler** | Genera documentación y audit trails | Acceso de lectura a todos los artefactos |
| **Orchestrator** | Rutea entre roles, enforce límites | Meta-nivel: puede invocar cualquier rol |

**Principio crítico: los roles se enforzan por acceso a herramientas, no por prompts.** El rol Builder no puede acceder a herramientas de escaneo de seguridad. El rol Guardian no puede acceder a herramientas de generación de código. Esto previene el problema del "agente servicial" donde un rol hace el trabajo de otro.

### 5. Las Tres Capas de Enforcement

GCDD requiere tres capas de enforcement, de más débil a más fuerte:

```
Capa 3: ESTRUCTURAL (más fuerte)
  Las herramientas rechazan operaciones no conformes a nivel de infraestructura.
  Ejemplo: create_bucket() rechaza encryption=S3_MANAGED, retorna error con la alternativa correcta.
  El agente NO PUEDE saltarse esto sin importar el prompt o la instrucción.

Capa 2: AUTORIZACIÓN DE HERRAMIENTAS
  Cada rol tiene una whitelist de herramientas que puede invocar.
  Ejemplo: Navigator puede llamar list_domains() pero no generate_code().
  El servidor MCP / router de herramientas rechaza llamadas no autorizadas.

Capa 1: PROMPT (más débil)
  La definición del rol incluye instrucciones y restricciones.
  Ejemplo: "Cuando te pidan generar código, responde: 'Eso lo hace Builder. Usa #builder.'"
  Útil para UX pero poco confiable como único mecanismo de enforcement.
```

**Las tres capas deben implementarse.** El enforcement solo por prompt falla ~20-30% del tiempo. La autorización de herramientas atrapa violaciones de límites de rol. El enforcement estructural atrapa violaciones de governance. Juntas, proveen defensa en profundidad.

---

## El Flujo GCDD

```
┌─────────────────────────────────────────────────────────────┐
│                 CONTRATO DE GOVERNANCE                      │
│  naming / seguridad / arquitectura / dominios / escaneo     │
│  ───────────────────────────────────────────────────────     │
│  Esto constrañe TODO lo que está abajo. Se carga antes      │
│  de escribir cualquier spec y se valida en cada etapa.      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  1. ORIENTAR                                                 │
│  Navigator identifica: ¿Qué dominio? ¿Qué tipo de           │
│  artefacto? ¿Qué perfil de dominio aplica? ¿Qué reglas      │
│  de governance se cargan?                                    │
│  Salida: Contexto cargado, usuario ruteado al Specifier      │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  2. ESPECIFICAR                                              │
│  Specifier captura requerimientos, constrañidos por          │
│  governance. La arquitectura se SELECCIONA (no se inventa)   │
│  basándose en el contexto.                                   │
│  Salida: requirements.md → design.md → tasks.md              │
│  Gate: Se requiere aprobación humana antes de continuar.     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  3. CONSTRUIR                                                │
│  Builder genera código/artefactos desde la spec aprobada.    │
│  Cada operación pasa por herramientas gobernadas que         │
│  enforzan:                                                   │
│  - Convenciones de nombres (auto-aplicadas, no manuales)     │
│  - Políticas de seguridad (encriptación, auth, mín. privil.) │
│  - Restricciones arquitectónicas (patrones, dependencias)    │
│  Salida: Código/artefactos conformes POR CONSTRUCCIÓN        │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  4. VALIDAR                                                  │
│  Guardian + Steward validan la salida:                       │
│  - Escaneo de seguridad (SAST, dependencias, OWASP)          │
│  - Scorecard de governance (naming, tags, dominios)          │
│  - Verificación de conformidad arquitectónica                │
│  Salida: Reporte de compliance. Bloquear o aprobar deploy.   │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  5. DOCUMENTAR                                               │
│  Chronicler genera:                                          │
│  - Documentación técnica (README, docs de API)               │
│  - Artefactos de compliance (audit trail, reporte governance)│
│  - Changelog y notas de deployment                           │
│  Salida: Documentación que satisface requisitos de auditoría │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  6. DESPLEGAR                                                │
│  El deployment solo procede si la validación pasó.           │
│  El contrato de governance se re-valida en tiempo de deploy. │
│  Salida: Artefacto desplegado + certificado de compliance    │
└──────────────────────────────────────────────────────────────┘
```

---

## Motor de Selección de Arquitectura

Una de las características únicas de GCDD: el agente no *inventa* una arquitectura — la **selecciona** de un catálogo gobernado basándose en las características de la especificación.

El contrato de governance define qué patrones arquitectónicos están disponibles y cuándo aplica cada uno:

```yaml
architecture:
  patterns:
    hexagonal:
      when:
        - "lógica de dominio compleja"
        - "múltiples integraciones externas"
        - "requiere aislamiento para testing"
      constraints:
        - "el core de dominio tiene cero dependencias de infraestructura"
        - "todo acceso externo a través de ports/adapters"
      recommended_for: ["APIs", "microservicios", "apps con dominio pesado"]

    event_driven:
      when:
        - "procesamiento asíncrono requerido"
        - "múltiples consumidores del mismo evento"
        - "consistencia eventual aceptable"
      constraints:
        - "los eventos son inmutables"
        - "los consumidores son idempotentes"
      recommended_for: ["pipelines de datos", "sistemas de notificación", "ETL"]

    layered:
      when:
        - "operaciones CRUD simples"
        - "equipo pequeño"
        - "time to market es crítico"
      constraints:
        - "máximo 4 capas"
        - "sin dependencias circulares entre capas"
      recommended_for: ["herramientas internas", "admin panels", "MVPs"]

    medallion:
      when:
        - "data product con etapas de transformación"
        - "flujo raw → limpio → agregado"
      constraints:
        - "cada capa tiene su propio storage"
        - "backfill desde raw siempre es posible"
      recommended_for: ["data lakes", "plataformas de analytics"]

  forbidden:
    - pattern: "monolito"
      when: "cantidad de servicios > 3 AND tamaño del equipo > 10"
      reason: "restricciones de escalamiento organizacional"
```

El rol Specifier usa este catálogo durante la fase de diseño: dados los requerimientos, evalúa qué patrones aplican y presenta la selección con razonamiento. El humano aprueba, y el Builder genera dentro de las restricciones del patrón seleccionado.

---

## Seguridad: OWASP y más allá

GCDD trata la seguridad como una preocupación de governance de primera clase, no como un paso extra al final:

```yaml
security:
  owasp:
    api_top_10:
      BOLA:  # Broken Object Level Authorization
        scan: "verificar auth a nivel de objeto en todos los endpoints"
        enforce: "todo acceso a recurso requiere validación de ownership"
        builder_constraint: "endpoints generados deben incluir middleware de auth"
      
      broken_auth:
        scan: "verificar auth en todos los endpoints"
        enforce: "ningún endpoint sin autenticación a menos que esté explícitamente whitelisted"
        builder_constraint: "decorador de auth obligatorio"

    web_top_10:
      injection:
        scan: "regla SAST para SQL/NoSQL/OS injection"
        enforce: "solo consultas parametrizadas"
        builder_constraint: "nunca generar concatenación de strings para queries"
      
      xss:
        scan: "regla SAST para XSS reflejado/almacenado"
        enforce: "encoding de salida en toda data controlada por usuario"
        builder_constraint: "middleware de sanitización auto-incluido"

  scanning:
    pre_commit:
      - "SAST (semgrep/bandit/eslint-security)"
      - "verificación de vulnerabilidades en dependencias (npm audit/pip-audit/trivy)"
      - "detección de secretos (gitleaks/trufflehog)"
    
    pre_deploy:
      - "escaneo de imagen de contenedor (trivy/grype)"
      - "escaneo de seguridad IaC (checkov/tfsec)"
      - "DAST en staging (OWASP ZAP)"
    
    post_deploy:
      - "protección en runtime (RASP/reglas WAF)"
      - "calendario de penetration testing"
```

El rol Guardian tiene acceso a herramientas de escaneo y valida contra estas reglas. El rol Builder genera código que ya sigue el `builder_constraint` de cada categoría.

---

## Implementando GCDD

### Para Claude Code / Claude Skills

```
.claude/
├── CLAUDE.md                      # Constitución GCDD
├── governance/
│   ├── governance-contract.yaml   # El contrato de governance
│   ├── profiles/
│   │   ├── data-aws.yaml          # Perfil de dominio
│   │   └── api-rest.yaml          # Perfiles componibles
│   └── validators/
│       ├── naming.py              # Lógica de validación de nombres
│       ├── security.py            # Validadores de políticas de seguridad
│       └── architecture.py        # Conformidad arquitectónica
├── skills/
│   ├── navigator.md               # Rol: orientar y rutear
│   ├── specifier.md               # Rol: capturar requerimientos
│   ├── builder.md                 # Rol: generar artefactos
│   ├── guardian.md                # Rol: validación de seguridad
│   ├── steward.md                 # Rol: validación de governance
│   └── chronicler.md             # Rol: documentación
└── tools/
    ├── governed_tools.py          # Herramientas con governance embebido
    └── mcp_server.py             # Servidor MCP exponiendo herramientas gobernadas
```

### Para Kiro (AWS IDE)

```
.kiro/
├── steering/
│   ├── agent-navigator.md         # Steering file por rol
│   ├── agent-specifier.md
│   ├── agent-builder.md
│   ├── agent-guardian.md
│   ├── agent-steward.md
│   └── agent-chronicler.md
├── hooks/
│   ├── validate-post-task.json    # Hooks para validación automática
│   └── approve-spec-phase.json
├── specs/                          # Artefactos de spec viven aquí
└── mcp-server/
    └── gcdd_server.py             # Servidor MCP con herramientas gobernadas
```

### Para Cursor / VS Code

```
.cursor/
├── rules/
│   ├── gcdd-constitution.md       # Equivalente a .cursorrules
│   └── role-definitions.md
├── governance/
│   └── governance-contract.yaml
└── mcp/
    └── gcdd_server.py             # Servidor MCP para herramientas gobernadas
```

### Para GitHub Copilot

```
.github/
├── copilot/
│   └── AGENTS.md                  # Constitución GCDD en formato Copilot
├── governance/
│   └── governance-contract.yaml
└── workflows/
    └── gcdd-validate.yml          # Validación de governance en CI/CD
```

---

## Niveles de Ceremonia

No todo cambio necesita el flujo GCDD completo. La metodología define tres niveles:

### Quick (Bug fixes, cambios menores)
- Saltar Orientar y Especificar
- Builder genera dentro de las restricciones de governance
- Steward valida automáticamente
- Sin gate de aprobación humana

### Standard (Features, componentes nuevos)
- Flujo completo: Orientar → Especificar → Construir → Validar → Documentar
- Aprobación humana en fase de spec
- Guardian valida seguridad
- Documentación completa

### Enterprise (Regulado, requiere auditoría)
- Flujo completo con gates adicionales
- Certificado de compliance requerido
- Audit trail generado en cada paso
- Múltiples aprobaciones humanas (spec + seguridad + governance)
- Deployment requiere reporte de compliance firmado

---

## Cómo Empezar

### 1. Define tu contrato de governance

Empieza con lo que ya enforzan manualmente: convenciones de nombres, políticas de seguridad, tags requeridos, patrones prohibidos. Escríbelos como YAML.

### 2. Construye herramientas gobernadas

Para cada operación que tus agentes realizan (crear un recurso, generar código, desplegar), envuélvela en una herramienta que valide contra el contrato de governance. La herramienta debe rechazar operaciones no conformes y retornar la alternativa correcta.

### 3. Define tus roles

Mapea el flujo de trabajo de tu equipo a roles GCDD. No necesitas los siete — empieza con Specifier + Builder + Steward y agrega según necesites.

### 4. Implementa las capas de enforcement

Empieza con la Capa 3 (estructural — herramientas gobernadas). Agrega la Capa 2 (autorización de herramientas) cuando tengas múltiples roles. La Capa 1 (prompt) es gratis — son tus definiciones de rol.

### 5. Mide

Rastrea: violaciones atrapadas en cada capa, tiempo de spec a deploy, ciclos de retrabajo, tasa de compliance al primer intento.

---

## Origen

GCDD surgió de experiencia real en producción construyendo sistemas de desarrollo asistido por AI en entornos enterprise regulados. Los patrones — contratos de governance, generación constrañida, especialización de agentes por acceso a herramientas, enforcement de tres capas — se descubrieron resolviendo problemas reales: convenciones de nombres conflictivas, políticas de seguridad obligatorias, compliance shift-left y el problema del "agente servicial" donde los LLMs ignoran los límites de rol a pesar de instrucciones explícitas.

La metodología fue diseñada para ser agnóstica de dominio y agnóstica de IDE desde el inicio, aplicable a cualquier organización que necesite desarrollo asistido por AI con garantías de governance — ya sea construyendo pipelines de datos, APIs REST, aplicaciones web, apps móviles o infraestructura.

---

## Contribuir

GCDD es una metodología abierta. Contribuciones bienvenidas:

- **Perfiles de Dominio**: Implementa contratos de governance para tu industria
- **Librerías de Herramientas**: Herramientas gobernadas para stacks tecnológicos específicos
- **Implementaciones de Agentes**: Implementaciones de roles para diferentes plataformas AI
- **Validación**: Datos empíricos sobre efectividad de enforcement
- **Documentación**: Guías, tutoriales, casos de estudio

---

## Licencia

MIT

---

## Referencias

- Spec-Driven Development: From Code to Contract in the Age of AI (arXiv, 2026)
- Constitutional SDD (arXiv, 2026)
- BMAD-METHOD: Breakthrough Method for Agile AI-Driven Development
- GitHub Spec Kit
- ThoughtWorks Technology Radar, Volume 33 (2025)
