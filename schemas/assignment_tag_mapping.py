from ma import ma
from models.assignment_tag_mapping import AssignmentTagMappingModel
from models.assignment import AssignmentModel
from models.tag import TagModel


class AssignmentTagMappingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AssignmentTagMappingModel
        load_instance = True
        load_only = ("assignment",)
        include_fk= True