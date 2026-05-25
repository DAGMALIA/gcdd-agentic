# Catálogo de Arquitectura GCDD

## Principio

El agente NO inventa una arquitectura. La SELECCIONA de este catálogo basándose en las
características del proyecto. El humano aprueba la selección.

## Reglas de Selección

Evalúa las características del proyecto contra los criterios `when` de cada patrón.
Presenta al usuario los patrones que aplican, con razonamiento, y deja que elija.

---

## Patrones Disponibles

### Hexagonal (Ports & Adapters)

**Cuándo usarla:**
- Lógica de dominio compleja con múltiples reglas de negocio
- 3 o más integraciones externas (bases de datos, APIs, colas, caches)
- Testing es prioridad (se necesita aislar el dominio de la infra)
- Producto de vida larga (>2 años esperados)

**Restricciones obligatorias:**
- El módulo core de dominio tiene CERO imports de infraestructura
- Todo acceso externo se hace a través de ports (interfaces/clases abstractas)
- Los adapters implementan ports, nunca se llaman directamente desde el core
- Inyección de dependencias para todos los adapters

**Estructura de carpetas:**
```
src/{dominio}/
├── core/           # Entidades, value objects, servicios de dominio
│   ├── entities/
│   ├── services/
│   └── exceptions/
├── ports/          # Interfaces (clases abstractas)
│   ├── inbound/    # Casos de uso (lo que el mundo exterior puede pedir)
│   └── outbound/   # Repositorios, clientes externos (lo que el core necesita)
├── adapters/       # Implementaciones concretas
│   ├── inbound/    # Controllers, CLI, event handlers
│   └── outbound/   # PostgresRepo, S3Client, SQSPublisher
└── app/            # Configuración, inyección de dependencias, bootstrap
```

**Ideal para:** APIs REST con dominio rico, microservicios, aplicaciones enterprise.

---

### Event-Driven

**Cuándo usarla:**
- Procesamiento asíncrono requerido
- Múltiples consumidores necesitan reaccionar al mismo evento
- Consistencia eventual es aceptable
- Microservicios que necesitan estar desacoplados

**Restricciones obligatorias:**
- Los eventos son inmutables después de publicación
- Los consumidores deben ser idempotentes
- Dead letter queue requerida para cada consumidor
- Versionado de schema de eventos requerido
- Orden de eventos garantizado solo dentro de la misma partition key

**Estructura de carpetas:**
```
src/
├── events/
│   ├── schemas/      # Definiciones de eventos (JSON Schema / Avro)
│   ├── producers/    # Publicadores de eventos
│   └── consumers/    # Handlers de eventos
├── domain/           # Lógica de negocio
├── infrastructure/
│   ├── messaging/    # SQS, Kafka, EventBridge adapters
│   └── storage/      # Persistencia
└── dlq/              # Dead letter queue handlers
```

**Ideal para:** Pipelines de datos, sistemas de notificación, ETL, integración entre servicios.

---

### Layered (Capas)

**Cuándo usarla:**
- Operaciones CRUD simples
- Equipo pequeño (<5 desarrolladores)
- Time to market es crítico
- Prototipo o MVP

**Restricciones obligatorias:**
- Máximo 4 capas: presentación, aplicación, dominio, infraestructura
- Sin dependencias circulares entre capas
- Cada capa solo depende de la capa directamente abajo
- No usar si el dominio va a crecer en complejidad

**Estructura de carpetas:**
```
src/
├── presentation/     # Controllers, views, serializers
├── application/      # Casos de uso, DTOs, servicios de aplicación
├── domain/           # Entidades, reglas de negocio
└── infrastructure/   # Repositorios, clientes externos, configs
```

**Ideal para:** Herramientas internas, admin panels, MVPs, CRUDs.

---

### Medallion

**Cuándo usarla:**
- Data product con etapas de transformación
- Flujo raw → limpio → agregado
- Consumo de analytics o BI
- Datos de múltiples fuentes que se consolidan

**Restricciones obligatorias:**
- Cada capa (raw/curated/product) tiene su propio storage
- La capa raw es append-only, nunca se modifica
- Backfill desde raw siempre debe ser posible
- Validación de schema entre capas
- Linaje de datos trazable de product a raw

**Estructura de carpetas:**
```
src/
├── ingestion/        # Extractores de fuentes de datos
├── raw/              # Capa bronce: datos tal cual llegaron
│   ├── schemas/
│   └── jobs/
├── curated/          # Capa plata: datos limpios y normalizados
│   ├── schemas/
│   ├── jobs/
│   └── quality/      # Reglas de calidad de datos
├── product/          # Capa oro: agregados listos para consumo
│   ├── schemas/
│   └── jobs/
└── catalog/          # Metadata, linaje, diccionario de datos
```

**Ideal para:** Data lakes, plataformas de analytics, data warehouses, data mesh.

---

### Serverless

**Cuándo usarla:**
- Procesamiento disparado por eventos
- Carga variable o impredecible
- Optimización de costos es prioridad
- Funciones independientes y stateless

**Restricciones obligatorias:**
- Ejecución de función < 15 minutos
- Funciones stateless únicamente
- Cold start aceptable para el caso de uso
- Operaciones idempotentes
- Sin dependencias de estado local (usar DynamoDB, S3, etc.)

**Estructura de carpetas:**
```
src/
├── functions/
│   ├── process-order/
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── send-notification/
│   │   ├── handler.py
│   │   └── requirements.txt
│   └── generate-report/
│       ├── handler.py
│       └── requirements.txt
├── shared/           # Código compartido entre funciones
│   ├── models/
│   └── utils/
├── infrastructure/   # IaC (CDK, SAM, Serverless Framework)
└── tests/
```

**Ideal para:** Webhooks, procesamiento de imágenes, APIs ligeras, tareas programadas.

---

### Microservicios

**Cuándo usarla:**
- Equipo grande (>10 personas) que necesita trabajar en paralelo
- Dominios de negocio claramente delimitados
- Escalamiento independiente por servicio
- Diferentes tecnologías por servicio son aceptables

**Restricciones obligatorias:**
- Cada servicio tiene su propia base de datos (no compartir DB)
- Comunicación entre servicios solo por API o eventos (nunca acceso directo a DB)
- Cada servicio es desplegable independientemente
- Service mesh o API gateway para routing
- Circuit breaker para resiliencia

**Estructura por servicio:**
```
services/
├── payments/
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── infrastructure/
├── customers/
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── infrastructure/
└── shared-contracts/    # Schemas de API compartidos
    ├── openapi/
    └── events/
```

**Ideal para:** Plataformas grandes, organizaciones con múltiples equipos, productos complejos.

---

## Patrones Prohibidos

| Patrón | Prohibido cuando | Razón |
|--------|-----------------|-------|
| Monolito | servicios > 3 AND equipo > 10 | Escalamiento organizacional |
| Base de datos compartida | servicios > 1 | Acoplamiento entre servicios |
| Big ball of mud | siempre | No es un patrón, es ausencia de él |

## Cómo presentar la selección al usuario

Cuando el Specifier evalúa la arquitectura, debe presentar:

1. Las características del proyecto detectadas
2. Los patrones que aplican (pueden ser varios)
3. El razonamiento de por qué cada uno aplica
4. La recomendación con tradeoffs claros
5. Esperar aprobación humana antes de continuar
