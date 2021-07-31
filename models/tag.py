from db import db
from typing import List


class TagModel(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    mappings = db.relationship("AssignmentTagMappingModel",lazy="dynamic",primaryjoin="TagModel.id == AssignmentTagMappingModel.tag_id")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'TagModel(name=%s)' % (self.name)

    def json(self):
        return {'name': self.name}

    @classmethod
    def find_by_name(cls, name) -> "TagModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
