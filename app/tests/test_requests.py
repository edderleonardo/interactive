from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.databases.database import Base
from app.helpers.db_dependency import get_db
from app.main import app

from app.scripts.create_grimorio_fixtures import create_grimorio_fixtures

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

create_grimorio_fixtures(TestingSessionLocal())


def test_get_all_requests():
    response = client.get("/solicitudes")
    assert response.status_code == status.HTTP_200_OK
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.status_code != status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_request_empty():
    response = client.post("/solicitud", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.status_code != status.HTTP_200_OK


def test_create_request_age_not_int():
    response = client.post("/solicitud", json={
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": "abc",
        "affinity": "Agua",
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.status_code != status.HTTP_200_OK
    response = response.json()
    error_msg = response['detail'][0]['msg']
    assert error_msg == 'Input should be a valid integer, unable to parse string as an integer'


def test_create_request_invalid_affinity():
    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "BEER",
    }
    response = client.post("/solicitud", json=request_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.status_code != status.HTTP_200_OK
    response = response.json()

    error_msg = response['detail']
    assert error_msg == 'Invalid affinity: BEER'


def test_create_request_success():
    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
        "status": "Pendiente"
    }
    response = client.post("/solicitud", json=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.status_code != status.HTTP_422_UNPROCESSABLE_ENTITY
    response = response.json()
    assert response['message'] == 'Request created successfully'
    assert response['data']['name'] == 'Juan'
    assert response['data']['last_name'] == 'Perez'
    assert response['data']['identification'] == '12345678'
    assert response['data']['age'] == 25
    assert response['data']['affinity'] == 'Agua'
    assert response['data']['status'] == 'Pendiente'


def test_create_request_rejected():
    request_data = {
        "name": "María Alejandra Valentina Sofía Isabel Carolina de los Ángeles",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Luz",
    }
    response = client.post("/solicitud", json=request_data)
    uuid_created = response.json()['data']['id']

    get_object_created = client.get(f"/solicitud/{uuid_created}")
    status = get_object_created.json()['data']['status']

    assert status == 'Rechazado'


def test_update_request_found():
    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
        "status": "Pendiente"
    }

    update_data = {
        "name": "Maria",
        "last_name": "Gomez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
        "status": "Pendiente"
    }

    response = client.post("/solicitud", json=request_data)
    uuid_created = response.json()['data']['id']
    update_response = client.put(f"/solicitud/{uuid_created}", json=update_data)
    assert update_response.status_code == status.HTTP_204_NO_CONTENT
    assert update_response.status_code != status.HTTP_404_NOT_FOUND


def test_update_request_not_found():
    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
        "status": "Pendiente"
    }
    response = client.put("/solicitud/12345678", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.status_code != status.HTTP_204_NO_CONTENT


def test_update_request_with_invalid_data():
    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
        "status": "Pendiente"
    }

    response = client.post("/solicitud", json=request_data)
    uuid_created = response.json()['data']['id']

    update_data_invalid_name = {
        "name": "María Alejandra Valentina Sofía Isabel Carolina de los Ángeles",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
        "status": "Pendiente"
    }

    response = client.put(f"/solicitud/{uuid_created}", json=update_data_invalid_name)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.status_code != status.HTTP_204_NO_CONTENT


def test_update_request_invalid_affinity():
    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
    }

    response = client.post("/solicitud", json=request_data)
    uuid_created = response.json()['data']['id']

    update_data_invalid_affinity = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "BEER",
        "status": "Pendiente"
    }

    response = client.put(f"/solicitud/{uuid_created}", json=update_data_invalid_affinity)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.status_code != status.HTTP_204_NO_CONTENT
    response = response.json()
    error_msg = response['detail']
    assert error_msg == 'Invalid affinity: BEER'


def test_update_invalid_status():
    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
        "status": "Pendiente"
    }

    response = client.post("/solicitud", json=request_data)
    uuid_created = response.json()['data']['id']

    update_data_invalid_status = {
        "status": "INVALID_STATUS"
    }

    response = client.patch(f"/solicitud/{uuid_created}/estatus", json=update_data_invalid_status)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.status_code != status.HTTP_204_NO_CONTENT
    response = response.json()
    error_msg = response['detail']
    assert error_msg == 'Invalid status'


def test_update_request_status_success():
    # cargar datos de los grimorios

    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
    }

    response = client.post("/solicitud", json=request_data)

    uuid_created = response.json()['data']['id']

    update_data = {
        "status": "Aprobado"
    }

    response = client.patch(f"/solicitud/{uuid_created}/estatus", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.status_code != status.HTTP_400_BAD_REQUEST
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.json()['message'] == 'Request status updated successfully'


def test_delete_request_not_found():
    response = client.delete("/solicitud/12345678")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.status_code != status.HTTP_204_NO_CONTENT


def test_delete_request():
    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
        "status": "Pendiente"
    }
    response = client.post("/solicitud", json=request_data)
    uuid_created = response.json()['data']['id']

    response = client.delete(f"/solicitud/{uuid_created}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.status_code != status.HTTP_404_NOT_FOUND


def test_assign_grimorio():
    request_data = {
        "name": "Juan",
        "last_name": "Perez",
        "identification": "12345678",
        "age": 25,
        "affinity": "Agua",
        "status": "Pendiente"
    }

    response = client.post("/solicitud", json=request_data)
    uuid_created = response.json()['data']['id']

    update_data = {
        "status": "Aprobado"
    }

    response = client.patch(f"/solicitud/{uuid_created}/estatus", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.status_code != status.HTTP_400_BAD_REQUEST
    assert response.status_code != status.HTTP_404_NOT_FOUND
    assert response.json()['message'] == 'Request status updated successfully'

    # verify if grimorio was assigned
    get_object_created = client.get(f"/solicitud/{uuid_created}")

    grimorio_assigned = get_object_created.json()['data']['grimorio']

    assert grimorio_assigned is not None
