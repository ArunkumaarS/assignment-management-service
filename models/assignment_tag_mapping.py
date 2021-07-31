from models import assignment
from db import db
from typing import List


class AssignmentTagMappingModel(db.Model):
    __tablename__ = "assignment_tag_mapping"

    id = db.Column(db.Integer, primary_key=True)
    assignment_id =db.Column(db.Integer,db.ForeignKey('assignments.id'),nullable=False)
    assignment = db.relationship("AssignmentModel",)
    tag_id =db.Column(db.Integer,db.ForeignKey('tags.id'),nullable=False)
    tag = db.relationship("TagModel",)

    def __init__(self, assignment_id, tag_id):
        self.assignment_id = assignment_id
        self.tag_id = tag_id

    def __repr__(self):
        return 'AssignmentTagMappingModel(assignment_id=%s, tag_id=%s)' % (self.assignment_id, self.tag_id)

    def json(self):
        return {'assignment_id': self.assignment_id, 'tag_id': self.tag_id}

    @classmethod
    def find_by_tag_name(cls, tag_name):
        return db.session.execute('SELECT a.* FROM assignment_tag_mapping atm join assignments a on atm.assignment_id = a.id join tags t on atm.tag_id = t.id WHERE t.name = :val', {'val': tag_name})

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
