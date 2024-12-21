import unittest
from src.model.User import User
from src.db.UserRepository import UserRepository

class NutrikitUser(unittest.TestCase) :
    def test_1_create_user(self) :
        user = User(
            id = "jheel",
            display_name = "Jheel Patel",
            email="jp9959@g.rit.edu",
            height = 55.0,
            password="1234567"
        )
        UserRepository.create(user)
        user = User(
            id="ahad",
            display_name="Ahad Khan",
            email="ak7160@rit.edu",
            height=5.5,
            password="345672"
        )
        UserRepository.create(user)

    def test_1_update_user(self) :
        user = User(
            id = "jheel",
            display_name = "Jheel",
            email="jp9959@rit.edu",
            height = 5.7,
            weight = 55.0,
        )
        UserRepository.update(user)

    def test_2_get_user_by_id(self):
        user = UserRepository.get_by_id("jheel")
        print(user.__dict__)

    def test_2_list_all_users(self):
        users = UserRepository.get_all()
        print([user.__dict__ for user in users])

    def test_3_delete_user(self):
        user = UserRepository.get_by_id("jheel")
        print(UserRepository.delete(user))

    def test_4_check_password_and_session(self):
        user = UserRepository.get_by_id("ahad")
        self.assertTrue(user.match_password("345672"))
        session_key = user.create_session_key()
        UserRepository.update(user)
        self.assertTrue(user.match_session_key(session_key))
        user.reset_session_key()
        self.assertFalse(user.match_session_key(session_key))