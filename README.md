# GCDD Agentic — Governance-Constrained Driven Development

<p align="center">
  <strong>Un framework agentic para construir y operar software donde el governance organizacional,<br>las políticas de seguridad y los estándares arquitectónicos se aplican <em>durante</em> la generación — no <em>después</em>.</strong>
</p>

<p align="center">
  <code>github.com/TU-USUARIO/gcdd-agentic</code>
</p>

<p align="center">
  <a href="#el-problema">El Problema</a> •
  <a href="#qué-es-gcdd">Qué es GCDD</a> •
  <a href="#los-5-conceptos">Los 5 Conceptos</a> •
  <a href="#instalación">Instalación</a> •
  <a href="#inicio-rápido">Inicio Rápido</a> •
  <a href="#documentación">Documentación</a> •
  <a href="#contribuir">Contribuir</a>
</p>

---

## El Problema

Le pedí a un agente AI: *"Crea un bucket S3 para datos de pago."*

Lo creó. Sin encriptación KMS. Sin tags. Con acceso público. Mi Glue job se llama `glue_customer_etl` en dev, `customer-etl-stg` en staging, y `CUST_ETL_PRODUCTION` en prod. Tres ambientes, tres convenciones, cero estándar.

**Spec-Driven Development** resolvió el intent drift. Pero tiene un punto ciego: la spec dice **QUÉ** construir — no **CÓMO** debe cumplir.

```
Flujo SDD:  Spec → AI genera → Linter detecta violaciones → Developer corrige → Repetir
Flujo GCDD: Governance → Spec constrañida → AI genera a través de tools gobernados → Conforme por construcción
```

## ¿Qué es GCDD?

GCDD agrega la capa que le falta a SDD: un **Contrato de Governance** (YAML) que constrañe todo lo que la AI genera — nombres, seguridad, arquitectura, tags, escaneos — antes de escribir la primera línea de código.

Las restricciones van en las **herramientas**, no en los **prompts**. Decirle a la AI "no uses S3_MANAGED" falla el 20-30% del tiempo. Una herramienta que rechaza `S3_MANAGED` y retorna "Usa KMS CMK" **nunca falla**.

## Los 5 Conceptos

| # | Concepto | Qué es |
|---|----------|--------|
| 1 | **Contrato de Governance** | Archivo YAML con TODAS las reglas organizacionales. No es documentación — es código que las herramientas consumen. |
| 2 | **Generación Constrañida** | Las restricciones se codifican en las herramientas que la AI usa, no en los prompts que lee. |
| 3 | **Perfiles de Dominio** | Implementaciones del contrato para industrias específicas (fintech, salud, datos, APIs). |
| 4 | **Especialización por Herramientas** | Los roles de agentes se enforzan por acceso a tools, no por instrucciones. |
| 5 | **Tres Capas de Enforcement** | Prompt (débil) + Autorización de tools (media) + Estructural (fuerte). |

## El Flujo

```
CONTRATO DE GOVERNANCE (constrañe todo)
    │
    ▼
1. ORIENTAR     → ¿Qué dominio? ¿Qué perfil? ¿Qué reglas?
2. ESPECIFICAR  → Requerimientos constrañidos. Arquitectura SELECCIONADA del catálogo.
3. CONSTRUIR    → Código conforme por construcción.
4. VALIDAR      → OWASP, naming, tags, scorecard de governance.
5. DOCUMENTAR   → Docs + audit trail.
6. DESPLEGAR    → Solo si validación pasó + certificado de compliance.
```

## Ejemplo: Antes vs Después

**Sin GCDD** — un `create_transaction` endpoint:
```python
@app.post("/transactions")
def create(request):
    bucket = s3.create_bucket("data-payments")  # Nombre inventado
    # Sin auth, sin ownership check, acepta card_number directo
    return {"status": "ok"}
```

**Con GCDD** — el mismo endpoint, constrañido por governance:
```python
# Governance: owasp.api_top_10.API1 — ownership check obligatorio
# Governance: pci_dss.requirement_3 — solo token, nunca PAN
@router.post("/api/v1/payments/transactions")  # naming enforced
@require_auth                                   # API2: auth obligatorio
async def create_transaction(
    request: TransactionCreateRequest,
    merchant_id: str = Depends(get_current_merchant),  # API1: del token, NUNCA del body
):
    use_case = CreateTransactionUseCase(repo)
    transaction = await use_case.execute(
        merchant_id=merchant_id,
        card_token=request.card_token,  # PCI-DSS: solo token
    )
    return TransactionResponse.from_entity(transaction)  # API3: filtra campos PCI
```

Ver el [ejemplo completo de NovaPay](examples/novapay-demo/) con governance contract, specs, código y reporte de validación.

## Instalación

### Claude Code (Personal — todos tus proyectos)

```bash
git clone https://github.com/TU-USUARIO/gcdd-agentic.git
mkdir -p ~/.claude/skills/gcdd
cp -r gcdd-agentic/.claude/skills/gcdd/* ~/.claude/skills/gcdd/
```

### Claude Code (Por proyecto — compartido con el equipo)

```bash
# Dentro de tu repositorio
mkdir -p .claude/skills/gcdd
cp -r gcdd-agentic/.claude/skills/gcdd/* .claude/skills/gcdd/
```

### Claude.ai (Skills en la interfaz web)

Descarga el ZIP desde [Releases](../../releases) y súbelo en **Customize > Skills**.

## Inicio Rápido

```bash
# 1. Copia la plantilla de governance contract a tu proyecto
mkdir -p .gcdd/governance
cp examples/governance-contract.example.yaml .gcdd/governance/contract.yaml

# 2. Edita con las reglas de tu organización (naming, security, architecture)

# 3. Abre Claude Code y dile:
# "Quiero construir un proyecto con governance. Lee .gcdd/governance/contract.yaml"
```

Ver la [guía completa de inicio rápido](docs/INICIO-RAPIDO.md).

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [Metodología](docs/METODOLOGIA.md) | Documento fundacional completo de GCDD |
| [Whitepaper (DOCX)](docs/GCDD-Metodologia-v1.0.docx) | Versión formal para compartir |
| [Inicio Rápido](docs/INICIO-RAPIDO.md) | Adopta GCDD en 15 minutos |
| [Comparación](docs/COMPARACION.md) | GCDD vs SDD vs BMAD vs GSD |
| [Origen](docs/ORIGEN.md) | Los 3 descubrimientos que dieron origen a GCDD |
| [Seguridad](docs/SEGURIDAD.md) | OWASP API/Web Top 10, escaneos, PCI-DSS |
| [Catálogo de Arquitectura](docs/CATALOGO-ARQUITECTURA.md) | 6 patrones con reglas de selección |
| [Implementación](docs/IMPLEMENTACION.md) | Claude Code, Kiro, Cursor, GitHub Copilot |

## Perfiles de Dominio

| Perfil | Dominio | Estado |
|--------|---------|--------|
| [infra-terraform](profiles/infra-terraform.yaml) | IaC con Terraform (AWS · GCP · Azure) | ✅ Disponible |
| [data-gcp](profiles/data-gcp.yaml) | Ingeniería de Datos en GCP | ✅ Disponible |
| [data-azure](profiles/data-azure.yaml) | Ingeniería de Datos en Azure | ✅ Disponible |
| [data-aws](profiles/data-aws.yaml) | Ingeniería de Datos en AWS | 🚧 En desarrollo |
| [api-rest](profiles/api-rest.yaml) | APIs REST | 🚧 En desarrollo |
| [webapp-react](profiles/webapp-react.yaml) | Aplicaciones Web React | 🚧 En desarrollo |
| [infra-k8s](profiles/infra-k8s.yaml) | Infraestructura Kubernetes | 🚧 En desarrollo |
| [fintech](profiles/fintech.yaml) | Servicios Financieros | 🚧 En desarrollo |
| [healthcare](profiles/healthcare.yaml) | Salud / HIPAA | 🚧 En desarrollo |

## Estructura del Repo

```
gcdd-agentic/
├── .claude/skills/gcdd/           # Skill instalable para Claude
│   ├── SKILL.md                   # Core del skill
│   ├── references/                # Docs que Claude consulta bajo demanda
│   └── templates/                 # Plantilla de governance contract
├── docs/                          # Documentación de la metodología
│   ├── METODOLOGIA.md             # Whitepaper completo
│   ├── GCDD-Metodologia-v1.0.docx # Versión formal
│   ├── INICIO-RAPIDO.md
│   ├── COMPARACION.md
│   ├── ORIGEN.md
│   ├── SEGURIDAD.md
│   ├── CATALOGO-ARQUITECTURA.md
│   └── IMPLEMENTACION.md
├── examples/
│   ├── governance-contract.example.yaml
│   └── novapay-demo/              # Ejemplo completo funcional
├── profiles/                      # Perfiles de dominio (en desarrollo)
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE                        # MIT
```

## Contribuir

GCDD es una metodología abierta. Contribuciones bienvenidas:

- **Perfiles de Dominio** — Implementa contratos de governance para tu industria
- **Ejemplos** — Proyectos demo que muestren GCDD en acción
- **Validadores** — Código que enforce reglas del contrato
- **Documentación** — Guías, tutoriales, traducciones
- **Métricas** — Datos empíricos sobre efectividad del enforcement

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para detalles.

## Licencia

MIT — ver [LICENSE](LICENSE).
