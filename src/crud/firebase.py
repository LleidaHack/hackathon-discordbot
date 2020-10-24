import firebase_admin
from models.user import User
from models.team import Team
from firebase_admin import firestore

DB_PATH_U = 'hackeps-2020/prod/users'
DB_PATH_T = 'hackeps-2020/prod/teams'
class firebase:
    def __init__(self,cert):
        self.cred = firebase_admin.credentials.Certificate(cert)
        self.db = firestore.client()
    def get_data(self,users_data,teams_data):
        teams_data=[]
        users_data={}
        users_ref = self.db.collection(DB_PATH_U)
        teams_ref = self.db.collection(DB_PATH_T)
        teams = teams_ref.stream()
        users = users_ref.stream()
        for u in users:
            u=u.to_dict()
            users_data[u['uid']]=User.from_dict(u)
            # users_data[u['uid']]=User(u['fullName'],u['email'],u['githubUrl'],u['nickname'])
        for t in teams:
            t=t.to_dict()
            tm=Team.from_dict(t)
            for m in t['members']:
                users_data[m.id].team=tm.name
                tm.add_user(users_data[m.id])
            teams_data.append(tm)