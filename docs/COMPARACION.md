# GCDD vs Metodologías Existentes

## Dónde se ubica GCDD en el ecosistema

```
                    ┌─────────────────────────────────────────────┐
                    │              GCDD                            │
                    │   Governance + Spec + Agentes + Enforcement  │
                    └──────────┬──────────────────────────────────┘
                               │
            ┌──────────────────┼──────────────────────┐
            │                  │                      │
    ┌───────▼───────┐  ┌──────▼──────┐  ┌────────────▼────────────┐
    │ Capa SDD      │  │ Capa Agentes│  │ Capa Governance         │
    │ (Spec Kit,    │  │ (BMAD, GSD) │  │ (Collibra, OneTrust,    │
    │  Kiro specs)  │  │             │  │  Acceldata)             │
    └───────────────┘  └─────────────┘  └─────────────────────────┘

    Las specs dicen a    Los agentes       El governance monitorea
    la AI QUÉ construir  ejecutan el       DESPUÉS del deployment
                         trabajo

    ─────────────── GCDD unifica los tres ─────────────────────────
    El governance constrañe las specs, las specs guían a los
    agentes, los agentes generan a través de herramientas
    gobernadas, el governance es estructural.
```

## Comparación de funcionalidades

| Funcionalidad | Vibe Coding | SDD (Spec Kit) | BMAD | GSD | GCDD |
|---------------|-------------|----------------|------|-----|------|
| Spec antes del código | ❌ | ✅ | ✅ | ✅ | ✅ |
| Especialización de agentes | ❌ | ❌ | ✅ (12+ agentes) | ✅ (paralelo) | ✅ (por acceso a tools) |
| Contrato de governance | ❌ | ❌ (solo constitución) | ❌ | ❌ | ✅ |
| Generación constrañida | ❌ | ❌ | ❌ | ❌ | ✅ |
| Seguridad shift-left | ❌ | ❌ | ❌ | ❌ | ✅ (OWASP embebido) |
| Selección de arquitectura | La AI decide | La AI decide | La AI decide | La AI decide | Catálogo gobernado |
| Enforcement de naming | Manual | Basado en prompt | Basado en prompt | Basado en prompt | A nivel de herramienta |
| Domain-specific | ❌ | ❌ | ❌ | ❌ | ✅ (perfiles) |
| Multi-dominio | N/A | N/A | N/A | N/A | ✅ (componible) |
| Mecanismo de enforcement | Ninguno | Prompt | Prompt + handoffs | Prompt | 3 capas |
| Agnóstico de IDE | ✅ | ✅ | ✅ | Mayormente Claude | ✅ |
| Certificado de compliance | ❌ | ❌ | ❌ | ❌ | ✅ |
| Audit trail | ❌ | ❌ | Parcial | ❌ | ✅ |
| Niveles de ceremonia | N/A | Un solo tamaño | ❌ | ❌ | Quick/Standard/Enterprise |

## Lo que GCDD NO es

- **No es un reemplazo de SDD.** GCDD extiende SDD. Sigues escribiendo specs. Solo las escribes dentro de restricciones de governance.
- **No es un reemplazo de BMAD/GSD.** Puedes usar los patrones de agentes de BMAD con la capa de governance de GCDD. Son complementarios.
- **No es una herramienta de compliance.** Collibra, OneTrust y Acceldata monitorean sistemas en producción. GCDD opera durante el desarrollo. Son fases diferentes.
- **No es waterfall.** El contrato de governance es un documento vivo. Evoluciona con la organización. Los niveles de ceremonia aseguran que no sobre-proceses cambios pequeños.
