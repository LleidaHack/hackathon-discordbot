import os
from typing import Union, Tuple, Dict, Optional

from firebase_admin import credentials, firestore, initialize_app

from src.models.invitation import Invitation
from src.models.team import Team
from src.models.user import User
from src.models.webuser import WebUser


class Firebase:
    def __init__(self):
        self.cred = credentials.Certificate("src\certificate.json")
        self.default_app = initialize_app(self.cred)
        self.db = firestore.client()

    def recover_web_user(self, email) -> Union[WebUser, bool]:
        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/users')
        for usr in todo_ref.stream():
            if usr.to_dict()['email'] == email:
                return WebUser(usr.to_dict()['accepted'], usr.to_dict()['birthDate'], usr.to_dict()['displayName'],
                               usr.to_dict()['email'], usr.to_dict()['fullName'], usr.to_dict()['githubUrl'],
                               usr.to_dict()['nickname'])
        return False

    def recover_web_group(self, name) -> Union[Team, bool]:
        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/teams')
        doc = todo_ref.document(name).get()
        if doc:
            return Team(doc.to_dict()['name'])
        return False

    def create_or_update_user(self, user: User) -> None:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/users')

        json = user.__dict__
        """{'username': user.username, "discriminator": user.discriminator, "id": user.discord_id,
        "email": user.email, "group": user.group_name}"""
        doc = todo_ref.document(user.discord_id)
        doc.set(json)

    def get_user(self, discord_id=None, username=None, discriminator=None) -> Union[User, bool]:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/users')
        if discord_id:
            doc = todo_ref.document(discord_id).get()
            #
            return User(doc.to_dict()['username'], doc.to_dict()['discrminator'], doc.to_dict()['id'],
                        doc.to_dict()['group'], doc.to_dict()['email'])
        else:
            for usr in todo_ref.stream():
                if (username is not None and usr.to_dict()['username'] == username) and (
                        discriminator is not None and discriminator == usr.to_dict()['discriminator']):
                    return User(usr.to_dict()['username'], usr.to_dict()['discrminator'], usr.to_dict()['id'],
                                usr.to_dict()['group'], usr.to_dict()['email'])

        return False

    def get_user_from_id(self, discord_id):
        return self.get_user(discord_id=discord_id)

    def get_user_from_name(self, username, discriminator):
        return self.get_user(username=username, discriminator=discriminator)

    def create_or_update_group(self, group: Team) -> None:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/groups')
        json = group.__dict__  # {'name': group.group_name, "members": group.users, "role_id": group.role_id}
        doc = todo_ref.document(group.name)
        doc.set(json)

    def get_group(self, group_name: str) -> Union[Team, bool]:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/groups')
        if group_name:
            doc = todo_ref.document(group_name).get()
            if doc.to_dict():
                return Team(doc.to_dict()['name'], doc.to_dict()['members'], doc.to_dict()['role_id'])
        return False

    def create_invitation(self, user_id, group_name) -> None:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        json = {'user_id': user_id, "group_name": group_name, "status": 'PENDING'}
        todo_ref.document(None).set(json)

    def get_invitation(self, user_id, group_name) -> Union[bool, Tuple[int, Invitation]]:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        for usr in todo_ref.stream():
            if usr.to_dict()['user_id'] == user_id and usr.to_dict()['group_name'] == group_name:
                invit = Invitation.from_dict(usr.to_dict())
                return usr.id, invit
        return False

    def accept_invitation(self, user_id, group_name) -> Optional[bool]:
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        invitation = self.get_invitation(user_id, group_name)
        if invitation:
            user_id, invitation = invitation
            invitation.accept()
            todo_ref.document(user_id).set(invitation)
        else:
            return False
