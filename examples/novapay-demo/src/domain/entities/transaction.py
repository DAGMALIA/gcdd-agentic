"""
Domain Layer — Transaction Entity
Governance: architecture.selected = layered
  - Esta capa NO importa nada de infrastructure
  - Contiene las reglas de negocio puras
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class TransactionStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"
    REFUNDED = "refunded"


@dataclass
class Transaction:
    """Entidad de dominio — Transacción de pago.

    Governance: pci_dss.requirement_3
    - card_last_four: solo los últimos 4 dígitos, nunca el PAN completo
    - card_token: referencia tokenizada, el PAN vive en el vault del procesador
    """

    merchant_id: str
    amount: int                              # En centavos, siempre positivo
    currency: str                            # ISO 4217
    card_token: str                          # Token, NUNCA PAN completo
    card_last_four: str                      # Solo últimos 4 dígitos
    id: str = field(default_factory=lambda: str(uuid4()))
    status: TransactionStatus = TransactionStatus.PENDING
    description: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validaciones de dominio — reglas de negocio puras."""
        if self.amount <= 0:
            raise ValueError("El monto debe ser positivo")
        if len(self.currency) != 3:
            raise ValueError("Currency debe ser ISO 4217 (3 caracteres)")
        if len(self.card_last_four) != 4 or not self.card_last_four.isdigit():
            raise ValueError("card_last_four debe ser exactamente 4 dígitos")

        # Governance: pci_dss.requirement_3 — NUNCA almacenar PAN
        if len(self.card_token) > 6 and self.card_token.isdigit():
            raise ValueError(
                "VIOLACIÓN PCI-DSS: card_token parece ser un PAN completo. "
                "Use tokenización antes de crear la entidad."
            )

    def approve(self) -> None:
        if self.status != TransactionStatus.PENDING:
            raise ValueError(f"No se puede aprobar una transacción en estado {self.status.value}")
        self.status = TransactionStatus.APPROVED

    def decline(self) -> None:
        if self.status != TransactionStatus.PENDING:
            raise ValueError(f"No se puede rechazar una transacción en estado {self.status.value}")
        self.status = TransactionStatus.DECLINED

    def refund(self) -> None:
        if self.status != TransactionStatus.APPROVED:
            raise ValueError("Solo transacciones aprobadas pueden ser reembolsadas")
        self.status = TransactionStatus.REFUNDED
