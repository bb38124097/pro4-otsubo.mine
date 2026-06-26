from boundary.account_registration_view import AccountRegistrationView
from control.account_manager import AccountManager

view = AccountRegistrationView()
manager = AccountManager()

view.display()

user_name = view.input_user_name()

if manager.check_user_name_length(user_name):
    user = manager.register_user(user_name)
    print(f"登録完了: {user.user_name}")
else:
    print("ユーザー名は20文字以内で入力してください")