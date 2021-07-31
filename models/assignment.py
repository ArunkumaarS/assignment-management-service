from db import db
from typing import List


class AssignmentModel(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False, unique=False)
    description = db.Column(db.String(256), nullable=True, unique=False)
    assignment_type = db.Column(db.String(256), nullable=False, unique=False)
    duration = db.Column(db.Integer, nullable=False, unique=False)
    mappings = db.relationship("AssignmentTagMappingModel",lazy="dynamic",primaryjoin="AssignmentModel.id == AssignmentTagMappingModel.assignment_id")

    def __init__(self, name, title, description, assignment_type, duration):
        self.name = name
        self.title = title
        self.description = description
        self.assignment_type = assignment_type
        self.duration = duration

    def __repr__(self):
        return 'AssignmentModel(name=%s, title=%s,description=%s,type=%s,duration=%s)' % (self.name,self.title,self.description,self.assignment_type,self.duration)

    def json(self):
        return {'name': self.name,
         'title': self.title,
         'description': self.description,
         'assignment_type': self.assignment_type,
         'duration': self.duration
        }

    @classmethod
    def find_by_id(cls, _id) -> "AssignmentModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
