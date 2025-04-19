def get_object(id, list):
    for object in list:
        if object['id'] == int(id):
            return object
        
def name_to_id(name: str, list: list) -> str:
    id = -1
    for o in list:
        if name == o['name']:
            return o['id']

def create_employee(id=None, name=None, telephone=None, salary=None, boss=None, department=None) -> dict:
    return {
        'id': id,
        'name': name,
        'telephone': telephone,
        'salary': salary,
        'boss': boss,
        'department': department
    }

def create_department(id=None, name=None) -> dict:
    return {
        'id': id,
        'name': name
    }