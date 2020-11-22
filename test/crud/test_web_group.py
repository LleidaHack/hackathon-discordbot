import unittest
from dotenv import load_dotenv

from src.crud.firebase import Firebase
class TestWebGroup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.DB = Firebase()

    
    def test_recover_web_group_notfound(self):
        web_group = self.DB.recover_web_group('patatita')
        self.assertEqual(web_group, None)

    def test_recover_web_group_invalid(self):
        web_group = self.DB.recover_web_group(None)
        self.assertEqual(web_group, None)
    
    def test_recover_web_group_correct(self):
        from src.models.group import Group

        web_group = self.DB.recover_web_group('Descans')
        self.assertEqual(web_group.__dict__, 
            Group(name="Descans").__dict__
        )


if __name__ == '__main__':
    unittest.main()
