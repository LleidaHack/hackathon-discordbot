import toml
config = toml.load('config.toml')
import logging
from src.crud.db_modules.db_module import WEB_DATABASE
import os

from typing import Union
from src.models.webuser import WebUser
from src.models.group import Group
import pandas as pd


class CSVDataBase(WEB_DATABASE):
    def __init__(self) -> None:
        self.csv_path = config['CSV_PATH']
        self.users_reader = pd.read_csv(self.csv_path)
    def recover_web_user(self, email) -> Union[WebUser, bool]:
        user = self.users_reader.loc[self.users_reader['email'] == email]
        logging.info(f'Buscando por el usuario con mail {email}')
        if user.values.any():
            logging.info(f'usuario encontrado: {user}')
            web_user = WebUser(accepted=user['accepted'], birthDate=user['birthDate'], displayName=user['displayName'], email=email, fullName=f"{user['name']} {user['lastname']}",
                githubUrl=user['githubUrl'],nickname=user['nickname'])
            return web_user
        return None

    def recover_web_group(self, name) -> Union[Group, bool]:
        return None

    def recover_web_group_and_user(self, email):
        return self.recover_web_user(email), None