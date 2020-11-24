class Invitation:

    def __init__(self, user_id: str, group_name: str):
        self.user_id: str = user_id
        self.group_name: str = group_name
        self.status: str = 'PENDING'

    def accept(self):
        self.status: str = 'ACCEPTED'

    def is_pending(self):
        return self.status == 'PENDING'
    @staticmethod
    def from_dict(entries):
        invitation = Invitation(entries['user_id'], entries['group_name'])
        if entries['status'] != 'PENDING':
            invitation.accept()
        return invitation

    def __str__(self):
        return f'Target: {self.user_id}, GroupName: {self.group_name}, status: {self.status}'