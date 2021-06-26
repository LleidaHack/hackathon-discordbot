from src.crud.db_modules.db_module import WEB_DATABASE
from typing import Union, Tuple, Dict, Optional, List
import os
from firebase_admin import credentials, firestore, initialize_app
from src.models.webuser import WebUser
from src.models.group import Group

class HackEPSDataBase(WEB_DATABASE):
    def __init__(self) -> None:
        self.cred = credentials.Certificate("src/certificate.json")
        self.default_app = initialize_app(self.cred)
        self.db = firestore.client()

    def recover_web_user(self, email) -> Union[WebUser, bool]:
        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/users')
        for usr in todo_ref.stream():
            if usr.to_dict()['email'] == email:
                return WebUser(usr.to_dict()['accepted'], usr.to_dict()['birthDate'], usr.to_dict()['displayName'],
                               usr.to_dict()['email'], usr.to_dict()['fullName'], usr.to_dict()['githubUrl'],
                               usr.to_dict()['nickname'])
        return None

    def recover_web_group(self, name) -> Union[Group, bool]:
        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/teams')
        doc = todo_ref.document(name).get()
        return Group(doc.to_dict()['name']) if doc.to_dict() else None

    def recover_web_group_and_user(self, email):
        users_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/users')
        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/teams')
        for grp in todo_ref.stream():
            members = grp.to_dict()['members']
            for member in members:
                user = users_ref.document(member.id).get().to_dict()
                if user['email'] == email:
                    return WebUser(user['accepted'], user['birthDate'], user['displayName'],
                               user['email'], user['fullName'], user['githubUrl'],
                               user['nickname']), Group(grp.to_dict()['name'])
        return self.recover_web_user(email), None