
class TestJoke():
    
    def __init__(self, interface):
        self.interface = interface

    async def run_tests(self):
        await self.test_not_working()   

    async def test_not_working(self):
        await self.interface.assert_reply_equals("eps!joke", "Aixó vull que peti")