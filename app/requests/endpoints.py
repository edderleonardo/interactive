from fastapi import APIRouter
from fastapi import Path
from fastapi import HTTPException
from starlette import status
from typing import List
from app.helpers.db_dependency import db_dependency

from app.requests.schemas import RequestCreate
from app.requests.schemas import RequestUpdate
from app.requests.schemas import RequestUpdateStatus
from app.requests.views import create_obj
from app.requests.views import request_exists
from app.requests.views import update_object
from app.requests.views import update_status
from app.requests.views import status_exists
from app.requests.views import get_all_objects
from app.requests.views import get_object
from app.requests.views import delete_object
from app.requests.views import get_grimoire_assignments

from app.scripts.create_grimorio_fixtures import create_grimorio_fixtures

router = APIRouter()


# Create grimorios fixtures
@router.get("/create-grimorios-fixtures", status_code=status.HTTP_200_OK)
async def create_grimorios_fixtures(db: db_dependency):
    """
    Create grimorios fixtures
    """
    create_grimorio_fixtures(db)
    return {
        "message": "Grimorios fixtures created successfully"
    }


@router.get("/solicitudes", status_code=status.HTTP_200_OK)
async def get_all_requests(db: db_dependency):
    """
    Get all requests
    """
    objects = get_all_objects(db)
    return {
        "message": "Requests retrieved successfully",
        "data": objects
    }


@router.get("/solicitud/{uuid}", status_code=status.HTTP_200_OK)
async def get_request(db: db_dependency, uuid: str):
    """
    Get a request by id
    """
    existing_request = request_exists(db, uuid)

    if not existing_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

    return {
        "message": "Request retrieved successfully",
        "data": get_object(db, uuid)
    }


@router.post("/solicitud", status_code=status.HTTP_200_OK)
async def create_request(db: db_dependency, request_data: RequestCreate):
    """
    Create a new request
    """
    request_data = request_data.model_dump()
    response = create_obj(db, request_data)
    return {
        "message": "Request created successfully",
        "data": response
    }


@router.put("/solicitud/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def update_request(db: db_dependency, request_data: RequestUpdate, uuid: str):
    """
    Get a request by id
    """
    existing_request = request_exists(db, uuid)

    if not existing_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    request_data = request_data.model_dump()
    update_object(db, uuid, request_data)
    return {
        "message": "Request updated successfully"
    }


@router.patch("/solicitud/{uuid}/estatus", status_code=status.HTTP_200_OK)
async def update_request_status(db: db_dependency, uuid: str, new_status: RequestUpdateStatus):
    """
    Update the status of a request
    """
    existing_request = request_exists(db, uuid)

    if not existing_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

    new_status = new_status.model_dump().get("status")
    is_valid_status = status_exists(new_status)
    if not is_valid_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")

    update_status(db, new_status, uuid)
    return {
        "message": "Request status updated successfully"
    }


@router.delete("/solicitud/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(db: db_dependency, uuid: str):
    """
    Delete a request by id
    """
    existing_request = request_exists(db, uuid)

    if not existing_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    delete_object(db, uuid)


@router.get("/asignaciones", status_code=status.HTTP_200_OK)
async def get_all_assignments(db: db_dependency):
    """
    Get all requests
    """
    objects = get_grimoire_assignments(db)
    return {
        "message": "Assignments retrieved successfully",
        "data": objects
    }