# Contribuir a GCDD

¡Gracias por tu interés en contribuir a GCDD!

## Formas de contribuir

### Perfiles de Dominio
Implementa un contrato de governance para tu industria o stack tecnológico.

1. Crea un archivo YAML en `profiles/` siguiendo la estructura de `examples/governance-contract.example.yaml`
2. Incluye: naming, security, architecture, tags, scanning, deployment
3. Agrega documentación explicando las reglas específicas de tu dominio
4. Abre un PR con el perfil y un ejemplo de uso

### Ejemplos
Proyectos demo que muestren GCDD en acción.

1. Crea una carpeta en `examples/` con tu proyecto
2. Incluye el governance contract, la spec, el código generado y el reporte de validación
3. Documenta qué reglas se aplicaron y cómo

### Validadores
Código que enforce las reglas del contrato de governance.

1. Python preferido (pero cualquier lenguaje es bienvenido)
2. Cada validador recibe el contrato de governance y un artefacto a validar
3. Retorna `{"valid": true}` o `{"valid": false, "error": "...", "suggestion": "..."}`
4. Incluye tests

### Documentación
Guías, tutoriales, traducciones, mejoras al whitepaper.

### Métricas
Datos empíricos sobre la efectividad del enforcement en tu organización.
Nos interesa:
- Violaciones de governance atrapadas por capa
- Tiempo de spec a deploy con y sin GCDD
- Tasa de compliance al primer intento
- Ciclos de retrabajo reducidos

## Proceso

1. Fork el repositorio
2. Crea una branch (`git checkout -b feature/mi-contribucion`)
3. Haz tus cambios
4. Asegúrate de que la documentación esté actualizada
5. Abre un Pull Request describiendo tu contribución

## Código de Conducta

Sé respetuoso, constructivo y colaborativo. GCDD es una metodología abierta
y todas las perspectivas son valiosas.

## Preguntas

Abre un Issue con la etiqueta `question` para cualquier duda.
