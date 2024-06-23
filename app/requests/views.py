import random
import re

from fastapi import HTTPException
from sqlalchemy.sql import exists
from starlette import status

from app.requests.models import Affinity
from app.requests.models import Request
from app.requests.models import RequestStatus
from app.requests.models import Grimorio
from sqlalchemy.orm import joinedload


def get_all_objects(db):
    """
    Get all requests
    """
    return db.query(Request).options(joinedload(Request.grimorio)).all()


def get_object(db, uuid):
    """
    Get a request by id
    """
    return db.query(Request).options(joinedload(Request.grimorio)).filter(Request.id == uuid).first()


def validate_field(value, regex_pattern):
    """
    Validate a field against a regex pattern.

    Args:
        value (str): The value to validate.
        regex_pattern (str): The regex pattern to match against.

    Returns:
        bool: True if the value matches the pattern, False otherwise.
    """
    return bool(re.match(regex_pattern, value))


def validate_request(request_data):
    name, last_name, identification, age, affinity = request_data.values()
    name_pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]{1,20}$'
    last_name_pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]{1,20}$'

    if not validate_field(name, name_pattern):
        return False

    if not validate_field(last_name, last_name_pattern):
        return False

    return True


def valid_affinity(affinity_value):
    """
    Validate the affinity value
    """
    return affinity_value in Affinity.__members__.values()


def create_obj(db, request_data):
    """
    Create a new request
    """
    is_valid = validate_request(request_data)
    affinity_value = request_data.get("affinity")
    is_valid_affinity = valid_affinity(affinity_value)

    if not is_valid_affinity:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Invalid affinity: {affinity_value}")

    request = Request(**request_data)
    request.affinity = Affinity(affinity_value)
    if not is_valid:
        # Invalid validations for name or last_name
        request.status = RequestStatus.REJECTED.value
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def request_exists(db, uuid):
    """
    Get a request by id
    """
    return db.query(exists().where(Request.id == uuid)).scalar()


def update_object(db, request_uuid, request_data):
    """
    Update a request by uuid
    """
    is_valid = validate_request(request_data)
    if not is_valid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid request data")

    affinity_value = request_data.get("affinity")
    is_valid_affinity = valid_affinity(affinity_value)

    if not is_valid_affinity:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Invalid affinity: {affinity_value}")

    db.query(Request).filter(Request.id == request_uuid).update(request_data)
    db.commit()
    return None


def status_exists(status):
    """
    Validate the status value
    """
    return status in RequestStatus.__members__.values()


def update_status(db, status, uuid):
    """
    Update the status of a request
    """
    get_status = RequestStatus(status)
    db.query(Request).filter(Request.id == uuid).update({"status": get_status})
    db.commit()
    if get_status == RequestStatus.APPROVED:
        grimorio = assign_grimorio(db)
        db.query(Request).filter(Request.id == uuid).update({"grimorio_id": grimorio.id})
        db.commit()
    return None


def delete_object(db, uuid):
    """
    Delete a request by id
    """
    db.query(Request).filter(Request.id == uuid).delete()
    db.commit()
    return None


def assign_grimorio(db):
    grimorios = db.query(Grimorio).all()
    total_ponderacion = sum(grimorio.ponderacion for grimorio in grimorios)
    random_num = random.uniform(0, total_ponderacion)
    cumulative_sum = 0
    selected_grimorio = None

    for grimorio in grimorios:
        cumulative_sum += grimorio.ponderacion
        if random_num < cumulative_sum:
            selected_grimorio = grimorio
            break

    return selected_grimorio


def get_grimoire_assignments(db):
    """
    Get all requests
    """
    return db.query(Grimorio).options(joinedload(Grimorio.requests)).all()
