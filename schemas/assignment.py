from ma import ma
from models.assignment import AssignmentModel


class AssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AssignmentModel
        load_instance = True
        include_fk = True