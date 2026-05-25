# Guía de Implementación GCDD

## Principio

GCDD es agnóstico de IDE y de plataforma. La metodología se adapta a cualquier entorno
que soporte agentes AI. Esta guía muestra cómo implementarlo en cada plataforma.

---

## Claude Code / Claude Skills

### Estructura de archivos

```
.claude/
├── CLAUDE.md                      # Constitución GCDD
├── governance/
│   ├── governance-contract.yaml   # Contrato de governance
│   ├── profiles/
│   │   ├── data-aws.yaml          # Perfil de dominio
│   │   └── api-rest.yaml          # Perfiles componibles
│   └── validators/
│       ├── naming.py              # Validador de nombres
│       ├── security.py            # Validador de seguridad
│       └── architecture.py        # Validador de arquitectura
├── skills/
│   ├── navigator.md               # Rol: orientar y rutear
│   ├── specifier.md               # Rol: capturar requerimientos
│   ├── builder.md                 # Rol: generar artefactos
│   ├── guardian.md                # Rol: validación de seguridad
│   ├── steward.md                 # Rol: validación de governance
│   └── chronicler.md             # Rol: documentación
└── tools/
    ├── governed_tools.py          # Herramientas con governance embebido
    └── mcp_server.py             # Servidor MCP
```

### Constitución (CLAUDE.md)

```markdown
# Constitución del Proyecto — GCDD

## Contrato de Governance
Este proyecto sigue GCDD. Todo código generado debe cumplir con
`.claude/governance/governance-contract.yaml`.

## Reglas No Negociables
1. Leer el contrato de governance ANTES de generar cualquier código
2. Validar cada nombre de recurso contra la sección naming
3. Validar cada configuración de seguridad contra la sección security
4. Seleccionar arquitectura del catálogo, no inventar
5. Ningún recurso sin los tags requeridos
6. Ningún endpoint público sin aprobación explícita

## Flujo
ORIENTAR → ESPECIFICAR → CONSTRUIR → VALIDAR → DOCUMENTAR → DESPLEGAR
```

### Ejemplo de validador

```python
# .claude/governance/validators/naming.py
import yaml
from pathlib import Path

def load_contract():
    contract_path = Path(__file__).parent.parent / "governance-contract.yaml"
    with open(contract_path) as f:
        return yaml.safe_load(f)

def validate_resource_name(resource_type: str, name: str) -> dict:
    contract = load_contract()
    naming = contract.get("naming", {})
    prefix = naming.get("global", {}).get("prefix", "")
    
    if prefix and not name.startswith(prefix):
        return {
            "valid": False,
            "error": f"Debe empezar con '{prefix}'",
            "suggestion": f"{prefix}-{name}",
            "rule": "naming.global.prefix"
        }
    return {"valid": True}
```

---

## Kiro (AWS IDE)

### Estructura de archivos

```
.kiro/
├── steering/
│   ├── agent-navigator.md
│   ├── agent-specifier.md
│   ├── agent-builder.md
│   ├── agent-guardian.md
│   ├── agent-steward.md
│   └── agent-chronicler.md
├── hooks/
│   ├── validate-post-task.json
│   └── approve-spec-phase.json
├── specs/
└── mcp-server/
    └── gcdd_server.py
```

### Ejemplo de steering file (agent-builder.md)

```markdown
# Builder — Generador de Código

## Identidad
Eres Builder, el rol de generación de código en el flujo GCDD.

## Responsabilidad ÚNICA
Generar código/artefactos desde specs aprobadas, a través de herramientas gobernadas.

## ANTES de generar cualquier código
1. Leer governance-contract.yaml
2. Verificar que la spec fue aprobada
3. Identificar el patrón de arquitectura aprobado

## Herramientas AUTORIZADAS
- gcdd_generate_code
- gcdd_validate_name
- gcdd_create_resource

## Herramientas PROHIBIDAS
- gcdd_scan_security (eso es de Guardian)
- gcdd_validate_governance (eso es de Steward)
- gcdd_create_spec (eso es de Specifier)

## Cuando te pidan algo fuera de tu rol
Responde EXACTAMENTE: "Eso lo maneja [Rol]. Usa #agent-[rol]."
NO intentes resolver parcialmente.
```

### Ejemplo de hook

```json
{
  "name": "validate-post-task",
  "trigger": "on-task-complete",
  "action": "invoke-agent",
  "agent": "agent-steward",
  "prompt": "Valida el código generado contra el contrato de governance"
}
```

---

## Cursor / VS Code

### Estructura de archivos

```
.cursor/
├── rules/
│   ├── gcdd-constitution.md
│   └── role-definitions.md
├── governance/
│   └── governance-contract.yaml
└── mcp/
    └── gcdd_server.py
```

### Constitución (.cursorrules o gcdd-constitution.md)

Mismo contenido que CLAUDE.md adaptado al formato de Cursor.

---

## GitHub Copilot

### Estructura de archivos

```
.github/
├── copilot/
│   └── AGENTS.md
├── governance/
│   └── governance-contract.yaml
└── workflows/
    └── gcdd-validate.yml
```

### Validación en CI/CD (gcdd-validate.yml)

```yaml
name: GCDD Governance Validation
on: [push, pull_request]

jobs:
  validate-governance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validar naming
        run: python .github/governance/validators/naming.py --check-all
      
      - name: Validar seguridad
        run: python .github/governance/validators/security.py --check-all
      
      - name: Escaneo SAST
        run: semgrep --config p/owasp-top-ten .
      
      - name: Detección de secretos
        run: gitleaks detect --source .
      
      - name: Escaneo de dependencias
        run: pip-audit
```

---

## Servidor MCP (cualquier plataforma)

El servidor MCP es la pieza clave del enforcement estructural. Expone herramientas
gobernadas que validan contra el contrato de governance antes de ejecutar.

```python
# mcp_server.py — Esqueleto de servidor MCP con governance
from typing import Any

# Permisos por rol
ROLE_PERMISSIONS = {
    "navigator":  {"gcdd_list_domains", "gcdd_explain_workflow", "gcdd_get_contract"},
    "specifier":  {"gcdd_validate_name", "gcdd_create_spec", "gcdd_select_architecture"},
    "builder":    {"gcdd_generate_code", "gcdd_validate_name", "gcdd_create_resource"},
    "guardian":   {"gcdd_scan_security", "gcdd_validate_scp", "gcdd_run_sast"},
    "steward":    {"gcdd_validate_governance", "gcdd_check_tags", "gcdd_scorecard"},
    "chronicler": {"gcdd_generate_docs", "gcdd_generate_changelog"},
}

def authorize(role: str, tool: str) -> bool:
    """Capa 2: Autorización de herramientas por rol."""
    allowed = ROLE_PERMISSIONS.get(role, set())
    if tool not in allowed:
        return False  # Retornar error: "Tool no autorizada para este rol"
    return True

def gcdd_create_resource(name: str, resource_type: str, config: dict) -> dict:
    """Capa 3: Enforcement estructural — la herramienta valida antes de crear."""
    # Validar nombre
    name_result = validate_name(resource_type, name)
    if not name_result["valid"]:
        return {"error": name_result["error"], "suggestion": name_result["suggestion"]}
    
    # Validar seguridad
    security_result = validate_security(config)
    if not security_result["valid"]:
        return {"error": security_result["error"], "correct_config": security_result["fix"]}
    
    # Validar tags
    tags_result = validate_tags(config.get("tags", {}))
    if not tags_result["valid"]:
        return {"error": tags_result["error"], "missing_tags": tags_result["missing"]}
    
    # Todo válido — crear el recurso
    return create_resource_impl(name, resource_type, config)
```
