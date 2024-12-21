import secrets
from hashlib import sha512

class User:
    def __init__(self, id, display_name, email=None, height=None, weight=None, password=None, session_key=None, password_hash=None):
        """

        @param id:
        @param display_name:
        @param email:
        @param height:
        @param weight:
        @param password:
        @param session_key:
        """
        self.id = id
        self.display_name = display_name
        self.email = email
        self.height = height
        self.weight = weight
        if password is not None:
            self.__password_hash = str(sha512(password.encode()).hexdigest())
        else:
            self.__password_hash = password_hash
        self.__session_key = session_key

    def match_password(self, password):
        return str(sha512(password.encode()).hexdigest()) == self.__password_hash

    def create_session_key(self):
        self.__session_key = secrets.token_hex(64)
        return self.__session_key

    def match_session_key(self, session_key):
        if self.__session_key is None or self.__session_key == "NA" :
            return False
        return self.__session_key == session_key

    def reset_session_key(self):
        self.__session_key = "NA"

    def set_password(self, password):
        if password is not None:
            self.__password_hash = str(sha512(password.encode()).hexdigest())
