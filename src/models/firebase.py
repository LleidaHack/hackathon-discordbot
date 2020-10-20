import firebase_admin
from firebase_admin import firestore

DB_PATH = 'hackeps-2020/prod/users'
class firebase:
    def __init__(self,cert):
        cred = firebase_admin.credentials.Certificate(cert)
        self.firebase=firebase_admin.initialize_app(cred)

    def get_data(self,id=None, name=None):
        db = firestore.client()
        users_ref = db.collection(DB_PATH)
        usrs = users_ref.stream()
        for usr in usrs:
            if (id is None and name is None) or (id is not None and usr.id == id) or (name is not None and name == usr.to_dict()['fullName']):
                return usr.to_dict()