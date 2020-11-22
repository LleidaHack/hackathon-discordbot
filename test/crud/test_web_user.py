import unittest
from dotenv import load_dotenv

from src.crud.firebase import Firebase
class TestWebUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.DB = Firebase()

    
    def test_recover_web_user_notfound(self):
        web_user = self.DB.recover_web_user('personadelmonton@gmail.com')
        self.assertEqual(web_user, None)

    def test_recover_web_user_invalid(self):
        web_user = self.DB.recover_web_user(32434)
        self.assertEqual(web_user, None)
        web_user = self.DB.recover_web_user(None)
        self.assertEqual(web_user, None)
    
    def test_recover_web_user_correct(self):
        from src.models.webuser import WebUser

        web_user = self.DB.recover_web_user('vitorlui@gmail.com')
        self.assertEqual(web_user.__dict__, 
            WebUser(accepted="YES",
                birthDate="1990-01-14", 
                displayName=None, 
                email="vitorlui@gmail.com",
                fullName="Vítor Luiz da Silva", 
                githubUrl="github.com/vitorlui", 
                nickname="VitorLui"
            ).__dict__
        )


if __name__ == '__main__':
    unittest.main()
