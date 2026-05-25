# Origen: Por qué existe GCDD

## El vacío en Spec-Driven Development

Para mediados de 2025, SDD había resuelto la primera crisis de la ingeniería asistida por AI: el intent drift. Herramientas como GitHub Spec Kit, BMAD y Kiro dieron a los equipos una forma de escribir specs antes del código, reduciendo el problema de output "plausible pero incorrecto".

Pero los equipos en industrias reguladas y entornos enterprise seguían chocando con la misma pared: **la spec no conoce tus reglas.**

Una spec dice "crea un bucket S3 para datos raw." No dice "el bucket debe llamarse `{prefix}-{dominio}-raw-{env}`, encriptado con KMS CMK (nunca S3_MANAGED), taggeado con `proyecto`, `owner`, `dominio`, `centro-costo` y `clasificacion-datos`, desplegado solo en `us-east-1`, sin acceso público." Esas reglas existen en wikis corporativas, políticas de seguridad, registros de decisiones arquitectónicas y las cabezas de ingenieros senior — en ningún lugar que el agente AI pueda consumir.

El resultado fue predecible: los agentes AI generaban código que pasaba la validación de spec pero violaba estándares organizacionales. Los equipos gastaban más tiempo corrigiendo problemas de compliance de lo que ahorraban con la generación AI. La promesa de SDD — de spec a código en horas — se rompía en cualquier entorno con requisitos reales de governance.

## Tres descubrimientos

GCDD se cristalizó a partir de tres descubrimientos hechos en producción:

### 1. Los prompts son sugerencias, las herramientas son restricciones

Decirle a un agente AI "no uses encriptación S3_MANAGED" en un system prompt funciona la mayoría del tiempo. Pero cuando un usuario dice "solo crea un bucket simple, no te preocupes por la encriptación", el agente prioriza ser servicial sobre sus instrucciones. Pasa aproximadamente el 20-30% del tiempo — suficiente para destruir la confianza.

La solución: codificar la regla en la herramienta misma. Cuando `create_bucket()` rechaza `S3_MANAGED` y retorna un error con "Usa KMS CMK en su lugar", el agente físicamente no puede violar la política. El enforcement se mueve de conductual (esperar que la AI obedezca) a estructural (la AI no tiene opción).

### 2. Los límites de rol requieren infraestructura, no instrucciones

Frameworks multi-agente como BMAD definen 12+ roles especializados: PM, Arquitecto, Desarrollador, QA. Pero las definiciones de rol viven en archivos markdown — son prompts. Cuando un usuario le pide al agente "Navigator" que genere código, el agente lo hace porque puede. Las herramientas están disponibles, el usuario pidió, y el modelo quiere ser servicial.

La solución: cada rol recibe una whitelist de herramientas que puede invocar. El Navigator tiene acceso a `list_domains()` y `explain_workflow()`, pero no a `generate_code()`. Cuando el Navigator intenta llamar una herramienta fuera de su whitelist, el sistema retorna "Herramienta no autorizada para este rol. Redirige al Builder." Esto es enforcement a nivel de infraestructura, no a nivel de prompt.

### 3. La arquitectura debe seleccionarse, no inventarse

Los agentes AI eligen patrones arquitectónicos basándose en sus datos de entrenamiento. Pide una API web y obtendrás arquitectura por capas — porque es lo que aparece con más frecuencia en los ejemplos de entrenamiento. Pero si tu organización estandariza en arquitectura hexagonal para servicios con dominio pesado, o event-driven para pipelines de datos, la AI no sabe eso.

La solución: definir un catálogo gobernado de patrones arquitectónicos con reglas de selección. "Cuando el proyecto tiene 3+ integraciones externas y lógica de dominio compleja, usar hexagonal. Cuando es procesamiento asíncrono con múltiples consumidores, usar event-driven." El agente selecciona del catálogo basándose en las características del proyecto, en vez de inventar desde datos de entrenamiento.

## De descubrimientos a metodología

Estos tres descubrimientos — herramientas como restricciones, límites de rol como infraestructura, arquitectura como selección — formaron el core de GCDD. Todo lo demás en la metodología se deriva de ellos:

- El **Contrato de Governance** es cómo las organizaciones codifican sus reglas en un formato legible por máquina que las herramientas pueden consumir.
- La **Generación Constrañida** es el principio de que el governance se enforza por herramientas, no por prompts.
- Los **Perfiles de Dominio** permiten a las organizaciones empaquetar sus contratos de governance para reuso entre equipos y proyectos.
- El **Enforcement de Tres Capas** asegura defensa en profundidad: prompt (awareness), autorización de herramientas (límites de rol), estructural (reglas de governance).
- Los **Niveles de Ceremonia** aseguran que la metodología escale hacia abajo para cambios pequeños y hacia arriba para deployments regulados.

GCDD no reemplaza SDD — agrega la capa de governance que SDD asume que alguien más manejará. Y no reemplaza frameworks multi-agente como BMAD — provee el mecanismo de enforcement que hace que la especialización de roles realmente funcione.
