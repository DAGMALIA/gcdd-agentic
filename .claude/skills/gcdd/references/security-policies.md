# Políticas de Seguridad GCDD

## Principio Central

La seguridad no se valida después de generar código — se embebe en la generación.
Cada categoría OWASP tiene un `builder_constraint` que el Builder debe seguir al generar.

## OWASP API Security Top 10

| ID | Nombre | Qué enforcar | Constraint del Builder |
|----|--------|-------------|----------------------|
| API1 | Broken Object Level Authorization | Todo acceso a recurso requiere validación de ownership | Endpoints generados incluyen middleware de auth |
| API2 | Broken Authentication | Ningún endpoint sin auth a menos que esté whitelisted | Decorador de auth obligatorio |
| API3 | Broken Object Property Level Authorization | Control de acceso a nivel de campo en campos sensibles | Serializers de respuesta filtran por rol |
| API4 | Unrestricted Resource Consumption | Rate limiting en todos los endpoints | Rate limiter middleware auto-incluido |
| API5 | Broken Function Level Authorization | Funciones admin requieren permisos elevados | Rutas admin en módulo separado con check de rol |
| API6 | Unrestricted Access to Sensitive Business Flows | Flujos sensibles requieren verificación adicional | CAPTCHA o step-up auth en flujos críticos |
| API7 | Server Side Request Forgery | Validación de URLs externas | Whitelist de dominios permitidos para requests externos |
| API8 | Security Misconfiguration | Headers de seguridad obligatorios | Headers CSP, HSTS, X-Frame-Options auto-incluidos |
| API9 | Improper Inventory Management | Documentación de todos los endpoints | OpenAPI spec auto-generada y versionada |
| API10 | Unsafe Consumption of APIs | Validación de responses de APIs externas | Schema validation en responses de terceros |

## OWASP Web Application Top 10

| ID | Nombre | Qué enforcar | Constraint del Builder |
|----|--------|-------------|----------------------|
| A01 | Broken Access Control | RBAC/ABAC en todas las rutas | Middleware de autorización obligatorio |
| A02 | Cryptographic Failures | Encriptación adecuada siempre | KMS/CMK para datos at-rest, TLS 1.2+ in-transit |
| A03 | Injection | Solo consultas parametrizadas | Nunca concatenación de strings para queries |
| A04 | Insecure Design | Arquitectura segura desde el diseño | Threat modeling en fase de spec |
| A05 | Security Misconfiguration | Configuración segura por defecto | Defaults seguros en todas las configuraciones |
| A06 | Vulnerable Components | Dependencias actualizadas y escaneadas | pip-audit/npm audit en pre-commit |
| A07 | Auth Failures | Autenticación robusta | MFA para operaciones sensibles |
| A08 | Data Integrity Failures | Verificación de integridad | Checksums en pipelines de CI/CD |
| A09 | Logging Failures | Logging de seguridad completo | Audit logging auto-incluido |
| A10 | SSRF | Validación de URLs server-side | Whitelist de dominios, no requests arbitrarios |

## Políticas de Escaneo

### Pre-commit (se ejecutan en cada commit)

```yaml
pre_commit:
  - tool: "semgrep"
    purpose: "Análisis estático de seguridad"
    config: "p/owasp-top-ten"
    fail_on: "error"
    description: "Detecta patrones de código inseguros"

  - tool: "gitleaks"
    purpose: "Detección de secretos"
    fail_on: "any"
    description: "Encuentra API keys, passwords, tokens en el código"

  - tool: "pip-audit / npm audit / cargo audit"
    purpose: "Vulnerabilidades en dependencias"
    fail_on: "high"
    description: "Verifica CVEs conocidos en dependencias"
```

### Pre-deploy (se ejecutan antes de desplegar)

```yaml
pre_deploy:
  - tool: "trivy"
    purpose: "Escaneo de imágenes de contenedor"
    target: "imágenes Docker"
    fail_on: "critical"

  - tool: "checkov / tfsec"
    purpose: "Seguridad de Infrastructure as Code"
    target: "templates CDK/Terraform/CloudFormation"
    fail_on: "high"

  - tool: "OWASP ZAP"
    purpose: "Análisis dinámico"
    target: "endpoints en staging"
    mode: "baseline scan"
```

### Post-deploy (se ejecutan después del despliegue)

```yaml
post_deploy:
  - tool: "OWASP ZAP full scan"
    schedule: "semanal"
    target: "endpoints de producción"

  - tool: "penetration testing"
    schedule: "trimestral"
    scope: "aplicación completa"
```

## Cómo aplicar seguridad en cada fase GCDD

**ESPECIFICAR**: El Specifier incluye requisitos de seguridad en el design.md basándose en
la clasificación de datos del dominio. Datos PII → encriptación obligatoria + audit logging.

**CONSTRUIR**: El Builder genera código que ya incluye middleware de auth, encriptación,
sanitización, rate limiting — según los builder_constraints de OWASP aplicables.

**VALIDAR**: El Guardian ejecuta los escaneos pre-deploy y genera el reporte de compliance.
Bloquea el deployment si hay findings críticos o altos.

**DESPLEGAR**: Solo procede si todos los escaneos pasaron. El certificado de compliance
registra qué escaneos se ejecutaron y sus resultados.
