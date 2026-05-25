# Requirements — NovaPay Payments API

## Governance
- **Contrato**: `.gcdd/governance/contract.yaml`
- **Nivel de ceremonia**: Enterprise
- **Arquitectura seleccionada**: Layered (CRUD, equipo pequeño, time to market)
- **Compliance**: PCI-DSS v4, OWASP API Top 10, OWASP Web Top 10

## Funcionalidad

### Endpoints requeridos

| Método | Endpoint | Descripción | Auth | Rol mínimo |
|--------|----------|-------------|------|------------|
| POST | /api/v1/payments/transactions | Crear transacción | OAuth2 | merchant |
| GET | /api/v1/payments/transactions/{id} | Consultar transacción | OAuth2 | merchant (owner) |
| GET | /api/v1/payments/transactions | Listar transacciones | OAuth2 | merchant (owner) |
| POST | /api/v1/payments/refunds | Crear reembolso | OAuth2 | admin |
| GET | /api/v1/payments/refunds/{id} | Consultar reembolso | OAuth2 | admin |
| GET | /api/v1/payments/settlements | Listar liquidaciones | OAuth2 | admin |

### Reglas de negocio
- Una transacción pertenece a un merchant (BOLA: verificar ownership siempre)
- Los refunds solo pueden ser creados por roles admin o supervisor (API5)
- Los datos de tarjeta se tokenizan, nunca se almacena PAN completo (PCI-DSS Req. 3)
- Toda operación genera un registro de auditoría (PCI-DSS Req. 10)
- Rate limit: 100 requests/minuto por merchant (API4)

## Constraints del Governance Contract

### Naming (auto-aplicado)
- Endpoints: `/api/v1/payments/{recurso}` — kebab-case, pluralizado, versionado
- Buckets: `novapay-payments-{proposito}-{env}`
- Lambdas: `novapay-payments-{accion}-{env}`
- Tablas: `payments_{entidad}_{proposito}` — snake_case
- IAM: `NOVAPAY-ROLE-PAYMENTS-{SERVICIO}-{ENV}` — UPPER_CASE

### Seguridad (embebida en generación)
- Todos los endpoints requieren OAuth2 con token expiration 15 min
- Middleware de auth con verificación de merchant_id (OWASP API1)
- Serializers filtran campos PCI: solo últimos 4 dígitos de tarjeta (API3)
- Rate limiter middleware por API key (API4)
- Audit logger middleware en cada endpoint que toca datos PCI (PCI-DSS Req. 10)
- TLS 1.2 mínimo (PCI-DSS Req. 4)
- Encriptación KMS CMK at-rest (nunca S3_MANAGED)

### Arquitectura (layered, constrañida)
```
src/
├── presentation/     # Controllers, serializers, middlewares
├── application/      # Casos de uso, DTOs
├── domain/           # Entidades, reglas de negocio
└── infrastructure/   # Repositorios, AWS clients
```
- Máximo 4 capas
- Sin dependencias circulares
- Cada capa solo depende de la directamente abajo

## Aprobación requerida

⚠️ **Gate Enterprise**: Esta spec requiere aprobación antes de continuar a la fase de Construir.
Aprobadores requeridos: tech-lead, security-team, compliance-officer.
