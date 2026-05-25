# GCDD — Inicio Rápido

Pon a funcionar el desarrollo constrañido por governance en 15 minutos.

---

## Paso 1: Crea tu contrato de governance (5 min)

Copia el ejemplo y personalízalo para tu organización:

```bash
mkdir -p .gcdd/governance
cp examples/governance-contract.example.yaml .gcdd/governance/contract.yaml
```

Edita `contract.yaml`. Empieza solo con estas secciones — puedes agregar el resto después:

```yaml
version: "1.0.0"
profile: "mi-org"

naming:
  global:
    prefix: "miorg"
    separator: "-"

security:
  encryption:
    at_rest: "required"
    key_management: "customer-managed"
  authentication:
    public_endpoints: "forbidden"
  authorization:
    wildcard_permissions: "forbidden"

environments:
  allowed: ["dev", "staging", "prod"]
```

Ese es tu contrato de governance mínimo viable. Ya enforza prefijos de nombres, encriptación, autenticación y ningún permiso IAM con wildcard.

---

## Paso 2: Crea tu constitución (5 min)

La constitución es el documento que tu agente AI lee. Referencia el contrato de governance y define los roles.

Para Claude Code, crea `CLAUDE.md`:

```markdown
# Constitución del Proyecto — GCDD

## Contrato de Governance
Este proyecto sigue GCDD (Governance-Constrained Driven Development).
Todo código generado debe cumplir con `.gcdd/governance/contract.yaml`.

## Reglas (no negociables)
1. Todo nombre de recurso debe empezar con el prefijo definido en el contrato de governance
2. Ningún recurso puede usar encriptación manejada por el proveedor — usar KMS CMK
3. Ningún endpoint puede ser público sin aprobación explícita
4. Ninguna política IAM puede usar wildcard (*) en resources
5. El patrón de arquitectura debe seleccionarse del contrato de governance, no inventarse

## Flujo de Trabajo
1. Antes de generar cualquier código, leer `.gcdd/governance/contract.yaml`
2. Validar cada nombre de recurso contra la sección de naming
3. Validar cada configuración de seguridad contra la sección de security
4. Seleccionar arquitectura de la sección architecture basándose en los requerimientos
5. Después de generar, validar contra todas las reglas de governance
```

Para Kiro, pon esto en `.kiro/steering/gcdd-constitution.md`.
Para Cursor, ponlo en `.cursorrules`.

---

## Paso 3: Agrega tu primer validador (5 min)

Crea un validador simple que enforce tu convención de nombres:

```python
# .gcdd/validators/naming.py
"""Validador de Nombres GCDD — enforza reglas de naming del contrato de governance."""

import re
import yaml
from pathlib import Path

def load_contract():
    contract_path = Path(__file__).parent.parent / "governance" / "contract.yaml"
    with open(contract_path) as f:
        return yaml.safe_load(f)

def validate_resource_name(resource_type: str, name: str) -> dict:
    """
    Valida un nombre de recurso contra el contrato de governance.
    
    Retorna:
        {"valid": True} o {"valid": False, "error": "...", "suggestion": "..."}
    """
    contract = load_contract()
    naming = contract.get("naming", {})
    global_rules = naming.get("global", {})
    resource_rules = naming.get("resources", {}).get(resource_type, {})
    
    prefix = global_rules.get("prefix", "")
    
    # Verificar prefijo
    if prefix and not name.startswith(prefix):
        return {
            "valid": False,
            "error": f"El nombre del recurso debe empezar con '{prefix}'",
            "suggestion": f"{prefix}-{name}",
            "rule": "naming.global.prefix"
        }
    
    # Verificar patrón si está definido
    pattern = resource_rules.get("pattern")
    if pattern:
        if not _matches_pattern(name, pattern, global_rules):
            return {
                "valid": False,
                "error": f"El nombre no coincide con el patrón: {pattern}",
                "example": resource_rules.get("example", ""),
                "rule": f"naming.resources.{resource_type}.pattern"
            }
    
    return {"valid": True}


def validate_environment(environment: str) -> dict:
    """Valida que el ambiente esté permitido."""
    contract = load_contract()
    allowed = contract.get("environments", {}).get("allowed", [])
    
    if environment not in allowed:
        return {
            "valid": False,
            "error": f"El ambiente '{environment}' no está permitido",
            "allowed": allowed,
            "rule": "environments.allowed"
        }
    
    return {"valid": True}


def _matches_pattern(name, pattern, global_rules):
    """Matching simple de patrón — extender según se necesite."""
    separator = global_rules.get("separator", "-")
    parts = name.split(separator)
    pattern_parts = pattern.split(separator)
    return len(parts) >= len(pattern_parts) - 1


# ─── Punto de entrada CLI ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Uso: python naming.py <tipo_recurso> <nombre>")
        print("Ejemplo: python naming.py s3_bucket miorg-pagos-raw-dev")
        sys.exit(1)
    
    result = validate_resource_name(sys.argv[1], sys.argv[2])
    if result["valid"]:
        print(f"✅ '{sys.argv[2]}' es válido para {sys.argv[1]}")
    else:
        print(f"❌ {result['error']}")
        if "suggestion" in result:
            print(f"   Sugerencia: {result['suggestion']}")
        if "example" in result:
            print(f"   Ejemplo: {result['example']}")
        sys.exit(1)
```

---

## Lo que tienes ahora

```
tu-proyecto/
├── .gcdd/
│   ├── governance/
│   │   └── contract.yaml          # Tus reglas
│   └── validators/
│       └── naming.py              # Enforza reglas de naming
├── CLAUDE.md                      # Constitución (o .cursorrules, etc.)
└── ... tu código ...
```

Tu agente AI ahora tiene:
- **Un contrato de governance** que define qué está permitido
- **Una constitución** que le dice que lea y siga el contrato
- **Un validador** que se puede llamar para verificar compliance

---

## Siguientes pasos

1. **Agrega más validadores**: security.py, architecture.py, tags.py
2. **Construye herramientas gobernadas**: Envuelve operaciones comunes (crear bucket, crear endpoint) en funciones que llaman validadores antes de ejecutar
3. **Define roles**: Divide tu constitución en roles especializados (Specifier, Builder, Guardian)
4. **Agrega escaneo**: Integra herramientas SAST/DAST en tu pipeline de CI
5. **Crea un perfil de dominio**: Empaqueta tu contrato de governance como un perfil reusable que otros en tu org puedan adoptar
6. **Mide**: Rastrea violaciones atrapadas, tiempo ahorrado, tasas de compliance al primer intento

---

## Ejemplos por dominio

| Estoy construyendo... | Empieza con |
|----------------------|-------------|
| Pipelines de datos en AWS | `examples/profiles/data-aws.yaml` |
| APIs REST | `examples/profiles/api-rest.yaml` |
| Apps web (React/Next.js) | `examples/profiles/webapp-react.yaml` |
| Infraestructura (Terraform/CDK) | `examples/profiles/infra-iac.yaml` |
| Apps móviles | `examples/profiles/mobile.yaml` |

Cada perfil es un contrato de governance pre-configurado que puedes usar tal cual o personalizar.
