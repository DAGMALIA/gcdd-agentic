"""
Infrastructure Layer — CDK Stack
Governance: TODO el naming, encriptación y tags vienen del contrato de governance.
Cada recurso tiene un comentario indicando qué regla del contrato aplica.
"""

from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_kms as kms,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_sqs as sqs,
    RemovalPolicy,
    Duration,
    Tags,
)
from constructs import Construct


class NovapayPaymentsStack(Stack):
    """Stack CDK para NovaPay Payments API.

    Governance contract: .gcdd/governance/contract.yaml
    Todos los recursos siguen las reglas de naming, seguridad y tags definidas ahí.
    """

    def __init__(self, scope: Construct, id: str, environment: str = "dev", **kwargs):
        super().__init__(scope, id, **kwargs)

        # ─── GOVERNANCE: VALIDAR AMBIENTE ────────────────────────────────
        # Governance: environments.allowed = ["dev", "staging", "prod"]
        allowed_envs = ["dev", "staging", "prod"]
        if environment not in allowed_envs:
            raise ValueError(
                f"VIOLACIÓN GOVERNANCE: Ambiente '{environment}' no permitido. "
                f"Permitidos: {allowed_envs} (environments.allowed)"
            )

        # ─── KMS KEY ────────────────────────────────────────────────────
        # Governance: security.encryption.key_management = "customer-managed"
        # Governance: security.encryption.forbidden = ["S3_MANAGED", "AES256_DEFAULT"]
        encryption_key = kms.Key(
            self, "PaymentsEncryptionKey",
            alias=f"novapay-payments-key-{environment}",
            enable_key_rotation=True,  # Best practice PCI-DSS
            description="KMS CMK para datos de pagos — governance: customer-managed",
        )

        # ─── DYNAMODB TABLE ─────────────────────────────────────────────
        # Governance: naming.resources.database_table.pattern = {dominio}_{entidad}_{proposito}
        # Nombre: payments_transactions_store
        transactions_table = dynamodb.Table(
            self, "TransactionsTable",
            table_name=f"payments_transactions_store",  # snake_case per governance
            partition_key=dynamodb.Attribute(
                name="merchant_id",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="transaction_id",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED,  # NUNCA DEFAULT
            encryption_key=encryption_key,
            point_in_time_recovery=True,  # PCI-DSS: recuperación de datos
        )

        # ─── S3 BUCKET PARA AUDIT LOGS ──────────────────────────────────
        # Governance: naming.resources.s3_bucket.pattern = {prefix}-{dominio}-{proposito}-{ambiente}
        # Nombre: novapay-payments-audit-logs-{env}
        # Governance: security.network — sin acceso público
        audit_logs_bucket = s3.Bucket(
            self, "AuditLogsBucket",
            bucket_name=f"novapay-payments-audit-logs-{environment}",
            encryption=s3.BucketEncryption.KMS,              # NUNCA S3_MANAGED
            encryption_key=encryption_key,                    # KMS CMK
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Governance: prohibido público
            enforce_ssl=True,                                 # PCI-DSS Req. 4: TLS obligatorio
            versioned=True,                                   # Audit trail inmutable
            removal_policy=RemovalPolicy.RETAIN,              # Nunca borrar logs de auditoría
        )

        # ─── SQS QUEUE PARA EVENTOS ─────────────────────────────────────
        # Governance: naming.resources.sqs_queue.pattern = {prefix}-{dominio}-{evento}-{ambiente}
        # Nombre: novapay-payments-transaction-completed-{env}
        dlq = sqs.Queue(
            self, "TransactionDLQ",
            queue_name=f"novapay-payments-transaction-completed-dlq-{environment}",
            encryption=sqs.QueueEncryption.KMS,
            encryption_master_key=encryption_key,
            retention_period=Duration.days(14),
        )

        transaction_events_queue = sqs.Queue(
            self, "TransactionEventsQueue",
            queue_name=f"novapay-payments-transaction-completed-{environment}",
            encryption=sqs.QueueEncryption.KMS,               # NUNCA SQS_MANAGED
            encryption_master_key=encryption_key,
            dead_letter_queue=sqs.DeadLetterQueue(
                queue=dlq,
                max_receive_count=3,
            ),
        )

        # ─── TAGS OBLIGATORIOS ───────────────────────────────────────────
        # Governance: tags.required — TODOS estos tags son obligatorios
        required_tags = {
            "project": "novapay-payments",
            "domain": "payments",
            "environment": environment,
            "owner": "equipo-payments",
            "cost-center": "CC-PAYMENTS-001",
            "data-classification": "pci",
            "compliance": "pci-dss-v4",
        }

        for key, value in required_tags.items():
            Tags.of(self).add(key, value)
