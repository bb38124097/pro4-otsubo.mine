from entity.user import User

class AccountManager:
    def __init__(self):
        self.users = []

    def check_user_name_length(self, user_name):
        return len(user_name) <= 20

    def register_user(self, user_name):
        account_id = len(self.users) + 1
        user = User(account_id, user_name)
        self.users.append(user)
        return user