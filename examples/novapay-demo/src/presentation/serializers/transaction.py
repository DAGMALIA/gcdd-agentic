"""
Presentation Layer — Transaction Serializers
Governance: owasp.api_top_10.API3 — campos PCI nunca se retornan completos
Governance: pci_dss.requirement_3 — solo últimos 4 dígitos, nunca PAN completo
"""

from pydantic import BaseModel, Field
from datetime import datetime
from src.domain.entities.transaction import Transaction


class TransactionCreateRequest(BaseModel):
    """Request para crear transacción.

    Governance: pci_dss.requirement_3
    - card_token: token de la tarjeta (NUNCA el PAN completo)
    - PROHIBIDO aceptar card_number, cvv, expiry como campos
    """

    amount: int = Field(..., gt=0, description="Monto en centavos")
    currency: str = Field(..., pattern="^[A-Z]{3}$", description="ISO 4217")
    card_token: str = Field(..., description="Token de tarjeta (nunca PAN)")
    description: str | None = Field(None, max_length=255)

    # ⛔ GOVERNANCE: Los siguientes campos están PROHIBIDOS por PCI-DSS Req. 3
    # card_number: PROHIBIDO — nunca aceptar PAN en el request
    # cvv: PROHIBIDO — nunca aceptar CVV
    # expiry_date: PROHIBIDO — nunca aceptar fecha de expiración


class TransactionResponse(BaseModel):
    """Response de transacción.

    Governance: owasp.api_top_10.API3
    - card_last_four: solo últimos 4 dígitos
    - NUNCA exponer card_token, merchant internal IDs, o metadata de infra
    """

    id: str
    amount: int
    currency: str
    status: str
    card_last_four: str = Field(..., description="Últimos 4 dígitos solamente")
    description: str | None
    created_at: datetime

    # ⛔ GOVERNANCE: Los siguientes campos NUNCA se incluyen en el response
    # merchant_id: FILTRADO — dato interno, no exponer
    # card_token: FILTRADO — dato PCI, no exponer
    # internal_reference: FILTRADO — dato de infraestructura

    @classmethod
    def from_entity(cls, entity: Transaction) -> "TransactionResponse":
        """Convierte entidad de dominio a response filtrado por governance."""
        return cls(
            id=entity.id,
            amount=entity.amount,
            currency=entity.currency,
            status=entity.status.value,
            card_last_four=entity.card_last_four,  # Solo últimos 4
            description=entity.description,
            created_at=entity.created_at,
            # merchant_id: NO SE INCLUYE (API3)
            # card_token: NO SE INCLUYE (PCI-DSS)
        )
