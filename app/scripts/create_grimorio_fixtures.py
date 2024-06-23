import uuid

from app.requests.models import Grimorio


def create_grimorio_fixtures(db):

    exist_objects = db.query(Grimorio).all()
    print(exist_objects)
    if exist_objects:
        return

    grimorios_data = [
        {"tipo_trebol": 1, "ponderacion": 60, "name": "Grimorio de un trébol"},
        {"tipo_trebol": 2, "ponderacion": 25, "name": "Grimorio de dos tréboles"},
        {"tipo_trebol": 3, "ponderacion": 10, "name": "Grimorio de tres tréboles"},
        {"tipo_trebol": 4, "ponderacion": 4, "name": "Grimorio de cuatro tréboles"},
        {"tipo_trebol": 5, "ponderacion": 1, "name": "Grimorio de cinco tréboles"},
    ]

    for grimorio_data in grimorios_data:
        grimorio = Grimorio(
            id=str(uuid.uuid4()),  # Genera un UUID para cada grimorio
            tipo_trebol=grimorio_data["tipo_trebol"],
            ponderacion=grimorio_data["ponderacion"],
            name=grimorio_data["name"]
        )
        db.add(grimorio)

    db.commit()
