"""
Presentation Layer — Transactions Controller
Governance: naming.resources.api_endpoint = /api/v1/payments/transactions
"""

from fastapi import APIRouter, Depends, HTTPException, status
from src.presentation.middlewares.auth import require_auth, require_role, get_current_merchant
from src.presentation.serializers.transaction import (
    TransactionCreateRequest,
    TransactionResponse,       # Governance: OWASP API3 — filtra campos PCI
)
from src.application.use_cases.create_transaction import CreateTransactionUseCase
from src.application.use_cases.get_transaction import GetTransactionUseCase
from src.application.use_cases.list_transactions import ListTransactionsUseCase
from src.infrastructure.repositories.transaction_repository import TransactionRepository

router = APIRouter(tags=["transactions"])
repo = TransactionRepository()


# ─── POST /api/v1/payments/transactions ──────────────────────────────────────
# Governance: owasp.api_top_10.API2 — @require_auth obligatorio
# Governance: owasp.api_top_10.API1 — merchant_id se extrae del token, no del body
@router.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
@require_auth
async def create_transaction(
    request: TransactionCreateRequest,
    merchant_id: str = Depends(get_current_merchant),
):
    """Crear una nueva transacción de pago."""
    use_case = CreateTransactionUseCase(repo)
    transaction = await use_case.execute(
        merchant_id=merchant_id,   # OWASP API1: ownership del merchant, NUNCA del body
        amount=request.amount,
        currency=request.currency,
        card_token=request.card_token,  # PCI-DSS Req.3: solo token, nunca PAN
        description=request.description,
    )
    return TransactionResponse.from_entity(transaction)


# ─── GET /api/v1/payments/transactions/{id} ──────────────────────────────────
# Governance: owasp.api_top_10.API1 — verificar que la transacción pertenece al merchant
@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse,
)
@require_auth
async def get_transaction(
    transaction_id: str,
    merchant_id: str = Depends(get_current_merchant),
):
    """Consultar una transacción por ID."""
    use_case = GetTransactionUseCase(repo)
    transaction = await use_case.execute(transaction_id, merchant_id)

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada",
        )

    # Governance: OWASP API1 — verificar ownership
    if transaction.merchant_id != merchant_id:
        # No revelar que existe — retornar 404, no 403 (previene enumeration)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada",
        )

    return TransactionResponse.from_entity(transaction)


# ─── GET /api/v1/payments/transactions ───────────────────────────────────────
# Governance: OWASP API1 — solo transacciones del merchant autenticado
@router.get(
    "/transactions",
    response_model=list[TransactionResponse],
)
@require_auth
async def list_transactions(
    merchant_id: str = Depends(get_current_merchant),
    limit: int = 20,
    offset: int = 0,
):
    """Listar transacciones del merchant autenticado."""
    use_case = ListTransactionsUseCase(repo)
    transactions = await use_case.execute(
        merchant_id=merchant_id,   # OWASP API1: filtra por owner, siempre
        limit=min(limit, 100),     # OWASP API4: cap de resultados
        offset=offset,
    )
    return [TransactionResponse.from_entity(t) for t in transactions]
