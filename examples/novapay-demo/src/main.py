"""
NovaPay Payments API — Punto de entrada
Generado con GCDD | Governance Contract: .gcdd/governance/contract.yaml
Arquitectura: Layered (presentation → application → domain → infrastructure)
Compliance: PCI-DSS v4, OWASP API Top 10
"""

from fastapi import FastAPI
from src.presentation.middlewares.auth import OAuth2Middleware
from src.presentation.middlewares.rate_limiter import RateLimiterMiddleware
from src.presentation.middlewares.audit_logger import AuditLoggerMiddleware  # PCI-DSS Req. 10
from src.presentation.middlewares.security_headers import SecurityHeadersMiddleware  # OWASP API8
from src.presentation.routes import transactions, refunds, settlements

app = FastAPI(
    title="NovaPay Payments API",
    version="1.0.0",
    docs_url=None,       # Deshabilitado en prod (OWASP API9: inventory management)
    redoc_url=None,
)

# ─── MIDDLEWARES DE SEGURIDAD (orden importa) ────────────────────────────────
# Governance: security.authentication.allowed_methods = ["OAuth2", "mTLS"]
app.add_middleware(OAuth2Middleware, token_expiration_minutes=15)

# Governance: owasp.api_top_10.API4 — rate limiting 100 req/min por merchant
app.add_middleware(RateLimiterMiddleware, max_requests=100, window_minutes=1)

# Governance: pci_dss.requirement_10 — audit logging de toda operación
app.add_middleware(AuditLoggerMiddleware)

# Governance: owasp.api_top_10.API8 — security headers
app.add_middleware(SecurityHeadersMiddleware)

# ─── RUTAS ───────────────────────────────────────────────────────────────────
# Governance: naming.resources.api_endpoint.pattern = /api/v{version}/{dominio}/{recurso}
app.include_router(transactions.router, prefix="/api/v1/payments")
app.include_router(refunds.router, prefix="/api/v1/payments")
app.include_router(settlements.router, prefix="/api/v1/payments")
