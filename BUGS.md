# QA Engineer Assessment – API Testing

## Descripción general

Este repositorio contiene pruebas automatizadas de una API REST desarrolladas como parte de una evaluación técnica para el rol de **QA Engineer**.

El objetivo del proyecto es validar el comportamiento real de la API, identificar inconsistencias en la implementación y documentar dichos hallazgos de forma clara y reproducible mediante pruebas automatizadas.

---

## Stack tecnológico

| Tecnología | Uso |
|----------|-----|
| Python 3.9 | Lenguaje base |
| FastAPI | Framework de la API |
| Pytest | Framework de testing |
| Starlette TestClient | Cliente para pruebas HTTP |
| JWT | Autenticación |

---

## Ejecución de pruebas

1. Crear y activar un entorno virtual
2. Instalar dependencias
3. Ejecutar pytest

```bash
python3 -m pytest
Enfoque de testing
Las pruebas fueron diseñadas para:

Validar flujos positivos y negativos

Confirmar códigos de respuesta HTTP reales

Detectar comportamientos inconsistentes

Documentar resultados sin asumir comportamientos ideales

El objetivo no fue forzar fallos, sino reflejar fielmente el comportamiento actual del sistema.

Cobertura de pruebas
Las pruebas cubren los siguientes endpoints:

Área	Endpoint
Salud del sistema	GET /health
Productos	POST /products
Productos	PUT /products/{id}
Productos	DELETE /products/{id}
Inventario	POST /inventory/adjust

Comportamientos observados
Durante la ejecución de las pruebas se identificaron los siguientes comportamientos relevantes.

OBS-001 – Creación de producto retorna 422 por campo quantity
Endpoint:
POST /products

Comportamiento observado:
La API retorna 422 Unprocessable Entity cuando el campo quantity no está presente en el cuerpo de la solicitud, aunque se envíe stock.

Ejemplo de request:

json
Copiar código
{
  "name": "Producto QA",
  "description": "Producto de prueba",
  "price": 25,
  "stock": 10
}
Respuesta:
422 Unprocessable Entity

Análisis QA:
El esquema de validación del endpoint requiere explícitamente el campo quantity.
Este comportamiento fue documentado y validado por las pruebas.

OBS-002 – Actualización de producto inexistente retorna 404
Endpoint:
PUT /products/{id}

Comportamiento observado:
Al intentar actualizar un producto que no existe, la API retorna:

404 Not Found

Análisis QA:
El comportamiento es consistente y alineado con prácticas REST.

OBS-003 – Ajuste de inventario con producto inexistente retorna 422
Endpoint:
POST /inventory/adjust

Ejemplo de request:

json
Copiar código
{
  "product_id": 99999,
  "quantity": 5
}
Respuesta:
422 Unprocessable Entity

Análisis QA:
La validación del body ocurre antes de verificar la existencia del producto, por lo que no se retorna 404.

OBS-004 – Eliminación de producto inexistente retorna 204
Endpoint:
DELETE /products/{id}

Comportamiento observado:
La API retorna 204 No Content aun cuando el producto no existe.

Análisis QA:
No se valida la existencia del recurso antes de responder exitosamente.

Organización de pruebas
Archivo	Descripción
test_api.py	Casos principales de la API
test_short.py	Pruebas compactas de endpoints clave
test_example.py	Prueba de referencia
conftest.py	Fixtures comunes y setup

Notas de QA
Las pruebas reflejan el comportamiento real, no el ideal

Los códigos HTTP fueron documentados tal como responde la API

Los escenarios inconsistentes se registraron como observaciones

El enfoque prioriza trazabilidad y claridad técnica

Conclusión
Este proyecto demuestra:

Capacidad para diseñar pruebas automatizadas de API

Identificación de inconsistencias funcionales

Documentación clara y profesional de hallazgos

Criterio QA aplicado a sistemas reales