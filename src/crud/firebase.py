import os
import logging
from src.crud.db_modules.csv import CSVDataBase
from src.crud.db_modules.hackeps import HackEPSDataBase
from src.crud.db_modules.db_module import WEB_DATABASE

from typing import Union, Tuple, Dict, Optional, List

from firebase_admin import credentials, firestore, initialize_app
import  src.crud.db_modules
from src.models.invitation import Invitation
from src.models.group import Group
from src.models.user import User
from src.models.webuser import WebUser
class WebDatabase:
    def __init__(self):
        self.authentication_type = os.getenv('USER_AUTHTYPE')
        self.web_database = None
        print(f'{self.authentication_type} INICIALIZADO .....')
        if self.authentication_type == 'hackeps':
            self.web_database = HackEPSDataBase()
        elif self.authentication_type == 'csv':
            self.web_database = CSVDataBase()

    def recover_web_group_and_user(self, email):
        return self.web_database.recover_web_group_and_user(email)
    def recover_web_group(self, group_name):
        return self.web_database.recover_web_group(group_name)

class BotDatabase:
    def __init__(self):
        self.default_app = initialize_app()
        self.db = firestore.client()

    def create_or_update_user(self, user: User) -> None:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/users')

        json = user.__dict__
        """{'username': user.username, "discriminator": user.discriminator, "id": user.discord_id,
        "email": user.email, "group_name": user.group_name}"""
        doc = todo_ref.document(str(user.discord_id))
        doc.set(json)


    def get_user(self, discord_id=None, username=None, discriminator=None, email=None) -> Union[User, bool]:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/users')
        if discord_id:
            doc = todo_ref.document(str(discord_id)).get()
            print(doc.to_dict())
            return User(doc.to_dict()['username'], doc.to_dict()['discriminator'], doc.to_dict()['discord_id'],
                    doc.to_dict()['group_name'], doc.to_dict()['email']) if doc.to_dict() else None

        else:
            for usr in todo_ref.stream():
                if (username is not None and usr.to_dict()['username'] == username) and (
                        discriminator is not None and discriminator == usr.to_dict()['discriminator']) or usr.to_dict()['email'] == email:
                    return User(usr.to_dict()['username'], usr.to_dict()['discriminator'], usr.to_dict()['discord_id'],
                                usr.to_dict()['group_name'], usr.to_dict()['email'])

        return None

    def get_user_from_id(self, discord_id):
        return self.get_user(discord_id=discord_id)


    def get_user_from_name(self, username, discriminator):
        return self.get_user(username=username, discriminator=discriminator)

    def create_or_update_group(self, group: Group) -> None:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/groups')
        json = group.__dict__  # {'name': group.group_name, "members": group.users, "role_id": group.role_id}
        doc = todo_ref.document(group.name)
        doc.set(json)

    def get_group(self, group_name: str) -> Optional[Group]:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/groups')
        if group_name:
            doc = todo_ref.document(group_name).get()
            if doc.to_dict():
                return Group(doc.to_dict()['name'], doc.to_dict()['members'], doc.to_dict()['role_id'])
        return None

    def create_invitation(self, user_id, group_name) -> None:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        json = {'user_id': user_id, "group_name": group_name, "status": 'PENDING'}
        todo_ref.document(str(user_id) + group_name).set(json)

    def get_invitations(self, user_id) -> List[Tuple[int, Invitation]]:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        res = []
        for usr in todo_ref.stream():
            if usr.to_dict()['user_id'] == user_id:
                invit = Invitation.from_dict(usr.to_dict())
                res.append((usr.id, invit))
        return res

    def get_invitation(self, user_id, group_name) -> Optional[Tuple[int, Invitation]]:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        for usr in todo_ref.stream():
            if usr.to_dict()['user_id'] == user_id and usr.to_dict()['group_name'] == group_name:
                invit = Invitation.from_dict(usr.to_dict())
                return usr.id, invit
        return None

    def accept_invitation(self, user_id, group_name) -> Optional[bool]:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        invitation = self.get_invitation(user_id, group_name)
        if invitation:
            user_id, invitation = invitation
            invitation.accept()
            todo_ref.document(user_id).set(invitation.__dict__)
            return True
        return False

    def delete_group (self, group_name):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/groups')
        if group_name:
            doc = todo_ref.document(group_name)
            if doc:
                doc.delete()