# Contrato de Governance — Estructura Completa

## Qué es

El contrato de governance es un archivo YAML que define TODAS las reglas organizacionales
que constrañen la generación de código. No es documentación — es código que los validadores
y herramientas consumen directamente.

## Estructura

```yaml
version: "1.0.0"
profile: "nombre-del-perfil"
description: "Descripción del perfil"
```

## Secciones

### naming — Convenciones de Nombres

Define cómo debe llamarse cada tipo de recurso.

```yaml
naming:
  global:
    separator: "-"          # Separador principal
    case: "kebab-case"      # Case global: kebab-case, snake_case, UPPER_CASE
    max_length: 63          # Longitud máxima
    prefix: "miorg"         # Prefijo obligatorio

  resources:
    s3_bucket:
      pattern: "{prefix}-{dominio}-{proposito}-{ambiente}"
      example: "miorg-pagos-raw-dev"
      validators:
        - "sin_mayusculas"
        - "sin_underscores"
        - "empieza_con_prefijo"

    api_endpoint:
      pattern: "/api/v{version}/{dominio}/{recurso}"
      example: "/api/v1/pagos/transacciones"
      validators:
        - "kebab_case"
        - "recursos_pluralizados"
        - "versionado"

    database_table:
      pattern: "{dominio}_{entidad}_{proposito}"
      example: "pagos_transacciones_historial"

    iam_role:
      pattern: "{PREFIX}-ROLE-{DOMINIO}-{SERVICIO}-{ENV}"
      example: "MIORG-ROLE-PAGOS-LAMBDA-DEV"

    lambda_function:
      pattern: "{prefix}-{dominio}-{accion}-{ambiente}"
      example: "miorg-pagos-procesar-dev"

    container_image:
      pattern: "{registry}/{dominio}/{servicio}:{version}"
      example: "ecr.miorg.com/pagos/procesador:1.2.3"
      validators:
        - "tag_semver"
        - "sin_latest_en_prod"
```

Cuando una organización tiene dos convenciones coexistentes (ej: una para datos y otra para
infra), se definen como variantes:

```yaml
naming:
  variants:
    data:
      separator: "_"
      case: "snake_case"
      pattern: "job_{dominio}_{subdominio}_{accion}_{ambiente}"
    infra:
      separator: "-"
      case: "UPPER_CASE"
      pattern: "{ORG}-{TIPO}-{DOMINIO}-{SERVICIO}-{AMBIENTE}"
```

### security — Políticas de Seguridad

```yaml
security:
  encryption:
    at_rest: "requerido"
    in_transit: "requerido"
    key_management: "customer-managed"
    forbidden:
      - "S3_MANAGED"
      - "AES256_DEFAULT"
    required:
      - "KMS_CMK"
      - "TLS_1_2_MINIMUM"

  authentication:
    public_endpoints: "prohibido"
    allowed_methods: ["OAuth2", "OIDC", "mTLS", "API_KEY_WITH_IAM"]
    mfa_required_for: ["acceso_prod", "operaciones_admin"]
    session_timeout_minutes: 30

  authorization:
    model: "RBAC"
    least_privilege: true
    wildcard_permissions: "prohibido"
    admin_access: "prohibido_en_codigo"
    service_accounts:
      require_rotation: true
      max_key_age_days: 90

  network:
    public_ip: "prohibido"
    vpc_required: true
    security_groups:
      no_open_ingress: true
      no_open_egress: false
```

### architecture — Patrones Arquitectónicos

```yaml
architecture:
  patterns:
    hexagonal:
      aliases: ["ports-and-adapters", "clean-architecture"]
      when:
        - "lógica de dominio compleja con múltiples reglas de negocio"
        - "3+ integraciones externas"
        - "testing es prioridad"
      constraints:
        - "core de dominio tiene CERO imports de infraestructura"
        - "todo acceso externo a través de ports (interfaces)"
        - "adapters implementan ports, nunca se llaman directamente"
      structure:
        - "src/{dominio}/core/"
        - "src/{dominio}/ports/"
        - "src/{dominio}/adapters/"
        - "src/{dominio}/app/"

    event_driven:
      when:
        - "procesamiento asíncrono"
        - "múltiples consumidores del mismo evento"
        - "consistencia eventual aceptable"
      constraints:
        - "eventos son inmutables"
        - "consumidores son idempotentes"
        - "dead letter queue por consumidor"

    layered:
      when:
        - "CRUD simple"
        - "equipo pequeño"
        - "MVP o prototipo"
      constraints:
        - "máximo 4 capas"
        - "sin dependencias circulares"

    medallion:
      when:
        - "data product con transformaciones"
        - "flujo raw → limpio → agregado"
      constraints:
        - "cada capa tiene su propio storage"
        - "raw es append-only"
        - "backfill siempre posible"

    serverless:
      when:
        - "carga variable/impredecible"
        - "optimización de costos"
      constraints:
        - "funciones < 15 minutos"
        - "stateless"
        - "idempotente"

  forbidden:
    - pattern: "monolito"
      when: "servicios > 3 AND equipo > 10"
      reason: "escalamiento organizacional"
    - pattern: "base_de_datos_compartida"
      when: "servicios > 1"
      reason: "acoplamiento"
```

### domains — Estructura de Dominios

```yaml
domains:
  pagos:
    description: "Procesamiento de pagos y transacciones"
    subdomains: ["transacciones", "reembolsos", "liquidaciones"]
    owner: "equipo-pagos"
    data_classification: "confidencial"

  clientes:
    description: "Gestión de clientes y perfiles"
    subdomains: ["perfiles", "preferencias", "lealtad"]
    owner: "equipo-clientes"
    data_classification: "pii"
```

### tags — Metadata Requerido

```yaml
tags:
  required:
    - key: "proyecto"
    - key: "dominio"
    - key: "ambiente"
    - key: "owner"
    - key: "centro-costo"
    - key: "clasificacion-datos"
      allowed_values: ["publico", "interno", "confidencial", "pii", "restringido"]
```

### environments — Ambientes

```yaml
environments:
  allowed: ["dev", "staging", "prod"]
  constraints:
    dev:
      regions: ["us-east-1", "us-west-2"]
      auto_deploy: true
      approval_required: false
    prod:
      regions: ["us-east-1"]
      auto_deploy: false
      approval_required: true
      approvers: ["tech-lead", "equipo-seguridad"]
      requires_compliance_report: true
```

### scanning — Escaneos de Seguridad

```yaml
scanning:
  pre_commit:
    required:
      - tool: "semgrep"
        config: "p/owasp-top-ten"
        fail_on: "error"
      - tool: "gitleaks"
        fail_on: "any"
      - tool: "pip-audit"
        fail_on: "high"

  pre_deploy:
    required:
      - tool: "trivy"
        target: "imágenes de contenedor"
        fail_on: "critical"
      - tool: "checkov"
        target: "templates IaC"
        fail_on: "high"

  post_deploy:
    recommended:
      - tool: "owasp-zap"
        target: "endpoints staging"
        schedule: "semanal"
```

### deployment — Políticas de Despliegue

```yaml
deployment:
  strategy:
    default: "blue-green"
    allowed: ["blue-green", "canary", "rolling"]
    forbidden: ["big-bang"]
  rollback:
    automatic: true
    trigger: "error_rate > 5% OR latency_p99 > 2s"
  compliance:
    require_report_before_deploy: true
    require_all_scans_passed: true
    require_documentation_updated: true
```
