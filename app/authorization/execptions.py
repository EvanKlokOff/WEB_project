class Is_existing_user(Exception):
    def __int__(self, user_name: str, email_address:str):
        self.user_name = user_name
        self.email_address = email_address

    def __str__(self):
        return f"user with name:{self.user_name} and email address:{self.email_address} is exist"

class Invalid_token(Exception):
    def str(self):
        return "token invalid"

class Is_existing_token(Exception):
    def __int__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"user with id:{self.user_name} already has refresh token"


class User_doesnt_exist(Exception):
    def __int__(self, user_name: str, email_address:str):
        self.user_name = user_name
        self.email_address = email_address

    def __str__(self):
        return f"user with name:{self.user_name} and email address:{self.email_address} isn't exist"

class Update_error(Exception):
    def __int__(self, user_name: str, email_address:str):
        self.user_name = user_name
        self.email_address = email_address

    def __str__(self):
        return f"error with update user with name:{self.user_name} and email address:{self.email_address}"
