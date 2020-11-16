import os
import logging

from firebase_admin import credentials, firestore, initialize_app

from models.team import Team
from models.user import User
from models.webuser import WebUser
import re

class Firebase:
    def __init__(self):
        self.cred = credentials.Certificate("src/certificate.json")
        self.default_app = initialize_app(self.cred)
        self.db = firestore.client()

    def recoverWebUser(self, email):
        logging.info("FIREBASE - Looking for "+  email)

        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/users')
        for usr in todo_ref.stream():
            if usr.to_dict()['email'] == email:
                return WebUser(usr.to_dict()['accepted'], usr.to_dict()['birthDate'], usr.to_dict()['displayName'],
                               usr.to_dict()['email'], usr.to_dict()['fullName'], usr.to_dict()['githubUrl'],
                               usr.to_dict()['nickname'])
        return False

    def recoverWebGroup(self, name):
        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/teams')
        doc = todo_ref.document(name).get()
        if doc:
            return Team(doc.to_dict()['name'])
        return False

    def recoverWebGroupByUser(self, email):
        users_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/users')
        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/teams')
        for grp in todo_ref.stream():
            members = grp.to_dict()['members']
            for member in members:
                user = users_ref.document(member.id).get().to_dict()
                if user['email'] == email:
                    return WebUser(user['accepted'], user['birthDate'], user['displayName'],
                               user['email'], user['fullName'], user['githubUrl'],
                               user['nickname']), Team(grp.to_dict()['name'])
        return self.recoverWebUser(email), None
    def createOrUpdateUser(self, user: User):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/users')

        json = {'username': user.username, "discriminator": user.discriminator, "id": user.discord_id,
                "email": user.email, "group": user.group_name}
        doc = todo_ref.document(str(user.discord_id))
        doc.set(json)
        pass

    def getUser(self, discord_id=None, username=None, discriminator=None, email = None):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/users')
        if discord_id:
            doc = todo_ref.document(discord_id).get()
            #
            return User(doc.to_dict()['username'], doc.to_dict()['discrminator'], doc.to_dict()['id'],
                        doc.to_dict()['group'], doc.to_dict()['email'])
        else:
            for usr in todo_ref.stream():
                if (username is not None and usr.to_dict()['username'] == username) and (
                        discriminator is not None and discriminator == usr.to_dict()['discriminator']) or usr.to_dict()['email'] == email:
                    return User(usr.to_dict()['username'], usr.to_dict()['discriminator'], usr.to_dict()['id'],
                                usr.to_dict()['group'], usr.to_dict()['email'])

        return False

    def createOrUpdateGroup(self, group: Team):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/groups')

        json = {'name': group.group_name, "members": group.members, "role_id": group.role_id}

        doc = todo_ref.document(group.group_name)
        doc.set(json)

    def getGroup(self, group_name):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/groups')
        if group_name:
            doc = todo_ref.document(group_name).get()
            if doc.to_dict():
                return Team(doc.to_dict()['name'], doc.to_dict()['members'], doc.to_dict()['role_id'])
        return False

    def createInvitation(self, user_id, group_name):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        json = {'user_id': user_id, "group_name": group_name, "status": 'PENDING'}
        todo_ref.document(None).set(json)

    def recoverInvitation(self, user_id, group_name):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        for usr in todo_ref.stream():

            if usr.to_dict()['user_id'] == user_id and usr.to_dict()['group_name'] == group_name:
                return (usr.id, usr.to_dict())
        return False

    def acceptInvitation(self, user_id, group_name):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        invitation = self.recoverInvitation(user_id, group_name)
        if invitation:
            invitation[1]['status'] = "ACCEPTED"
            todo_ref.document(invitation[0]).set(invitation[1])
        else:
            return False
