import uuid

from flask_bcrypt import generate_password_hash, check_password_hash


class ModelHelper:

    @staticmethod
    def get_unique_id():
        return str(uuid.uuid4())

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def check_hash(password, hash):
        return check_password_hash(hash, password)
