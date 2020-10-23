from firebase_admin import credentials, firestore, initialize_app
import os
class Firebase:
    def __init__(self):
        self.cred = credentials.Certificate('src\certificate.json')
        self.default_app = initialize_app(self.cred)
        self.db = firestore.client()
    
    def recoverWebUser(self, email):
        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/users')
        for usr in todo_ref.stream():
            if (usr.to_dict()['email'] == email):
                return usr.id, usr.to_dict()
        return False
    def recoverWebGroup(self, name):
        todo_ref = self.db.collection(os.getenv('HACKESP2020_DB_PATH') + '/teams')
        doc = todo_ref.document(name).get()
        if doc:
            return doc.to_dict()
        return False
    def createOrUpdateUser(self, username, discriminator, discord_id, email = "", group=None):
        if group:
            self.addUserToGroup(group, discord_id)
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/users')

        json = {'username':username,"discriminator":discriminator,"id": discord_id,"email": email,"group": group}
        doc = todo_ref.document(discord_id)
        doc.set(json)
        pass

    def getUser(self, discord_id = None, username = None, discriminator = None):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/users')
        if discord_id:
            doc = todo_ref.document(discord_id).get()
            return doc.to_dict()
        else:
            for usr in todo_ref.stream():
                if (username is not None and usr.to_dict()['username'] == username) and (discriminator is not None and discriminator == usr.to_dict()['discriminator']):
                    return usr.id, usr.to_dict()
        return False
    def joinGroup(self, discord_id, group_name):
        user = self.getUser(discord_id=discord_id)
        if user:
            self.createOrUpdateUser(user['username'], user['discriminator'], user['id'], user['email'], group_name)
        else: return False
    def leaveGroup(self, discord_id):
        user = self.getUser(discord_id=discord_id)
        if user:
            self.createOrUpdateUser(user['username'], user['discriminator'], user['id'], user['email'], '')
        else: return False
        
    def createOrUpdateGroup(self, group_name = None, users = None, role_id=None, json=None):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/groups')

        if not json:
            json = {'name':group_name, "members":users, "role_id":role_id}
        doc = todo_ref.document(group_name)
        doc.set(json)

    def getGroup(self, group_name):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/groups')
        if group_name:
            doc = todo_ref.document(group_name).get()
            return doc.to_dict()
        return False

    def addUserToGroup(self, group_name, user_id):
        group = self.getGroup(group_name)
        print(group)
        print(len(group["members"]))
        if group and len(group["members"]) < 4:
            group['members'].append(user_id)
            self.createOrUpdateGroup(group_name = group_name, json=group)
        return False

    def removeUserToGroup(self, group_name, user_id):
        group = self.getGroup(group_name)
        if group and user_id in group["members"]:
            group['members'].remove(user_id)
            self.createOrUpdateGroup(group_name = group_name, json=group)
        return False

    def createInvitation(self, user_id, group_name):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')

        json = {'user_id':user_id,"group_name":group_name,"status": 'PENDING'}
        todo_ref.document(None).set(json)

    def recoverInvitation(self, user_id, group_name):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        for usr in todo_ref.stream():
            if (usr.to_dict()['user_id'] == user_id and usr.to_dict()['group_name'] == group_name):
                return (usr.id, usr.to_dict())
        return False
    def acceptInvitation(self, user_id, group_name):
        todo_ref = self.db.collection(os.getenv('DISCORD_DB_PATH') + '/invite')
        invitation = self.recoverInvitation(user_id, group_name)
        if invitation:
            invitation[1]['status'] = "ACCEPTED"
            todo_ref.document(invitation[0]).set(invitation[1]) 
        else: return False
                