import json

person = {
    'name': 'Bert',
    'age': 27,
    'hobbies': ['Football', 'Rugby', 'Tennis']
}

personStr = json.dumps(person, indent=4)

with open("readme.txt", "w") as f:
    f.write(personStr)

with open("readme.txt") as f:
    personReadStr = f.read()
    new_person = json.loads(personReadStr)
    
    print(new_person['name'])