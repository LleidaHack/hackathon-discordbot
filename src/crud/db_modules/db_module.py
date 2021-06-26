from abc import ABC, abstractmethod
from typing import Union
from src.models.group import Group
from src.models.webuser import WebUser


class WEB_DATABASE(ABC):
    @abstractmethod
    def recover_web_user(self, email) -> Union[WebUser, bool]:
        pass

    @abstractmethod
    def recover_web_group(self, name) -> Union[Group, bool]:
        pass

    @abstractmethod
    def recover_web_group_and_user(self, email):
        pass
