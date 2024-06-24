# La comunidad del trebol ☘️

Este proyecto es una aplicación para gestionar las solitudes que se reciben en la comunidad del trebol. 

## Requisitos

Existen dos maneras de correr el proyecto, la primera es de manera local y la segunda es con Docker. 
A continuación se detallan los requisitos para cada una de ellas.

### Para la manera local:

Requisitos

- Python 3.11

Instalar las dependencias:

```bash
pip install -r requirements.txt
```
Visitar localhost:8000 en tu navegador.

### Tests
Para correr los tests de la aplicación, correr el siguiente comando:

```bash
pytest
```

### Para la manera con Docker:

Requsitos

- Docker
- Docker Compose

Correr el siguiente comando:

```bash
docker compose -f local.yml up --build
```

Visitar localhost:8000 en tu navegador.

### Tests
Para correr los tests de la aplicación, correr el siguiente comando:

```bash
docker compose -f local.yml run --rm server pytest
``` 


##  Descripción de los endpoints

### GET /create_grimorios_fixtures_create_grimorios_fixtures
- Crea los grimorios de prueba. IMPORTANTE: Este endpoint es el primero que se debe correr para poder crear los grimorios

### GET /solicitudes
- Devuelve todas las solicitudes.

### GET /solicitud/{uuid}
- Devuelve una solicitud en particular.

### PUT /solicitud/{uuid}
- Actualiza una solicitud.

### DELETE /solicitud/{uuid}
- Elimina una solicitud.

### POST /solicitud
- Crea una solicitud.

### PATCH /solicitud/{uuid}/status
- Actualiza el estado de una solicitud. Cuando el status es aceptado, se crea una asignación para un grimorio. 

### GET /asignaciones
- Devuelve todas las asignaciones.





