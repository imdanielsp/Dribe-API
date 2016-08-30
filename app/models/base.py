from app import db

LAZY = 'dynamic'


class BaseModel:
    abstract = True

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    def get_dict(self):
        raise NotImplementedError

    @staticmethod
    def build_from_args(**kwargs):
        raise NotImplementedError
