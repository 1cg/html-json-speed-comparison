import json
from dataclasses import dataclass

# ========================================================
# Contact Model
# ========================================================

@dataclass
class Contact:
    # mock contacts database
    db = {}

    id: str
    first: str
    last: str
    phone: str
    email: str

    def __init__(self, id_=None, first=None, last=None, phone=None, email=None):
        self.id = id_
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email
        self.errors = {}

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    @classmethod
    def all(cls):
        return list(cls.db.values())

    @classmethod
    def load_db(cls):
        with open('contacts.json', 'r') as contacts_file:
            contacts = json.load(contacts_file)
            cls.db.clear()
            for c in contacts:
                cls.db[c['id']] = Contact(c['id'], c['first'], c['last'], c['phone'], c['email'])

