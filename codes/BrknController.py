from flask import request

class BrknController:
    def handle(self):
        data = request.get_json()
        user = self.find_user(data['user_id'])
        if user is None
            raise Exception('user not found')
        token = generate_token(user.id)
        return {'token': token}
